#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "PhysicsTools/XGBoost/interface/XGBooster.h"
#include "fastjet/contrib/SoftKiller.hh"
#include "correction.h"
#include <fstream>

namespace pat {

  class HIMuonMVAProducer : public edm::global::EDProducer<> {
  public:
    explicit HIMuonMVAProducer(const edm::ParameterSet& iConfig)
        : muonToken_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
          pfCandidateToken_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("pfCandidates"))),
          centralityToken_(consumes<int>(iConfig.getParameter<edm::InputTag>("centrality"))),
          etaToken_(consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>("etaMap"))),
          rhoToken_(consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>("rhoMap"))),
          patMuonPutToken_(produces<pat::MuonCollection>()),
          pfMaxEta_(iConfig.getParameter<double>("pf_maxAbsEta")),
          skRadius_(iConfig.getParameter<double>("sk_radius")),
          muonMinPt_(iConfig.getParameter<double>("muon_minPt")),
          rVeto_(iConfig.getParameter<double>("iso_rVeto")),
          rCone_(iConfig.getParameter<double>("iso_rCone")),
          era_(iConfig.getParameter<std::string>("era")),
          isoCorr_(getCorrection(iConfig)),
          isoModel_(getModel(iConfig)) {}
    ~HIMuonMVAProducer() override{};

    void produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const override;

    static void fillDescriptions(edm::ConfigurationDescriptions&);

  private:
    const edm::EDGetTokenT<pat::MuonCollection> muonToken_;
    const edm::EDGetTokenT<reco::CandidateView> pfCandidateToken_;
    const edm::EDGetTokenT<int> centralityToken_;
    const edm::EDGetTokenT<std::vector<double>> etaToken_;
    const edm::EDGetTokenT<std::vector<double>> rhoToken_;
    const edm::EDPutTokenT<pat::MuonCollection> patMuonPutToken_;
    const reco::PFCandidate convert_;
    const double pfMaxEta_, skRadius_, muonMinPt_, rVeto_, rCone_;
    const std::string era_;
    const std::shared_ptr<const correction::Correction> isoCorr_;
    const std::unique_ptr<const XGBooster> isoModel_;

    std::shared_ptr<const correction::Correction> getCorrection(const edm::ParameterSet& iConfig) {
      const auto& csetIsoRhoCorrections =
          correction::CorrectionSet::from_file(iConfig.getParameter<edm::FileInPath>("file_isoCorr").fullPath());
      return csetIsoRhoCorrections->at("iso_rho_correction");
    }

    const XGBooster* getModel(const edm::ParameterSet& iConfig, const int& nfeat = 8) {
      auto model = new XGBooster(iConfig.getParameter<edm::FileInPath>("file_isoModel").fullPath());
      for (int i = 0; i < nfeat; i++)
        model->addFeature(std::to_string(i));
      return model;
    }

    enum WP { WP95, WP90, WP85, WP80 };
    bool passMVAIso(const double&, const double&, const WP& wp) const;
  };

}  // namespace pat

bool pat::HIMuonMVAProducer::passMVAIso(const double& mva, const double& cent, const WP& wp) const {
  double cut(10.);
  const auto cen = cent > 90. ? 90. : cent;
  const auto cen2 = cen * cen;
  const auto cen3 = cen * cen * cen;
  if (era_ == "Run3_2023_PbPb") {
    //Working point: WP95
    if (wp == WP95)
      cut = 2.5013048021519e-07 * cen3 + -4.4318470411403026e-05 * cen2 + -0.00018650828215223606 * cent +
            0.6619448537464798;
    //Working point: WP90
    else if (wp == WP90)
      cut = 3.1499095131546186e-07 * cen3 + -5.105264775309079e-05 * cen2 + -0.0012154777916773905 * cent +
            0.4482742002988437;
    //Working point: WP85
    else if (wp == WP85)
      cut = 1.966079439693525e-07 * cen3 + -2.5188338688520636e-05 * cen2 + -0.0020240481028307054 * cent +
            0.3124087777351221;
    //Working point: WP80
    else if (wp == WP80)
      cut = 1.676826751604636e-07 * cen3 + -1.630479601666753e-05 * cen2 + -0.0019206974744949037 * cent +
            0.22760841936362564;
  } else if (era_ == "Run3_2024_PbPb") {
    //Working point: WP95
    if (wp == WP95)
      cut = 8.885008633932616e-10 * cen3 + 1.2493577343059896e-06 * cen2 + -0.001600414736859661 * cent +
            0.6341177456491892;
    //Working point: WP90
    else if (wp == WP90)
      cut = -1.798172635149033e-07 * cen3 + 2.1841904928376438e-05 * cen2 + -0.0033099620109025727 * cent +
            0.42072804518132556;
    //Working point: WP85
    else if (wp == WP85)
      cut = -1.3254809352128999e-07 * cen3 + 1.9497513214154113e-05 * cen2 + -0.0030196506143452193 * cent +
            0.2844028745198661;
    //Working point: WP80
    else if (wp == WP80)
      cut = -1.9711654928305663e-08 * cen3 + 6.787189363764862e-06 * cen2 + -0.002185372987065078 * cent +
            0.20226176263228562;
  } else if (era_ == "Run3_2025_PbPb") {
    //Working point: WP95
    if (wp == WP95)
      cut = 3.7925539303746796e-07 * cen3 + -4.9700855211787375e-05 * cen2 + -0.00041756134699110056 * cent +
            0.6904379945632768;
    //Working point: WP90
    else if (wp == WP90)
      cut = 2.563071765332463e-07 * cen3 + -3.2401274666438957e-05 * cen2 + -0.002493800741968257 * cent +
            0.48616194520357725;
    //Working point: WP85
    else if (wp == WP85)
      cut = 6.641963305833581e-08 * cen3 + -3.07625591543076e-07 * cen2 + -0.00342383634510742 * cent +
            0.3431824130712797;
    //Working point: WP80
    else if (wp == WP80)
      cut = 3.4366600896827934e-08 * cen3 + 6.9597864047222735e-06 * cen2 + -0.0031384524523537776 * cent +
            0.25002692183217673;
  } else
    throw std::logic_error("[ERROR] Wrong era for HIMuonMVAProducer");
  return mva < cut;
}

void pat::HIMuonMVAProducer::produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  // extract input information
  const auto& muons = iEvent.get(muonToken_);
  const auto& pfCandidates = iEvent.get(pfCandidateToken_);
  const auto& etaMap = iEvent.get(etaToken_);
  const auto& rhoMap = iEvent.get(rhoToken_);
  const double cent = iEvent.get(centralityToken_) / 2.0;

  // select PF candidates
  std::vector<std::tuple<double, double, double, int, int, double>> selPFCands;
  if (etaMap.size() > 1) {
    selPFCands.reserve(pfCandidates.size());
    std::vector<std::vector<fastjet::PseudoJet>> particlesForSK(etaMap.size() - 1);
    for (const auto& pf : pfCandidates) {
      // determine eta category
      int ieta(-1);
      for (size_t i = 1; i < etaMap.size(); i++)
        if (pf.eta() >= etaMap[i - 1] && pf.eta() < etaMap[i]) {
          ieta = i - 1;
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
    std::vector<double> skThrs(etaMap.size() - 1);
    for (size_t i = 0; i < particlesForSK.size(); i++) {
      const auto& particles = particlesForSK[i];
      if (not particles.empty()) {
        fastjet::contrib::SoftKiller soft_killer(etaMap[i], etaMap[i + 1], skRadius_, skRadius_);
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
    for (size_t i = 1; i < etaMap.size(); i++)
      if (muon.eta() >= etaMap[i - 1] && muon.eta() < etaMap[i]) {
        rho = rhoMap[i - 1];
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
      const auto dR2 = reco::deltaR2(muon.eta(), muon.phi(), eta, phi);
      if (dR2 >= rVeto_ * rVeto_ && dR2 <= rCone_ * rCone_)
        (id == 5 ? skPFNeuIso : (id == 4 ? skPFPhoIso : skPFChIso)) += pt * (pt > skThr);
    }
    const auto& skPFIso = skPFChIso + skPFNeuIso + skPFPhoIso;

    // extract PF isolation
    const auto& pfChIso = muon.pfIsolationR04().sumChargedHadronPt;
    const auto& pfNeuIso = muon.pfIsolationR04().sumNeutralHadronEt;
    const auto& pfPhoIso = muon.pfIsolationR04().sumPhotonEt;
    const auto& pfIso = pfChIso + pfNeuIso + pfPhoIso;

    // correct the PF isolation variables
    const auto& pfRelIso = (pfIso - isoCorr_->evaluate({{"PFIso", "mu", rho}})) / muon.pt();
    const auto& pfChRelIso = (pfChIso - isoCorr_->evaluate({{"PFChIso", "mu", rho}})) / muon.pt();
    const auto& skPFRelIso = (skPFIso - isoCorr_->evaluate({{"skPFIso", "mu", rho}})) / muon.pt();
    const auto& skPFChRelIso = (skPFChIso - isoCorr_->evaluate({{"skPFChIso", "mu", rho}})) / muon.pt();

    // compute the isolation from MVA
    const std::vector<double> inputs(
        {std::abs(muon.eta()), muon.phi(), rho, ip3DSig, pfRelIso, pfChRelIso, skPFRelIso, skPFChRelIso});
    const std::vector<float> features(inputs.begin(), inputs.end());
    const auto isoValue = 1. - isoModel_->predict(features);
    muon.addUserFloat("hiMVAIso", isoValue);
    muon.addUserInt("hiMVAIsoWP95", passMVAIso(isoValue, cent, WP95));
    muon.addUserInt("hiMVAIsoWP90", passMVAIso(isoValue, cent, WP90));
    muon.addUserInt("hiMVAIsoWP85", passMVAIso(isoValue, cent, WP85));
    muon.addUserInt("hiMVAIsoWP80", passMVAIso(isoValue, cent, WP80));
  }

  iEvent.emplace(patMuonPutToken_, std::move(output));
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void pat::HIMuonMVAProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("muons", edm::InputTag("slimmedMuons"))->setComment("muon input collection");
  desc.add<edm::InputTag>("pfCandidates", edm::InputTag("packedPFCandidates"))
      ->setComment("PF candidate input collection");
  desc.add<edm::InputTag>("centrality", edm::InputTag("centralityBin:HFtowers"))->setComment("centrality");
  desc.add<edm::InputTag>("etaMap", edm::InputTag("hiFJRhoProducerFinerBins:mapEtaEdges"))
      ->setComment("eta ranges for rho and soft killer");
  desc.add<edm::InputTag>("rhoMap", edm::InputTag("hiFJRhoProducerFinerBins:mapToRho"))->setComment("rho");
  desc.add<double>("pf_maxAbsEta", 2.8)->setComment("Maximum absolute eta for PF candidates");
  desc.add<double>("sk_radius", 0.4)->setComment("Radius for soft killer threshold");
  desc.add<double>("muon_minPt", 0.0)->setComment("Muon minimum pt");
  desc.add<double>("iso_rVeto", 1.E-3)->setComment("Isolation veto radius");
  desc.add<double>("iso_rCone", 0.3)->setComment("Isolation cone radius");
  desc.add<std::string>("era", "")->setComment("Era");
  desc.add<edm::FileInPath>("file_isoModel", {})->setComment("Path to isolation model");
  desc.add<edm::FileInPath>("file_isoCorr", {})->setComment("Path to isolation rho correction");
  descriptions.add("hiMuons", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(HIMuonMVAProducer);
