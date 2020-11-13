#include "HeavyIonsAnalysis/EGMAnalysis/plugins/ggHiNtuplizer.h"
#include "HeavyIonsAnalysis/EGMAnalysis/plugins/GenParticleParentage.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoEgamma/EgammaTools/interface/EcalClusterLocal.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

using namespace std::placeholders;

ggHiNtuplizer::ggHiNtuplizer(const edm::ParameterSet& ps) {
  doGenParticles_ = ps.getParameter<bool>("doGenParticles");
  doElectrons_ = ps.getParameter<bool>("doElectrons");
  doPhotons_ = ps.getParameter<bool>("doPhotons");
  doMuons_ = ps.getParameter<bool>("doMuons");

  isParticleGun_ = ps.getParameter<bool>("isParticleGun");

  vertexToken_ = consumes<std::vector<reco::Vertex>>(ps.getParameter<edm::InputTag>("vertexSrc"));
  rhoToken_ = consumes<double>(ps.getParameter<edm::InputTag>("rhoSrc"));

  if (doGenParticles_) {
    pileupToken_ = consumes<std::vector<PileupSummaryInfo>>(ps.getParameter<edm::InputTag>("pileupSrc"));
    genParticlesToken_ = consumes<std::vector<reco::GenParticle>>(ps.getParameter<edm::InputTag>("genParticleSrc"));
  }

  if (doElectrons_) {
    electronsToken_ = consumes<edm::View<reco::GsfElectron>>(ps.getParameter<edm::InputTag>("electronSrc"));
    beamSpotToken_ = consumes<reco::BeamSpot>(ps.getParameter<edm::InputTag>("beamSpotSrc"));
    conversionsToken_ = consumes<reco::ConversionCollection>(ps.getParameter<edm::InputTag>("conversionsSrc"));
  }

  if (doPhotons_) {
    photonsToken_ = consumes<edm::View<reco::Photon>>(ps.getParameter<edm::InputTag>("photonSrc"));
  }

  if (doMuons_) {
    muonsToken_ = consumes<edm::View<reco::Muon>>(ps.getParameter<edm::InputTag>("muonSrc"));
  }

  // initialize output TTree
  edm::Service<TFileService> fs;
  tree_ = fs->make<TTree>("EventTree", "electrons, photons, muons");

  tree_->Branch("run", &run_);
  tree_->Branch("event", &event_);
  tree_->Branch("lumis", &lumis_);

  tree_->Branch("rho", &rho_);

  if (doGenParticles_) {
    tree_->Branch("nPUInfo", &nPUInfo_);
    tree_->Branch("nPU", &nPU_);
    tree_->Branch("puBX", &puBX_);
    tree_->Branch("puTrue", &puTrue_);

    tree_->Branch("nMC", &nMC_);

    tree_->Branch("mcVtx_x", &mcVtx_x_);
    tree_->Branch("mcVtx_y", &mcVtx_y_);
    tree_->Branch("mcVtx_z", &mcVtx_z_);

    tree_->Branch("mcPID", &mcPID_);
    tree_->Branch("mcStatus", &mcStatus_);
    tree_->Branch("mcPt", &mcPt_);
    tree_->Branch("mcEta", &mcEta_);
    tree_->Branch("mcPhi", &mcPhi_);
    tree_->Branch("mcE", &mcE_);
    tree_->Branch("mcEt", &mcEt_);
    tree_->Branch("mcMass", &mcMass_);

    tree_->Branch("mcParentage", &mcParentage_);
    tree_->Branch("mcMomPID", &mcMomPID_);
    tree_->Branch("mcMomPt", &mcMomPt_);
    tree_->Branch("mcMomEta", &mcMomEta_);
    tree_->Branch("mcMomPhi", &mcMomPhi_);
    tree_->Branch("mcMomMass", &mcMomMass_);
    tree_->Branch("mcGMomPID", &mcGMomPID_);
    tree_->Branch("mcIndex", &mcIndex_);

    tree_->Branch("mcCalIsoDR03", &mcCalIsoDR03_);
    tree_->Branch("mcCalIsoDR04", &mcCalIsoDR04_);
    tree_->Branch("mcTrkIsoDR03", &mcTrkIsoDR03_);
    tree_->Branch("mcTrkIsoDR04", &mcTrkIsoDR04_);
  }

  if (doElectrons_) {
    tree_->Branch("nEle", &nEle_);

    tree_->Branch("eleD0", &eleD0_);
    tree_->Branch("eleDz", &eleDz_);
    tree_->Branch("eleD0Err", &eleD0Err_);
    tree_->Branch("eleDzErr", &eleDzErr_);
    tree_->Branch("eleTrkPt", &eleTrkPt_);
    tree_->Branch("eleTrkEta", &eleTrkEta_);
    tree_->Branch("eleTrkPhi", &eleTrkPhi_);
    tree_->Branch("eleTrkCharge", &eleTrkCharge_);
    tree_->Branch("eleTrkPtErr", &eleTrkPtErr_);
    tree_->Branch("eleTrkChi2", &eleTrkChi2_);
    tree_->Branch("eleTrkNdof", &eleTrkNdof_);
    tree_->Branch("eleTrkNormalizedChi2", &eleTrkNormalizedChi2_);
    tree_->Branch("eleTrkValidHits", &eleTrkValidHits_);
    tree_->Branch("eleTrkLayers", &eleTrkLayers_);
    tree_->Branch("eleMissHits", &eleMissHits_);
    tree_->Branch("eleIP3D", &eleIP3D_);
    tree_->Branch("eleIP3DErr", &eleIP3DErr_);

    tree_->Branch("elePt", &elePt_);
    tree_->Branch("eleEta", &eleEta_);
    tree_->Branch("elePhi", &elePhi_);
    tree_->Branch("eleCharge", &eleCharge_);
    tree_->Branch("eleEn", &eleEn_);

    tree_->Branch("eleSCEn", &eleSCEn_);
    tree_->Branch("eleESEn", &eleESEn_);
    tree_->Branch("eleSCEta", &eleSCEta_);
    tree_->Branch("eleSCPhi", &eleSCPhi_);
    tree_->Branch("eleSCRawEn", &eleSCRawEn_);
    tree_->Branch("eleSCEtaWidth", &eleSCEtaWidth_);
    tree_->Branch("eleSCPhiWidth", &eleSCPhiWidth_);
    tree_->Branch("eleSCClustersSize", &eleSCClustersSize_);
    tree_->Branch("eleSeedEn", &eleSeedEn_);
    tree_->Branch("eleSeedEta", &eleSeedEta_);
    tree_->Branch("eleSeedPhi", &eleSeedPhi_);

    tree_->Branch("eleHoverE", &eleHoverE_);
    tree_->Branch("eleHoverEBc", &eleHoverEBc_);
    tree_->Branch("eleEoverP", &eleEoverP_);
    tree_->Branch("eleEoverPInv", &eleEoverPInv_);
    tree_->Branch("eleEcalE", &eleEcalE_);
    tree_->Branch("elePAtVtx", &elePAtVtx_);
    tree_->Branch("elePAtSC", &elePAtSC_);
    tree_->Branch("elePAtCluster", &elePAtCluster_);
    tree_->Branch("elePAtSeed", &elePAtSeed_);
    tree_->Branch("eledEtaAtVtx", &eledEtaAtVtx_);
    tree_->Branch("eledPhiAtVtx", &eledPhiAtVtx_);
    tree_->Branch("eledEtaSeedAtVtx", &eledEtaSeedAtVtx_);
    tree_->Branch("eleSigmaIEtaIEta", &eleSigmaIEtaIEta_);
    tree_->Branch("eleSigmaIPhiIPhi", &eleSigmaIPhiIPhi_);
    tree_->Branch("eleBrem", &eleBrem_);

    tree_->Branch("eleConvVeto", &eleConvVeto_);

    tree_->Branch("eleR9", &eleR9_);
    tree_->Branch("eleE3x3", &eleE3x3_);
    tree_->Branch("eleE5x5", &eleE5x5_);
    tree_->Branch("eleR9Full5x5", &eleR9Full5x5_);
    tree_->Branch("eleE3x3Full5x5", &eleE3x3Full5x5_);
    tree_->Branch("eleE5x5Full5x5", &eleE5x5Full5x5_);
    tree_->Branch("eleSigmaIEtaIEta_2012", &eleSigmaIEtaIEta_2012_);

    tree_->Branch("elePFChIso", &elePFChIso_);
    tree_->Branch("elePFPhoIso", &elePFPhoIso_);
    tree_->Branch("elePFNeuIso", &elePFNeuIso_);
    tree_->Branch("elePFPUIso", &elePFPUIso_);

    tree_->Branch("eleSeedCryEta", &eleSeedCryEta_);
    tree_->Branch("eleSeedCryPhi", &eleSeedCryPhi_);
    tree_->Branch("eleSeedCryIeta", &eleSeedCryIeta_);
    tree_->Branch("eleSeedCryIphi", &eleSeedCryIphi_);
  }

  if (doPhotons_) {
    tree_->Branch("nPho", &nPho_);

    tree_->Branch("phoE", &phoE_);
    tree_->Branch("phoEt", &phoEt_);
    tree_->Branch("phoEta", &phoEta_);
    tree_->Branch("phoPhi", &phoPhi_);

    tree_->Branch("phoEcorrStdEcal", &phoEcorrStdEcal_);
    tree_->Branch("phoEcorrPhoEcal", &phoEcorrPhoEcal_);
    tree_->Branch("phoEcorrRegr1", &phoEcorrRegr1_);
    tree_->Branch("phoEcorrRegr2", &phoEcorrRegr2_);
    tree_->Branch("phoEcorrErrStdEcal", &phoEcorrErrStdEcal_);
    tree_->Branch("phoEcorrErrPhoEcal", &phoEcorrErrPhoEcal_);
    tree_->Branch("phoEcorrErrRegr1", &phoEcorrErrRegr1_);
    tree_->Branch("phoEcorrErrRegr2", &phoEcorrErrRegr2_);

    tree_->Branch("phoSCE", &phoSCE_);
    tree_->Branch("phoSCRawE", &phoSCRawE_);
    tree_->Branch("phoSCEta", &phoSCEta_);
    tree_->Branch("phoSCPhi", &phoSCPhi_);
    tree_->Branch("phoSCEtaWidth", &phoSCEtaWidth_);
    tree_->Branch("phoSCPhiWidth", &phoSCPhiWidth_);
    tree_->Branch("phoSCBrem", &phoSCBrem_);
    tree_->Branch("phoSCnHits", &phoSCnHits_);
    tree_->Branch("phoSCflags", &phoSCflags_);
    tree_->Branch("phoSCinClean", &phoSCinClean_);
    tree_->Branch("phoSCinUnClean", &phoSCinUnClean_);
    tree_->Branch("phoSCnBC", &phoSCnBC_);
    tree_->Branch("phoESEn", &phoESEn_);

    tree_->Branch("phoIsPFPhoton", &phoIsPFPhoton_);
    tree_->Branch("phoIsStandardPhoton", &phoIsStandardPhoton_);
    tree_->Branch("phoHasPixelSeed", &phoHasPixelSeed_);
    tree_->Branch("phoHasConversionTracks", &phoHasConversionTracks_);
    tree_->Branch("phoHadTowerOverEm", &phoHadTowerOverEm_);
    tree_->Branch("phoHoverE", &phoHoverE_);
    tree_->Branch("phoHoverEValid", &phoHoverEValid_);
    tree_->Branch("phoSigmaIEtaIEta", &phoSigmaIEtaIEta_);
    tree_->Branch("phoR9", &phoR9_);
    tree_->Branch("phoE1x5", &phoE1x5_);
    tree_->Branch("phoE2x5", &phoE2x5_);
    tree_->Branch("phoE3x3", &phoE3x3_);
    tree_->Branch("phoE5x5", &phoE5x5_);
    tree_->Branch("phoMaxEnergyXtal", &phoMaxEnergyXtal_);
    tree_->Branch("phoSigmaEtaEta", &phoSigmaEtaEta_);
    tree_->Branch("phoSigmaIEtaIEta_2012", &phoSigmaIEtaIEta_2012_);
    tree_->Branch("phoR9_2012", &phoR9_2012_);
    tree_->Branch("phoE1x5_2012", &phoE1x5_2012_);
    tree_->Branch("phoE2x5_2012", &phoE2x5_2012_);
    tree_->Branch("phoE3x3_2012", &phoE3x3_2012_);
    tree_->Branch("phoE5x5_2012", &phoE5x5_2012_);
    tree_->Branch("phoMaxEnergyXtal_2012", &phoMaxEnergyXtal_2012_);
    tree_->Branch("phoSigmaEtaEta_2012", &phoSigmaEtaEta_2012_);

    tree_->Branch("phoBC1E", &phoBC1E_);
    tree_->Branch("phoBC1Ecorr", &phoBC1Ecorr_);
    tree_->Branch("phoBC1Eta", &phoBC1Eta_);
    tree_->Branch("phoBC1Phi", &phoBC1Phi_);
    tree_->Branch("phoBC1size", &phoBC1size_);
    tree_->Branch("phoBC1flags", &phoBC1flags_);
    tree_->Branch("phoBC1inClean", &phoBC1inClean_);
    tree_->Branch("phoBC1inUnClean", &phoBC1inUnClean_);
    tree_->Branch("phoBC1rawID", &phoBC1rawID_);

    if (doGenParticles_) {
      tree_->Branch("pho_genMatchedIndex", &pho_genMatchedIndex_);
    }
  }

  if (doMuons_) {
    tree_->Branch("nMu", &nMu_);

    tree_->Branch("muPt", &muPt_);
    tree_->Branch("muEta", &muEta_);
    tree_->Branch("muPhi", &muPhi_);
    tree_->Branch("muCharge", &muCharge_);
    tree_->Branch("muType", &muType_);
    tree_->Branch("muIsGood", &muIsGood_);

    tree_->Branch("muD0", &muD0_);
    tree_->Branch("muDz", &muDz_);
    tree_->Branch("muIP3D", &muIP3D_);
    tree_->Branch("muD0Err", &muD0Err_);
    tree_->Branch("muDzErr", &muDzErr_);
    tree_->Branch("muIP3DErr", &muIP3DErr_);
    tree_->Branch("muChi2NDF", &muChi2NDF_);
    tree_->Branch("muInnerD0", &muInnerD0_);
    tree_->Branch("muInnerDz", &muInnerDz_);

    tree_->Branch("muInnerD0Err", &muInnerD0Err_);
    tree_->Branch("muInnerDzErr", &muInnerDzErr_);
    tree_->Branch("muInnerPt", &muInnerPt_);
    tree_->Branch("muInnerPtErr", &muInnerPtErr_);
    tree_->Branch("muInnerEta", &muInnerEta_);

    tree_->Branch("muTrkLayers", &muTrkLayers_);
    tree_->Branch("muPixelLayers", &muPixelLayers_);
    tree_->Branch("muPixelHits", &muPixelHits_);
    tree_->Branch("muMuonHits", &muMuonHits_);
    tree_->Branch("muTrkQuality", &muTrkQuality_);
    tree_->Branch("muStations", &muStations_);
    tree_->Branch("muIsoTrk", &muIsoTrk_);
    tree_->Branch("muPFChIso", &muPFChIso_);
    tree_->Branch("muPFPhoIso", &muPFPhoIso_);
    tree_->Branch("muPFNeuIso", &muPFNeuIso_);
    tree_->Branch("muPFPUIso", &muPFPUIso_);

    tree_->Branch("muIDSoft", &muIDSoft_);
    tree_->Branch("muIDLoose", &muIDLoose_);
    tree_->Branch("muIDMedium", &muIDMedium_);
    tree_->Branch("muIDMediumPrompt", &muIDMediumPrompt_);
    tree_->Branch("muIDTight", &muIDTight_);
    tree_->Branch("muIDGlobalHighPt", &muIDGlobalHighPt_);
    tree_->Branch("muIDTrkHighPt", &muIDTrkHighPt_);
    tree_->Branch("muIDInTime", &muIDInTime_);
  }
}

ggHiNtuplizer::~ggHiNtuplizer() {}

void ggHiNtuplizer::analyze(const edm::Event& e, const edm::EventSetup& es) {
  // cleanup from previous event

  if (doGenParticles_) {
    nPUInfo_ = 0;
    nPU_.clear();
    puBX_.clear();
    puTrue_.clear();

    nMC_ = 0;

    mcVtx_x_.clear();
    mcVtx_y_.clear();
    mcVtx_z_.clear();

    mcPID_.clear();
    mcStatus_.clear();
    mcPt_.clear();
    mcEta_.clear();
    mcPhi_.clear();
    mcE_.clear();
    mcEt_.clear();
    mcMass_.clear();

    mcParentage_.clear();
    mcMomPID_.clear();
    mcMomPt_.clear();
    mcMomEta_.clear();
    mcMomPhi_.clear();
    mcMomMass_.clear();
    mcGMomPID_.clear();
    mcIndex_.clear();

    mcCalIsoDR03_.clear();
    mcCalIsoDR04_.clear();
    mcTrkIsoDR03_.clear();
    mcTrkIsoDR04_.clear();
  }

  if (doElectrons_) {
    nEle_ = 0;

    eleD0_.clear();
    eleDz_.clear();
    eleD0Err_.clear();
    eleDzErr_.clear();
    eleTrkPt_.clear();
    eleTrkEta_.clear();
    eleTrkPhi_.clear();
    eleTrkCharge_.clear();
    eleTrkPtErr_.clear();
    eleTrkChi2_.clear();
    eleTrkNdof_.clear();
    eleTrkNormalizedChi2_.clear();
    eleTrkValidHits_.clear();
    eleTrkLayers_.clear();
    eleMissHits_.clear();
    eleIP3D_.clear();
    eleIP3DErr_.clear();

    elePt_.clear();
    eleEta_.clear();
    elePhi_.clear();
    eleCharge_.clear();
    eleEn_.clear();

    eleSCEn_.clear();
    eleESEn_.clear();
    eleSCEta_.clear();
    eleSCPhi_.clear();
    eleSCRawEn_.clear();
    eleSCEtaWidth_.clear();
    eleSCPhiWidth_.clear();
    eleSCClustersSize_.clear();
    eleSeedEn_.clear();
    eleSeedEta_.clear();
    eleSeedPhi_.clear();

    eleHoverE_.clear();
    eleHoverEBc_.clear();
    eleEoverP_.clear();
    eleEoverPInv_.clear();
    eleEcalE_.clear();
    elePAtVtx_.clear();
    elePAtSC_.clear();
    elePAtCluster_.clear();
    elePAtSeed_.clear();
    eleBrem_.clear();
    eledEtaAtVtx_.clear();
    eledPhiAtVtx_.clear();
    eledEtaSeedAtVtx_.clear();
    eleSigmaIEtaIEta_.clear();
    eleSigmaIPhiIPhi_.clear();

    eleConvVeto_.clear();

    elePFChIso_.clear();
    elePFPhoIso_.clear();
    elePFNeuIso_.clear();
    elePFPUIso_.clear();

    eleR9_.clear();
    eleE3x3_.clear();
    eleE5x5_.clear();
    eleR9Full5x5_.clear();
    eleE3x3Full5x5_.clear();
    eleE5x5Full5x5_.clear();
    eleSigmaIEtaIEta_2012_.clear();

    eleSeedCryEta_.clear();
    eleSeedCryPhi_.clear();
    eleSeedCryIeta_.clear();
    eleSeedCryIphi_.clear();
  }

  if (doPhotons_) {
    nPho_ = 0;

    phoE_.clear();
    phoEt_.clear();
    phoEta_.clear();
    phoPhi_.clear();

    phoEcorrStdEcal_.clear();
    phoEcorrPhoEcal_.clear();
    phoEcorrRegr1_.clear();
    phoEcorrRegr2_.clear();
    phoEcorrErrStdEcal_.clear();
    phoEcorrErrPhoEcal_.clear();
    phoEcorrErrRegr1_.clear();
    phoEcorrErrRegr2_.clear();

    phoSCE_.clear();
    phoSCRawE_.clear();
    phoSCEta_.clear();
    phoSCPhi_.clear();
    phoSCEtaWidth_.clear();
    phoSCPhiWidth_.clear();
    phoSCBrem_.clear();
    phoSCnHits_.clear();
    phoSCflags_.clear();
    phoSCinClean_.clear();
    phoSCinUnClean_.clear();
    phoSCnBC_.clear();
    phoESEn_.clear();

    phoIsPFPhoton_.clear();
    phoIsStandardPhoton_.clear();
    phoHasPixelSeed_.clear();
    phoHasConversionTracks_.clear();
    phoHadTowerOverEm_.clear();
    phoHoverE_.clear();
    phoHoverEValid_.clear();
    phoSigmaIEtaIEta_.clear();
    phoR9_.clear();
    phoE1x5_.clear();
    phoE2x5_.clear();
    phoE3x3_.clear();
    phoE5x5_.clear();
    phoMaxEnergyXtal_.clear();
    phoSigmaEtaEta_.clear();
    phoSigmaIEtaIEta_2012_.clear();
    phoR9_2012_.clear();
    phoE1x5_2012_.clear();
    phoE2x5_2012_.clear();
    phoE3x3_2012_.clear();
    phoE5x5_2012_.clear();
    phoMaxEnergyXtal_2012_.clear();
    phoSigmaEtaEta_2012_.clear();

    phoBC1E_.clear();
    phoBC1Ecorr_.clear();
    phoBC1Eta_.clear();
    phoBC1Phi_.clear();
    phoBC1size_.clear();
    phoBC1flags_.clear();
    phoBC1inClean_.clear();
    phoBC1inUnClean_.clear();
    phoBC1rawID_.clear();

    pho_genMatchedIndex_.clear();
  }

  if (doMuons_) {
    nMu_ = 0;

    muPt_.clear();
    muEta_.clear();
    muPhi_.clear();
    muCharge_.clear();
    muType_.clear();
    muIsGood_.clear();

    muD0_.clear();
    muDz_.clear();
    muD0Err_.clear();
    muDzErr_.clear();
    muChi2NDF_.clear();
    muInnerD0_.clear();
    muInnerDz_.clear();
    muIP3D_.clear();
    muIP3DErr_.clear();

    muInnerD0Err_.clear();
    muInnerDzErr_.clear();
    muInnerPt_.clear();
    muInnerPtErr_.clear();
    muInnerEta_.clear();

    muTrkLayers_.clear();
    muPixelLayers_.clear();
    muPixelHits_.clear();
    muMuonHits_.clear();
    muTrkQuality_.clear();
    muStations_.clear();
    muIsoTrk_.clear();
    muPFChIso_.clear();
    muPFPhoIso_.clear();
    muPFNeuIso_.clear();
    muPFPUIso_.clear();

    muIDSoft_.clear();
    muIDLoose_.clear();
    muIDMedium_.clear();
    muIDMediumPrompt_.clear();
    muIDTight_.clear();
    muIDGlobalHighPt_.clear();
    muIDTrkHighPt_.clear();
    muIDInTime_.clear();
  }

  run_ = e.id().run();
  event_ = e.id().event();
  lumis_ = e.luminosityBlock();

  edm::Handle<double> rhoH;
  e.getByToken(rhoToken_, rhoH);
  rho_ = *rhoH;

  // MC truth
  if (doGenParticles_) {
    fillPileupInfo(e);
    fillGenParticles(e);
  }

  edm::Handle<std::vector<reco::Vertex>> vertices;
  e.getByToken(vertexToken_, vertices);

  // best-known primary vertex coordinates
  reco::Vertex pv(math::XYZPoint(0, 0, -999), math::Error<3>::type());
  for (auto const& vertex : *vertices) {
    if (!vertex.isFake()) {
      pv = vertex;
      break;
    }
  }

  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  es.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder);
  tb = trackBuilder.product();

  if (doElectrons_)
    fillElectrons(e, es, pv);
  if (doPhotons_)
    fillPhotons(e, es, pv);
  if (doMuons_)
    fillMuons(e, es, pv);

  tree_->Fill();
}

void ggHiNtuplizer::fillPileupInfo(const edm::Event& e) {
  // Fills information about pileup from MC truth.
  edm::Handle<std::vector<PileupSummaryInfo>> pileup;
  e.getByToken(pileupToken_, pileup);

  for (const auto& pu : *pileup) {
    nPU_.push_back(pu.getPU_NumInteractions());
    puTrue_.push_back(pu.getTrueNumInteractions());
    puBX_.push_back(pu.getBunchCrossing());

    ++nPUInfo_;
  }
}

void ggHiNtuplizer::fillGenParticles(const edm::Event& e) {
  edm::Handle<std::vector<reco::GenParticle>> genParticles;
  e.getByToken(genParticlesToken_, genParticles);

  // loop over MC particles
  for (auto p = genParticles->begin(); p != genParticles->end(); ++p) {
    // skip all primary particles if not particle gun MC
    if (!isParticleGun_ && !p->mother())
      continue;

    // stable particles with pT > 5 GeV
    bool isStableFast = (p->status() == 1 && p->pt() > 5.0);

    // stable leptons
    bool isStableLepton = (p->status() == 1 && abs(p->pdgId()) >= 11 && abs(p->pdgId()) <= 16);

    // (unstable) Z, W, H, top, bottom
    bool isHeavy =
        (p->pdgId() == 23 || abs(p->pdgId()) == 24 || p->pdgId() == 25 || abs(p->pdgId()) == 6 || abs(p->pdgId()) == 5);

    // reduce size of output root file
    if (!isStableFast && !isStableLepton && !isHeavy)
      continue;

    mcVtx_x_.push_back(p->vx());
    mcVtx_y_.push_back(p->vy());
    mcVtx_z_.push_back(p->vz());

    mcPID_.push_back(p->pdgId());
    mcStatus_.push_back(p->status());
    mcPt_.push_back(p->pt());
    mcEta_.push_back(p->eta());
    mcPhi_.push_back(p->phi());
    mcE_.push_back(p->energy());
    mcEt_.push_back(p->et());
    mcMass_.push_back(p->mass());

    reco::GenParticleRef partRef = reco::GenParticleRef(genParticles, p - genParticles->begin());
    GenParticleParentage particleHistory(partRef);

    mcParentage_.push_back((particleHistory.hasLeptonParent() << 4) + (particleHistory.hasBosonParent() << 3) +
                           (particleHistory.hasNonPromptParent() << 2) + (particleHistory.hasQCDParent() << 1) +
                           (particleHistory.hasExoticParent() << 0));

    int momPID = -999;
    float momPt = -999;
    float momEta = -999;
    float momPhi = -999;
    float momMass = -999;
    int gmomPID = -999;

    if (particleHistory.hasRealParent()) {
      reco::GenParticleRef momRef = particleHistory.parent();

      // mother
      if (momRef.isNonnull() && momRef.isAvailable()) {
        momPID = momRef->pdgId();
        momPt = momRef->pt();
        momEta = momRef->eta();
        momPhi = momRef->phi();
        momMass = momRef->mass();

        // grandmother
        GenParticleParentage motherParticle(momRef);
        if (motherParticle.hasRealParent()) {
          reco::GenParticleRef grandmother = motherParticle.parent();
          gmomPID = grandmother->pdgId();
        }
      }
    }

    mcMomPID_.push_back(momPID);
    mcMomPt_.push_back(momPt);
    mcMomEta_.push_back(momEta);
    mcMomPhi_.push_back(momPhi);
    mcMomMass_.push_back(momMass);
    mcGMomPID_.push_back(gmomPID);

    mcIndex_.push_back(p - genParticles->begin());

    mcCalIsoDR03_.push_back(getGenCalIso(genParticles, p, 0.3 * 0.3, false, false));
    mcCalIsoDR04_.push_back(getGenCalIso(genParticles, p, 0.4 * 0.4, false, false));
    mcTrkIsoDR03_.push_back(getGenTrkIso(genParticles, p, 0.3 * 0.3));
    mcTrkIsoDR04_.push_back(getGenTrkIso(genParticles, p, 0.4 * 0.4));

    nMC_++;
  }  // gen-level particles loop
}

float ggHiNtuplizer::getGenCalIso(edm::Handle<std::vector<reco::GenParticle>>& handle,
                                  reco::GenParticleCollection::const_iterator thisPart,
                                  float dR2Max,
                                  bool removeMu,
                                  bool removeNu) {
  float etSum = 0;

  for (auto p = handle->begin(); p != handle->end(); ++p) {
    if (p == thisPart)
      continue;
    if (p->status() != 1)
      continue;

    // has to come from the same collision
    if (thisPart->collisionId() != p->collisionId())
      continue;

    int pdgCode = abs(p->pdgId());

    // skip muons/neutrinos, if requested
    if (removeMu && pdgCode == 13)
      continue;
    if (removeNu && (pdgCode == 12 || pdgCode == 14 || pdgCode == 16))
      continue;

    // must be within deltaR cone
    float dR2 = reco::deltaR2(thisPart->momentum(), p->momentum());
    if (dR2 > dR2Max)
      continue;

    etSum += p->et();
  }

  return etSum;
}

float ggHiNtuplizer::getGenTrkIso(edm::Handle<std::vector<reco::GenParticle>>& handle,
                                  reco::GenParticleCollection::const_iterator thisPart,
                                  float dR2Max) {
  float ptSum = 0;

  for (auto p = handle->begin(); p != handle->end(); ++p) {
    if (p == thisPart)
      continue;
    if (p->status() != 1)
      continue;
    // exclude neutral particles
    if (p->charge() == 0)
      continue;

    // has to come from the same collision
    if (thisPart->collisionId() != p->collisionId())
      continue;

    // must be within deltaR2 cone
    float dR2 = reco::deltaR2(thisPart->momentum(), p->momentum());
    if (dR2 > dR2Max)
      continue;

    ptSum += p->pt();
  }

  return ptSum;
}

void ggHiNtuplizer::fillElectrons(const edm::Event& e, const edm::EventSetup& es, reco::Vertex& pv) {
  // Fills tree branches with electrons.
  edm::Handle<edm::View<reco::GsfElectron>> gsfElectrons;
  e.getByToken(electronsToken_, gsfElectrons);

  edm::ESHandle<CaloGeometry> caloGeometry;
  es.get<CaloGeometryRecord>().get(caloGeometry);

  edm::Handle<reco::ConversionCollection> conversions;
  e.getByToken(conversionsToken_, conversions);

  edm::Handle<reco::BeamSpot> beamSpot;
  e.getByToken(beamSpotToken_, beamSpot);

  // loop over electrons
  for (auto ele = gsfElectrons->begin(); ele != gsfElectrons->end(); ++ele) {
    eleD0_.push_back(ele->gsfTrack()->dxy(pv.position()));
    eleDz_.push_back(ele->gsfTrack()->dz(pv.position()));
    eleD0Err_.push_back(ele->gsfTrack()->dxyError());
    eleDzErr_.push_back(ele->gsfTrack()->dzError());
    eleTrkPt_.push_back(ele->gsfTrack()->pt());
    eleTrkEta_.push_back(ele->gsfTrack()->eta());
    eleTrkPhi_.push_back(ele->gsfTrack()->phi());
    eleTrkCharge_.push_back(ele->gsfTrack()->charge());
    eleTrkPtErr_.push_back(ele->gsfTrack()->ptError());
    eleTrkChi2_.push_back(ele->gsfTrack()->chi2());
    eleTrkNdof_.push_back(ele->gsfTrack()->ndof());
    eleTrkNormalizedChi2_.push_back(ele->gsfTrack()->normalizedChi2());
    eleTrkValidHits_.push_back(ele->gsfTrack()->numberOfValidHits());
    eleTrkLayers_.push_back(ele->gsfTrack()->hitPattern().trackerLayersWithMeasurement());
    eleMissHits_.push_back(ele->gsfTrack()->numberOfLostHits());

    elePt_.push_back(ele->pt());
    eleEta_.push_back(ele->eta());
    elePhi_.push_back(ele->phi());
    eleCharge_.push_back(ele->charge());
    eleEn_.push_back(ele->energy());

    eleSCEn_.push_back(ele->superCluster()->energy());
    eleESEn_.push_back(ele->superCluster()->preshowerEnergy());
    eleSCEta_.push_back(ele->superCluster()->eta());
    eleSCPhi_.push_back(ele->superCluster()->phi());
    eleSCRawEn_.push_back(ele->superCluster()->rawEnergy());
    eleSCEtaWidth_.push_back(ele->superCluster()->etaWidth());
    eleSCPhiWidth_.push_back(ele->superCluster()->phiWidth());
    eleSCClustersSize_.push_back(ele->superCluster()->clustersSize());
    eleSeedEn_.push_back(ele->superCluster()->seed()->energy());
    eleSeedEta_.push_back(ele->superCluster()->seed()->eta());
    eleSeedPhi_.push_back(ele->superCluster()->seed()->phi());

    eleHoverE_.push_back(ele->hcalOverEcal());
    eleHoverEBc_.push_back(ele->hcalOverEcalBc());
    eleEoverP_.push_back(ele->eSuperClusterOverP());
    eleEoverPInv_.push_back(1. / ele->ecalEnergy() - 1. / ele->trackMomentumAtVtx().R());
    eleEcalE_.push_back(ele->ecalEnergy());
    elePAtVtx_.push_back(ele->trackMomentumAtVtx().R());
    elePAtSC_.push_back(ele->trackMomentumAtCalo().R());
    elePAtCluster_.push_back(ele->trackMomentumAtEleClus().R());
    elePAtSeed_.push_back(ele->trackMomentumOut().R());
    eledEtaAtVtx_.push_back(ele->deltaEtaSuperClusterTrackAtVtx());
    eledPhiAtVtx_.push_back(ele->deltaPhiSuperClusterTrackAtVtx());
    eledEtaSeedAtVtx_.push_back(ele->deltaEtaSeedClusterTrackAtVtx());
    eleSigmaIEtaIEta_.push_back(ele->sigmaIetaIeta());
    eleSigmaIPhiIPhi_.push_back(ele->sigmaIphiIphi());
    eleBrem_.push_back(ele->fbrem());

    /* updated in CMSSW_10_6_X */
    bool passConvVeto = !ConversionTools::hasMatchedConversion(*ele, *conversions, beamSpot->position());
    eleConvVeto_.push_back((int)passConvVeto);

    // full 5x5
    eleR9_.push_back(ele->r9());
    eleE3x3_.push_back(ele->r9() * ele->superCluster()->energy());
    eleE5x5_.push_back(ele->e5x5());
    eleR9Full5x5_.push_back(ele->full5x5_r9());
    eleE3x3Full5x5_.push_back(ele->full5x5_r9() * ele->superCluster()->energy());
    eleE5x5Full5x5_.push_back(ele->full5x5_e5x5());
    eleSigmaIEtaIEta_2012_.push_back(ele->full5x5_sigmaIetaIeta());

    // isolation
    reco::GsfElectron::PflowIsolationVariables pfIso = ele->pfIsolationVariables();
    elePFChIso_.push_back(pfIso.sumChargedHadronPt);
    elePFPhoIso_.push_back(pfIso.sumPhotonEt);
    elePFNeuIso_.push_back(pfIso.sumNeutralHadronEt);
    elePFPUIso_.push_back(pfIso.sumPUPt);

    // initialize with unphysical values
    float eleIP3D = -999;
    float eleIP3DErr = -999;
    if (pv.isValid()) {
      // 3D impact parameter
      reco::TransientTrack tt = tb->build(ele->gsfTrack().get());
      eleIP3D = IPTools::absoluteImpactParameter3D(tt, pv).second.value();
      eleIP3DErr = IPTools::absoluteImpactParameter3D(tt, pv).second.error();
    }

    eleIP3D_.push_back(eleIP3D);
    eleIP3DErr_.push_back(eleIP3DErr);

    // local coordinates
    edm::Ptr<reco::CaloCluster> theseed = ele->superCluster()->seed();
    auto subdetid = theseed->hitsAndFractions().at(0).first.subdetId();

    /* updated in CMSSW_10_4_X */
    //EcalClusterLocal local;

    /* x, y instead of eta, phi in the endcap */
    float eta, phi, thetatilt, phitilt;
    int ieta, iphi;

    if (subdetid == EcalBarrel) {
      //local.localCoordsEB(*theseed, es, eta, phi, ieta, iphi, thetatilt, phitilt);
      egammaTools::localEcalClusterCoordsEB(*theseed, *caloGeometry, eta, phi, ieta, iphi, thetatilt, phitilt);
    } else {
      //local.localCoordsEE(*theseed, es, eta, phi, ieta, iphi, thetatilt, phitilt);
      egammaTools::localEcalClusterCoordsEE(*theseed, *caloGeometry, eta, phi, ieta, iphi, thetatilt, phitilt);
    }

    eleSeedCryEta_.push_back(eta);
    eleSeedCryPhi_.push_back(phi);
    eleSeedCryIeta_.push_back(ieta);
    eleSeedCryIphi_.push_back(iphi);

    ++nEle_;
  }  // electrons loop
}

void ggHiNtuplizer::fillPhotons(const edm::Event& e, const edm::EventSetup& es, reco::Vertex& pv) {
  edm::Handle<edm::View<reco::Photon>> recoPhotons;
  e.getByToken(photonsToken_, recoPhotons);

  // loop over photons
  for (auto pho = recoPhotons->begin(); pho != recoPhotons->end(); ++pho) {
    phoE_.push_back(pho->energy());
    phoEt_.push_back(pho->et());
    phoEta_.push_back(pho->eta());
    phoPhi_.push_back(pho->phi());

    // energies from different types of corrections
    phoEcorrStdEcal_.push_back(pho->getCorrectedEnergy(reco::Photon::P4type::ecal_standard));
    phoEcorrPhoEcal_.push_back(pho->getCorrectedEnergy(reco::Photon::P4type::ecal_photons));
    phoEcorrRegr1_.push_back(pho->getCorrectedEnergy(reco::Photon::P4type::regression1));
    phoEcorrRegr2_.push_back(pho->getCorrectedEnergy(reco::Photon::P4type::regression2));
    // errors for those corrections
    phoEcorrErrStdEcal_.push_back(pho->getCorrectedEnergyError(reco::Photon::P4type::ecal_standard));
    phoEcorrErrPhoEcal_.push_back(pho->getCorrectedEnergyError(reco::Photon::P4type::ecal_photons));
    phoEcorrErrRegr1_.push_back(pho->getCorrectedEnergyError(reco::Photon::P4type::regression1));
    phoEcorrErrRegr2_.push_back(pho->getCorrectedEnergyError(reco::Photon::P4type::regression2));

    // SuperCluster info
    phoSCE_.push_back(pho->superCluster()->energy());
    phoSCRawE_.push_back(pho->superCluster()->rawEnergy());
    phoSCEta_.push_back(pho->superCluster()->eta());
    phoSCPhi_.push_back(pho->superCluster()->phi());
    phoSCEtaWidth_.push_back(pho->superCluster()->etaWidth());
    phoSCPhiWidth_.push_back(pho->superCluster()->phiWidth());
    phoSCBrem_.push_back(pho->superCluster()->phiWidth() / pho->superCluster()->etaWidth());
    phoSCnHits_.push_back(pho->superCluster()->size());
    phoSCflags_.push_back(pho->superCluster()->flags());
    phoSCinClean_.push_back((int)pho->superCluster()->isInClean());
    phoSCinUnClean_.push_back((int)pho->superCluster()->isInUnclean());
    phoSCnBC_.push_back((int)pho->superCluster()->clustersSize());
    phoESEn_.push_back(pho->superCluster()->preshowerEnergy());

    phoIsPFPhoton_.push_back((int)pho->isPFlowPhoton());
    phoIsStandardPhoton_.push_back((int)pho->isStandardPhoton());
    phoHasPixelSeed_.push_back((int)pho->hasPixelSeed());
    phoHasConversionTracks_.push_back((int)pho->hasConversionTracks());
    phoHadTowerOverEm_.push_back(pho->hadTowOverEm());
    phoHoverE_.push_back(pho->hadronicOverEm());
    phoHoverEValid_.push_back(pho->hadronicOverEmValid());
    phoSigmaIEtaIEta_.push_back(pho->sigmaIetaIeta());
    phoR9_.push_back(pho->r9());

    // additional shower shape variables
    phoE3x3_.push_back(pho->e3x3());
    phoE1x5_.push_back(pho->e1x5());
    phoE2x5_.push_back(pho->e2x5());
    phoE5x5_.push_back(pho->e5x5());
    phoMaxEnergyXtal_.push_back(pho->maxEnergyXtal());
    phoSigmaEtaEta_.push_back(pho->sigmaEtaEta());

    // full 5x5
    phoSigmaIEtaIEta_2012_.push_back(pho->full5x5_sigmaIetaIeta());
    phoR9_2012_.push_back(pho->full5x5_r9());
    phoE1x5_2012_.push_back(pho->full5x5_e1x5());
    phoE2x5_2012_.push_back(pho->full5x5_e2x5());
    phoE3x3_2012_.push_back(pho->full5x5_e3x3());
    phoE5x5_2012_.push_back(pho->full5x5_e5x5());
    phoMaxEnergyXtal_2012_.push_back(pho->full5x5_maxEnergyXtal());
    phoSigmaEtaEta_2012_.push_back(pho->full5x5_sigmaEtaEta());

    // seed BC
    if (pho->superCluster()->seed().isAvailable() && pho->superCluster()->seed().isNonnull()) {
      phoBC1E_.push_back(pho->superCluster()->seed()->energy());
      phoBC1Ecorr_.push_back(pho->superCluster()->seed()->correctedEnergy());
      phoBC1Eta_.push_back(pho->superCluster()->seed()->eta());
      phoBC1Phi_.push_back(pho->superCluster()->seed()->phi());
      phoBC1size_.push_back(pho->superCluster()->seed()->size());
      phoBC1flags_.push_back(pho->superCluster()->seed()->flags());
      phoBC1inClean_.push_back(pho->superCluster()->seed()->isInClean());
      phoBC1inUnClean_.push_back(pho->superCluster()->seed()->isInUnclean());
      phoBC1rawID_.push_back(pho->superCluster()->seed()->seed().rawId());
    } else {
      phoBC1E_.push_back(-999);
      phoBC1Ecorr_.push_back(-999);
      phoBC1Eta_.push_back(-999);
      phoBC1Phi_.push_back(-999);
      phoBC1size_.push_back(-999);
      phoBC1flags_.push_back(-999);
      phoBC1inClean_.push_back(-999);
      phoBC1inUnClean_.push_back(-999);
      phoBC1rawID_.push_back(0);
    }

    /////////////////////////////// MC matching //////////////////////////
    if (doGenParticles_) {
      constexpr float delta2 = 0.15 * 0.15;

      bool gpTemp = false;
      float currentMaxPt = -1;
      int matchedIndex = -1;

      for (unsigned igen = 0; igen < mcEt_.size(); ++igen) {
        if (mcStatus_[igen] != 1 || mcPID_[igen] != 22)
          continue;
        if (reco::deltaR2(pho->eta(), pho->phi(), mcEta_[igen], mcPhi_[igen]) < delta2 && mcPt_[igen] > currentMaxPt) {
          gpTemp = true;
          currentMaxPt = mcPt_[igen];
          matchedIndex = igen;
        }
      }

      // if no matching photon was found try with other particles
      std::vector<int> otherPdgIds_ = {1, 11};
      if (!gpTemp) {
        currentMaxPt = -1;
        for (unsigned igen = 0; igen < mcEt_.size(); ++igen) {
          if (mcStatus_[igen] != 1 ||
              find(otherPdgIds_.begin(), otherPdgIds_.end(), std::abs(mcPID_[igen])) == otherPdgIds_.end())
            continue;
          if (reco::deltaR2(pho->eta(), pho->phi(), mcEta_[igen], mcPhi_[igen]) < delta2 &&
              mcPt_[igen] > currentMaxPt) {
            gpTemp = true;
            currentMaxPt = mcPt_[igen];
            matchedIndex = igen;
          }
        }
      }

      pho_genMatchedIndex_.push_back(matchedIndex);
    }

    nPho_++;
  }  // photons loop
}

void ggHiNtuplizer::fillMuons(const edm::Event& e, const edm::EventSetup& es, reco::Vertex& pv) {
  // Fills tree branches with muons.
  edm::Handle<edm::View<reco::Muon>> recoMuons;
  e.getByToken(muonsToken_, recoMuons);

  for (const auto& mu : *recoMuons) {
    if (mu.pt() < 3.0)
      continue;
    if (!(mu.isPFMuon() || mu.isGlobalMuon() || mu.isTrackerMuon()))
      continue;

    muPt_.push_back(mu.pt());
    muEta_.push_back(mu.eta());
    muPhi_.push_back(mu.phi());
    muCharge_.push_back(mu.charge());
    muType_.push_back(mu.type());
    muIsGood_.push_back(muon::isGoodMuon(mu, muon::selectionTypeFromString("TMOneStationTight")));

    muD0_.push_back(mu.muonBestTrack()->dxy(pv.position()));
    muDz_.push_back(mu.muonBestTrack()->dz(pv.position()));
    muD0Err_.push_back(mu.muonBestTrack()->dxyError());
    muDzErr_.push_back(mu.muonBestTrack()->dzError());

    // initialize with unphysical values
    float muIP3D = -999;
    float muIP3DErr = -999;
    if (pv.isValid()) {
      // 3D impact parameter
      reco::TransientTrack tt = tb->build(mu.muonBestTrack().get());
      muIP3D = IPTools::absoluteImpactParameter3D(tt, pv).second.value();
      muIP3DErr = IPTools::absoluteImpactParameter3D(tt, pv).second.error();
    }
    muIP3D_.push_back(muIP3D);
    muIP3DErr_.push_back(muIP3DErr);

    const reco::TrackRef glbMu = mu.globalTrack();
    const reco::TrackRef innMu = mu.innerTrack();

    if (glbMu.isNull()) {
      muChi2NDF_.push_back(-99);
      muMuonHits_.push_back(-99);
    } else {
      muChi2NDF_.push_back(glbMu->normalizedChi2());
      muMuonHits_.push_back(glbMu->hitPattern().numberOfValidMuonHits());
    }

    if (innMu.isNull()) {
      muInnerD0_.push_back(-99);
      muInnerDz_.push_back(-99);

      muInnerD0Err_.push_back(-99);
      muInnerDzErr_.push_back(-99);
      muInnerPt_.push_back(-99);
      muInnerPtErr_.push_back(-99);
      muInnerEta_.push_back(-99);

      muTrkLayers_.push_back(-99);
      muPixelLayers_.push_back(-99);
      muPixelHits_.push_back(-99);
      muTrkQuality_.push_back(-99);
    } else {
      muInnerD0_.push_back(innMu->dxy(pv.position()));
      muInnerDz_.push_back(innMu->dz(pv.position()));

      muInnerD0Err_.push_back(innMu->dxyError());
      muInnerDzErr_.push_back(innMu->dzError());
      muInnerPt_.push_back(innMu->pt());
      muInnerPtErr_.push_back(innMu->ptError());
      muInnerEta_.push_back(innMu->eta());

      muTrkLayers_.push_back(innMu->hitPattern().trackerLayersWithMeasurement());
      muPixelLayers_.push_back(innMu->hitPattern().pixelLayersWithMeasurement());
      muPixelHits_.push_back(innMu->hitPattern().numberOfValidPixelHits());
      muTrkQuality_.push_back(innMu->quality(reco::TrackBase::highPurity));
    }

    muStations_.push_back(mu.numberOfMatchedStations());
    muIsoTrk_.push_back(mu.isolationR03().sumPt);
    muPFChIso_.push_back(mu.pfIsolationR04().sumChargedHadronPt);
    muPFPhoIso_.push_back(mu.pfIsolationR04().sumPhotonEt);
    muPFNeuIso_.push_back(mu.pfIsolationR04().sumNeutralHadronEt);
    muPFPUIso_.push_back(mu.pfIsolationR04().sumPUPt);

    muIDSoft_.push_back(mu.passed(reco::Muon::SoftMvaId));
    muIDLoose_.push_back(mu.passed(reco::Muon::CutBasedIdLoose));
    muIDMedium_.push_back(mu.passed(reco::Muon::CutBasedIdMedium));
    muIDMediumPrompt_.push_back(mu.passed(reco::Muon::CutBasedIdMediumPrompt));
    muIDTight_.push_back(mu.passed(reco::Muon::CutBasedIdTight));
    muIDGlobalHighPt_.push_back(mu.passed(reco::Muon::CutBasedIdGlobalHighPt));
    muIDTrkHighPt_.push_back(mu.passed(reco::Muon::CutBasedIdTrkHighPt));
    muIDInTime_.push_back(mu.passed(reco::Muon::InTimeMuon));

    nMu_++;
  }  // muons loop
}

DEFINE_FWK_MODULE(ggHiNtuplizer);
