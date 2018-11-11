#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "EgammaAnalysis/ElectronTools/interface/SuperClusterHelper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "HeavyIonsAnalysis/PhotonAnalysis/interface/GenParticleParentage.h"
#include "HeavyIonsAnalysis/PhotonAnalysis/interface/ggHiNtuplizer.h"
#include "HeavyIonsAnalysis/PhotonAnalysis/src/pfIsoCalculator.h"

ggHiNtuplizer::ggHiNtuplizer(const edm::ParameterSet& ps) :
  effectiveAreas_( (ps.getParameter<edm::FileInPath>("effAreasConfigFile")).fullPath() )
{
  // class instance configuration
  doGenParticles_         = ps.getParameter<bool>("doGenParticles");
  doElectrons_            = ps.getParameter<bool>("doElectrons");
  doPhotons_              = ps.getParameter<bool>("doPhotons");
  doMuons_                = ps.getParameter<bool>("doMuons");
  runOnParticleGun_       = ps.getParameter<bool>("runOnParticleGun");
  useValMapIso_           = ps.getParameter<bool>("useValMapIso");
  doPfIso_                = ps.getParameter<bool>("doPfIso");
  doRecHitsEB_            = ps.getParameter<bool>("doRecHitsEB");
  doRecHitsEE_            = ps.getParameter<bool>("doRecHitsEE");
  if (doGenParticles_) {
    genPileupCollection_    = consumes<std::vector<PileupSummaryInfo>>(ps.getParameter<edm::InputTag>("pileupCollection"));
    genParticlesCollection_ = consumes<std::vector<reco::GenParticle>>(ps.getParameter<edm::InputTag>("genParticleSrc"));
  }
  if (doElectrons_)
    gsfElectronsCollection_ = consumes<edm::View<reco::GsfElectron>>(ps.getParameter<edm::InputTag>("gsfElectronLabel"));
  if (doPhotons_)
    recoPhotonsCollection_  = consumes<edm::View<reco::Photon>>(ps.getParameter<edm::InputTag>("recoPhotonSrc"));
  if (doMuons_)
    recoMuonsCollection_    = consumes<edm::View<reco::Muon>>(ps.getParameter<edm::InputTag>("recoMuonSrc"));
  vtxCollection_          = consumes<std::vector<reco::Vertex>>(ps.getParameter<edm::InputTag>("VtxLabel"));
  doVID_                  = ps.getParameter<bool>("doElectronVID");
  if (doVID_) {
    rhoToken_               = consumes<double>(ps.getParameter<edm::InputTag>("rho"));
    beamSpotToken_          = consumes<reco::BeamSpot>(ps.getParameter <edm::InputTag>("beamSpot"));
    conversionsToken_       = consumes< reco::ConversionCollection >(ps.getParameter<edm::InputTag>("conversions"));
    eleVetoIdMapToken_      = consumes<edm::ValueMap<bool> >(ps.getParameter<edm::InputTag>("electronVetoID"));
    eleLooseIdMapToken_     = consumes<edm::ValueMap<bool> >(ps.getParameter<edm::InputTag>("electronLooseID"));
    eleMediumIdMapToken_    = consumes<edm::ValueMap<bool> >(ps.getParameter<edm::InputTag>("electronMediumID"));
    eleTightIdMapToken_     = consumes<edm::ValueMap<bool> >(ps.getParameter<edm::InputTag>("electronTightID"));
  }
  if (useValMapIso_) {
    recoPhotonsHiIso_     = consumes<edm::ValueMap<reco::HIPhotonIsolation> > (
      ps.getParameter<edm::InputTag>("recoPhotonHiIsolationMap"));
  }
  if(doRecHitsEB_){
      recHitsEB_ = consumes<EcalRecHitCollection> (
        ps.getUntrackedParameter<edm::InputTag>("recHitsEB",
          edm::InputTag("ecalRecHit","EcalRecHitsEB")));
  }
  if(doRecHitsEE_){
      recHitsEE_ = consumes<EcalRecHitCollection> (
        ps.getUntrackedParameter<edm::InputTag>("recHitsEE",
          edm::InputTag("ecalRecHit","EcalRecHitsEE")));
  }

  if (doPfIso_) {
    pfCollection_         = consumes<edm::View<reco::PFCandidate> > (
      ps.getParameter<edm::InputTag>("particleFlowCollection"));
  }

  // initialize output TTree
  edm::Service<TFileService> fs;
  tree_ = fs->make<TTree>("EventTree", "Event data");

  tree_->Branch("run",    &run_);
  tree_->Branch("event",  &event_);
  tree_->Branch("lumis",  &lumis_);
  tree_->Branch("isData", &isData_);

  if (doGenParticles_) {
    tree_->Branch("nPUInfo",      &nPUInfo_);
    tree_->Branch("nPU",          &nPU_);
    tree_->Branch("puBX",         &puBX_);
    tree_->Branch("puTrue",       &puTrue_);

    tree_->Branch("nMC",          &nMC_);
    tree_->Branch("mcPID",        &mcPID_);
    tree_->Branch("mcStatus",     &mcStatus_);
    tree_->Branch("mcVtx_x",      &mcVtx_x_);
    tree_->Branch("mcVtx_y",      &mcVtx_y_);
    tree_->Branch("mcVtx_z",      &mcVtx_z_);
    tree_->Branch("mcPt",         &mcPt_);
    tree_->Branch("mcEta",        &mcEta_);
    tree_->Branch("mcPhi",        &mcPhi_);
    tree_->Branch("mcE",          &mcE_);
    tree_->Branch("mcEt",         &mcEt_);
    tree_->Branch("mcMass",       &mcMass_);
    tree_->Branch("mcParentage",  &mcParentage_);
    tree_->Branch("mcMomPID",     &mcMomPID_);
    tree_->Branch("mcMomPt",      &mcMomPt_);
    tree_->Branch("mcMomEta",     &mcMomEta_);
    tree_->Branch("mcMomPhi",     &mcMomPhi_);
    tree_->Branch("mcMomMass",    &mcMomMass_);
    tree_->Branch("mcGMomPID",    &mcGMomPID_);
    tree_->Branch("mcIndex",      &mcIndex_);
    tree_->Branch("mcCalIsoDR03", &mcCalIsoDR03_);
    tree_->Branch("mcCalIsoDR04", &mcCalIsoDR04_);
    tree_->Branch("mcTrkIsoDR03", &mcTrkIsoDR03_);
    tree_->Branch("mcTrkIsoDR04", &mcTrkIsoDR04_);
  }

  if (doElectrons_) {
    tree_->Branch("nEle",                  &nEle_);
    tree_->Branch("eleCharge",             &eleCharge_);
    tree_->Branch("eleChargeConsistent",   &eleChargeConsistent_);
    tree_->Branch("eleSCPixCharge",        &eleSCPixCharge_);
    tree_->Branch("eleCtfCharge",          &eleCtfCharge_);
    tree_->Branch("eleEn",                 &eleEn_);
    tree_->Branch("eleD0",                 &eleD0_);
    tree_->Branch("eleDz",                 &eleDz_);
    tree_->Branch("eleD0Err",              &eleD0Err_);
    tree_->Branch("eleDzErr",              &eleDzErr_);
    tree_->Branch("eleTrkPt",              &eleTrkPt_);
    tree_->Branch("eleTrkEta",             &eleTrkEta_);
    tree_->Branch("eleTrkPhi",             &eleTrkPhi_);
    tree_->Branch("eleTrkCharge",          &eleTrkCharge_);
    tree_->Branch("eleTrkChi2",            &eleTrkChi2_);
    tree_->Branch("eleTrkNdof",            &eleTrkNdof_);
    tree_->Branch("eleTrkNormalizedChi2",  &eleTrkNormalizedChi2_);
    tree_->Branch("eleTrkValidHits",       &eleTrkValidHits_);
    tree_->Branch("eleTrkLayers",          &eleTrkLayers_);

    tree_->Branch("elePt",                 &elePt_);
    tree_->Branch("eleEta",                &eleEta_);
    tree_->Branch("elePhi",                &elePhi_);
    tree_->Branch("eleSCEn",               &eleSCEn_);
    tree_->Branch("eleESEn",               &eleESEn_);
    tree_->Branch("eleSCEta",              &eleSCEta_);
    tree_->Branch("eleSCPhi",              &eleSCPhi_);
    tree_->Branch("eleSCRawEn",            &eleSCRawEn_);
    tree_->Branch("eleSCEtaWidth",         &eleSCEtaWidth_);
    tree_->Branch("eleSCPhiWidth",         &eleSCPhiWidth_);
    tree_->Branch("eleHoverE",             &eleHoverE_);
    tree_->Branch("eleHoverEBc",           &eleHoverEBc_);
    tree_->Branch("eleEoverP",             &eleEoverP_);
    tree_->Branch("eleEoverPInv",          &eleEoverPInv_);
    tree_->Branch("eleBrem",               &eleBrem_);
    tree_->Branch("eledEtaAtVtx",          &eledEtaAtVtx_);
    tree_->Branch("eledPhiAtVtx",          &eledPhiAtVtx_);
    tree_->Branch("eleSigmaIEtaIEta",      &eleSigmaIEtaIEta_);
    tree_->Branch("eleSigmaIEtaIEta_2012", &eleSigmaIEtaIEta_2012_);
    tree_->Branch("eleSigmaIPhiIPhi",      &eleSigmaIPhiIPhi_);
    // tree_->Branch("eleConvVeto",           &eleConvVeto_);  // TODO: not available in reco::
    tree_->Branch("eleMissHits",           &eleMissHits_);
    tree_->Branch("eleESEffSigmaRR",       &eleESEffSigmaRR_);
    tree_->Branch("elePFChIso",            &elePFChIso_);
    tree_->Branch("elePFPhoIso",           &elePFPhoIso_);
    tree_->Branch("elePFNeuIso",           &elePFNeuIso_);
    tree_->Branch("elePFPUIso",            &elePFPUIso_);
    tree_->Branch("elePFChIso03",          &elePFChIso03_);
    tree_->Branch("elePFPhoIso03",         &elePFPhoIso03_);
    tree_->Branch("elePFNeuIso03",         &elePFNeuIso03_);
    tree_->Branch("elePFChIso04",          &elePFChIso04_);
    tree_->Branch("elePFPhoIso04",         &elePFPhoIso04_);
    tree_->Branch("elePFNeuIso04",         &elePFNeuIso04_);
    tree_->Branch("elePFRelIsoWithEA",     &elePFRelIsoWithEA_);
    tree_->Branch("elePFRelIsoWithDBeta",  &elePFRelIsoWithDBeta_);

    tree_->Branch("eleR9",                 &eleR9_);
    tree_->Branch("eleE3x3",               &eleE3x3_);
    tree_->Branch("eleE5x5",               &eleE5x5_);
    tree_->Branch("eleR9Full5x5",          &eleR9Full5x5_);
    tree_->Branch("eleE3x3Full5x5",        &eleE3x3Full5x5_);
    tree_->Branch("eleE5x5Full5x5",        &eleE5x5Full5x5_);
    tree_->Branch("NClusters",             &NClusters_);
    tree_->Branch("NEcalClusters",         &NEcalClusters_);
    tree_->Branch("eleSeedEn",             &eleSeedEn_);
    tree_->Branch("eleSeedEta",            &eleSeedEta_);
    tree_->Branch("eleSeedPhi",            &eleSeedPhi_);
    tree_->Branch("eleSeedCryEta",         &eleSeedCryEta_);
    tree_->Branch("eleSeedCryPhi",         &eleSeedCryPhi_);
    tree_->Branch("eleSeedCryIeta",        &eleSeedCryIeta_);
    tree_->Branch("eleSeedCryIphi",        &eleSeedCryIphi_);

    tree_->Branch("eleBC1E",               &eleBC1E_);
    tree_->Branch("eleBC1Eta",             &eleBC1Eta_);
    tree_->Branch("eleBC2E",               &eleBC2E_);
    tree_->Branch("eleBC2Eta",             &eleBC2Eta_);
    tree_->Branch("eleIDVeto",             &eleIDVeto_);
    tree_->Branch("eleIDLoose",            &eleIDLoose_);
    tree_->Branch("eleIDMedium",           &eleIDMedium_);
    tree_->Branch("eleIDTight",            &eleIDTight_);
    tree_->Branch("elepassConversionVeto", &elepassConversionVeto_);
    tree_->Branch("eleEffAreaTimesRho",    &eleEffAreaTimesRho_);
  }

  if (doPhotons_) {
    tree_->Branch("nPho",                  &nPho_);
    tree_->Branch("phoE",                  &phoE_);
    tree_->Branch("phoEt",                 &phoEt_);
    tree_->Branch("phoEta",                &phoEta_);
    tree_->Branch("phoPhi",                &phoPhi_);

    tree_->Branch("phoEcorrStdEcal",       &phoEcorrStdEcal_);
    tree_->Branch("phoEcorrPhoEcal",       &phoEcorrPhoEcal_);
    tree_->Branch("phoEcorrRegr1",         &phoEcorrRegr1_);
    tree_->Branch("phoEcorrRegr2",         &phoEcorrRegr2_);
    tree_->Branch("phoEcorrErrStdEcal",    &phoEcorrErrStdEcal_);
    tree_->Branch("phoEcorrErrPhoEcal",    &phoEcorrErrPhoEcal_);
    tree_->Branch("phoEcorrErrRegr1",      &phoEcorrErrRegr1_);
    tree_->Branch("phoEcorrErrRegr2",      &phoEcorrErrRegr2_);

    tree_->Branch("phoSCE",                &phoSCE_);
    tree_->Branch("phoSCRawE",             &phoSCRawE_);
    tree_->Branch("phoSCEta",              &phoSCEta_);
    tree_->Branch("phoSCPhi",              &phoSCPhi_);
    tree_->Branch("phoSCEtaWidth",         &phoSCEtaWidth_);
    tree_->Branch("phoSCPhiWidth",         &phoSCPhiWidth_);
    tree_->Branch("phoSCBrem",             &phoSCBrem_);
    tree_->Branch("phoSCnHits",            &phoSCnHits_);
    tree_->Branch("phoSCflags",            &phoSCflags_);
    tree_->Branch("phoSCinClean",          &phoSCinClean_);
    tree_->Branch("phoSCinUnClean",        &phoSCinUnClean_);
    tree_->Branch("phoSCnBC",              &phoSCnBC_);
    tree_->Branch("phoESEn",               &phoESEn_);

    tree_->Branch("phoPSCE",               &phoPSCE_);
    tree_->Branch("phoPSCRawE",            &phoPSCRawE_);
    tree_->Branch("phoPSCEta",             &phoPSCEta_);
    tree_->Branch("phoPSCPhi",             &phoPSCPhi_);
    tree_->Branch("phoPSCEtaWidth",        &phoPSCEtaWidth_);
    tree_->Branch("phoPSCPhiWidth",        &phoPSCPhiWidth_);
    tree_->Branch("phoPSCBrem",            &phoPSCBrem_);
    tree_->Branch("phoPSCnHits",           &phoPSCnHits_);
    tree_->Branch("phoPSCflags",           &phoPSCflags_);
    tree_->Branch("phoPSCinClean",         &phoPSCinClean_);
    tree_->Branch("phoPSCinUnClean",       &phoPSCinUnClean_);
    tree_->Branch("phoPSCnBC",             &phoPSCnBC_);
    tree_->Branch("phoPESEn",              &phoPESEn_);

    tree_->Branch("phoIsPFPhoton",         &phoIsPFPhoton_);
    tree_->Branch("phoIsStandardPhoton",   &phoIsStandardPhoton_);
    tree_->Branch("phoHasPixelSeed",       &phoHasPixelSeed_);
    tree_->Branch("phoHasConversionTracks",&phoHasConversionTracks_);
    // tree_->Branch("phoEleVeto",            &phoEleVeto_);        // TODO: not available in reco::
    tree_->Branch("phoR9",                 &phoR9_);
    tree_->Branch("phoHadTowerOverEm",     &phoHadTowerOverEm_);
    tree_->Branch("phoHoverE",             &phoHoverE_);
    tree_->Branch("phoSigmaIEtaIEta",      &phoSigmaIEtaIEta_);
    // tree_->Branch("phoSigmaIEtaIPhi",      &phoSigmaIEtaIPhi_);  // TODO: not available in reco::
    // tree_->Branch("phoSigmaIPhiIPhi",      &phoSigmaIPhiIPhi_);  // TODO: not available in reco::
    tree_->Branch("phoE1x5",               &phoE1x5_);
    tree_->Branch("phoE2x5",               &phoE2x5_);
    tree_->Branch("phoE3x3",               &phoE3x3_);
    tree_->Branch("phoE5x5",               &phoE5x5_);
    tree_->Branch("phoMaxEnergyXtal",      &phoMaxEnergyXtal_);
    tree_->Branch("phoSigmaEtaEta",        &phoSigmaEtaEta_);
    tree_->Branch("phoR1x5",               &phoR1x5_);
    tree_->Branch("phoR2x5",               &phoR2x5_);
    tree_->Branch("phoR9_2012",            &phoR9_2012_);
    tree_->Branch("phoSigmaIEtaIEta_2012", &phoSigmaIEtaIEta_2012_);
    tree_->Branch("phoE1x5_2012",          &phoE1x5_2012_);
    tree_->Branch("phoE2x5_2012",          &phoE2x5_2012_);
    tree_->Branch("phoE3x3_2012",          &phoE3x3_2012_);
    tree_->Branch("phoE5x5_2012",          &phoE5x5_2012_);
    tree_->Branch("phoMaxEnergyXtal_2012", &phoMaxEnergyXtal_2012_);
    tree_->Branch("phoSigmaEtaEta_2012",   &phoSigmaEtaEta_2012_);
    tree_->Branch("phoR1x5_2012",          &phoR1x5_2012_);
    tree_->Branch("phoR2x5_2012",          &phoR2x5_2012_);

    tree_->Branch("phoBC1E",               &phoBC1E_);
    tree_->Branch("phoBC1Ecorr",           &phoBC1Ecorr_);
    tree_->Branch("phoBC1Eta",             &phoBC1Eta_);
    tree_->Branch("phoBC1Phi",             &phoBC1Phi_);
    tree_->Branch("phoBC1size",            &phoBC1size_);
    tree_->Branch("phoBC1flags",           &phoBC1flags_);
    tree_->Branch("phoBC1inClean",         &phoBC1inClean_);
    tree_->Branch("phoBC1inUnClean",       &phoBC1inUnClean_);
    tree_->Branch("phoBC1rawID",           &phoBC1rawID_);

    /* tree_->Branch("phoBC2E",               &phoBC2E_); */
    /* tree_->Branch("phoBC2Eta",             &phoBC2Eta_); */
    /* tree_->Branch("phoBC2Phi",             &phoBC2Phi_); */

    tree_->Branch("pho_ecalClusterIsoR2", &pho_ecalClusterIsoR2_);
    tree_->Branch("pho_ecalClusterIsoR3", &pho_ecalClusterIsoR3_);
    tree_->Branch("pho_ecalClusterIsoR4", &pho_ecalClusterIsoR4_);
    tree_->Branch("pho_ecalClusterIsoR5", &pho_ecalClusterIsoR5_);
    tree_->Branch("pho_hcalRechitIsoR1", &pho_hcalRechitIsoR1_);
    tree_->Branch("pho_hcalRechitIsoR2", &pho_hcalRechitIsoR2_);
    tree_->Branch("pho_hcalRechitIsoR3", &pho_hcalRechitIsoR3_);
    tree_->Branch("pho_hcalRechitIsoR4", &pho_hcalRechitIsoR4_);
    tree_->Branch("pho_hcalRechitIsoR5", &pho_hcalRechitIsoR5_);
    tree_->Branch("pho_trackIsoR1PtCut20", &pho_trackIsoR1PtCut20_);
    tree_->Branch("pho_trackIsoR2PtCut20", &pho_trackIsoR2PtCut20_);
    tree_->Branch("pho_trackIsoR3PtCut20", &pho_trackIsoR3PtCut20_);
    tree_->Branch("pho_trackIsoR4PtCut20", &pho_trackIsoR4PtCut20_);
    tree_->Branch("pho_trackIsoR5PtCut20", &pho_trackIsoR5PtCut20_);
    tree_->Branch("pho_swissCrx", &pho_swissCrx_);
    tree_->Branch("pho_seedTime", &pho_seedTime_);

    if (doGenParticles_) {
      tree_->Branch("pho_genMatchedIndex", &pho_genMatchedIndex_);
    }

    if (doRecHitsEB_ || doRecHitsEE_) {
      // rechit info
      tree_->Branch("nRH", &nRH_);
      tree_->Branch("rhRawId", &rhRawId_);
      tree_->Branch("rhieta", &rhieta_);
      tree_->Branch("rhiphi", &rhiphi_);
      tree_->Branch("rhix", &rhix_);
      tree_->Branch("rhiy", &rhiy_);
      tree_->Branch("rhE", &rhE_);
      tree_->Branch("rhEt", &rhEt_);
      tree_->Branch("rhEta", &rhEta_);
      tree_->Branch("rhPhi", &rhPhi_);
      tree_->Branch("rhChi2", &rhChi2_);
      tree_->Branch("rhEerror", &rhEerror_);
      tree_->Branch("rhFlags", &rhFlags_);
      tree_->Branch("rhPhoIdx", &rhPhoIdx_);
      tree_->Branch("rhBCIdx", &rhBCIdx_);
    }

    if (doPfIso_) {
      tree_->Branch("pfcIso1",&pfcIso1);
      tree_->Branch("pfcIso2",&pfcIso2);
      tree_->Branch("pfcIso3",&pfcIso3);
      tree_->Branch("pfcIso4",&pfcIso4);
      tree_->Branch("pfcIso5",&pfcIso5);

      tree_->Branch("pfpIso1",&pfpIso1);
      tree_->Branch("pfpIso2",&pfpIso2);
      tree_->Branch("pfpIso3",&pfpIso3);
      tree_->Branch("pfpIso4",&pfpIso4);
      tree_->Branch("pfpIso5",&pfpIso5);

      tree_->Branch("pfnIso1",&pfnIso1);
      tree_->Branch("pfnIso2",&pfnIso2);
      tree_->Branch("pfnIso3",&pfnIso3);
      tree_->Branch("pfnIso4",&pfnIso4);
      tree_->Branch("pfnIso5",&pfnIso5);
    }
  }

  if (doMuons_) {
    tree_->Branch("nMu",                   &nMu_);
    tree_->Branch("muPt",                  &muPt_);
    tree_->Branch("muEta",                 &muEta_);
    tree_->Branch("muPhi",                 &muPhi_);
    tree_->Branch("muCharge",              &muCharge_);
    tree_->Branch("muType",                &muType_);
    tree_->Branch("muIsGood",              &muIsGood_);
    tree_->Branch("muD0",                  &muD0_);
    tree_->Branch("muDz",                  &muDz_);
    tree_->Branch("muChi2NDF",             &muChi2NDF_);
    tree_->Branch("muInnerD0",             &muInnerD0_);
    tree_->Branch("muInnerDz",             &muInnerDz_);
    tree_->Branch("muTrkLayers",           &muTrkLayers_);
    tree_->Branch("muPixelLayers",         &muPixelLayers_);
    tree_->Branch("muPixelHits",           &muPixelHits_);
    tree_->Branch("muMuonHits",            &muMuonHits_);
    tree_->Branch("muTrkQuality",          &muTrkQuality_);
    tree_->Branch("muStations",            &muStations_);
    tree_->Branch("muIsoTrk",              &muIsoTrk_);
    tree_->Branch("muPFChIso",             &muPFChIso_);
    tree_->Branch("muPFPhoIso",            &muPFPhoIso_);
    tree_->Branch("muPFNeuIso",            &muPFNeuIso_);
    tree_->Branch("muPFPUIso",             &muPFPUIso_);
  }
}

void ggHiNtuplizer::analyze(const edm::Event& e, const edm::EventSetup& es)
{
  // cleanup from previous event

  if (doGenParticles_) {
    nPUInfo_ = 0;
    nPU_                  .clear();
    puBX_                 .clear();
    puTrue_               .clear();

    nMC_ = 0;
    mcPID_                .clear();
    mcStatus_             .clear();
    mcVtx_x_              .clear();
    mcVtx_y_              .clear();
    mcVtx_z_              .clear();
    mcPt_                 .clear();
    mcEta_                .clear();
    mcPhi_                .clear();
    mcE_                  .clear();
    mcEt_                 .clear();
    mcMass_               .clear();
    mcParentage_          .clear();
    mcMomPID_             .clear();
    mcMomPt_              .clear();
    mcMomEta_             .clear();
    mcMomPhi_             .clear();
    mcMomMass_            .clear();
    mcGMomPID_            .clear();
    mcIndex_              .clear();
    mcCalIsoDR03_         .clear();
    mcCalIsoDR04_         .clear();
    mcTrkIsoDR03_         .clear();
    mcTrkIsoDR04_         .clear();
  }

  if (doElectrons_) {
    nEle_ = 0;
    eleCharge_            .clear();
    eleChargeConsistent_  .clear();
    eleSCPixCharge_       .clear();
    eleCtfCharge_         .clear();
    eleEn_                .clear();
    eleD0_                .clear();
    eleDz_                .clear();
    eleD0Err_             .clear();
    eleDzErr_             .clear();
    eleTrkPt_             .clear();
    eleTrkEta_            .clear();
    eleTrkPhi_            .clear();
    eleTrkCharge_         .clear();
    eleTrkChi2_           .clear();
    eleTrkNdof_           .clear();
    eleTrkNormalizedChi2_ .clear();
    eleTrkValidHits_      .clear();
    eleTrkLayers_         .clear();
    elePt_                .clear();
    eleEta_               .clear();
    elePhi_               .clear();
    eleSCEn_              .clear();
    eleESEn_              .clear();
    eleSCEta_             .clear();
    eleSCPhi_             .clear();
    eleSCRawEn_           .clear();
    eleSCEtaWidth_        .clear();
    eleSCPhiWidth_        .clear();
    eleHoverE_            .clear();
    eleHoverEBc_          .clear();
    eleEoverP_            .clear();
    eleEoverPInv_         .clear();
    eleBrem_              .clear();
    eledEtaAtVtx_         .clear();
    eledPhiAtVtx_         .clear();
    eleSigmaIEtaIEta_     .clear();
    eleSigmaIEtaIEta_2012_.clear();
    eleSigmaIPhiIPhi_     .clear();
    // eleConvVeto_          .clear();  // TODO: not available in reco::
    eleMissHits_          .clear();
    eleESEffSigmaRR_      .clear();
    elePFChIso_           .clear();
    elePFPhoIso_          .clear();
    elePFNeuIso_          .clear();
    elePFPUIso_           .clear();
    elePFChIso03_         .clear();
    elePFPhoIso03_        .clear();
    elePFNeuIso03_        .clear();
    elePFChIso04_         .clear();
    elePFPhoIso04_        .clear();
    elePFNeuIso04_        .clear();
    elePFRelIsoWithEA_    .clear();
    elePFRelIsoWithDBeta_ .clear();
    eleR9_                .clear();
    eleE3x3_              .clear();
    eleE5x5_              .clear();
    eleR9Full5x5_         .clear();
    eleE3x3Full5x5_       .clear();
    eleE5x5Full5x5_       .clear();
    NClusters_            .clear();
    NEcalClusters_        .clear();
    eleSeedEn_            .clear();
    eleSeedEta_           .clear();
    eleSeedPhi_           .clear();
    eleSeedCryEta_        .clear();
    eleSeedCryPhi_        .clear();
    eleSeedCryIeta_       .clear();
    eleSeedCryIphi_       .clear();
    eleBC1E_              .clear();
    eleBC1Eta_            .clear();
    eleBC2E_              .clear();
    eleBC2Eta_            .clear();
    eleIDVeto_            .clear();
    eleIDLoose_           .clear();
    eleIDMedium_          .clear();
    eleIDTight_           .clear();
    elepassConversionVeto_.clear();
    eleEffAreaTimesRho_   .clear();
  }

  if (doPhotons_) {
    nPho_ = 0;
    phoE_                 .clear();
    phoEt_                .clear();
    phoEta_               .clear();
    phoPhi_               .clear();

    phoEcorrStdEcal_      .clear();
    phoEcorrPhoEcal_      .clear();
    phoEcorrRegr1_        .clear();
    phoEcorrRegr2_        .clear();
    phoEcorrErrStdEcal_   .clear();
    phoEcorrErrPhoEcal_   .clear();
    phoEcorrErrRegr1_     .clear();
    phoEcorrErrRegr2_     .clear();

    phoSCE_               .clear();
    phoSCRawE_            .clear();
    phoSCEta_             .clear();
    phoSCPhi_             .clear();
    phoSCEtaWidth_        .clear();
    phoSCPhiWidth_        .clear();
    phoSCBrem_            .clear();
    phoSCnHits_           .clear();
    phoSCflags_           .clear();
    phoSCinClean_         .clear();
    phoSCinUnClean_       .clear();
    phoSCnBC_             .clear();
    phoESEn_              .clear();

    phoPSCE_              .clear();
    phoPSCRawE_           .clear();
    phoPSCEta_            .clear();
    phoPSCPhi_            .clear();
    phoPSCEtaWidth_       .clear();
    phoPSCPhiWidth_       .clear();
    phoPSCBrem_           .clear();
    phoPSCnHits_          .clear();
    phoPSCflags_          .clear();
    phoPSCinClean_        .clear();
    phoPSCinUnClean_      .clear();
    phoPSCnBC_            .clear();
    phoPESEn_             .clear();

    phoIsPFPhoton_        .clear();
    phoIsStandardPhoton_  .clear();
    phoHasPixelSeed_      .clear();
    phoHasConversionTracks_.clear();
    // phoEleVeto_           .clear();  // TODO: not available in reco::
    phoR9_                .clear();
    phoHadTowerOverEm_    .clear();
    phoHoverE_            .clear();
    phoSigmaIEtaIEta_     .clear();
    // phoSigmaIEtaIPhi_     .clear();  // TODO: not available in reco::
    // phoSigmaIPhiIPhi_     .clear();  // TODO: not available in reco::
    phoE1x5_              .clear();
    phoE2x5_              .clear();
    phoE3x3_              .clear();
    phoE5x5_              .clear();
    phoMaxEnergyXtal_     .clear();
    phoSigmaEtaEta_       .clear();
    phoR1x5_              .clear();
    phoR2x5_              .clear();
    phoR9_2012_           .clear();
    phoSigmaIEtaIEta_2012_.clear();
    phoE1x5_2012_         .clear();
    phoE2x5_2012_         .clear();
    phoE3x3_2012_         .clear();
    phoE5x5_2012_         .clear();
    phoMaxEnergyXtal_2012_.clear();
    phoSigmaEtaEta_2012_  .clear();
    phoR1x5_2012_         .clear();
    phoR2x5_2012_         .clear();

    phoBC1E_              .clear();
    phoBC1Ecorr_          .clear();
    phoBC1Eta_            .clear();
    phoBC1Phi_            .clear();
    phoBC1size_           .clear();
    phoBC1flags_          .clear();
    phoBC1inClean_        .clear();
    phoBC1inUnClean_      .clear();
    phoBC1rawID_          .clear();

    /* phoBC2E_              .clear(); */
    /* phoBC2Eta_            .clear(); */
    /* phoBC2Phi_            .clear(); */
    pho_ecalClusterIsoR2_.clear();
    pho_ecalClusterIsoR3_.clear();
    pho_ecalClusterIsoR4_.clear();
    pho_ecalClusterIsoR5_.clear();
    pho_hcalRechitIsoR1_.clear();
    pho_hcalRechitIsoR2_.clear();
    pho_hcalRechitIsoR3_.clear();
    pho_hcalRechitIsoR4_.clear();
    pho_hcalRechitIsoR5_.clear();
    pho_trackIsoR1PtCut20_.clear();
    pho_trackIsoR2PtCut20_.clear();
    pho_trackIsoR3PtCut20_.clear();
    pho_trackIsoR4PtCut20_.clear();
    pho_trackIsoR5PtCut20_.clear();
    pho_swissCrx_.clear();
    pho_seedTime_.clear();

    pho_genMatchedIndex_.clear();

    // rechit info
    if (doRecHitsEB_ || doRecHitsEE_) {
      nRH_ = 0;
      rhRawId_.clear();
      rhieta_.clear();
      rhiphi_.clear();
      rhix_.clear();
      rhiy_.clear();
      rhE_.clear();
      rhEt_.clear();
      rhEta_.clear();
      rhPhi_.clear();
      rhChi2_.clear();
      rhEerror_.clear();
      rhFlags_.clear();
      rhPhoIdx_.clear();
      rhBCIdx_.clear();
    }

    //photon pf isolation stuff
    if (doPfIso_) {
      pfcIso1.clear();
      pfcIso2.clear();
      pfcIso3.clear();
      pfcIso4.clear();
      pfcIso5.clear();
      pfpIso1.clear();
      pfpIso2.clear();
      pfpIso3.clear();
      pfpIso4.clear();
      pfpIso5.clear();
      pfnIso1.clear();
      pfnIso2.clear();
      pfnIso3.clear();
      pfnIso4.clear();
      pfnIso5.clear();
    }
  }

  if (doMuons_) {
    nMu_ = 0;
    muPt_                 .clear();
    muEta_                .clear();
    muPhi_                .clear();
    muCharge_             .clear();
    muType_               .clear();
    muIsGood_             .clear();
    muD0_                 .clear();
    muDz_                 .clear();
    muChi2NDF_            .clear();
    muInnerD0_            .clear();
    muInnerDz_            .clear();
    muTrkLayers_          .clear();
    muPixelLayers_        .clear();
    muPixelHits_          .clear();
    muMuonHits_           .clear();
    muTrkQuality_         .clear();
    muStations_           .clear();
    muIsoTrk_             .clear();
    muPFChIso_            .clear();
    muPFPhoIso_           .clear();
    muPFNeuIso_           .clear();
    muPFPUIso_            .clear();
  }

  run_    = e.id().run();
  event_  = e.id().event();
  lumis_  = e.luminosityBlock();
  isData_ = e.isRealData();

  // MC truth
  if (doGenParticles_ && !isData_) {
    fillGenPileupInfo(e);
    fillGenParticles(e);
  }

  edm::Handle<std::vector<reco::Vertex> > vtxHandle;
  e.getByToken(vtxCollection_, vtxHandle);

  // best-known primary vertex coordinates
  math::XYZPoint pv(0, 0, 0);
  for (const auto& v : *vtxHandle)
    if (!v.isFake()) {
      pv.SetXYZ(v.x(), v.y(), v.z());
      break;
    }

  if (doRecHitsEB_ || doRecHitsEE_) {
      edm::ESHandle<CaloGeometry> pGeo;
      es.get<CaloGeometryRecord>().get(pGeo);
      geo = pGeo.product();
  }

  if (doElectrons_) fillElectrons(e, es, pv);
  if (doPhotons_) fillPhotons(e, es, pv);
  if (doMuons_) fillMuons(e, es, pv);

  tree_->Fill();
}

void ggHiNtuplizer::fillGenPileupInfo(const edm::Event& e)
{
  // Fills information about pileup from MC truth.

  edm::Handle<std::vector<PileupSummaryInfo> > genPileupHandle;
  e.getByToken(genPileupCollection_, genPileupHandle);

  for (const auto& pu : *genPileupHandle) {
    nPU_   .push_back(pu.getPU_NumInteractions());
    puTrue_.push_back(pu.getTrueNumInteractions());
    puBX_  .push_back(pu.getBunchCrossing());

    nPUInfo_++;
  }

}

void ggHiNtuplizer::fillGenParticles(const edm::Event& e)
{
  // Fills tree branches with generated particle info.

  edm::Handle<std::vector<reco::GenParticle> > genParticlesHandle;
  e.getByToken(genParticlesCollection_, genParticlesHandle);

  // loop over MC particles
  for (auto p = genParticlesHandle->begin(); p != genParticlesHandle->end(); ++p) {
    // skip all primary particles if not particle gun MC
    if (!runOnParticleGun_ && !p->mother()) continue;

    // stable particles with pT > 5 GeV
    bool isStableFast = (p->status() == 1 && p->pt() > 5.0);

    // stable leptons
    bool isStableLepton = (p->status() == 1 && abs(p->pdgId()) >= 11 && abs(p->pdgId()) <= 16);

    // (unstable) Z, W, H, top, bottom
    bool isHeavy = (p->pdgId() == 23 || abs(p->pdgId()) == 24 || p->pdgId() == 25 ||
        abs(p->pdgId()) == 6 || abs(p->pdgId()) == 5);

    // reduce size of output root file
    if (!isStableFast && !isStableLepton && !isHeavy)
      continue;

    mcPID_   .push_back(p->pdgId());
    mcStatus_.push_back(p->status());
    mcVtx_x_ .push_back(p->vx());
    mcVtx_y_ .push_back(p->vy());
    mcVtx_z_ .push_back(p->vz());
    mcPt_    .push_back(p->pt());
    mcEta_   .push_back(p->eta());
    mcPhi_   .push_back(p->phi());
    mcE_     .push_back(p->energy());
    mcEt_    .push_back(p->et());
    mcMass_  .push_back(p->mass());

    reco::GenParticleRef partRef = reco::GenParticleRef(genParticlesHandle, p - genParticlesHandle->begin());
    genpartparentage::GenParticleParentage particleHistory(partRef);

    mcParentage_.push_back(particleHistory.hasLeptonParent()    * 16 +
                           particleHistory.hasBosonParent()     * 8  +
                           particleHistory.hasNonPromptParent() * 4  +
                           particleHistory.hasQCDParent()       * 2  +
                           particleHistory.hasExoticParent());

    int   momPID  = -999;
    float momPt   = -999;
    float momEta  = -999;
    float momPhi  = -999;
    float momMass = -999;
    int   gmomPID = -999;

    if (particleHistory.hasRealParent()) {
      reco::GenParticleRef momRef = particleHistory.parent();

      // mother
      if (momRef.isNonnull() && momRef.isAvailable()) {
        momPID  = momRef->pdgId();
        momPt   = momRef->pt();
        momEta  = momRef->eta();
        momPhi  = momRef->phi();
        momMass = momRef->mass();

        // granny
        genpartparentage::GenParticleParentage motherParticle(momRef);
        if (motherParticle.hasRealParent()) {
          reco::GenParticleRef granny = motherParticle.parent();
          gmomPID = granny->pdgId();
        }
      }
    }

    mcMomPID_ .push_back(momPID);
    mcMomPt_  .push_back(momPt);
    mcMomEta_ .push_back(momEta);
    mcMomPhi_ .push_back(momPhi);
    mcMomMass_.push_back(momMass);
    mcGMomPID_.push_back(gmomPID);

    mcIndex_  .push_back(p - genParticlesHandle->begin());

    mcCalIsoDR03_.push_back(getGenCalIso(genParticlesHandle, p, 0.3, false, false));
    mcCalIsoDR04_.push_back(getGenCalIso(genParticlesHandle, p, 0.4, false, false));
    mcTrkIsoDR03_.push_back(getGenTrkIso(genParticlesHandle, p, 0.3) );
    mcTrkIsoDR04_.push_back(getGenTrkIso(genParticlesHandle, p, 0.4) );

    nMC_++;
  } // gen-level particles loop

}

float ggHiNtuplizer::getGenCalIso(edm::Handle<std::vector<reco::GenParticle> > &handle,
                                  reco::GenParticleCollection::const_iterator thisPart,
                                  float dRMax, bool removeMu, bool removeNu)
{
  // Returns Et sum.

  float etSum = 0;

  for (auto p = handle->begin(); p != handle->end(); ++p) {
    if (p == thisPart) continue;
    if (p->status() != 1) continue;

    // has to come from the same collision
    if (thisPart->collisionId() != p->collisionId())
      continue;

    int pdgCode = abs(p->pdgId());

    // skip muons/neutrinos, if requested
    if (removeMu && pdgCode == 13) continue;
    if (removeNu && (pdgCode == 12 || pdgCode == 14 || pdgCode == 16)) continue;

    // must be within deltaR cone
    float dR = reco::deltaR(thisPart->momentum(), p->momentum());
    if (dR > dRMax) continue;

    etSum += p->et();
  }

  return etSum;
}

float ggHiNtuplizer::getGenTrkIso(edm::Handle<std::vector<reco::GenParticle> > &handle,
                                  reco::GenParticleCollection::const_iterator thisPart, float dRMax)
{
  // Returns pT sum without counting neutral particles.

  float ptSum = 0;

  for (auto p = handle->begin(); p != handle->end(); ++p) {
    if (p == thisPart) continue;
    if (p->status() != 1) continue;
    if (p->charge() == 0) continue;  // do not count neutral particles

    // has to come from the same collision
    if (thisPart->collisionId() != p->collisionId())
      continue;

    // must be within deltaR cone
    float dR = reco::deltaR(thisPart->momentum(), p->momentum());
    if (dR > dRMax) continue;

    ptSum += p->pt();
  }

  return ptSum;
}

void ggHiNtuplizer::fillElectrons(const edm::Event& e, const edm::EventSetup& es, math::XYZPoint& pv)
{
  // Fills tree branches with reco GSF electrons.

  edm::Handle<edm::View<reco::GsfElectron> > gsfElectronsHandle;
  e.getByToken(gsfElectronsCollection_, gsfElectronsHandle);

  edm::Handle<reco::ConversionCollection> conversions;
  edm::Handle<reco::BeamSpot> theBeamSpot;

  edm::Handle<edm::ValueMap<bool> > veto_id_decisions;
  edm::Handle<edm::ValueMap<bool> > loose_id_decisions;
  edm::Handle<edm::ValueMap<bool> > medium_id_decisions;
  edm::Handle<edm::ValueMap<bool> > tight_id_decisions;

  edm::Handle<double> rhoH;
  if (!rhoToken_.isUninitialized())
    e.getByToken(rhoToken_, rhoH);
  float rho = rhoH.isValid() ? *rhoH : -999;

  if (doVID_) {
    // Get the conversions collection
    e.getByToken(conversionsToken_, conversions);

    // Get the beam spot
    e.getByToken(beamSpotToken_, theBeamSpot);

    // Get the electron ID data from the event stream.
    // Note: this implies that the VID ID modules have been run upstream.
    // If you need more info, check with the EGM group.
    e.getByToken(eleVetoIdMapToken_, veto_id_decisions);
    e.getByToken(eleLooseIdMapToken_, loose_id_decisions);
    e.getByToken(eleMediumIdMapToken_, medium_id_decisions);
    e.getByToken(eleTightIdMapToken_, tight_id_decisions);
  }


  // loop over electrons
  for (auto ele = gsfElectronsHandle->begin(); ele != gsfElectronsHandle->end(); ++ele) {
    eleCharge_           .push_back(ele->charge());
    eleChargeConsistent_ .push_back((int)ele->isGsfCtfScPixChargeConsistent());
    eleSCPixCharge_      .push_back(ele->scPixCharge());
    if (!(ele->closestTrack().isNull())) {
      eleCtfCharge_        .push_back(ele->closestTrack()->charge());
    } else {
      eleCtfCharge_        .push_back(-99.);
    }
    eleEn_               .push_back(ele->energy());
    eleD0_               .push_back(ele->gsfTrack()->dxy(pv));
    eleDz_               .push_back(ele->gsfTrack()->dz(pv));
    eleD0Err_            .push_back(ele->gsfTrack()->dxyError());
    eleDzErr_            .push_back(ele->gsfTrack()->dzError());
    eleTrkPt_            .push_back(ele->gsfTrack()->pt());
    eleTrkEta_           .push_back(ele->gsfTrack()->eta());
    eleTrkPhi_           .push_back(ele->gsfTrack()->phi());
    eleTrkCharge_        .push_back(ele->gsfTrack()->charge());
    eleTrkChi2_          .push_back(ele->gsfTrack()->chi2());
    eleTrkNdof_          .push_back(ele->gsfTrack()->ndof());
    eleTrkNormalizedChi2_.push_back(ele->gsfTrack()->normalizedChi2());
    eleTrkValidHits_     .push_back(ele->gsfTrack()->numberOfValidHits());
    eleTrkLayers_        .push_back(ele->gsfTrack()->hitPattern().trackerLayersWithMeasurement());
    elePt_               .push_back(ele->pt());
    eleEta_              .push_back(ele->eta());
    elePhi_              .push_back(ele->phi());
    eleSCEn_             .push_back(ele->superCluster()->energy());
    eleESEn_             .push_back(ele->superCluster()->preshowerEnergy());
    eleSCEta_            .push_back(ele->superCluster()->eta());
    eleSCPhi_            .push_back(ele->superCluster()->phi());
    eleSCRawEn_          .push_back(ele->superCluster()->rawEnergy());
    eleSCEtaWidth_       .push_back(ele->superCluster()->etaWidth());
    eleSCPhiWidth_       .push_back(ele->superCluster()->phiWidth());
    eleHoverE_           .push_back(ele->hcalOverEcal());
    eleHoverEBc_         .push_back(ele->hcalOverEcalBc());
    eleEoverP_           .push_back(ele->eSuperClusterOverP());
    eleEoverPInv_        .push_back(std::abs(1./ele->ecalEnergy() - 1./ele->trackMomentumAtVtx().R()));
    eleBrem_             .push_back(ele->fbrem());
    eledEtaAtVtx_        .push_back(ele->deltaEtaSuperClusterTrackAtVtx());
    eledPhiAtVtx_        .push_back(ele->deltaPhiSuperClusterTrackAtVtx());
    eleSigmaIEtaIEta_    .push_back(ele->sigmaIetaIeta());
    eleSigmaIPhiIPhi_    .push_back(ele->sigmaIphiIphi());
    // eleConvVeto_         .push_back((int)ele->passConversionVeto()); // TODO: not available in reco::
    eleMissHits_         .push_back(ele->gsfTrack()->numberOfLostHits());

    // full 5x5
    eleSigmaIEtaIEta_2012_.push_back(ele->full5x5_sigmaIetaIeta());

    // isolation
    reco::GsfElectron::PflowIsolationVariables pfIso = ele->pfIsolationVariables();
    elePFChIso_          .push_back(pfIso.sumChargedHadronPt);
    elePFPhoIso_         .push_back(pfIso.sumPhotonEt);
    elePFNeuIso_         .push_back(pfIso.sumNeutralHadronEt);
    elePFPUIso_          .push_back(pfIso.sumPUPt);

    double area = effectiveAreas_.getEffectiveArea(ele->superCluster()->eta());
    elePFRelIsoWithEA_   .push_back((pfIso.sumChargedHadronPt + std::max(0.0,
      pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - rho * area)) / ele->pt());
    elePFRelIsoWithDBeta_.push_back((pfIso.sumChargedHadronPt + std::max(0.0,
      pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - 0.5 * pfIso.sumPUPt)) / ele->pt());

    // calculation on the fly
    pfIsoCalculator pfIsoCal(e, pfCollection_, pv);
    if (std::abs(ele->superCluster()->eta()) > 1.566) {
      elePFChIso03_          .push_back(pfIsoCal.getPfIso(*ele, 1, 0.3, 0.015, 0.));
      elePFChIso04_          .push_back(pfIsoCal.getPfIso(*ele, 1, 0.4, 0.015, 0.));
      elePFPhoIso03_         .push_back(pfIsoCal.getPfIso(*ele, 4, 0.3, 0.08, 0.));
      elePFPhoIso04_         .push_back(pfIsoCal.getPfIso(*ele, 4, 0.4, 0.08, 0.));
    } else {
      elePFChIso03_          .push_back(pfIsoCal.getPfIso(*ele, 1, 0.3, 0.0, 0.));
      elePFChIso04_          .push_back(pfIsoCal.getPfIso(*ele, 1, 0.4, 0.0, 0.));
      elePFPhoIso03_         .push_back(pfIsoCal.getPfIso(*ele, 4, 0.3, 0.0, 0.));
      elePFPhoIso04_         .push_back(pfIsoCal.getPfIso(*ele, 4, 0.4, 0.0, 0.));
    }

    elePFNeuIso03_         .push_back(pfIsoCal.getPfIso(*ele, 5, 0.3, 0., 0.));
    elePFNeuIso04_         .push_back(pfIsoCal.getPfIso(*ele, 5, 0.4, 0., 0.));

    eleR9_               .push_back(ele->r9());
    eleE3x3_             .push_back(ele->r9()*ele->superCluster()->energy());
    eleE5x5_             .push_back(ele->e5x5());
    eleR9Full5x5_        .push_back(ele->full5x5_r9());
    eleE3x3Full5x5_      .push_back(ele->full5x5_r9()*ele->superCluster()->energy());
    eleE5x5Full5x5_      .push_back(ele->full5x5_e5x5());

    // seed
    NClusters_            .push_back(ele->superCluster()->clustersSize());
    NEcalClusters_        .push_back(std::max(0, (int)(ele->superCluster()->clustersEnd() - ele->superCluster()->clustersBegin())));
    eleSeedEn_            .push_back(ele->superCluster()->seed()->energy());
    eleSeedEta_           .push_back(ele->superCluster()->seed()->eta());
    eleSeedPhi_           .push_back(ele->superCluster()->seed()->phi());
    // local coordinates
    edm::Ptr<reco::CaloCluster> theseed = ele->superCluster()->seed();
    EcalClusterLocal ecalLocal;
    if (theseed->hitsAndFractions().at(0).first.subdetId() == EcalBarrel) {
      float cryPhi, cryEta, thetatilt, phitilt;
      int ieta, iphi;
      ecalLocal.localCoordsEB(*(theseed), es, cryEta, cryPhi, ieta, iphi, thetatilt, phitilt);
      eleSeedCryEta_  .push_back(cryEta);
      eleSeedCryPhi_  .push_back(cryPhi);
      eleSeedCryIeta_ .push_back(ieta);
      eleSeedCryIphi_ .push_back(iphi);
    } else {
      float cryX, cryY, thetatilt, phitilt;
      int ix, iy;
      ecalLocal.localCoordsEE(*(theseed), es, cryX, cryY, ix, iy, thetatilt, phitilt);
      eleSeedCryEta_  .push_back(0);
      eleSeedCryPhi_  .push_back(0);
      eleSeedCryIeta_ .push_back(0);
      eleSeedCryIphi_ .push_back(0);
    }

    if (doVID_) {
      eleEffAreaTimesRho_.push_back(area * rho);

      bool passConvVeto = !ConversionTools::hasMatchedConversion(*ele,
          conversions,
          theBeamSpot->position());
      elepassConversionVeto_.push_back( (int) passConvVeto );

      // parameters of the very first PFCluster
      // reco::CaloCluster_iterator bc = ele->superCluster()->clustersBegin();
      // if (bc != ele->superCluster()->clustersEnd()) {
      //    eleBC2E_  .push_back((*bc)->energy());
      //    eleBC2Eta_.push_back((*bc)->eta());
      // } else {
      //    eleBC2E_  .push_back(-99);
      //    eleBC2Eta_.push_back(-99);
      // }

      const edm::Ptr<reco::GsfElectron> elePtr(gsfElectronsHandle, ele - gsfElectronsHandle->begin()); //value map is keyed of edm::Ptrs so we need to make one
      bool passVetoID   = false;
      bool passLooseID  = false;
      bool passMediumID = false;
      bool passTightID  = false;
      if (veto_id_decisions.isValid()) {
        passVetoID   = (*veto_id_decisions)[elePtr];
        passLooseID  = (*loose_id_decisions)[elePtr];
        passMediumID = (*medium_id_decisions)[elePtr];
        passTightID  = (*tight_id_decisions)[elePtr];
      }
      eleIDVeto_            .push_back((int)passVetoID);
      eleIDLoose_           .push_back((int)passLooseID);
      eleIDMedium_          .push_back((int)passMediumID);
      eleIDTight_           .push_back((int)passTightID);
    }

    nEle_++;
  } // electrons loop
}

void ggHiNtuplizer::fillPhotons(const edm::Event& e, const edm::EventSetup& es, math::XYZPoint& pv)
{
  // Fills tree branches with photons.

  edm::Handle<edm::View<reco::Photon> > recoPhotonsHandle;
  e.getByToken(recoPhotonsCollection_, recoPhotonsHandle);
  edm::Handle<edm::ValueMap<reco::HIPhotonIsolation> > recoPhotonHiIsoHandle;
  edm::ValueMap<reco::HIPhotonIsolation> isoMap;
  if (useValMapIso_) {
    e.getByToken(recoPhotonsHiIso_, recoPhotonHiIsoHandle);
    isoMap = * recoPhotonHiIsoHandle;
  }

  edm::Handle<EcalRecHitCollection> recHitsEBHandle;
  if (doRecHitsEB_) {
      e.getByToken(recHitsEB_, recHitsEBHandle);
  }
  edm::Handle<EcalRecHitCollection> recHitsEEHandle;
  if (doRecHitsEE_) {
      e.getByToken(recHitsEE_, recHitsEEHandle);
  }

  // loop over photons
  for (auto pho = recoPhotonsHandle->begin(); pho != recoPhotonsHandle->end(); ++pho) {
    phoE_             .push_back(pho->energy());
    phoEt_            .push_back(pho->et());
    phoEta_           .push_back(pho->eta());
    phoPhi_           .push_back(pho->phi());

    // energies from different types of corrections
    phoEcorrStdEcal_  .push_back(pho->getCorrectedEnergy(reco::Photon::P4type::ecal_standard));
    phoEcorrPhoEcal_  .push_back(pho->getCorrectedEnergy(reco::Photon::P4type::ecal_photons));
    phoEcorrRegr1_    .push_back(pho->getCorrectedEnergy(reco::Photon::P4type::regression1));
    phoEcorrRegr2_    .push_back(pho->getCorrectedEnergy(reco::Photon::P4type::regression2));
    // errors for those corrections
    phoEcorrErrStdEcal_  .push_back(pho->getCorrectedEnergyError(reco::Photon::P4type::ecal_standard));
    phoEcorrErrPhoEcal_  .push_back(pho->getCorrectedEnergyError(reco::Photon::P4type::ecal_photons));
    phoEcorrErrRegr1_    .push_back(pho->getCorrectedEnergyError(reco::Photon::P4type::regression1));
    phoEcorrErrRegr2_    .push_back(pho->getCorrectedEnergyError(reco::Photon::P4type::regression2));

    // SuperCluster info
    phoSCE_           .push_back(pho->superCluster()->energy());
    phoSCRawE_        .push_back(pho->superCluster()->rawEnergy());
    phoSCEta_         .push_back(pho->superCluster()->eta());
    phoSCPhi_         .push_back(pho->superCluster()->phi());
    phoSCEtaWidth_    .push_back(pho->superCluster()->etaWidth());
    phoSCPhiWidth_    .push_back(pho->superCluster()->phiWidth());
    phoSCBrem_        .push_back(pho->superCluster()->phiWidth()/pho->superCluster()->etaWidth());
    phoSCnHits_       .push_back(pho->superCluster()->size());
    phoSCflags_       .push_back(pho->superCluster()->flags());
    phoSCinClean_     .push_back((int)pho->superCluster()->isInClean());
    phoSCinUnClean_   .push_back((int)pho->superCluster()->isInUnclean());
    phoSCnBC_         .push_back((int)pho->superCluster()->clustersSize());
    phoESEn_          .push_back(pho->superCluster()->preshowerEnergy());
    // PF SuperCluster info
    if (pho->parentSuperCluster().isAvailable() && pho->parentSuperCluster().isNonnull()) {
        phoPSCE_           .push_back(pho->parentSuperCluster()->energy());
        phoPSCRawE_        .push_back(pho->parentSuperCluster()->rawEnergy());
        phoPSCEta_         .push_back(pho->parentSuperCluster()->eta());
        phoPSCPhi_         .push_back(pho->parentSuperCluster()->phi());
        phoPSCEtaWidth_    .push_back(pho->parentSuperCluster()->etaWidth());
        phoPSCPhiWidth_    .push_back(pho->parentSuperCluster()->phiWidth());
        phoPSCBrem_        .push_back(pho->parentSuperCluster()->phiWidth()/pho->parentSuperCluster()->etaWidth());
        phoPSCnHits_       .push_back(pho->parentSuperCluster()->size());
        phoPSCflags_       .push_back(pho->parentSuperCluster()->flags());
        phoPSCinClean_     .push_back((int)pho->parentSuperCluster()->isInClean());
        phoPSCinUnClean_   .push_back((int)pho->parentSuperCluster()->isInUnclean());
        phoPSCnBC_         .push_back((int)pho->parentSuperCluster()->clustersSize());
        phoPESEn_          .push_back(pho->parentSuperCluster()->preshowerEnergy());
    }
    else {
        phoPSCE_           .push_back(-999);
        phoPSCRawE_        .push_back(-999);
        phoPSCEta_         .push_back(-999);
        phoPSCPhi_         .push_back(-999);
        phoPSCEtaWidth_    .push_back(-999);
        phoPSCPhiWidth_    .push_back(-999);
        phoPSCBrem_        .push_back(-999);
        phoPSCnHits_       .push_back(-999);
        phoPSCflags_       .push_back(-999);
        phoPSCinClean_     .push_back(-999);
        phoPSCinUnClean_   .push_back(-999);
        phoPSCnBC_         .push_back(-999);
        phoPESEn_          .push_back(-999);
    }

    phoIsPFPhoton_    .push_back((int)pho->isPFlowPhoton());
    phoIsStandardPhoton_.push_back((int)pho->isStandardPhoton());
    phoHasPixelSeed_  .push_back((int)pho->hasPixelSeed());
    phoHasConversionTracks_.push_back((int)pho->hasConversionTracks());
    // phoEleVeto_       .push_back((int)pho->passElectronVeto());   // TODO: not available in reco::
    phoR9_            .push_back(pho->r9());
    phoHadTowerOverEm_.push_back(pho->hadTowOverEm());
    phoHoverE_        .push_back(pho->hadronicOverEm());
    phoSigmaIEtaIEta_ .push_back(pho->sigmaIetaIeta());
    // phoSigmaIEtaIPhi_ .push_back(pho->sep());   // TODO: not available in reco::
    // phoSigmaIPhiIPhi_ .push_back(pho->spp());   // TODO: not available in reco::

    // additional shower shape variables
    phoE3x3_          .push_back(pho->e3x3());
    phoE1x5_          .push_back(pho->e1x5());
    phoE2x5_          .push_back(pho->e2x5());
    phoE5x5_          .push_back(pho->e5x5());
    phoMaxEnergyXtal_ .push_back(pho->maxEnergyXtal());
    phoSigmaEtaEta_   .push_back(pho->sigmaEtaEta());
    phoR1x5_          .push_back(pho->r1x5());
    phoR2x5_          .push_back(pho->r2x5());

    // full 5x5
    phoR9_2012_           .push_back(pho->full5x5_r9());
    phoSigmaIEtaIEta_2012_.push_back(pho->full5x5_sigmaIetaIeta());
    phoE1x5_2012_.push_back(pho->full5x5_e1x5());
    phoE2x5_2012_.push_back(pho->full5x5_e2x5());
    phoE3x3_2012_.push_back(pho->full5x5_e3x3());
    phoE5x5_2012_.push_back(pho->full5x5_e5x5());
    phoMaxEnergyXtal_2012_.push_back(pho->full5x5_maxEnergyXtal());
    phoSigmaEtaEta_2012_.push_back(pho->full5x5_sigmaEtaEta());
    phoR1x5_2012_.push_back(pho->full5x5_r1x5());
    phoR2x5_2012_.push_back(pho->full5x5_r2x5());

    // seed BC
    if (pho->superCluster()->seed().isAvailable() && pho->superCluster()->seed().isNonnull()) {
        phoBC1E_        .push_back(pho->superCluster()->seed()->energy());
        phoBC1Ecorr_    .push_back(pho->superCluster()->seed()->correctedEnergy());
        phoBC1Eta_      .push_back(pho->superCluster()->seed()->eta());
        phoBC1Phi_      .push_back(pho->superCluster()->seed()->phi());
        phoBC1size_     .push_back(pho->superCluster()->seed()->size());
        phoBC1flags_    .push_back(pho->superCluster()->seed()->flags());
        phoBC1inClean_  .push_back(pho->superCluster()->seed()->isInClean());
        phoBC1inUnClean_.push_back(pho->superCluster()->seed()->isInUnclean());
        phoBC1rawID_    .push_back(pho->superCluster()->seed()->seed().rawId());
    }
    else {
        phoBC1E_        .push_back(-999);
        phoBC1Ecorr_    .push_back(-999);
        phoBC1Eta_      .push_back(-999);
        phoBC1Phi_      .push_back(-999);
        phoBC1size_     .push_back(-999);
        phoBC1flags_    .push_back(-999);
        phoBC1inClean_  .push_back(-999);
        phoBC1inUnClean_.push_back(-999);
        phoBC1rawID_    .push_back(0);
    }

    // parameters of the very first PFCluster
    // reco::CaloCluster_iterator bc = pho->superCluster()->clustersBegin();
    // if (bc != pho->superCluster()->clustersEnd()) {
    //    phoBC2E_  .push_back((*bc)->energy());
    //    phoBC2Eta_.push_back((*bc)->eta());
    // } else {
    //    phoBC2E_  .push_back(-99);
    //    phoBC2Eta_.push_back(-99);
    // }

    if (useValMapIso_) {
      unsigned int idx = pho - recoPhotonsHandle->begin();
      edm::RefToBase<reco::Photon> photonRef = recoPhotonsHandle->refAt(idx);

      pho_ecalClusterIsoR2_.push_back(isoMap[photonRef].ecalClusterIsoR2());
      pho_ecalClusterIsoR3_.push_back(isoMap[photonRef].ecalClusterIsoR3());
      pho_ecalClusterIsoR4_.push_back(isoMap[photonRef].ecalClusterIsoR4());
      pho_ecalClusterIsoR5_.push_back(isoMap[photonRef].ecalClusterIsoR5());
      pho_hcalRechitIsoR1_.push_back(isoMap[photonRef].hcalRechitIsoR1());
      pho_hcalRechitIsoR2_.push_back(isoMap[photonRef].hcalRechitIsoR2());
      pho_hcalRechitIsoR3_.push_back(isoMap[photonRef].hcalRechitIsoR3());
      pho_hcalRechitIsoR4_.push_back(isoMap[photonRef].hcalRechitIsoR4());
      pho_hcalRechitIsoR5_.push_back(isoMap[photonRef].hcalRechitIsoR5());
      pho_trackIsoR1PtCut20_.push_back(isoMap[photonRef].trackIsoR1PtCut20());
      pho_trackIsoR2PtCut20_.push_back(isoMap[photonRef].trackIsoR2PtCut20());
      pho_trackIsoR3PtCut20_.push_back(isoMap[photonRef].trackIsoR3PtCut20());
      pho_trackIsoR4PtCut20_.push_back(isoMap[photonRef].trackIsoR4PtCut20());
      pho_trackIsoR5PtCut20_.push_back(isoMap[photonRef].trackIsoR5PtCut20());
      pho_swissCrx_.push_back(isoMap[photonRef].swissCrx());
      pho_seedTime_.push_back(isoMap[photonRef].seedTime());
    }

    if (doRecHitsEB_ || doRecHitsEE_) {

        int iBC = 0;
        for (reco::CaloCluster_iterator bc = pho->superCluster()->clustersBegin(); bc != pho->superCluster()->clustersEnd(); ++bc) {

            for (const auto& hitBC : (*bc)->hitsAndFractions()) {

                const DetId & rhDetId = hitBC.first;
                edm::Handle<EcalRecHitCollection>* recHitsHandle;

                if (rhDetId.subdetId() == EcalBarrel && doRecHitsEB_) {
                    recHitsHandle = (&recHitsEBHandle);
                }
                else if (rhDetId.subdetId() == EcalEndcap && doRecHitsEE_) {
                    recHitsHandle = (&recHitsEEHandle);
                }
                else continue;

                EcalRecHitCollection::const_iterator rhIter = (*recHitsHandle)->find(rhDetId);
                const EcalRecHit & rh = (*rhIter);

                rhRawId_.push_back(rhDetId.rawId());
                if (rhDetId.subdetId() == EcalBarrel) {
                    rhieta_.push_back(EBDetId(rhDetId).ieta());
                    rhiphi_.push_back(EBDetId(rhDetId).iphi());
                    rhix_.push_back(-999);
                    rhiy_.push_back(-999);
                }
                else if (rhDetId.subdetId() == EcalEndcap) {
                    rhieta_.push_back(-999);
                    rhiphi_.push_back(-999);
                    rhix_.push_back(EEDetId(rhDetId).ix());
                    rhiy_.push_back(EEDetId(rhDetId).iy());
                }
                else {
                    rhieta_.push_back(-999);
                    rhiphi_.push_back(-999);
                    rhix_.push_back(-999);
                    rhiy_.push_back(-999);
                }
                rhE_.push_back(rh.energy());

                math::XYZPoint posXYZ((geo->getPosition(rhDetId)).x() - pv.x(),
                                      (geo->getPosition(rhDetId)).y() - pv.y(),
                                      (geo->getPosition(rhDetId)).z() - pv.z());

                rhEt_.push_back(rh.energy()*sin(posXYZ.theta()));
                rhEta_.push_back(posXYZ.eta());
                rhPhi_.push_back(posXYZ.phi());
                rhChi2_.push_back(rh.chi2());
                rhEerror_.push_back(rh.energyError());

                uint32_t flagTmp = 0;
                for (unsigned int iFlag=0; iFlag<32; ++iFlag) {
                    if (rh.checkFlag(iFlag))
                        flagTmp |= 1 << iFlag;
                }
                rhFlags_.push_back(flagTmp);

                rhPhoIdx_.push_back(nPho_);
                rhBCIdx_.push_back(iBC);
                nRH_++;
            }
            iBC++;
        }
    }

    if (doPfIso_) {
      pfIsoCalculator pfIso(e, pfCollection_, pv);
      // particle flow isolation
      pfcIso1.push_back( pfIso.getPfIso(*pho, 1, 0.1, 0.02, 0.0, 0 ));
      pfcIso2.push_back( pfIso.getPfIso(*pho, 1, 0.2, 0.02, 0.0, 0 ));
      pfcIso3.push_back( pfIso.getPfIso(*pho, 1, 0.3, 0.02, 0.0, 0 ));
      pfcIso4.push_back( pfIso.getPfIso(*pho, 1, 0.4, 0.02, 0.0, 0 ));
      pfcIso5.push_back( pfIso.getPfIso(*pho, 1, 0.5, 0.02, 0.0, 0 ));

      pfnIso1.push_back( pfIso.getPfIso(*pho, 5, 0.1, 0.0, 0.0, 0 ));
      pfnIso2.push_back( pfIso.getPfIso(*pho, 5, 0.2, 0.0, 0.0, 0 ));
      pfnIso3.push_back( pfIso.getPfIso(*pho, 5, 0.3, 0.0, 0.0, 0 ));
      pfnIso4.push_back( pfIso.getPfIso(*pho, 5, 0.4, 0.0, 0.0, 0 ));
      pfnIso5.push_back( pfIso.getPfIso(*pho, 5, 0.5, 0.0, 0.0, 0 ));

      pfpIso1.push_back( pfIso.getPfIso(*pho, 4, 0.1, 0.0, 0.0, 0.015 ));
      pfpIso2.push_back( pfIso.getPfIso(*pho, 4, 0.2, 0.0, 0.0, 0.015 ));
      pfpIso3.push_back( pfIso.getPfIso(*pho, 4, 0.3, 0.0, 0.0, 0.015 ));
      pfpIso4.push_back( pfIso.getPfIso(*pho, 4, 0.4, 0.0, 0.0, 0.015 ));
      pfpIso5.push_back( pfIso.getPfIso(*pho, 4, 0.5, 0.0, 0.0, 0.015 ));
    }

    //////////////////////////////////// MC matching ////////////////////////////////////
    if (doGenParticles_ && !isData_) {
      constexpr float delta2 = 0.15*0.15;

      bool gpTemp = false;
      float currentMaxPt = -1;
      int matchedIndex = -1;

      for (unsigned igen = 0; igen < mcEt_.size(); ++igen) {
        if (mcStatus_[igen] != 1 || mcPID_[igen] != 22) continue;
        if (reco::deltaR2(pho->eta(), pho->phi(), mcEta_[igen], mcPhi_[igen]) < delta2 &&
            mcPt_[igen] > currentMaxPt) {

          gpTemp = true;
          currentMaxPt = mcPt_[igen];
          matchedIndex = igen;
        }
      }

      // if no matching photon was found try with other particles
      std::vector<int> otherPdgIds_ = {1, 11};
      if ( !gpTemp ) {
        currentMaxPt = -1;
        for (unsigned igen = 0; igen < mcEt_.size(); ++igen) {
          if (mcStatus_[igen] != 1 || find(otherPdgIds_.begin(), otherPdgIds_.end(), std::abs(mcPID_[igen])) == otherPdgIds_.end()) continue;
          if (reco::deltaR2(pho->eta(), pho->phi(), mcEta_[igen], mcPhi_[igen]) < delta2 &&
              mcPt_[igen] > currentMaxPt) {

            gpTemp = true;
            currentMaxPt = mcPt_[igen];
            matchedIndex = igen;
          }
        } // end of loop over gen particles
      } // if not matched to gen photon

      pho_genMatchedIndex_.push_back(matchedIndex);
    } // if it's a MC

    nPho_++;
  } // photons loop
}

void ggHiNtuplizer::fillMuons(const edm::Event& e, const edm::EventSetup& es, math::XYZPoint& pv)
{
  // Fills tree branches with reco muons.

  edm::Handle<edm::View<reco::Muon> > recoMuonsHandle;
  e.getByToken(recoMuonsCollection_, recoMuonsHandle);

  for (const auto& mu : *recoMuonsHandle) {
    if (mu.pt() < 5) continue;
    if (!(mu.isPFMuon() || mu.isGlobalMuon() || mu.isTrackerMuon())) continue;

    muPt_    .push_back(mu.pt());
    muEta_   .push_back(mu.eta());
    muPhi_   .push_back(mu.phi());
    muCharge_.push_back(mu.charge());
    muType_  .push_back(mu.type());
    muIsGood_.push_back(muon::isGoodMuon(mu, muon::selectionTypeFromString("TMOneStationTight")));
    muD0_    .push_back(mu.muonBestTrack()->dxy(pv));
    muDz_    .push_back(mu.muonBestTrack()->dz(pv));

    const reco::TrackRef glbMu = mu.globalTrack();
    const reco::TrackRef innMu = mu.innerTrack();

    if (glbMu.isNull()) {
      muChi2NDF_ .push_back(-99);
      muMuonHits_.push_back(-99);
    } else {
      muChi2NDF_.push_back(glbMu->normalizedChi2());
      muMuonHits_.push_back(glbMu->hitPattern().numberOfValidMuonHits());
    }

    if (innMu.isNull()) {
      muInnerD0_     .push_back(-99);
      muInnerDz_     .push_back(-99);
      muTrkLayers_   .push_back(-99);
      muPixelLayers_ .push_back(-99);
      muPixelHits_   .push_back(-99);
      muTrkQuality_  .push_back(-99);
    } else {
      muInnerD0_     .push_back(innMu->dxy(pv));
      muInnerDz_     .push_back(innMu->dz(pv));
      muTrkLayers_   .push_back(innMu->hitPattern().trackerLayersWithMeasurement());
      muPixelLayers_ .push_back(innMu->hitPattern().pixelLayersWithMeasurement());
      muPixelHits_   .push_back(innMu->hitPattern().numberOfValidPixelHits());
      muTrkQuality_  .push_back(innMu->quality(reco::TrackBase::highPurity));
    }

    muStations_ .push_back(mu.numberOfMatchedStations());
    muIsoTrk_   .push_back(mu.isolationR03().sumPt);
    muPFChIso_  .push_back(mu.pfIsolationR04().sumChargedHadronPt);
    muPFPhoIso_ .push_back(mu.pfIsolationR04().sumPhotonEt);
    muPFNeuIso_ .push_back(mu.pfIsolationR04().sumNeutralHadronEt);
    muPFPUIso_  .push_back(mu.pfIsolationR04().sumPUPt);

    nMu_++;
  } // muons loop
}

DEFINE_FWK_MODULE(ggHiNtuplizer);
