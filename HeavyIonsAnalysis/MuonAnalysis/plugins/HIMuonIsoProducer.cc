#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "fastjet/contrib/SoftKiller.hh"
#include "correction.h"
#include "TMVA/RBDT.hxx"
#include "TMVA/RInferenceUtils.hxx"


namespace pat {

  class HIMuonIsoProducer : public edm::global::EDProducer<> {
  public:
    explicit HIMuonIsoProducer(const edm::ParameterSet& iConfig)
        : muonToken_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
          pfCandidateToken_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("pfCandidates"))),
          etaToken_(consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>("etaMap"))),
          rhoToken_(consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>("rhoMap"))),
          patMuonPutToken_(produces<pat::MuonCollection>()),
          pfMaxEta_(iConfig.getParameter<double>("pf_maxAbsEta")),
          skRadius_(iConfig.getParameter<double>("sk_radius")),
          muonMinPt_(iConfig.getParameter<double>("muon_minPt")),
          rVeto_(iConfig.getParameter<double>("iso_rVeto")),
          rCone_(iConfig.getParameter<double>("iso_rCone")),
          isoCorr_(getCorrection(iConfig)),
          isoModel_(getModel(iConfig)) {}
    ~HIMuonIsoProducer() override{};

    void produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const override;

    static void fillDescriptions(edm::ConfigurationDescriptions&);

  private:
    const edm::EDGetTokenT<pat::MuonCollection> muonToken_;
    const edm::EDGetTokenT<reco::CandidateView> pfCandidateToken_;
    const edm::EDGetTokenT<std::vector<double>> etaToken_;
    const edm::EDGetTokenT<std::vector<double>> rhoToken_;
    const edm::EDPutTokenT<pat::MuonCollection> patMuonPutToken_;

    const reco::PFCandidate convert_;
    const double pfMaxEta_, skRadius_, muonMinPt_, rVeto_, rCone_;
    const std::shared_ptr<const correction::Correction> isoCorr_;
    const std::unique_ptr<TMVA::Experimental::RBDT<>> isoModel_;

    std::shared_ptr<const correction::Correction> getCorrection(const edm::ParameterSet& iConfig) {
      const auto& csetIsoRhoCorrections = correction::CorrectionSet::from_file(iConfig.getParameter<edm::FileInPath>("file_isoCorr").fullPath());
      return csetIsoRhoCorrections->at("iso_rho_correction");
    }

    TMVA::Experimental::RBDT<>* getModel(const edm::ParameterSet& iConfig) {
      return new TMVA::Experimental::RBDT<>("muiso_BDT", iConfig.getParameter<edm::FileInPath>("file_isoModel").fullPath());
    }
  };

}  // namespace pat

void pat::HIMuonIsoProducer::produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  // extract input information
  const auto& muons = iEvent.get(muonToken_);
  const auto& pfCandidates = iEvent.get(pfCandidateToken_);
  const auto& etaMap = iEvent.get(etaToken_);
  const auto& rhoMap = iEvent.get(rhoToken_);

  // select PF candidates
  std::vector<std::tuple<double, double, double, int, int, double>> selPFCands;
  if (etaMap.size() > 1) {
    selPFCands.reserve(pfCandidates.size());
    std::vector<std::vector<fastjet::PseudoJet>> particlesForSK(etaMap.size()-1);
    for (const auto& pf : pfCandidates) {
      // determine eta category
      int ieta(-1);
      for (size_t i=1; i<etaMap.size(); i++)
        if (pf.eta() >= etaMap[i-1] && pf.eta() < etaMap[i]) {
          ieta = i-1;
          break;
        }
      if (ieta < 0)
        continue;
      // fill particles for soft killer
      particlesForSK[ieta].emplace_back(pf.px(), pf.py(), pf.pz(), pf.energy());
      // fill selected PF candidates
      const auto& id = convert_.translatePdgIdToType(pf.pdgId());
      if (id > 0 && id <= 5 && std::abs(pf.eta()) <= pfMaxEta_)
        selPFCands.emplace_back(pf.pt(), pf.eta(), pf.phi(), id, ieta, 0.0);
    }
  
    // compute soft killer thresholds
    std::vector<double> skThrs(etaMap.size()-1);
    for (size_t i=0; i<particlesForSK.size(); i++) {
	  const auto& particles = particlesForSK[i];
	  if (not particles.empty()) {
	    fastjet::contrib::SoftKiller soft_killer(etaMap[i], etaMap[i+1], skRadius_, skRadius_);
        std::vector<fastjet::PseudoJet> soft_killed_event;
        soft_killer.apply(particles, soft_killed_event, skThrs[i]);
      }
    }

    // add soft killer thresholds to selected PF candidates
    for (auto& cand : selPFCands)
      std::get<5>(cand) = skThrs[std::get<4>(cand)];
  }

  // initialize output muon collection
  pat::MuonCollection output(muons);

  // loop over output muons
  for (auto& muon : output) {
    if (muon.pt() < muonMinPt_)
      continue;

    // associate rho value
    double rho(-1.);
    for (size_t i=1; i<etaMap.size(); i++)
      if (muon.eta() >= etaMap[i-1] && muon.eta() < etaMap[i]) {
		rho = rhoMap[i-1];
		break;
	  }
    if (rho < 0)
      continue;

    // compute IP3D significance
    const auto ip3DSig = std::abs(muon.dB(pat::Muon::PV3D)) / muon.edB(pat::Muon::PV3D);

    // compute soft killer isolation
    double skPFChIso(0.), skPFNeuIso(0.), skPFPhoIso(0.);
    for (const auto& cand : selPFCands) {
	  const auto& [pt, eta, phi, id, ieta, skThr] = cand;
	  const auto dR = reco::deltaR(muon.eta(), muon.phi(), eta, phi);
	  if (dR >= rVeto_ && dR <= rCone_)
	    (id == 5 ? skPFNeuIso : (id == 4 ? skPFPhoIso : skPFChIso)) += pt * (pt > skThr);
    }
    const auto& skPFIso = skPFChIso + skPFNeuIso + skPFPhoIso;

    // extract PF isolation
    const auto& pfChIso = muon.pfIsolationR04().sumChargedHadronPt;
    const auto& pfNeuIso = muon.pfIsolationR04().sumNeutralHadronEt;
    const auto& pfPhoIso = muon.pfIsolationR04().sumPhotonEt;
    const auto& pfIso = pfChIso  + pfNeuIso + pfPhoIso;

    // correct the PF isolation variables
    const auto& pfRelIso = (pfIso - isoCorr_->evaluate({{"PFIso", "mu", rho}})) / muon.pt();
    const auto& pfChRelIso = (pfChIso - isoCorr_->evaluate({{"PFChIso", "mu", rho}})) / muon.pt();
    const auto& skPFRelIso = (skPFIso - isoCorr_->evaluate({{"skPFIso", "mu", rho}})) / muon.pt();
    const auto& skPFChRelIso = (skPFChIso - isoCorr_->evaluate({{"skPFChIso", "mu", rho}})) / muon.pt();

    // compute the isolation from MVA
    const std::vector<double> inputs({std::abs(muon.eta()), muon.phi(), rho, ip3DSig, pfRelIso, pfChRelIso, skPFRelIso, skPFChRelIso});
    const std::vector<float> features(inputs.begin(), inputs.end());
    const auto isoValue = 1. - isoModel_->Compute(features)[0];
    muon.addUserFloat("hiIso", isoValue);
  }

  iEvent.emplace(patMuonPutToken_, std::move(output));
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void pat::HIMuonIsoProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("muons", edm::InputTag("slimmedMuons"))->setComment("muon input collection");
  desc.add<edm::InputTag>("pfCandidates", edm::InputTag("packedPFCandidates"))->setComment("PF candidate input collection");
  desc.add<edm::InputTag>("etaMap", edm::InputTag("hiFJRhoProducerFinerBins:mapEtaEdges"))->setComment("eta ranges for rho and soft killer");
  desc.add<edm::InputTag>("rhoMap", edm::InputTag("hiFJRhoProducerFinerBins:mapToRho"))->setComment("rho");
  desc.add<double>("pf_maxAbsEta", 2.8)->setComment("Maximum absolute eta for PF candidates");
  desc.add<double>("sk_radius", 0.4)->setComment("Radius for soft killer threshold");
  desc.add<double>("muon_minPt", 0.0)->setComment("Muon minimum pt");
  desc.add<double>("iso_rVeto", 1.E-3)->setComment("Isolation veto radius");
  desc.add<double>("iso_rCone", 0.3)->setComment("Isolation cone radius");
  desc.add<edm::FileInPath>("file_isoModel", edm::FileInPath("HeavyIonsAnalysis/Configuration/data/muiso_BDT.root"))->setComment("Path to isolation model");
  desc.add<edm::FileInPath>("file_isoCorr", edm::FileInPath("HeavyIonsAnalysis/Configuration/data/lepton_spectra_train_weights.json.gz"))->setComment("Path to isolation rho correction");
  descriptions.add("hiIsoMuons", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(HIMuonIsoProducer);
