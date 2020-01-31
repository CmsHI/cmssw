#ifndef ggHiNtuplizer_h
#define ggHiNtuplizer_h

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/HIPhotonIsolation.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

#include <TTree.h>

class ggHiNtuplizer : public edm::EDAnalyzer {

 public:

   ggHiNtuplizer(const edm::ParameterSet&);
   virtual ~ggHiNtuplizer() {};

 private:

   virtual void analyze(const edm::Event&, const edm::EventSetup&);

   void fillGenParticles (const edm::Event&);
   void fillGenPileupInfo(const edm::Event&);
   void fillElectrons    (const edm::Event&, const edm::EventSetup&, reco::Vertex& pv);
   void fillPhotons      (const edm::Event&, const edm::EventSetup&, reco::Vertex& pv);
   void fillMuons        (const edm::Event&, const edm::EventSetup&, reco::Vertex& pv);

   // Et and pT sums
   float getGenCalIso(edm::Handle<std::vector<reco::GenParticle> >&, reco::GenParticleCollection::const_iterator, float dRMax, bool removeMu, bool removeNu);
   float getGenTrkIso(edm::Handle<std::vector<reco::GenParticle> >&, reco::GenParticleCollection::const_iterator, float dRMax);

   // switches
   bool doGenParticles_;
   bool doElectrons_;
   bool doPhotons_;
   bool doMuons_;
   bool runOnParticleGun_;
   bool useValMapIso_;
   bool doPfIso_;
   bool removePhotonPfIsoFootprint_;
   bool doEleEReg_;
   bool doEffectiveAreas_;
   bool doVID_;
   bool doPhoEReg_;
   bool doRecHitsEB_;
   bool doRecHitsEE_;

   // handles to collections of objects
   edm::EDGetTokenT<std::vector<PileupSummaryInfo> >    genPileupCollection_;
   edm::EDGetTokenT<std::vector<reco::GenParticle> >    genParticlesCollection_;
   edm::EDGetTokenT<edm::View<reco::GsfElectron> > gsfElectronsCollection_;
   edm::EDGetTokenT<edm::ValueMap<bool> > eleVetoIdMapToken_;
   edm::EDGetTokenT<edm::ValueMap<bool> > eleLooseIdMapToken_;
   edm::EDGetTokenT<edm::ValueMap<bool> > eleMediumIdMapToken_;
   edm::EDGetTokenT<edm::ValueMap<bool> > eleTightIdMapToken_;
   edm::EDGetTokenT<edm::View<reco::Photon> >      recoPhotonsCollection_;
   edm::EDGetTokenT<edm::ValueMap<reco::HIPhotonIsolation> > recoPhotonsHiIso_;
   edm::EDGetTokenT<edm::View<reco::Muon> >        recoMuonsCollection_;
   edm::EDGetTokenT<std::vector<reco::Vertex> >         vtxCollection_;
   edm::EDGetTokenT<double> rhoToken_;
   edm::EDGetTokenT<reco::BeamSpot> beamSpotToken_;
   edm::EDGetTokenT<reco::ConversionCollection> conversionsToken_;
   edm::EDGetTokenT<edm::View<reco::PFCandidate> >    pfCollection_;

   edm::EDGetToken particleBasedIsolationPhoton_;

   edm::EDGetTokenT<EcalRecHitCollection> recHitsEB_;
   edm::EDGetTokenT<EcalRecHitCollection> recHitsEE_;

   const CaloGeometry *geo;
   const CaloTopology* topo;
   const TransientTrackBuilder* tb;

   EffectiveAreas effectiveAreas_;

   TTree*         tree_;

   // variables associated with tree branches
   UInt_t         run_;
   ULong64_t      event_;
   UInt_t         lumis_;
   Bool_t         isData_;
   Float_t        rho_;

   // PileupSummaryInfo
   Int_t          nPUInfo_;
   std::vector<int>    nPU_;
   std::vector<int>    puBX_;
   std::vector<float>  puTrue_;

   // reco::GenParticle
   Int_t          nMC_;
   std::vector<int>    mcPID_;
   std::vector<int>    mcStatus_;
   std::vector<float>  mcVtx_x_;
   std::vector<float>  mcVtx_y_;
   std::vector<float>  mcVtx_z_;
   std::vector<float>  mcPt_;
   std::vector<float>  mcEta_;
   std::vector<float>  mcPhi_;
   std::vector<float>  mcE_;
   std::vector<float>  mcEt_;
   std::vector<float>  mcMass_;
   std::vector<int>    mcParentage_;
   std::vector<int>    mcMomPID_;
   std::vector<float>  mcMomPt_;
   std::vector<float>  mcMomEta_;
   std::vector<float>  mcMomPhi_;
   std::vector<float>  mcMomMass_;
   std::vector<int>    mcGMomPID_;
   std::vector<int>    mcIndex_;
   std::vector<float>  mcCalIsoDR03_;
   std::vector<float>  mcCalIsoDR04_;
   std::vector<float>  mcTrkIsoDR03_;
   std::vector<float>  mcTrkIsoDR04_;

   // reco::GsfElectron
   Int_t          nEle_;
   std::vector<int>    eleCharge_;
   std::vector<int>    eleChargeConsistent_;
   std::vector<int>    eleSCPixCharge_;
   std::vector<int>    eleCtfCharge_;
   std::vector<float>  eleEn_;
   std::vector<float>  eleD0_;
   std::vector<float>  eleDz_;
   std::vector<float>  eleIP3D_;
   std::vector<float>  eleD0Err_;
   std::vector<float>  eleDzErr_;
   std::vector<float>  eleIP3DErr_;
   std::vector<float>  eleTrkPt_;
   std::vector<float>  eleTrkEta_;
   std::vector<float>  eleTrkPhi_;
   std::vector<int>    eleTrkCharge_;
   std::vector<float>  eleTrkPtErr_;
   std::vector<float>  eleTrkChi2_;
   std::vector<float>  eleTrkNdof_;
   std::vector<float>  eleTrkNormalizedChi2_;
   std::vector<int>    eleTrkValidHits_;
   std::vector<int>    eleTrkLayers_;
   std::vector<float>  elePt_;
   std::vector<float>  eleEta_;
   std::vector<float>  elePhi_;
   std::vector<float>  eleSCEn_;
   std::vector<float>  eleESEn_;
   std::vector<float>  eleSCEta_;
   std::vector<float>  eleSCPhi_;
   std::vector<float>  eleSCRawEn_;
   std::vector<float>  eleSCEtaWidth_;
   std::vector<float>  eleSCPhiWidth_;
   std::vector<float>  eleHoverE_;
   std::vector<float>  eleHoverEBc_;
   std::vector<float>  eleEoverP_;
   std::vector<float>  eleEoverPInv_;
   std::vector<float>  eleEcalE_;
   std::vector<float>  elePAtVtx_;
   std::vector<float>  elePAtSC_;
   std::vector<float>  elePAtCluster_;
   std::vector<float>  elePAtSeed_;
   std::vector<float>  eleBrem_;
   std::vector<float>  eledEtaAtVtx_;
   std::vector<float>  eledPhiAtVtx_;
   std::vector<float>  eledEtaSeedAtVtx_;
   std::vector<float>  eleSigmaIEtaIEta_;
   std::vector<float>  eleSigmaIEtaIEta_2012_;
   std::vector<float>  eleSigmaIPhiIPhi_;
   std::vector<int>    eleConvVeto_;
   std::vector<int>    eleMissHits_;
   std::vector<float>  eleESEffSigmaRR_;
   std::vector<float>  elePFChIso_;
   std::vector<float>  elePFPhoIso_;
   std::vector<float>  elePFNeuIso_;
   std::vector<float>  elePFPUIso_;
   std::vector<float>  elePFChIso03_;
   std::vector<float>  elePFPhoIso03_;
   std::vector<float>  elePFNeuIso03_;
   std::vector<float>  elePFChIso04_;
   std::vector<float>  elePFPhoIso04_;
   std::vector<float>  elePFNeuIso04_;
   std::vector<float>  elePFRelIsoWithEA_;
   std::vector<float>  elePFRelIsoWithDBeta_;
   std::vector<float>  eleEffAreaTimesRho_;
   std::vector<float>  eleR9_;
   std::vector<float>  eleE3x3_;
   std::vector<float>  eleE5x5_;
   std::vector<float>  eleR9Full5x5_;
   std::vector<float>  eleE3x3Full5x5_;
   std::vector<float>  eleE5x5Full5x5_;
   std::vector<int>    NClusters_;
   std::vector<int>    NEcalClusters_;
   std::vector<float>  eleSeedEn_;
   std::vector<float>  eleSeedEta_;
   std::vector<float>  eleSeedPhi_;
   std::vector<float>  eleSeedCryEta_;
   std::vector<float>  eleSeedCryPhi_;
   std::vector<float>  eleSeedCryIeta_;
   std::vector<float>  eleSeedCryIphi_;
   std::vector<float>  eleSeedE3x3_;
   std::vector<float>  eleSeedE5x5_;
   std::vector<float>  eleSEE_;
   std::vector<float>  eleSPP_;
   std::vector<float>  eleSEP_;
   std::vector<float>  eleSeedEMax_;
   std::vector<float>  eleSeedE2nd_;
   std::vector<float>  eleSeedETop_;
   std::vector<float>  eleSeedEBottom_;
   std::vector<float>  eleSeedELeft_;
   std::vector<float>  eleSeedERight_;
   std::vector<float>  eleSeedE2x5Max_;
   std::vector<float>  eleSeedE2x5Top_;
   std::vector<float>  eleSeedE2x5Bottom_;
   std::vector<float>  eleSeedE2x5Left_;
   std::vector<float>  eleSeedE2x5Right_;
   std::vector<float>  eleESOverRaw_;
   std::vector<float>  eleChargeMode_;
   std::vector<float>  eleTrkQoverPMode_;
   std::vector<float>  eleTrkPMode_;
   std::vector<float>  eleTrkPtMode_;
   std::vector<float>  eleTrkEtaMode_;
   std::vector<float>  eleTrkPhiMode_;
   std::vector<float>  eleTrkQoverPModeErr_;
   std::vector<float>  eleTrkPtModeErr_;
   std::vector<float>  eleBC1E_;
   std::vector<float>  eleBC1Eta_;
   std::vector<float>  eleBC2E_;
   std::vector<float>  eleBC2Eta_;
   std::vector<int>    eleIDVeto_; //50nsV1 is depreacated; updated in 76X
   std::vector<int>    eleIDLoose_;
   std::vector<int>    eleIDMedium_;
   std::vector<int>    eleIDTight_;

   // reco::Photon
   Int_t          nPho_;
   std::vector<float>  phoE_;
   std::vector<float>  phoEt_;
   std::vector<float>  phoEta_;
   std::vector<float>  phoPhi_;

   std::vector<float>  phoEcorrStdEcal_;
   std::vector<float>  phoEcorrPhoEcal_;
   std::vector<float>  phoEcorrRegr1_;
   std::vector<float>  phoEcorrRegr2_;
   std::vector<float>  phoEcorrErrStdEcal_;
   std::vector<float>  phoEcorrErrPhoEcal_;
   std::vector<float>  phoEcorrErrRegr1_;
   std::vector<float>  phoEcorrErrRegr2_;

   std::vector<float>  phoSCE_;
   std::vector<float>  phoSCRawE_;
   std::vector<float>  phoSCEta_;
   std::vector<float>  phoSCPhi_;
   std::vector<float>  phoSCEtaWidth_;
   std::vector<float>  phoSCPhiWidth_;
   std::vector<float>  phoSCBrem_;
   std::vector<int>    phoSCnHits_;
   std::vector<uint32_t> phoSCflags_;
   std::vector<int>    phoSCinClean_;
   std::vector<int>    phoSCinUnClean_;
   std::vector<int>    phoSCnBC_;
   std::vector<float>  phoESEn_;

   std::vector<float>  phoPSCE_;
   std::vector<float>  phoPSCRawE_;
   std::vector<float>  phoPSCEta_;
   std::vector<float>  phoPSCPhi_;
   std::vector<float>  phoPSCEtaWidth_;
   std::vector<float>  phoPSCPhiWidth_;
   std::vector<float>  phoPSCBrem_;
   std::vector<int>    phoPSCnHits_;
   std::vector<uint32_t> phoPSCflags_;
   std::vector<int>    phoPSCinClean_;
   std::vector<int>    phoPSCinUnClean_;
   std::vector<int>    phoPSCnBC_;
   std::vector<float>  phoPESEn_;

   std::vector<int>    phoIsPFPhoton_;
   std::vector<int>    phoIsStandardPhoton_;
   std::vector<int>    phoHasPixelSeed_;
   std::vector<int>    phoHasConversionTracks_;
// std::vector<int>    phoEleVeto_;         // TODO: not available in reco::
   std::vector<float>  phoHadTowerOverEm_;
   std::vector<float>  phoHoverE_;
   //std::vector<int>    phoHoverEValid_;   // not available in 94X
   std::vector<float>  phoSigmaIEtaIEta_;
   std::vector<float>  phoR9_;
   std::vector<float>  phoE1x5_;
   std::vector<float>  phoE2x5_;
   std::vector<float>  phoE3x3_;
   std::vector<float>  phoE5x5_;
   std::vector<float>  phoMaxEnergyXtal_;
   std::vector<float>  phoSigmaEtaEta_;

   std::vector<float>  phoSigmaIEtaIEta_2012_;
   std::vector<float>  phoR9_2012_;
   std::vector<float>  phoE1x5_2012_;
   std::vector<float>  phoE2x5_2012_;
   std::vector<float>  phoE3x3_2012_;
   std::vector<float>  phoE5x5_2012_;
   std::vector<float>  phoMaxEnergyXtal_2012_;
   std::vector<float>  phoSigmaEtaEta_2012_;

   std::vector<float>  phoHadTowerOverEm1_;
   std::vector<float>  phoHadTowerOverEm2_;
   std::vector<float>  phoHoverE1_;
   std::vector<float>  phoHoverE2_;

   std::vector<float>  phoSigmaIEtaIPhi_;
   std::vector<float>  phoSigmaIPhiIPhi_;
   std::vector<float>  phoR1x5_;
   std::vector<float>  phoR2x5_;
   std::vector<float>  phoE2nd_;
   std::vector<float>  phoETop_;
   std::vector<float>  phoEBottom_;
   std::vector<float>  phoELeft_;
   std::vector<float>  phoERight_;
   std::vector<float>  phoE1x3_;
   std::vector<float>  phoE2x2_;
   std::vector<float>  phoE2x5Max_;
   std::vector<float>  phoE2x5Top_;
   std::vector<float>  phoE2x5Bottom_;
   std::vector<float>  phoE2x5Left_;
   std::vector<float>  phoE2x5Right_;
   //std::vector<float>  phoSMMajor_;   // TODO: enable when they become available in future releases
   //std::vector<float>  phoSMMinor_;   // TODO: enable when they become available in future releases
   //std::vector<float>  phoSMAlpha_;   // TODO: enable when they become available in future releases

   std::vector<float>  phoSigmaIEtaIPhi_2012_;
   std::vector<float>  phoSigmaIPhiIPhi_2012_;
   std::vector<float>  phoR1x5_2012_;
   std::vector<float>  phoR2x5_2012_;
   std::vector<float>  phoE2nd_2012_;
   std::vector<float>  phoETop_2012_;
   std::vector<float>  phoEBottom_2012_;
   std::vector<float>  phoELeft_2012_;
   std::vector<float>  phoERight_2012_;
   std::vector<float>  phoE1x3_2012_;
   std::vector<float>  phoE2x2_2012_;
   std::vector<float>  phoE2x5Max_2012_;
   std::vector<float>  phoE2x5Top_2012_;
   std::vector<float>  phoE2x5Bottom_2012_;
   std::vector<float>  phoE2x5Left_2012_;
   std::vector<float>  phoE2x5Right_2012_;
   //std::vector<float>  phoSMMajor_2012_;   // TODO: enable when they become available in future releases
   //std::vector<float>  phoSMMinor_2012_;   // TODO: enable when they become available in future releases
   //std::vector<float>  phoSMAlpha_2012_;   // TODO: enable when they become available in future releases

   std::vector<float>  phoBC1E_;
   std::vector<float>  phoBC1Ecorr_;
   std::vector<float>  phoBC1Eta_;
   std::vector<float>  phoBC1Phi_;
   std::vector<int>    phoBC1size_;
   std::vector<uint32_t> phoBC1flags_;
   std::vector<int>    phoBC1inClean_;
   std::vector<int>    phoBC1inUnClean_;
   std::vector<uint32_t> phoBC1rawID_;

   /* std::vector<float>  phoBC2E_; */
   /* std::vector<float>  phoBC2Eta_; */
   /* std::vector<float>  phoBC2Phi_; */
   std::vector<float>  pho_ecalClusterIsoR2_;
   std::vector<float>  pho_ecalClusterIsoR3_;
   std::vector<float>  pho_ecalClusterIsoR4_;
   std::vector<float>  pho_ecalClusterIsoR5_;
   std::vector<float>  pho_hcalRechitIsoR1_;
   std::vector<float>  pho_hcalRechitIsoR2_;
   std::vector<float>  pho_hcalRechitIsoR3_;
   std::vector<float>  pho_hcalRechitIsoR4_;
   std::vector<float>  pho_hcalRechitIsoR5_;
   std::vector<float>  pho_trackIsoR1PtCut20_;
   std::vector<float>  pho_trackIsoR2PtCut20_;
   std::vector<float>  pho_trackIsoR3PtCut20_;
   std::vector<float>  pho_trackIsoR4PtCut20_;
   std::vector<float>  pho_trackIsoR5PtCut20_;
   std::vector<float>  pho_swissCrx_;
   std::vector<float>  pho_seedTime_;
   std::vector<int>    pho_genMatchedIndex_;

   // rechit info
   int nRH_;
   std::vector<uint32_t> rhRawId_;
   std::vector<int> rhieta_;
   std::vector<int> rhiphi_;
   std::vector<int> rhix_;
   std::vector<int> rhiy_;
   std::vector<float> rhE_;
   std::vector<float> rhEt_;
   std::vector<float> rhEta_;
   std::vector<float> rhPhi_;
   std::vector<float> rhChi2_;
   std::vector<float> rhEerror_;
   std::vector<uint32_t> rhFlags_;
   std::vector<int> rhPhoIdx_;   // index of the photon this rechit belongs to
   std::vector<int> rhBCIdx_;    // index of this rechit's BC in the SC

   // photon pf isolation stuff
   std::vector<float> pfcIso1_;
   std::vector<float> pfcIso2_;
   std::vector<float> pfcIso3_;
   std::vector<float> pfcIso4_;
   std::vector<float> pfcIso5_;

   std::vector<float> pfpIso1_;
   std::vector<float> pfpIso2_;
   std::vector<float> pfpIso3_;
   std::vector<float> pfpIso4_;
   std::vector<float> pfpIso5_;

   std::vector<float> pfnIso1_;
   std::vector<float> pfnIso2_;
   std::vector<float> pfnIso3_;
   std::vector<float> pfnIso4_;
   std::vector<float> pfnIso5_;

   std::vector<float> pfpIso1subSC_;
   std::vector<float> pfpIso2subSC_;
   std::vector<float> pfpIso3subSC_;
   std::vector<float> pfpIso4subSC_;
   std::vector<float> pfpIso5subSC_;

   // photon pf isolation UE-subtracted
   std::vector<float> pfcIso1subUE_;
   std::vector<float> pfcIso2subUE_;
   std::vector<float> pfcIso3subUE_;
   std::vector<float> pfcIso4subUE_;
   std::vector<float> pfcIso5subUE_;

   std::vector<float> pfpIso1subUE_;
   std::vector<float> pfpIso2subUE_;
   std::vector<float> pfpIso3subUE_;
   std::vector<float> pfpIso4subUE_;
   std::vector<float> pfpIso5subUE_;

   std::vector<float> pfnIso1subUE_;
   std::vector<float> pfnIso2subUE_;
   std::vector<float> pfnIso3subUE_;
   std::vector<float> pfnIso4subUE_;
   std::vector<float> pfnIso5subUE_;

   std::vector<float> pfpIso1subSCsubUE_;
   std::vector<float> pfpIso2subSCsubUE_;
   std::vector<float> pfpIso3subSCsubUE_;
   std::vector<float> pfpIso4subSCsubUE_;
   std::vector<float> pfpIso5subSCsubUE_;

   // photon pf isolation with pT cut and UE-subtracted
   std::vector<float> pfcIso1pTgt1p0subUE_;
   std::vector<float> pfcIso2pTgt1p0subUE_;
   std::vector<float> pfcIso3pTgt1p0subUE_;
   std::vector<float> pfcIso4pTgt1p0subUE_;
   std::vector<float> pfcIso5pTgt1p0subUE_;

   std::vector<float> pfcIso1pTgt2p0subUE_;
   std::vector<float> pfcIso2pTgt2p0subUE_;
   std::vector<float> pfcIso3pTgt2p0subUE_;
   std::vector<float> pfcIso4pTgt2p0subUE_;
   std::vector<float> pfcIso5pTgt2p0subUE_;

   // remove if deemed useless
   std::vector<float> pfcIso1pTgt3p0subUE_;
   std::vector<float> pfcIso2pTgt3p0subUE_;
   std::vector<float> pfcIso3pTgt3p0subUE_;
   std::vector<float> pfcIso4pTgt3p0subUE_;
   std::vector<float> pfcIso5pTgt3p0subUE_;
   // remove if deemed useless - END

   // photon pf isolation UE-subtracted and cone excluded
   std::vector<float> pfcIso2subUEec_;
   std::vector<float> pfcIso3subUEec_;
   std::vector<float> pfcIso4subUEec_;

   std::vector<float> pfpIso2subUEec_;
   std::vector<float> pfpIso3subUEec_;
   std::vector<float> pfpIso4subUEec_;

   std::vector<float> pfnIso2subUEec_;
   std::vector<float> pfnIso3subUEec_;
   std::vector<float> pfnIso4subUEec_;

   std::vector<float> pfcIso2pTgt2p0subUEec_;
   std::vector<float> pfcIso3pTgt2p0subUEec_;
   std::vector<float> pfcIso4pTgt2p0subUEec_;

   // reco::Muon
   Int_t          nMu_;
   std::vector<float>  muPt_;
   std::vector<float>  muEta_;
   std::vector<float>  muPhi_;
   std::vector<int>    muCharge_;
   std::vector<int>    muType_;
   std::vector<int>    muIsGood_;
   
   std::vector<int>    muIsGlobal_;
   std::vector<int>    muIsTracker_;
   std::vector<int>    muIsPF_;
   std::vector<int>    muIsSTA_;

   std::vector<float>  muD0_;
   std::vector<float>  muDz_;
   std::vector<float>  muIP3D_;
   std::vector<float>  muD0Err_;
   std::vector<float>  muDzErr_;
   std::vector<float>  muIP3DErr_;
   std::vector<float>  muChi2NDF_;
   std::vector<float>  muInnerD0_;
   std::vector<float>  muInnerDz_;

   std::vector<float>  muInnerD0Err_;
   std::vector<float>  muInnerDzErr_;
   std::vector<float>  muInnerPt_;
   std::vector<float>  muInnerPtErr_;
   std::vector<float>  muInnerEta_;

   std::vector<int>    muTrkLayers_;
   std::vector<int>    muPixelLayers_;
   std::vector<int>    muPixelHits_;
   std::vector<int>    muMuonHits_;
   std::vector<int>    muTrkQuality_;
   std::vector<int>    muStations_;
   std::vector<float>  muIsoTrk_;
   std::vector<float>  muPFChIso_;
   std::vector<float>  muPFPhoIso_;
   std::vector<float>  muPFNeuIso_;
   std::vector<float>  muPFPUIso_;
   //https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Muon_selectors_Since_9_4_X
   std::vector<int>    muIDSoft_;
   std::vector<int>    muIDLoose_;
   std::vector<int>    muIDMedium_;
   std::vector<int>    muIDMediumPrompt_;
   std::vector<int>    muIDTight_;
   std::vector<int>    muIDGlobalHighPt_;
   std::vector<int>    muIDTrkHighPt_;
};

#endif
