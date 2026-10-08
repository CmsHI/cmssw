#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "RecoEgamma/EgammaTools/interface/EgammaRandomSeeds.h"
#include "correction.h"
#include "TRandom3.h"

template <typename T>
class CorrectedEGammaProducerT : public edm::stream::EDProducer<> {
public:
  explicit CorrectedEGammaProducerT(const edm::ParameterSet&);
  ~CorrectedEGammaProducerT() override {}
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  void produce(edm::Event&, const edm::EventSetup&) override;

private:
  void calibrateObject(pat::Electron&, double, bool) const;
  void calibrateObject(pat::Photon&, double, bool) const;
  void calibrateObject(reco::GsfElectron&, double, bool) const;
  void calibrateObject(reco::Photon&, double, bool) const;
  void setRandomSeed(const edm::Event&, const T&, size_t, size_t);

  const std::unique_ptr<TRandom3> rng_;
  const std::unique_ptr<correction::CorrectionSet> cset_;
  const edm::EDGetTokenT<std::vector<T>> srcToken_;
  const edm::EDGetTokenT<int> centralityToken_;
};

template <typename T>
CorrectedEGammaProducerT<T>::CorrectedEGammaProducerT(const edm::ParameterSet& conf)
    : rng_(new TRandom3()),
      cset_(correction::CorrectionSet::from_file(conf.getParameter<edm::FileInPath>("correctionFile").fullPath())),
      srcToken_(consumes<std::vector<T>>(conf.getParameter<edm::InputTag>("src"))),
      centralityToken_(consumes<int>(conf.getParameter<edm::InputTag>("centrality"))) {
  produces<std::vector<T>>();
}

template <typename T>
void CorrectedEGammaProducerT<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("gedGsfElectrons"));
  desc.add<edm::InputTag>("centrality", edm::InputTag("centralityBin:HFtowers"));
  desc.add<edm::FileInPath>("correctionFile", {});
  descriptions.addWithDefaultLabel(desc);
}

template <typename T>
void CorrectedEGammaProducerT<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto out = std::make_unique<std::vector<T>>();
  const bool isMC = not iEvent.isRealData();
  const double cent = iEvent.get(centralityToken_) / 2.0;
  const auto& source = iEvent.get(srcToken_);
  for (const auto& obj : source) {
    out->push_back(obj);
    setRandomSeed(iEvent, obj, source.size(), out->size());
    calibrateObject(out->back(), cent, isMC);
  }
  iEvent.put(std::move(out));
}

template <typename T>
void CorrectedEGammaProducerT<T>::calibrateObject(pat::Electron& ele, double cent, bool isMC) const {
  ele.addUserFloat("rawPt", ele.pt());
  calibrateObject(dynamic_cast<reco::GsfElectron&>(ele), cent, isMC);
}

template <typename T>
void CorrectedEGammaProducerT<T>::calibrateObject(pat::Photon& pho, double cent, bool isMC) const {
  pho.addUserFloat("rawEnergy", pho.getCorrectedEnergy(reco::Photon::P4type::regression2));
  pho.addUserFloat("rawEnergyError", pho.getCorrectedEnergyError(reco::Photon::P4type::regression2));
  calibrateObject(dynamic_cast<reco::Photon&>(pho), cent, isMC);
}

template <typename T>
void CorrectedEGammaProducerT<T>::calibrateObject(reco::GsfElectron& ele, double cent, bool isMC) const {
  const double aeta = std::abs(ele.superCluster()->eta());
  const auto fsmear = isMC ? rng_->Gaus(1., cset_->at("ElectronSmear")->evaluate({aeta, cent})) : 1.0;
  const auto fscale = fsmear * cset_->at("ElectronScale")->evaluate({isMC ? "mc" : "data", "nominal", aeta, cent});
  const math::PtEtaPhiMLorentzVector corP4(fscale * ele.pt(), ele.eta(), ele.phi(), 0.000511);
  const math::XYZTLorentzVector newP4(corP4.x(), corP4.y(), corP4.z(), corP4.t());
  ele.correctMomentum(newP4, ele.trackMomentumError(), ele.p4Error(reco::GsfElectron::P4_COMBINATION));
}

template <typename T>
void CorrectedEGammaProducerT<T>::calibrateObject(reco::Photon& pho, double cent, bool isMC) const {
  const double aeta = std::abs(pho.superCluster()->eta());
  const auto smear = isMC ? cset_->at("PhotonSmear")->evaluate({"PhoEt", "nominal", aeta, cent}) : 0.0;
  const auto scale = cset_->at("PhotonScale")->evaluate({"PhoEt", isMC ? "mc" : "data", "nominal", aeta, cent});
  const auto fscale = scale * (isMC ? rng_->Gaus(1., smear) : 1.0);
  const auto corEnergy = fscale * pho.getCorrectedEnergy(reco::Photon::P4type::regression2);
  const auto corEnergyError =
      std::hypot(fscale * pho.getCorrectedEnergyError(reco::Photon::P4type::regression2), scale * smear * corEnergy);
  pho.setCorrectedEnergy(reco::Photon::P4type::regression2, corEnergy, corEnergyError, true);
}

template <typename T>
void CorrectedEGammaProducerT<T>::setRandomSeed(const edm::Event& iEvent, const T& obj, size_t size, size_t index) {
  rng_->SetSeed(obj.superCluster().isNonnull() ? egamma::getRandomSeedFromSC(iEvent, obj.superCluster())
                                               : egamma::getRandomSeedFromObj(iEvent, obj, size, index));
}

using CorrectedSSElectronProducer = CorrectedEGammaProducerT<reco::GsfElectron>;
using CorrectedSSPatElectronProducer = CorrectedEGammaProducerT<pat::Electron>;
using CorrectedSSPhotonProducer = CorrectedEGammaProducerT<reco::Photon>;
using CorrectedSSPatPhotonProducer = CorrectedEGammaProducerT<pat::Photon>;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(CorrectedSSElectronProducer);
DEFINE_FWK_MODULE(CorrectedSSPatElectronProducer);
DEFINE_FWK_MODULE(CorrectedSSPhotonProducer);
DEFINE_FWK_MODULE(CorrectedSSPatPhotonProducer);
