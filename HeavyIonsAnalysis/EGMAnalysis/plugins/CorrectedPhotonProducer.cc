/*
 *  adapted from:
 *    RecoEgamma/EgammaTools/plugins/CalibratedPhotonProducers.cc
 *    RecoEgamma/EgammaTools/src/PhotonEnergyCalibrator.cc
 *  extended + simplified for HI use
 */

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "HeavyIonsAnalysis/EGMAnalysis/interface/EnergyScaleCorrector.h"
#include "RecoEgamma/EgammaTools/interface/EgammaRandomSeeds.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "TRandom2.h"

#include <memory>
#include <vector>

template <typename T>
class CorrectedPhotonProducerT : public edm::stream::EDProducer<> {
public:
  explicit CorrectedPhotonProducerT(const edm::ParameterSet&);
  ~CorrectedPhotonProducerT() override {}
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  void produce(edm::Event&, const edm::EventSetup&) override;

private:
  void setRandomSeed(const edm::Event& iEvent, const T& obj, size_t size, size_t index);

  bool semiDeterministic_;
  std::unique_ptr<TRandom2> semiDeterministicRng_;
  edm::EDGetTokenT<edm::View<T>> photonToken_;
  edm::EDGetTokenT<int> centralityToken_;
  EnergyScaleCorrector energyCorrector_;
};

template <typename T>
CorrectedPhotonProducerT<T>::CorrectedPhotonProducerT(const edm::ParameterSet& conf)
    : semiDeterministic_(conf.getParameter<bool>("semiDeterministic")),
      semiDeterministicRng_(new TRandom2()),
      photonToken_(consumes<edm::View<T>>(conf.getParameter<edm::InputTag>("src"))),
      centralityToken_(consumes<int>(conf.getParameter<edm::InputTag>("centrality"))),
      energyCorrector_(conf.getParameter<std::string>("correctionFile"),
                       semiDeterministicRng_.get(),
                       conf.getParameter<double>("minPt")) {
  produces<std::vector<T>>();
}

template <typename T>
void CorrectedPhotonProducerT<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("gedPhotons"));
  desc.add<edm::InputTag>("centrality", edm::InputTag("centralityBin"));
  desc.add<std::string>("correctionFile", std::string());
  desc.add<double>("minPt", 20.0);
  desc.add<bool>("semiDeterministic", true);
  descriptions.addWithDefaultLabel(desc);
}

template <typename T>
void CorrectedPhotonProducerT<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<T>> photons;
  iEvent.getByToken(photonToken_, photons);
  edm::Handle<int> bin;
  iEvent.getByToken(centralityToken_, bin);

  auto out = std::make_unique<std::vector<T>>();
  for (const auto& pho : *photons) {
    out->push_back(pho);
    auto pout = dynamic_cast<pat::Photon*>(&(out->back()));
    if (pout)
      pout->addUserFloat("rawEt", pho.et());

    if (semiDeterministic_)
      setRandomSeed(iEvent, pho, photons->size(), out->size());

    energyCorrector_.calibratePhoton(out->back(), *bin);
  }

  iEvent.put(std::move(out));
}

template <typename T>
void CorrectedPhotonProducerT<T>::setRandomSeed(const edm::Event& iEvent, const T& obj, size_t size, size_t index) {
  semiDeterministicRng_->SetSeed(obj.superCluster().isNonnull()
                                     ? egamma::getRandomSeedFromSC(iEvent, obj.superCluster())
                                     : egamma::getRandomSeedFromObj(iEvent, obj, size, index));
}

using CorrectedPhotonProducer = CorrectedPhotonProducerT<reco::Photon>;
using CorrectedPatPhotonProducer = CorrectedPhotonProducerT<pat::Photon>;

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(CorrectedPhotonProducer);
DEFINE_FWK_MODULE(CorrectedPatPhotonProducer);
