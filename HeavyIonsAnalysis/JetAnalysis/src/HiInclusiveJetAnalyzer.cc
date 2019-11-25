/*
  Based on the jet response analyzer
  Modified by Matt Nguyen, November 2010

*/

#include "HeavyIonsAnalysis/JetAnalysis/interface/HiInclusiveJetAnalyzer.h"

#include "DataFormats/CaloTowers/interface/CaloTowerCollection.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "RecoBTag/SecondaryVertex/interface/TrackKinematics.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/HiGenData/interface/GenHIEvent.h"
#include "TMath.h"

#include "fastjet/contrib/Njettiness.hh"
#include "fastjet/AreaDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/contrib/SoftDrop.hh"

using namespace std;
using namespace edm;
using namespace reco;

HiInclusiveJetAnalyzer::HiInclusiveJetAnalyzer(const edm::ParameterSet& iConfig) :
	trackSelector(iConfig.getParameter<edm::ParameterSet>("trackSelection")),
        trackPseudoSelector(iConfig.getParameter<edm::ParameterSet>("trackSelection")),
        pseudoVertexV0Filter(iConfig.getParameter<edm::ParameterSet>("trackPairV0Filter")),
        trackPairV0Filter(iConfig.getParameter<edm::ParameterSet>("trackPairV0Filter"))
{

  doMatch_ = iConfig.getUntrackedParameter<bool>("matchJets",false);
  jetTagLabel_ = iConfig.getParameter<InputTag>("jetTag");
  jetTag_ = consumes<reco::JetView> (jetTagLabel_);
  jetTagPat_ = consumes<pat::JetCollection> (jetTagLabel_);
  matchTag_ = consumes<reco::JetView> (iConfig.getUntrackedParameter<InputTag>("matchTag"));
  matchTagPat_ = consumes<pat::JetCollection> (iConfig.getUntrackedParameter<InputTag>("matchTag"));
  
  // vtxTag_ = iConfig.getUntrackedParameter<edm::InputTag>("vtxTag",edm::InputTag("hiSelectedVertex"));
  vtxTag_ = consumes<vector<reco::Vertex> >        (iConfig.getUntrackedParameter<edm::InputTag>("vtxTag",edm::InputTag("offlinePrimaryVertices")));  
  // iConfig.getUntrackedParameter<edm::InputTag>("vtxTag",edm::InputTag("hiSelectedVertex"));
  trackTag_ = consumes<reco::TrackCollection> (iConfig.getParameter<InputTag>("trackTag"));
  useQuality_ = iConfig.getUntrackedParameter<bool>("useQuality",1);
  trackQuality_ = iConfig.getUntrackedParameter<string>("trackQuality","highPurity");

  jetName_ = iConfig.getUntrackedParameter<string>("jetName");
  doGenTaus_ = iConfig.getUntrackedParameter<bool>("doGenTaus",0);
  doSubJets_ = iConfig.getUntrackedParameter<bool>("doSubJets",0);
  doJetConstituents_ = iConfig.getUntrackedParameter<bool>("doJetConstituents", false);
  doGenSubJets_ = iConfig.getUntrackedParameter<bool>("doGenSubJets", false);
  subjetGenTag_ = consumes<reco::JetView> (iConfig.getUntrackedParameter<InputTag>("subjetGenTag"));

  //reWTA reclustering
  doWTARecluster_ = iConfig.getUntrackedParameter<bool>("doWTARecluster", false);

  // useGenTaus = true;
  // if (iConfig.exists("genTau1"))
  //   tokenGenTau1_          = consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("genTau1"));
  // else useGenTaus = false;
  // if (iConfig.exists("genTau2"))
  //   tokenGenTau2_          = consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("genTau2"));
  // else useGenTaus = false;
  // if (iConfig.exists("genTau3"))
  //   tokenGenTau3_          = consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("genTau3"));
  // else useGenTaus = false;
 
  isPythia6_ = iConfig.getUntrackedParameter<bool>("isPythia6",false);  
  isMC_ = iConfig.getUntrackedParameter<bool>("isMC",false);
  useHepMC_ = iConfig.getUntrackedParameter<bool> ("useHepMC",false);
  fillGenJets_ = iConfig.getUntrackedParameter<bool>("fillGenJets",false);

  doExtendedFlavorTagging_ = iConfig.getUntrackedParameter<bool>("doExtendedFlavorTagging",false);
  doHiJetID_ = iConfig.getUntrackedParameter<bool>("doHiJetID",false);
  doStandardJetID_ = iConfig.getUntrackedParameter<bool>("doStandardJetID",false);

  rParam = iConfig.getParameter<double>("rParam");
  hardPtMin_ = iConfig.getUntrackedParameter<double>("hardPtMin",4);
  jetPtMin_ = iConfig.getParameter<double>("jetPtMin");

  if(isMC_){
    genjetTag_ = consumes<vector<reco::GenJet>>(iConfig.getParameter<InputTag>("genjetTag"));
    if(useHepMC_) eventInfoTag_ = consumes<HepMCProduct> (iConfig.getParameter<InputTag>("eventInfoTag"));
    //eventGenInfoTag_ = consumes<GenEventInfoProduct> (iConfig.getParameter<InputTag>("eventInfoTag"));
  }
  verbose_ = iConfig.getUntrackedParameter<bool>("verbose",false);

  useVtx_ = iConfig.getUntrackedParameter<bool>("useVtx",true);
  useJEC_ = iConfig.getUntrackedParameter<bool>("useJEC",true);
  usePat_ = iConfig.getUntrackedParameter<bool>("usePAT",true);

  doLifeTimeTagging_ = iConfig.getUntrackedParameter<bool>("doLifeTimeTagging",false);
  doLifeTimeTaggingExtras_ = iConfig.getUntrackedParameter<bool>("doLifeTimeTaggingExtras",true);
  saveBfragments_  = iConfig.getUntrackedParameter<bool>("saveBfragments",false);
  skipCorrections_  = iConfig.getUntrackedParameter<bool>("skipCorrections",false);

  pfCandidateLabel_ = consumes<reco::PFCandidateCollection> (iConfig.getUntrackedParameter<edm::InputTag>("pfCandidateLabel",edm::InputTag("particleFlowTmp")));

  doTower = iConfig.getUntrackedParameter<bool>("doTower",false);
  if(doTower){
    TowerSrc_ = consumes<CaloTowerCollection>( iConfig.getUntrackedParameter<edm::InputTag>("towersSrc",edm::InputTag("towerMaker")));
  }
  
  // EBSrc_ = iConfig.getUntrackedParameter<edm::InputTag>("EBRecHitSrc",edm::InputTag("ecalRecHit","EcalRecHitsEB"));
  // EESrc_ = iConfig.getUntrackedParameter<edm::InputTag>("EERecHitSrc",edm::InputTag("ecalRecHit","EcalRecHitsEE"));
  // HcalRecHitHFSrc_ = iConfig.getUntrackedParameter<edm::InputTag>("hcalHFRecHitSrc",edm::InputTag("hfreco"));
  // HcalRecHitHBHESrc_ = iConfig.getUntrackedParameter<edm::InputTag>("hcalHBHERecHitSrc",edm::InputTag("hbhereco"));
  doExtraCTagging_ = iConfig.getUntrackedParameter<bool>("doExtraCTagging",false);

  genParticleSrc_ = consumes<reco::GenParticleCollection> (iConfig.getUntrackedParameter<edm::InputTag>("genParticles",edm::InputTag("hiGenParticles")));

  if (doExtendedFlavorTagging_) {
    jetFlavourInfosToken_ = consumes<reco::JetFlavourInfoMatchingCollection>( iConfig.getParameter<edm::InputTag>("jetFlavourInfos") );
    if (doSubJets_) {
      useSubjets_ = iConfig.exists("subjetFlavourInfos") && iConfig.exists("groomedJets");
      if (useSubjets_) {
        subjetFlavourInfosToken_ = consumes<reco::JetFlavourInfoMatchingCollection>(iConfig.getParameter<edm::InputTag>("subjetFlavourInfos"));
        groomedJetsToken_ = consumes<edm::View<reco::Jet> >(iConfig.getParameter<edm::InputTag>("groomedJets"));
      }
    }
  }

  if(doLifeTimeTagging_){
    bTagJetName_ = iConfig.getUntrackedParameter<string>("bTagJetName");
    ipTagInfos_ = bTagJetName_+"ImpactParameter";
    svTagInfos_ = bTagJetName_+"SecondaryVertex";
    trackCHEBJetTags_ = bTagJetName_+"TrackCountingHighEffBJetTags";
    trackCHPBJetTags_ = bTagJetName_+"TrackCountingHighPurBJetTags";
    jetPBJetTags_ = bTagJetName_+"JetProbabilityBJetTags";
    jetBPBJetTags_ = bTagJetName_+"JetBProbabilityBJetTags";
    simpleSVHighEffBJetTags_ = bTagJetName_+"SimpleSecondaryVertexHighEffBJetTags";
    simpleSVHighPurBJetTags_ = bTagJetName_+"SimpleSecondaryVertexHighPurBJetTags";
    combinedSVV1BJetTags_ = bTagJetName_+"CombinedSecondaryVertexBJetTags";
    combinedSVV2BJetTags_ = bTagJetName_+"CombinedSecondaryVertexV2BJetTags";
    deepCSVJetTags_ = bTagJetName_+"PfDeepCSVJetTags:probb";
  }

  //  cout<<" jet collection : "<<jetTag_<<endl;
  doSubEvent_ = 0;

  if(isMC_){
    //     cout<<" genjet collection : "<<genjetTag_<<endl;
    genPtMin_ = iConfig.getUntrackedParameter<double>("genPtMin",10);
    doSubEvent_ = iConfig.getUntrackedParameter<bool>("doSubEvent",0);
  }

  fastjet::contrib::OnePass_KT_Axes     onepass_kt_axes;
  fastjet::contrib::NormalizedMeasure normalizedMeasure(1.,rParam);
  routine_ = std::auto_ptr<fastjet::contrib::Njettiness> ( new fastjet::contrib::Njettiness( onepass_kt_axes, normalizedMeasure) );
}



HiInclusiveJetAnalyzer::~HiInclusiveJetAnalyzer() { }



void
HiInclusiveJetAnalyzer::beginRun(const edm::Run& run,
				 const edm::EventSetup & es) {}

void
HiInclusiveJetAnalyzer::beginJob() {

  //string jetTagName = jetTag_.label()+"_tree";
  string jetTagTitle = jetTagLabel_.label()+" Jet Analysis Tree";
  t = fs1->make<TTree>("t",jetTagTitle.c_str());

  //  TTree* t= new TTree("t","Jet Response Analyzer");
  //t->Branch("run",&jets_.run,"run/I");
  t->Branch("evt",&jets_.evt,"evt/I");
  //t->Branch("lumi",&jets_.lumi,"lumi/I");
  t->Branch("b",&jets_.b,"b/F");
  if (useVtx_) {
    t->Branch("vx",&jets_.vx,"vx/F");
    t->Branch("vy",&jets_.vy,"vy/F");
    t->Branch("vz",&jets_.vz,"vz/F");
  }

  t->Branch("nref",&jets_.nref,"nref/I");
  t->Branch("rawpt",jets_.rawpt,"rawpt[nref]/F");
  if(!skipCorrections_) t->Branch("jtpt",jets_.jtpt,"jtpt[nref]/F");
  t->Branch("jteta",jets_.jteta,"jteta[nref]/F");
  t->Branch("jty",jets_.jty,"jty[nref]/F");
  t->Branch("jtphi",jets_.jtphi,"jtphi[nref]/F");
  t->Branch("jtpu",jets_.jtpu,"jtpu[nref]/F");
  t->Branch("jtm",jets_.jtm,"jtm[nref]/F");
  t->Branch("jtarea",jets_.jtarea,"jtarea[nref]/F");

  //for reWTA reclustering
  if(doWTARecluster_){
    t->Branch("WTAeta",jets_.WTAeta,"WTAeta[nref]/F");
    t->Branch("WTAphi",jets_.WTAphi,"WTAphi[nref]/F");
  }

  t->Branch("jtPfCHF",jets_.jtPfCHF,"jtPfCHF[nref]/F");
  t->Branch("jtPfNHF",jets_.jtPfNHF,"jtPfNHF[nref]/F");
  t->Branch("jtPfCEF",jets_.jtPfCEF,"jtPfCEF[nref]/F");
  t->Branch("jtPfNEF",jets_.jtPfNEF,"jtPfNEF[nref]/F");
  t->Branch("jtPfMUF",jets_.jtPfMUF,"jtPfMUF[nref]/F");

  t->Branch("jtPfCHM",jets_.jtPfCHM,"jtPfCHM[nref]/I");
  t->Branch("jtPfNHM",jets_.jtPfNHM,"jtPfNHM[nref]/I");
  t->Branch("jtPfCEM",jets_.jtPfCEM,"jtPfCEM[nref]/I");
  t->Branch("jtPfNEM",jets_.jtPfNEM,"jtPfNEM[nref]/I");
  t->Branch("jtPfMUM",jets_.jtPfMUM,"jtPfMUM[nref]/I");

  t->Branch("jttau1",jets_.jttau1,"jttau1[nref]/F");
  t->Branch("jttau2",jets_.jttau2,"jttau2[nref]/F");
  t->Branch("jttau3",jets_.jttau3,"jttau3[nref]/F");

  if(doExtendedFlavorTagging_){
  	t->Branch("jtHadronFlavor",jets_.jtHadronFlavor,"jtHadronFlavor[nref]/F");
	t->Branch("jtPartonFlavor",jets_.jtPartonFlavor,"jtPartonFlavor[nref]/F");
  } 
 
  if(doSubJets_) {
    t->Branch("jtSubJetPt",&jets_.jtSubJetPt);
    t->Branch("jtSubJetEta",&jets_.jtSubJetEta);
    t->Branch("jtSubJetPhi",&jets_.jtSubJetPhi);
    t->Branch("jtSubJetM",&jets_.jtSubJetM);
    t->Branch("jtSubJetHadronFlavor",&jets_.jtSubJetHadronFlavor);
    t->Branch("jtSubJetPartonFlavor",&jets_.jtSubJetPartonFlavor);
    t->Branch("jtSubJetHadronDR",&jets_.jtSubJetHadronDR);
    t->Branch("jtSubJetHadronPt",&jets_.jtSubJetHadronPt);
    t->Branch("jtSubJetHadronEta",&jets_.jtSubJetHadronEta);
    t->Branch("jtSubJetHadronPhi",&jets_.jtSubJetHadronPhi);
    t->Branch("jtSubJetHadronPdg",&jets_.jtSubJetHadronPdg);
    t->Branch("jtSubJetPartonDR",&jets_.jtSubJetPartonDR);
    t->Branch("jtSubJetPartonPt",&jets_.jtSubJetPartonPt);
    t->Branch("jtSubJetPartonEta",&jets_.jtSubJetPartonEta);
    t->Branch("jtSubJetPartonPhi",&jets_.jtSubJetPartonPhi);
    t->Branch("jtSubJetPartonPdg",&jets_.jtSubJetPartonPdg);
  }

  if(doJetConstituents_){
    t->Branch("jtConstituentsId",&jets_.jtConstituentsId);
    t->Branch("jtConstituentsE",&jets_.jtConstituentsE);
    t->Branch("jtConstituentsPt",&jets_.jtConstituentsPt);
    t->Branch("jtConstituentsEta",&jets_.jtConstituentsEta);
    t->Branch("jtConstituentsPhi",&jets_.jtConstituentsPhi);
    t->Branch("jtConstituentsM",&jets_.jtConstituentsM);  
    t->Branch("jtSDConstituentsId",&jets_.jtSDConstituentsId);
    t->Branch("jtSDConstituentsE",&jets_.jtSDConstituentsE);
    t->Branch("jtSDConstituentsPt",&jets_.jtSDConstituentsPt);
    t->Branch("jtSDConstituentsEta",&jets_.jtSDConstituentsEta);
    t->Branch("jtSDConstituentsPhi",&jets_.jtSDConstituentsPhi);
    t->Branch("jtSDConstituentsM",&jets_.jtSDConstituentsM);  
  }
  // jet ID information, jet composition
  if(doHiJetID_){
    t->Branch("trackMax", jets_.trackMax,"trackMax[nref]/F");
    t->Branch("trackSum", jets_.trackSum,"trackSum[nref]/F");
    t->Branch("trackN", jets_.trackN,"trackN[nref]/I");
    t->Branch("trackHardSum", jets_.trackHardSum,"trackHardSum[nref]/F");
    t->Branch("trackHardN", jets_.trackHardN,"trackHardN[nref]/I");

    t->Branch("chargedMax", jets_.chargedMax,"chargedMax[nref]/F");
    t->Branch("chargedSum", jets_.chargedSum,"chargedSum[nref]/F");
    t->Branch("chargedN", jets_.chargedN,"chargedN[nref]/I");
    t->Branch("chargedHardSum", jets_.chargedHardSum,"chargedHardSum[nref]/F");
    t->Branch("chargedHardN", jets_.chargedHardN,"chargedHardN[nref]/I");

    t->Branch("photonMax", jets_.photonMax,"photonMax[nref]/F");
    t->Branch("photonSum", jets_.photonSum,"photonSum[nref]/F");
    t->Branch("photonN", jets_.photonN,"photonN[nref]/I");
    t->Branch("photonHardSum", jets_.photonHardSum,"photonHardSum[nref]/F");
    t->Branch("photonHardN", jets_.photonHardN,"photonHardN[nref]/I");

    t->Branch("neutralMax", jets_.neutralMax,"neutralMax[nref]/F");
    t->Branch("neutralSum", jets_.neutralSum,"neutralSum[nref]/F");
    t->Branch("neutralN", jets_.neutralN,"neutralN[nref]/I");

    t->Branch("hcalSum", jets_.hcalSum,"hcalSum[nref]/F");
    t->Branch("ecalSum", jets_.ecalSum,"ecalSum[nref]/F");

    t->Branch("eMax", jets_.eMax,"eMax[nref]/F");
    t->Branch("eSum", jets_.eSum,"eSum[nref]/F");
    t->Branch("eN", jets_.eN,"eN[nref]/I");

    t->Branch("muMax", jets_.muMax,"muMax[nref]/F");
    t->Branch("muSum", jets_.muSum,"muSum[nref]/F");
    t->Branch("muN", jets_.muN,"muN[nref]/I");
  }

  if(doStandardJetID_){
    t->Branch("fHPD",jets_.fHPD,"fHPD[nref]/F");
    t->Branch("fRBX",jets_.fRBX,"fRBX[nref]/F");
    t->Branch("n90",jets_.n90,"n90[nref]/I");
    t->Branch("fSubDet1",jets_.fSubDet1,"fSubDet1[nref]/F");
    t->Branch("fSubDet2",jets_.fSubDet2,"fSubDet2[nref]/F");
    t->Branch("fSubDet3",jets_.fSubDet3,"fSubDet3[nref]/F");
    t->Branch("fSubDet4",jets_.fSubDet4,"fSubDet4[nref]/F");
    t->Branch("restrictedEMF",jets_.restrictedEMF,"restrictedEMF[nref]/F");
    t->Branch("nHCAL",jets_.nHCAL,"nHCAL[nref]/I");
    t->Branch("nECAL",jets_.nECAL,"nECAL[nref]/I");
    t->Branch("apprHPD",jets_.apprHPD,"apprHPD[nref]/F");
    t->Branch("apprRBX",jets_.apprRBX,"apprRBX[nref]/F");

    //  t->Branch("hitsInN90",jets_.n90,"hitsInN90[nref]");
    t->Branch("n2RPC",jets_.n2RPC,"n2RPC[nref]/I");
    t->Branch("n3RPC",jets_.n3RPC,"n3RPC[nref]/I");
    t->Branch("nRPC",jets_.nRPC,"nRPC[nref]/I");

    t->Branch("fEB",jets_.fEB,"fEB[nref]/F");
    t->Branch("fEE",jets_.fEE,"fEE[nref]/F");
    t->Branch("fHB",jets_.fHB,"fHB[nref]/F");
    t->Branch("fHE",jets_.fHE,"fHE[nref]/F");
    t->Branch("fHO",jets_.fHO,"fHO[nref]/F");
    t->Branch("fLong",jets_.fLong,"fLong[nref]/F");
    t->Branch("fShort",jets_.fShort,"fShort[nref]/F");
    t->Branch("fLS",jets_.fLS,"fLS[nref]/F");
    t->Branch("fHFOOT",jets_.fHFOOT,"fHFOOT[nref]/F");
  }

  // Jet ID
  if(doMatch_){
    if(!skipCorrections_) t->Branch("matchedPt", jets_.matchedPt,"matchedPt[nref]/F");
    t->Branch("matchedRawPt", jets_.matchedRawPt,"matchedRawPt[nref]/F");
    t->Branch("matchedPu", jets_.matchedPu,"matchedPu[nref]/F");
    t->Branch("matchedR", jets_.matchedR,"matchedR[nref]/F");
  }

  // b-jet discriminators
  if (doLifeTimeTagging_) {

    t->Branch("discr_ssvHighEff",jets_.discr_ssvHighEff,"discr_ssvHighEff[nref]/F");
    t->Branch("discr_ssvHighPur",jets_.discr_ssvHighPur,"discr_ssvHighPur[nref]/F");

    t->Branch("discr_csvV1",jets_.discr_csvV1,"discr_csvV1[nref]/F");
    t->Branch("discr_csvV2",jets_.discr_csvV2,"discr_csvV2[nref]/F");
    t->Branch("discr_deepCSV",jets_.discr_deepCSV,"discr_deepCSV[nref]/F");
    t->Branch("discr_muByIp3",jets_.discr_muByIp3,"discr_muByIp3[nref]/F");
    t->Branch("discr_muByPt",jets_.discr_muByPt,"discr_muByPt[nref]/F");
    t->Branch("discr_prob",jets_.discr_prob,"discr_prob[nref]/F");
    t->Branch("discr_probb",jets_.discr_probb,"discr_probb[nref]/F");
    t->Branch("discr_tcHighEff",jets_.discr_tcHighEff,"discr_tcHighEff[nref]/F");
    t->Branch("discr_tcHighPur",jets_.discr_tcHighPur,"discr_tcHighPur[nref]/F");

    t->Branch("nsvtx",    jets_.nsvtx,    "nsvtx[nref]/I");
    t->Branch("svType", &jets_.svType);
    t->Branch("svtxntrk", &jets_.svtxntrk);
    t->Branch("svtxdl",   &jets_.svtxdl);
    t->Branch("svtxdls",  &jets_.svtxdls);
    t->Branch("svtxdl2d", &jets_.svtxdl2d);
    t->Branch("svtxdls2d", &jets_.svtxdls2d);
    t->Branch("svtxm",    &jets_.svtxm);
    t->Branch("svtxpt",   &jets_.svtxpt);
    t->Branch("svtxmcorr", jets_.svtxmcorr, "svtxmcorr[nref]/F");

    t->Branch("nIPtrk",jets_.nIPtrk,"nIPtrk[nref]/I");
    t->Branch("nselIPtrk",jets_.nselIPtrk,"nselIPtrk[nref]/I");

    if (doLifeTimeTaggingExtras_) {
      t->Branch("nIP",&jets_.nIP,"nIP/I");
      t->Branch("ipJetIndex",jets_.ipJetIndex,"ipJetIndex[nIP]/I");
      t->Branch("ipPt",jets_.ipPt,"ipPt[nIP]/F");
      t->Branch("ipProb0",jets_.ipProb0,"ipProb0[nIP]/F");
      t->Branch("ipProb1",jets_.ipProb1,"ipProb1[nIP]/F");
      t->Branch("ip2d",jets_.ip2d,"ip2d[nIP]/F");
      t->Branch("ip2dSig",jets_.ip2dSig,"ip2dSig[nIP]/F");
      t->Branch("ip3d",jets_.ip3d,"ip3d[nIP]/F");
      t->Branch("ip3dSig",jets_.ip3dSig,"ip3dSig[nIP]/F");
      t->Branch("ipDist2Jet",jets_.ipDist2Jet,"ipDist2Jet[nIP]/F");
      t->Branch("ipDist2JetSig",jets_.ipDist2JetSig,"ipDist2JetSig[nIP]/F");
      t->Branch("ipClosest2Jet",jets_.ipClosest2Jet,"ipClosest2Jet[nIP]/F");
      if(doExtraCTagging_){
	t->Branch("trackPtRel",jets_.trackPtRel,"trackPtRel[nIP]/F");
	t->Branch("trackPPar",jets_.trackPPar,"trackPPar[nIP]/F");
	t->Branch("trackPParRatio",jets_.trackPParRatio,"trackPParRatio[nIP]/F");
	t->Branch("trackDeltaR",jets_.trackDeltaR,"trackDeltaR[nIP]/F");
	t->Branch("trackPtRatio",jets_.trackPtRatio,"trackPtRatio[nIP]/F");
	t->Branch("trackSumJetDeltaR",jets_.trackSumJetDeltaR,"trackSumJetDeltaR[nref]/F");
      }

    }

    if (doExtraCTagging_){
      t->Branch("svtxTrkSumChi2", jets_.svtxTrkSumChi2,"svtxTrkSumChi2[nref]/F");
      t->Branch("svtxTrkNetCharge",jets_.svtxTrkNetCharge,"svtxTrkNetCharge[nref]/I");
      t->Branch("svtxNtrkInCone",jets_.svtxNtrkInCone,"svtxNtrkInCone[nref]/I");
      
      t->Branch("svJetDeltaR", &jets_.svJetDeltaR);
      t->Branch("trackSip2dSigAboveCharm",jets_.trackSip2dSigAboveCharm, "trackSip2dSigAboveCharm[nref]/F");
      t->Branch("trackSip3dSigAboveCharm",jets_.trackSip3dSigAboveCharm, "trackSip3dSigAboveCharm[nref]/F");
      t->Branch("trackSip2dValAboveCharm",jets_.trackSip2dValAboveCharm, "trackSip2dValAboveCharm[nref]/F");
      t->Branch("trackSip3dValAboveCharm",jets_.trackSip3dValAboveCharm, "trackSip3dValAboveCharm[nref]/F");

    }

    t->Branch("mue",     jets_.mue,     "mue[nref]/F");
    t->Branch("mupt",    jets_.mupt,    "mupt[nref]/F");
    t->Branch("mueta",   jets_.mueta,   "mueta[nref]/F");
    t->Branch("muphi",   jets_.muphi,   "muphi[nref]/F");
    t->Branch("mudr",    jets_.mudr,    "mudr[nref]/F");
    t->Branch("muptrel", jets_.muptrel, "muptrel[nref]/F");
    t->Branch("muchg",   jets_.muchg,   "muchg[nref]/I");
  }


  if(isMC_){
    t->Branch("beamId1",&jets_.beamId1,"beamId1/I");
    t->Branch("beamId2",&jets_.beamId2,"beamId2/I");

    t->Branch("pthat",&jets_.pthat,"pthat/F");

    // Only matched gen jets
    t->Branch("refpt",jets_.refpt,"refpt[nref]/F");
    t->Branch("refeta",jets_.refeta,"refeta[nref]/F");
    t->Branch("refy",jets_.refy,"refy[nref]/F");
    t->Branch("refphi",jets_.refphi,"refphi[nref]/F");
    t->Branch("refm",jets_.refm,"refm[nref]/F");
    t->Branch("refarea",jets_.refarea,"refarea[nref]/F");

    if(doGenTaus_) {
      t->Branch("reftau1",jets_.reftau1,"reftau1[nref]/F");
      t->Branch("reftau2",jets_.reftau2,"reftau2[nref]/F");
      t->Branch("reftau3",jets_.reftau3,"reftau3[nref]/F");
    }
    t->Branch("refdphijt",jets_.refdphijt,"refdphijt[nref]/F");
    t->Branch("refdrjt",jets_.refdrjt,"refdrjt[nref]/F");
    // matched parton
    t->Branch("refparton_pt",jets_.refparton_pt,"refparton_pt[nref]/F");
    t->Branch("refparton_flavor",jets_.refparton_flavor,"refparton_flavor[nref]/I");

    if(isPythia6_){
	    t->Branch("refparton_flavorProcess",jets_.refparton_flavorProcess,"refparton_flavorProcess[nref]/I");			
    }

    if(isPythia6_){ // for GSP to bb identify for a event, not for a jet
	    //			t->Branch("refGSP_Channel"             ,jets_.refGSP_Channel,            "refGSP_Channel/I");
	    t->Branch("refGSP_gpt"                 ,jets_.refGSP_gpt,                "refGSP_gpt[nref]/F");
	    t->Branch("refGSP_geta"                ,jets_.refGSP_geta,               "refGSP_geta[nref]/F");
	    t->Branch("refGSP_gphi"                ,jets_.refGSP_gphi,               "refGSP_gphi[nref]/F");
	    t->Branch("refGSP_gidx"                ,jets_.refGSP_gidx,               "refGSP_gidx[nref]/F");
	    t->Branch("refGSP_b1pt"                ,jets_.refGSP_b1pt,               "refGSP_b1pt[nref]/F");
	    t->Branch("refGSP_b1eta"               ,jets_.refGSP_b1eta,              "refGSP_b1eta[nref]/F");
	    t->Branch("refGSP_b1phi"               ,jets_.refGSP_b1phi,              "refGSP_b1phi[nref]/F");
	    t->Branch("refGSP_b2pt"                ,jets_.refGSP_b2pt,               "refGSP_b2pt[nref]/F");
	    t->Branch("refGSP_b2eta"               ,jets_.refGSP_b2eta,              "refGSP_b2eta[nref]/F");
	    t->Branch("refGSP_b2phi"               ,jets_.refGSP_b2phi,              "refGSP_b2phi[nref]/F");
	    //			t->Branch("refGSP_b1Match_jtIdx"       ,jets_.refGSP_b1Match_jtIdx,      "refGSP_b1Match_jtIdx/I");
	    t->Branch("refGSP_b1Match_jtdR"        ,jets_.refGSP_b1Match_jtdR,       "refGSP_b1Match_jtdR[nref]/F");
	    //			t->Branch("refGSP_b1Match_Subjt1dR"    ,jets_.refGSP_b1Match_Subjt1dR,   "refGSP_b1Match_Subjt1dR/F");
	    //			t->Branch("refGSP_b1Match_Subjt2dR"    ,jets_.refGSP_b1Match_Subjt2dR,   "refGSP_b1Match_Subjt2dR/F");
	    //			t->Branch("refGSP_b2Match_jtIdx"       ,jets_.refGSP_b2Match_jtIdx,      "refGSP_b2Match_jtIdx/I");
	    t->Branch("refGSP_b2Match_jtdR"        ,jets_.refGSP_b2Match_jtdR,       "refGSP_b2Match_jtdR[nref]/F");
	    //			t->Branch("refGSP_b1Match_Subjt1dR"    ,jets_.refGSP_b1Match_Subjt1dR,   "refGSP_b1Match_Subjt1dR/F");
	    //			t->Branch("refGSP_b1Match_Subjt2dR"    ,jets_.refGSP_b1Match_Subjt2dR,   "refGSP_b1Match_Subjt2dR/F");
	    t->Branch("refGSP_bbdR"                ,jets_.refGSP_bbdR,               "refGSP_bbdR[nref]/F");
	    //			t->Branch("refGSP_bbdxy"               ,jets_.refGSP_bbdxy,              "refGSP_bbdxy/F");
	    //			t->Branch("refGSP_bbdz"                ,jets_.refGSP_bbdz,               "refGSP_bbdz/F");
	    t->Branch("refGSP_bbzg"                ,jets_.refGSP_bbzg,               "refGSP_bbzg[nref]/F");
	    t->Branch("refGSP_SubJtMatched"        ,jets_.refGSP_SubJtMatched,       "refGSP_SubJtMatched[nref]/I");     
    }

    if(doGenSubJets_) {
      t->Branch("refptG",jets_.refptG,"refptG[nref]/F");
      t->Branch("refetaG",jets_.refetaG,"refetaG[nref]/F");
      t->Branch("refphiG",jets_.refphiG,"refphiG[nref]/F");
      t->Branch("refmG",jets_.refmG,"refmG[nref]/F");
      t->Branch("refSubJetPt",&jets_.refSubJetPt);
      t->Branch("refSubJetEta",&jets_.refSubJetEta);
      t->Branch("refSubJetPhi",&jets_.refSubJetPhi);
      t->Branch("refSubJetM",&jets_.refSubJetM);
    }

    if(doJetConstituents_){
      t->Branch("refConstituentsId",&jets_.refConstituentsId);
      t->Branch("refConstituentsE",&jets_.refConstituentsE);
      t->Branch("refConstituentsPt",&jets_.refConstituentsPt);
      t->Branch("refConstituentsEta",&jets_.refConstituentsEta);
      t->Branch("refConstituentsPhi",&jets_.refConstituentsPhi);
      t->Branch("refConstituentsM",&jets_.refConstituentsM);  
      t->Branch("refSDConstituentsId",&jets_.refSDConstituentsId);
      t->Branch("refSDConstituentsE",&jets_.refSDConstituentsE);
      t->Branch("refSDConstituentsPt",&jets_.refSDConstituentsPt);
      t->Branch("refSDConstituentsEta",&jets_.refSDConstituentsEta);
      t->Branch("refSDConstituentsPhi",&jets_.refSDConstituentsPhi);
      t->Branch("refSDConstituentsM",&jets_.refSDConstituentsM);  
    }

    
    t->Branch("genChargedSum", jets_.genChargedSum,"genChargedSum[nref]/F");
    t->Branch("genHardSum", jets_.genHardSum,"genHardSum[nref]/F");
    t->Branch("signalChargedSum", jets_.signalChargedSum,"signalChargedSum[nref]/F");
    t->Branch("signalHardSum", jets_.signalHardSum,"signalHardSum[nref]/F");

    if(doSubEvent_){
      t->Branch("subid",jets_.subid,"subid[nref]/I");
    }

    if(fillGenJets_){
      // For all gen jets, matched or unmatched
      t->Branch("ngen",&jets_.ngen,"ngen/I");
      t->Branch("genmatchindex",jets_.genmatchindex,"genmatchindex[ngen]/I");
      t->Branch("genpt",jets_.genpt,"genpt[ngen]/F");
      t->Branch("geneta",jets_.geneta,"geneta[ngen]/F");
      t->Branch("geny",jets_.geny,"geny[ngen]/F");
      if(doGenTaus_) {
        t->Branch("gentau1",jets_.gentau1,"gentau1[ngen]/F");
        t->Branch("gentau2",jets_.gentau2,"gentau2[ngen]/F");
        t->Branch("gentau3",jets_.gentau3,"gentau3[ngen]/F");
      }
      t->Branch("genphi",jets_.genphi,"genphi[ngen]/F");
      t->Branch("genm",jets_.genm,"genm[ngen]/F");
      t->Branch("gendphijt",jets_.gendphijt,"gendphijt[ngen]/F");
      t->Branch("gendrjt",jets_.gendrjt,"gendrjt[ngen]/F");

      //for reWTA reclustering
      if(doWTARecluster_){
        t->Branch("WTAgeneta",jets_.WTAgeneta,"WTAgeneta[ngen]/F");
        t->Branch("WTAgenphi",jets_.WTAgenphi,"WTAgenphi[ngen]/F");
      }

      if(doGenSubJets_) {
        t->Branch("genptG",jets_.genptG,"genptG[ngen]/F");
        t->Branch("genetaG",jets_.genetaG,"genetaG[ngen]/F");
        t->Branch("genphiG",jets_.genphiG,"genphiG[ngen]/F");
        t->Branch("genmG",jets_.genmG,"genmG[ngen]/F");
        t->Branch("genSubJetPt",&jets_.genSubJetPt);
        t->Branch("genSubJetEta",&jets_.genSubJetEta);
        t->Branch("genSubJetPhi",&jets_.genSubJetPhi);
        t->Branch("genSubJetM",&jets_.genSubJetM);
      }

      if(doJetConstituents_){
	t->Branch("genConstituentsId",&jets_.genConstituentsId);
	t->Branch("genConstituentsE",&jets_.genConstituentsE);
	t->Branch("genConstituentsPt",&jets_.genConstituentsPt);
	t->Branch("genConstituentsEta",&jets_.genConstituentsEta);
	t->Branch("genConstituentsPhi",&jets_.genConstituentsPhi);
	t->Branch("genConstituentsM",&jets_.genConstituentsM);  
	t->Branch("genSDConstituentsId",&jets_.genSDConstituentsId);
	t->Branch("genSDConstituentsE",&jets_.genSDConstituentsE);
	t->Branch("genSDConstituentsPt",&jets_.genSDConstituentsPt);
	t->Branch("genSDConstituentsEta",&jets_.genSDConstituentsEta);
	t->Branch("genSDConstituentsPhi",&jets_.genSDConstituentsPhi);
	t->Branch("genSDConstituentsM",&jets_.genSDConstituentsM);  
      }
      
      if(doSubEvent_){
	t->Branch("gensubid",jets_.gensubid,"gensubid[ngen]/I");
      }
    }

    if(saveBfragments_  ) {
      t->Branch("bMult",&jets_.bMult,"bMult/I");
      t->Branch("bJetIndex",jets_.bJetIndex,"bJetIndex[bMult]/I");
      t->Branch("bStatus",jets_.bStatus,"bStatus[bMult]/I");
      t->Branch("bVx",jets_.bVx,"bVx[bMult]/F");
      t->Branch("bVy",jets_.bVy,"bVy[bMult]/F");
      t->Branch("bVz",jets_.bVz,"bVz[bMult]/F");
      t->Branch("bPt",jets_.bPt,"bPt[bMult]/F");
      t->Branch("bEta",jets_.bEta,"bEta[bMult]/F");
      t->Branch("bPhi",jets_.bPhi,"bPhi[bMult]/F");
      t->Branch("bPdg",jets_.bPdg,"bPdg[bMult]/I");
      t->Branch("bChg",jets_.bChg,"bChg[bMult]/I");
    }

  }

}


void
HiInclusiveJetAnalyzer::analyze(const Event& iEvent,
				const EventSetup& iSetup) {
  int event = iEvent.id().event();
  int run = iEvent.id().run();
  int lumi = iEvent.id().luminosityBlock();

  jets_.run = run;
  jets_.evt = event;
  jets_.lumi = lumi;

  LogDebug("HiInclusiveJetAnalyzer")<<"START event: "<<event<<" in run "<<run<<endl;

  int bin = -1;
  double hf = 0.;
  double b = 999.;

  // loop the events

  jets_.bin = bin;
  jets_.hf = hf;

  reco::Vertex::Point vtx(0,0,0);
  if (useVtx_) {
    edm::Handle<vector<reco::Vertex> >vertex;
    iEvent.getByToken(vtxTag_, vertex);

    if(vertex->size()>0) {
      jets_.vx=vertex->begin()->x();
      jets_.vy=vertex->begin()->y();
      jets_.vz=vertex->begin()->z();
      vtx = vertex->begin()->position();
    }
  }

  edm::Handle<pat::JetCollection> patjets;
  if(usePat_)iEvent.getByToken(jetTagPat_, patjets);

  edm::Handle<pat::JetCollection> patmatchedjets;
  iEvent.getByToken(matchTagPat_, patmatchedjets);

  edm::Handle<reco::JetView> matchedjets;
  iEvent.getByToken(matchTag_, matchedjets);

  if(doGenSubJets_)
    iEvent.getByToken(subjetGenTag_, gensubjets_);
  
  edm::Handle<reco::JetView> jets;
  iEvent.getByToken(jetTag_, jets);

  edm::Handle<reco::PFCandidateCollection> pfCandidates;
  iEvent.getByToken(pfCandidateLabel_,pfCandidates);

  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByToken(trackTag_,tracks);

  edm::Handle<reco::GenParticleCollection> genparts;
  iEvent.getByToken(genParticleSrc_,genparts);


  // get tower information
  edm::Handle<CaloTowerCollection> towers;
  if(doTower){
    iEvent.getByToken(TowerSrc_,towers);
  }

  // FILL JRA TREE
  jets_.b = b;
  jets_.nref = 0;

  if( doJetConstituents_ ){
    jets_.jtConstituentsId.clear();
    jets_.jtConstituentsE.clear();
    jets_.jtConstituentsPt.clear();
    jets_.jtConstituentsEta.clear();
    jets_.jtConstituentsPhi.clear();
    jets_.jtConstituentsM.clear();
    jets_.jtSDConstituentsE.clear();
    jets_.jtSDConstituentsPt.clear();
    jets_.jtSDConstituentsEta.clear();
    jets_.jtSDConstituentsPhi.clear();
    jets_.jtSDConstituentsM.clear();

    jets_.refConstituentsId.clear();
    jets_.refConstituentsE.clear();
    jets_.refConstituentsPt.clear();
    jets_.refConstituentsEta.clear();
    jets_.refConstituentsPhi.clear();
    jets_.refConstituentsM.clear();
    jets_.refSDConstituentsE.clear();
    jets_.refSDConstituentsPt.clear();
    jets_.refSDConstituentsEta.clear();
    jets_.refSDConstituentsPhi.clear();
    jets_.refSDConstituentsM.clear();

    jets_.genConstituentsId.clear();
    jets_.genConstituentsE.clear();
    jets_.genConstituentsPt.clear();
    jets_.genConstituentsEta.clear();
    jets_.genConstituentsPhi.clear();
    jets_.genConstituentsM.clear();
    jets_.genSDConstituentsE.clear();
    jets_.genSDConstituentsPt.clear();
    jets_.genSDConstituentsEta.clear();
    jets_.genSDConstituentsPhi.clear();
    jets_.genSDConstituentsM.clear();
  }



  for(unsigned int j = 0; j < jets->size(); ++j){
    const reco::Jet& jet = (*jets)[j];

    if(jet.pt() < jetPtMin_) continue;
    if (useJEC_ && usePat_){
      jets_.rawpt[jets_.nref]=(*patjets)[j].correctedJet("Uncorrected").pt();
    }

    math::XYZVector jetDir = jet.momentum().Unit();

    if(doLifeTimeTagging_){
      jets_.discr_ssvHighEff[jets_.nref]=(*patjets)[j].bDiscriminator(simpleSVHighEffBJetTags_);
      jets_.discr_ssvHighPur[jets_.nref]=(*patjets)[j].bDiscriminator(simpleSVHighPurBJetTags_);
      jets_.discr_csvV1[jets_.nref]=(*patjets)[j].bDiscriminator(combinedSVV1BJetTags_);
      jets_.discr_csvV2[jets_.nref]=(*patjets)[j].bDiscriminator(combinedSVV2BJetTags_);
      jets_.discr_deepCSV[jets_.nref]=(*patjets)[j].bDiscriminator(deepCSVJetTags_);
      jets_.discr_prob[jets_.nref]=(*patjets)[j].bDiscriminator(jetPBJetTags_);
      jets_.discr_probb[jets_.nref]=(*patjets)[j].bDiscriminator(jetBPBJetTags_);
      jets_.discr_tcHighEff[jets_.nref]=(*patjets)[j].bDiscriminator(trackCHEBJetTags_);
      jets_.discr_tcHighPur[jets_.nref]=(*patjets)[j].bDiscriminator(trackCHPBJetTags_);


      if((*patjets)[j].hasTagInfo(svTagInfos_.c_str()) ){
	
	const reco::SecondaryVertexTagInfo *svTagInfo = (*patjets)[j].tagInfoSecondaryVertex(svTagInfos_.c_str());

	jets_.nsvtx[jets_.nref]     = svTagInfo->nVertices();
	
	
	std::vector<int> svtxntrks;
	std::vector<float> svjetDr, svtxdl, svtxdls, svtxdl2d, svtxdls2d, svtxm, svtxpt;
	std::vector<int> svType;
	if(jets_.nsvtx[jets_.nref]==0){
		svtxntrks.push_back(-999);
		svjetDr.push_back(-999);
		svtxdl.push_back(-999);
		svtxdls.push_back(-999);
		svtxdl2d.push_back(-999);
		svtxm.push_back(-999);
		svtxpt.push_back(-999);	
		svType.push_back(-999);
	}
	for (int ivtx=0; ivtx<jets_.nsvtx[jets_.nref]; ivtx++) {
	//  if(jets_.nsvtx[jets_.nref]>1) cout << "ntrks: " << svTagInfo->nVertexTracks(ivtx) << endl;
	  svtxntrks.push_back(svTagInfo->nVertexTracks(ivtx));
	  if(doExtraCTagging_) svjetDr.push_back(reco::deltaR(svTagInfo->flightDirection(ivtx),jetDir));

	  // this is the 3d flight distance, for 2-D use (0,true)
	  Measurement1D m1D = svTagInfo->flightDistance(ivtx);
	  svtxdl.push_back(m1D.value());
	  svtxdls.push_back(m1D.significance());
	  Measurement1D m2D = svTagInfo->flightDistance(ivtx,true);
          svtxdl2d.push_back(m2D.value());
          svtxdls2d.push_back(m2D.significance());
          const Vertex& svtx = svTagInfo->secondaryVertex(ivtx);
	  
	  double svtxM = svtx.p4().mass();
          double svtxPt = svtx.p4().pt();
	  //if(jets_.nsvtx[jets_.nref]>1) cout << "svtxm: "<< svtxM << " svtxpt: "<< svtxPt << endl;
	  svtxm.push_back(svtxM); 
	  svtxpt.push_back(svtxPt);
	 
	  if(doExtraCTagging_){
	    double trkSumChi2=0;
	    int trkNetCharge=0;
	    int nTrkInCone=0;
	    int nsvtxtrks=0;
	    TrackRefVector svtxTracks = svTagInfo->vertexTracks(ivtx);
	    for(unsigned int itrk=0; itrk<svtxTracks.size(); itrk++){
	      nsvtxtrks++;
	      trkSumChi2 += svtxTracks.at(itrk)->chi2();
	      trkNetCharge += svtxTracks.at(itrk)->charge();
	      if(reco::deltaR(svtxTracks.at(itrk)->momentum(),jetDir)<rParam) nTrkInCone++;
	    }
	    jets_.svtxTrkSumChi2[jets_.nref] = trkSumChi2;
	    jets_.svtxTrkNetCharge[jets_.nref] = trkNetCharge;
	    jets_.svtxNtrkInCone[jets_.nref] = nTrkInCone;
	    
	    //try out the corrected mass (http://arxiv.org/pdf/1504.07670v1.pdf)
	    //mCorr=srqt(m^2+p^2sin^2(th)) + p*sin(th)
	    double sinth = svtx.p4().Vect().Unit().Cross(svTagInfo->flightDirection(0).unit()).Mag2();
	    sinth = sqrt(sinth);
	    jets_.svtxmcorr[jets_.nref] = sqrt(pow(svtxM,2)+(pow(svtxPt,2)*pow(sinth,2)))+svtxPt*sinth;
	  }
	  
	  TrackRefVector svtxTracks = svTagInfo->vertexTracks(ivtx);
	  unsigned nVtxTypeTrks=0, nVtxTypeVertices=0, nAssocTrks=0;
	  for(unsigned int itrk=0; itrk<svtxTracks.size(); itrk++){
		  if(svTagInfo->trackWeight(ivtx, svtxTracks.at(itrk)) >= 0.5) nAssocTrks++; //0.5 is default value
	  }
	  if(nAssocTrks>0){
		  bool isTrackVertex = (nAssocTrks==1);
		  ++*(isTrackVertex ? &nVtxTypeTrks : &nVtxTypeVertices); // <-- holy complicated logic, batman! From GhostTrackComputer.cc
	  }
	  if(nVtxTypeVertices) svType.push_back(0);
	  else if(nVtxTypeTrks) svType.push_back(1);
	  else svType.push_back(2);	

	  if(svtx.ndof()>0)jets_.svtxnormchi2[jets_.nref]  = svtx.chi2()/svtx.ndof();
	}
	jets_.svType.push_back(svType);
	jets_.svtxntrk.push_back(svtxntrks);
        jets_.svJetDeltaR.push_back(svjetDr);
        jets_.svtxdl.push_back(svtxdl);
        jets_.svtxdls.push_back(svtxdls);
        jets_.svtxdl2d.push_back(svtxdl2d);
        jets_.svtxdls2d.push_back(svtxdls2d);
        jets_.svtxm.push_back(svtxm);
        jets_.svtxpt.push_back(svtxpt);

      }

      if((*patjets)[j].hasTagInfo(ipTagInfos_.c_str()) ){
	const reco::TrackIPTagInfo *ipTagInfo = (*patjets)[j].tagInfoTrackIP(ipTagInfos_.c_str());
	
	jets_.nIPtrk[jets_.nref] = ipTagInfo->tracks().size();
	jets_.nselIPtrk[jets_.nref] = ipTagInfo->selectedTracks().size();

	if (doLifeTimeTaggingExtras_) {

	  TrackRefVector selTracks=ipTagInfo->selectedTracks();


	  GlobalPoint pv(ipTagInfo->primaryVertex()->position().x(),ipTagInfo->primaryVertex()->position().y(),ipTagInfo->primaryVertex()->position().z());

  	  reco::TrackKinematics allKinematics;	 
 
	  for(int it=0;it<jets_.nselIPtrk[jets_.nref] ;it++){
	    jets_.ipJetIndex[jets_.nIP + it]= jets_.nref;
	    reco::btag::TrackIPData data = ipTagInfo->impactParameterData()[it];
	    jets_.ipPt[jets_.nIP + it] = selTracks[it]->pt();
	    jets_.ipEta[jets_.nIP + it] = selTracks[it]->eta();
	    jets_.ipDxy[jets_.nIP + it] = selTracks[it]->dxy(ipTagInfo->primaryVertex()->position());
	    jets_.ipDz[jets_.nIP + it] = selTracks[it]->dz(ipTagInfo->primaryVertex()->position());
	    jets_.ipChi2[jets_.nIP + it] = selTracks[it]->normalizedChi2();
	    jets_.ipNHit[jets_.nIP + it] = selTracks[it]->numberOfValidHits();
	    jets_.ipNHitPixel[jets_.nIP + it] = selTracks[it]->hitPattern().numberOfValidPixelHits();
	    jets_.ipNHitStrip[jets_.nIP + it] = selTracks[it]->hitPattern().numberOfValidStripHits();
	    jets_.ipIsHitL1[jets_.nIP + it]  = selTracks[it]->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::SubDetector(1),1); //(inBarrel, layer)
	    jets_.ipProb0[jets_.nIP + it] = ipTagInfo->probabilities(0)[it];
	    jets_.ip2d[jets_.nIP + it] = data.ip2d.value();
	    jets_.ip2dSig[jets_.nIP + it] = data.ip2d.significance();
	    jets_.ip3d[jets_.nIP + it] = data.ip3d.value();
	    jets_.ip3dSig[jets_.nIP + it] = data.ip3d.significance();
	    jets_.ipDist2Jet[jets_.nIP + it] = data.distanceToJetAxis.value();
	    jets_.ipClosest2Jet[jets_.nIP + it] = (data.closestToJetAxis - pv).mag();  //decay length
	    
	    //additional info for charm tagger dev
	    if(doExtraCTagging_){
	      math::XYZVector trackMom = selTracks[it]->momentum();
	      jets_.trackPtRel[jets_.nIP + it] = ROOT::Math::VectorUtil::Perp(trackMom,jetDir);
	      jets_.trackPPar[jets_.nIP + it] = jetDir.Dot(trackMom);
	      jets_.trackDeltaR[jets_.nIP + it] = ROOT::Math::VectorUtil::DeltaR(trackMom,jetDir); 
	      jets_.trackPtRatio[jets_.nIP + it] = ROOT::Math::VectorUtil::Perp(trackMom, jetDir)/ std::sqrt(trackMom.Mag2());
	      jets_.trackPParRatio[jets_.nIP + it] = jetDir.Dot(trackMom)/ std::sqrt(trackMom.Mag2());
	      const Track track = *(selTracks[it]);
	      allKinematics.add(track);
	    }
	  }
	  
	  if(doExtraCTagging_){
	    jets_.trackSumJetDeltaR[jets_.nref] = ROOT::Math::VectorUtil::DeltaR(allKinematics.vectorSum(),jetDir);
	    
	    //do some sorting to get the impact parameter of all tracks in descending order
	    jets_.trackSip2dSigAboveCharm[jets_.nref] = getAboveCharmThresh(selTracks, *ipTagInfo, 1);
	    jets_.trackSip3dSigAboveCharm[jets_.nref] = getAboveCharmThresh(selTracks, *ipTagInfo, 2);
	    jets_.trackSip2dValAboveCharm[jets_.nref] = getAboveCharmThresh(selTracks, *ipTagInfo, 3);
	    jets_.trackSip3dValAboveCharm[jets_.nref] = getAboveCharmThresh(selTracks, *ipTagInfo, 4);
	  }
	  jets_.nIP += jets_.nselIPtrk[jets_.nref];
	}
      }

      const PFCandidateCollection *pfCandidateColl = &(*pfCandidates);
      int pfMuonIndex = getPFJetMuon(jet, pfCandidateColl);

      if(pfMuonIndex >=0){
	const reco::PFCandidate muon = pfCandidateColl->at(pfMuonIndex);
	jets_.mupt[jets_.nref]    =  muon.pt();
	jets_.mueta[jets_.nref]   =  muon.eta();
	jets_.muphi[jets_.nref]   =  muon.phi();
	jets_.mue[jets_.nref]     =  muon.energy();
	jets_.mudr[jets_.nref]    =  reco::deltaR(jet,muon);
	jets_.muptrel[jets_.nref] =  getPtRel(muon, jet);
	jets_.muchg[jets_.nref]   =  muon.charge();
      }else{
	jets_.mupt[jets_.nref]    =  0.0;
	jets_.mueta[jets_.nref]   =  0.0;
	jets_.muphi[jets_.nref]   =  0.0;
	jets_.mue[jets_.nref]     =  0.0;
	jets_.mudr[jets_.nref]    =  9.9;
	jets_.muptrel[jets_.nref] =  0.0;
	jets_.muchg[jets_.nref]   = 0;
      }
    }

    if(doHiJetID_){
      // Jet ID variables

      jets_.muMax[jets_.nref] = 0;
      jets_.muSum[jets_.nref] = 0;
      jets_.muN[jets_.nref] = 0;

      jets_.eMax[jets_.nref] = 0;
      jets_.eSum[jets_.nref] = 0;
      jets_.eN[jets_.nref] = 0;

      jets_.neutralMax[jets_.nref] = 0;
      jets_.neutralSum[jets_.nref] = 0;
      jets_.neutralN[jets_.nref] = 0;

      jets_.photonMax[jets_.nref] = 0;
      jets_.photonSum[jets_.nref] = 0;
      jets_.photonN[jets_.nref] = 0;
      jets_.photonHardSum[jets_.nref] = 0;
      jets_.photonHardN[jets_.nref] = 0;

      jets_.chargedMax[jets_.nref] = 0;
      jets_.chargedSum[jets_.nref] = 0;
      jets_.chargedN[jets_.nref] = 0;
      jets_.chargedHardSum[jets_.nref] = 0;
      jets_.chargedHardN[jets_.nref] = 0;

      jets_.trackMax[jets_.nref] = 0;
      jets_.trackSum[jets_.nref] = 0;
      jets_.trackN[jets_.nref] = 0;
      jets_.trackHardSum[jets_.nref] = 0;
      jets_.trackHardN[jets_.nref] = 0;

      jets_.hcalSum[jets_.nref] = 0;
      jets_.ecalSum[jets_.nref] = 0;

      jets_.genChargedSum[jets_.nref] = 0;
      jets_.genHardSum[jets_.nref] = 0;

      jets_.signalChargedSum[jets_.nref] = 0;
      jets_.signalHardSum[jets_.nref] = 0;

      jets_.subid[jets_.nref] = -1;

      for(unsigned int icand = 0; icand < tracks->size(); ++icand){
	const reco::Track& track = (*tracks)[icand];
	if(useQuality_ ){
	  bool goodtrack = track.quality(reco::TrackBase::qualityByName(trackQuality_));
	  if(!goodtrack) continue;
	}

	double dr = deltaR(jet,track);
	if(dr < rParam){
	  double ptcand = track.pt();
	  jets_.trackSum[jets_.nref] += ptcand;
	  jets_.trackN[jets_.nref] += 1;

	  if(ptcand > hardPtMin_){
	    jets_.trackHardSum[jets_.nref] += ptcand;
	    jets_.trackHardN[jets_.nref] += 1;

	  }
	  if(ptcand > jets_.trackMax[jets_.nref]) jets_.trackMax[jets_.nref] = ptcand;
	}
      }

      for(unsigned int icand = 0; icand < pfCandidates->size(); ++icand){
        const reco::PFCandidate& track = (*pfCandidates)[icand];
        double dr = deltaR(jet,track);
        if(dr < rParam){
	  double ptcand = track.pt();
	  int pfid = track.particleId();

	  switch(pfid){
	  case 1:
	    jets_.chargedSum[jets_.nref] += ptcand;
	    jets_.chargedN[jets_.nref] += 1;
	    if(ptcand > hardPtMin_){
	      jets_.chargedHardSum[jets_.nref] += ptcand;
	      jets_.chargedHardN[jets_.nref] += 1;
	    }
	    if(ptcand > jets_.chargedMax[jets_.nref]) jets_.chargedMax[jets_.nref] = ptcand;
	    break;

	  case 2:
	    jets_.eSum[jets_.nref] += ptcand;
	    jets_.eN[jets_.nref] += 1;
	    if(ptcand > jets_.eMax[jets_.nref]) jets_.eMax[jets_.nref] = ptcand;
	    break;

	  case 3:
	    jets_.muSum[jets_.nref] += ptcand;
	    jets_.muN[jets_.nref] += 1;
	    if(ptcand > jets_.muMax[jets_.nref]) jets_.muMax[jets_.nref] = ptcand;
	    break;

	  case 4:
	    jets_.photonSum[jets_.nref] += ptcand;
	    jets_.photonN[jets_.nref] += 1;
	    if(ptcand > hardPtMin_){
	      jets_.photonHardSum[jets_.nref] += ptcand;
	      jets_.photonHardN[jets_.nref] += 1;
	    }
	    if(ptcand > jets_.photonMax[jets_.nref]) jets_.photonMax[jets_.nref] = ptcand;
	    break;

	  case 5:
	    jets_.neutralSum[jets_.nref] += ptcand;
	    jets_.neutralN[jets_.nref] += 1;
	    if(ptcand > jets_.neutralMax[jets_.nref]) jets_.neutralMax[jets_.nref] = ptcand;
	    break;

	  default:
	    break;

	  }
	}
      }

      // Calorimeter fractions
      // Jet ID for CaloJets
      if(doTower){
	// changing it to take things from towers
	for(unsigned int i = 0; i < towers->size(); ++i){
	  
	  const CaloTower & hit= (*towers)[i];
	  double dr = deltaR(jet.eta(), jet.phi(), hit.p4(vtx).Eta(), hit.p4(vtx).Phi());
	  if(dr < rParam){
	    jets_.ecalSum[jets_.nref] += hit.emEt(vtx);
	    jets_.hcalSum[jets_.nref] += hit.hadEt(vtx);
	  }
	}
      }
    }

    if(doMatch_){

      // Alternative reconstruction matching (PF for calo, calo for PF)

      double drMin = 100;
      for(unsigned int imatch = 0 ; imatch < matchedjets->size(); ++imatch){
	const reco::Jet& mjet = (*matchedjets)[imatch];

	double dr = deltaR(jet,mjet);
	if(dr < drMin){
	  jets_.matchedPt[jets_.nref] = mjet.pt();

	  if(usePat_){
	    const pat::Jet& mpatjet = (*patmatchedjets)[imatch];
	    jets_.matchedRawPt[jets_.nref] = mpatjet.correctedJet("Uncorrected").pt();
	    jets_.matchedPu[jets_.nref] = mpatjet.pileup();
	  }
	  jets_.matchedR[jets_.nref] = dr;
	  drMin = dr;
	}
      }

    }

    jets_.jtpt[jets_.nref] = jet.pt();
    jets_.jteta[jets_.nref] = jet.eta();
    jets_.jtphi[jets_.nref] = jet.phi();
    jets_.jty[jets_.nref] = jet.eta();
    jets_.jtpu[jets_.nref] = jet.pileup();
    jets_.jtm[jets_.nref] = jet.mass();
    jets_.jtarea[jets_.nref] = jet.jetArea();

    //recluster the jet constituents in reWTA scheme-------------------------
    if(doWTARecluster_){
      std::vector<fastjet::PseudoJet> candidates;
      auto daughters = jet.getJetConstituents();
      for(auto it = daughters.begin(); it!=daughters.end(); ++it){
        candidates.push_back(fastjet::PseudoJet((**it).px(), (**it).py(), (**it).pz(), (**it).energy()));
      }
      auto cs = new fastjet::ClusterSequence(candidates, WTAjtDef);
      std::vector<fastjet::PseudoJet> wtajt = fastjet::sorted_by_pt(cs->inclusive_jets(0));

      jets_.WTAeta[jets_.nref] = (wtajt.size() > 0) ? wtajt[0].eta() : -999;
      jets_.WTAphi[jets_.nref] = (wtajt.size() > 0) ? wtajt[0].phi_std() : -999;
      delete cs;
    }
    //------------------------------------------------------------------

    jets_.jttau1[jets_.nref] = -999.;
    jets_.jttau2[jets_.nref] = -999.;
    jets_.jttau3[jets_.nref] = -999.;

   edm::Handle<reco::JetFlavourInfoMatchingCollection> theJetFlavourInfos;
   edm::Handle<reco::JetFlavourInfoMatchingCollection> theSubjetFlavourInfos;
   edm::Handle<edm::View<reco::Jet> > groomedJets; 
   if(doExtendedFlavorTagging_){
	   iEvent.getByToken(jetFlavourInfosToken_, theJetFlavourInfos );
	   if(doSubJets_ && useSubjets_){
		   iEvent.getByToken(subjetFlavourInfosToken_, theSubjetFlavourInfos);
		   iEvent.getByToken(groomedJetsToken_, groomedJets);
	   }   

	int ijet=0;
	for(reco::JetFlavourInfoMatchingCollection::const_iterator j= theJetFlavourInfos->begin(); j!=theJetFlavourInfos->end(); j++, ijet++){
		   const reco::Jet *flavorMatch = (*j).first.get();	
//		   if(abs(flavorMatch->pt() - jets_.rawpt[jets_.nref]) < 0.1){
		   if( sqrt(reco::deltaR2(flavorMatch->eta(), flavorMatch->phi(), jet.eta(), jet.phi() )) <0.05  ){
			   jets_.jtHadronFlavor[jets_.nref] = (*j).second.getHadronFlavour();
			   jets_.jtPartonFlavor[jets_.nref] = (*j).second.getPartonFlavour();
		   }	
	}
   }

    if(doSubJets_) analyzeSubjets(jet, jets_.nref, theSubjetFlavourInfos, groomedJets);

    if(usePat_){
      if( (*patjets)[j].hasUserFloat(jetName_+"Njettiness:tau1") )
        jets_.jttau1[jets_.nref] = (*patjets)[j].userFloat(jetName_+"Njettiness:tau1");
      if( (*patjets)[j].hasUserFloat(jetName_+"Njettiness:tau2") )
        jets_.jttau2[jets_.nref] = (*patjets)[j].userFloat(jetName_+"Njettiness:tau2");
      if( (*patjets)[j].hasUserFloat(jetName_+"Njettiness:tau3") )
        jets_.jttau3[jets_.nref] = (*patjets)[j].userFloat(jetName_+"Njettiness:tau3");

      if( (*patjets)[j].isPFJet()) {
        jets_.jtPfCHF[jets_.nref] = (*patjets)[j].chargedHadronEnergyFraction();
        jets_.jtPfNHF[jets_.nref] = (*patjets)[j].neutralHadronEnergyFraction();
        jets_.jtPfCEF[jets_.nref] = (*patjets)[j].chargedEmEnergyFraction();
        jets_.jtPfNEF[jets_.nref] = (*patjets)[j].neutralEmEnergyFraction();
        jets_.jtPfMUF[jets_.nref] = (*patjets)[j].muonEnergyFraction();

        jets_.jtPfCHM[jets_.nref] = (*patjets)[j].chargedHadronMultiplicity();
        jets_.jtPfNHM[jets_.nref] = (*patjets)[j].neutralHadronMultiplicity();
        jets_.jtPfCEM[jets_.nref] = (*patjets)[j].electronMultiplicity();
        jets_.jtPfNEM[jets_.nref] = (*patjets)[j].photonMultiplicity();
        jets_.jtPfMUM[jets_.nref] = (*patjets)[j].muonMultiplicity();
      }
    }

    if(isMC_){

      for(UInt_t i = 0; i < genparts->size(); ++i){
	const reco::GenParticle& p = (*genparts)[i];
	if ( p.status()!=1 || p.charge()==0) continue;
	double dr = deltaR(jet,p);
	if(dr < rParam){
	  double ppt = p.pt();
	  jets_.genChargedSum[jets_.nref] += ppt;
	  if(ppt > hardPtMin_) jets_.genHardSum[jets_.nref] += ppt;
	  if(p.collisionId() == 0){
	    jets_.signalChargedSum[jets_.nref] += ppt;
	    if(ppt > hardPtMin_) jets_.signalHardSum[jets_.nref] += ppt;
	  }
	}
      }
    }

    if(isMC_ && usePat_){
      const reco::GenJet * genjet = (*patjets)[j].genJet();

      if(genjet){
	jets_.refpt[jets_.nref] = genjet->pt();
	jets_.refeta[jets_.nref] = genjet->eta();
	jets_.refphi[jets_.nref] = genjet->phi();
        jets_.refm[jets_.nref] = genjet->mass();
        jets_.refarea[jets_.nref] = genjet->jetArea();
        jets_.refy[jets_.nref] = genjet->eta();
	jets_.refdphijt[jets_.nref] = reco::deltaPhi(jet.phi(), genjet->phi());
	jets_.refdrjt[jets_.nref] = reco::deltaR(jet.eta(),jet.phi(),genjet->eta(),genjet->phi());

	if(doSubEvent_){
	  const GenParticle* gencon = genjet->getGenConstituent(0);
	  jets_.subid[jets_.nref] = gencon->collisionId();
	}

        if(doGenSubJets_)
	  analyzeRefSubjets(*genjet);

      }else{
	jets_.refpt[jets_.nref] = -999.;
	jets_.refeta[jets_.nref] = -999.;
	jets_.refphi[jets_.nref] = -999.;
        jets_.refm[jets_.nref] = -999.;
        jets_.refarea[jets_.nref] = -999.;
	jets_.refy[jets_.nref] = -999.;
	jets_.refdphijt[jets_.nref] = -999.;
	jets_.refdrjt[jets_.nref] = -999.;

	if( doJetConstituents_ ){
	  std::vector<int>   refCId;	  
	  std::vector<float> refCE;
	  std::vector<float> refCPt;
	  std::vector<float> refCEta;
	  std::vector<float> refCPhi;
	  std::vector<float> refCM;
	  refCId.push_back(-999);	  
	  refCE.push_back(-999);
	  refCPt.push_back(-999);
	  refCEta.push_back(-999);
	  refCPhi.push_back(-999);
	  refCM.push_back(-999);

	  jets_.refConstituentsId.push_back(refCId);
	  jets_.refConstituentsE.push_back(refCE);
	  jets_.refConstituentsPt.push_back(refCPt);
	  jets_.refConstituentsEta.push_back(refCEta);
	  jets_.refConstituentsPhi.push_back(refCPhi);
	  jets_.refConstituentsM.push_back(refCM);
	  
	  std::vector<int> refSDId;
	  std::vector<float> refSDCE;
	  std::vector<float> refSDCPt;
	  std::vector<float> refSDCEta;
	  std::vector<float> refSDCPhi;
	  std::vector<float> refSDCM;
	  
	  refSDId.push_back(-999);
	  refSDCE.push_back(-999);
	  refSDCPt.push_back(-999);
	  refSDCEta.push_back(-999);
	  refSDCPhi.push_back(-999);
	  refSDCM.push_back(-999);
	  
	  jets_.refSDConstituentsId.push_back(refSDId);
	  jets_.refSDConstituentsE.push_back(refSDCE);
	  jets_.refSDConstituentsPt.push_back(refSDCPt);
	  jets_.refSDConstituentsEta.push_back(refSDCEta);
	  jets_.refSDConstituentsPhi.push_back(refSDCPhi);
	  jets_.refSDConstituentsM.push_back(refSDCM);
	}

	if(doGenSubJets_) {
	  jets_.refptG[jets_.nref]  = -999.;
	  jets_.refetaG[jets_.nref] = -999.;
          jets_.refphiG[jets_.nref] = -999.;
          jets_.refmG[jets_.nref]   = -999.;

          std::vector<float> sjpt;
          std::vector<float> sjeta;
          std::vector<float> sjphi;
          std::vector<float> sjm;
          sjpt.push_back(-999.);
          sjeta.push_back(-999.);
          sjphi.push_back(-999.);
          sjm.push_back(-999.);

          jets_.refSubJetPt.push_back(sjpt);
          jets_.refSubJetEta.push_back(sjeta);
          jets_.refSubJetPhi.push_back(sjphi);
          jets_.refSubJetM.push_back(sjm);
        }
      }
      jets_.reftau1[jets_.nref] = -999.;
      jets_.reftau2[jets_.nref] = -999.;
      jets_.reftau3[jets_.nref] = -999.;
      
      jets_.jtPartonFlavor[jets_.nref] = (*patjets)[j].partonFlavour();
      jets_.jtHadronFlavor[jets_.nref] = (*patjets)[j].hadronFlavour();
      
          
	//Matt's flavor production code
      if(isPythia6_){
	//int partonFlavor = (*patjets)[j].partonFlavour();
	
	if(jets_.jtHadronFlavor[jets_.nref]==4||jets_.jtHadronFlavor[jets_.nref]==5){
	  
	  int partonMatchIndex = findMatchedParton(jet.eta(), jet.phi(), 0.3, genparts, jets_.jtHadronFlavor[jets_.nref]);
	  if(partonMatchIndex<0){
	    cout<< "jet " << jets_.nref << " declared flavor " << jets_.jtHadronFlavor[jets_.nref] << " couldn't find the parton "<<endl;
	    jets_.refparton_flavorProcess[jets_.nref] = 0;
	  }
	  else{
	    int flavorProcess =  getFlavorProcess(partonMatchIndex, genparts);
	    jets_.refparton_flavorProcess[jets_.nref] = flavorProcess;
	  }
	  
	  // GSP-bbbar tag
	  if( jets_.refparton_flavorProcess[jets_.nref] == 6){
			      int MatchedPartonId= (*genparts)[partonMatchIndex].pdgId();
			      int partonPairIndex=-1;
			      int momIndex = findMatchedParton( (float)(*genparts)[partonMatchIndex].mother(0)->eta() , (float)(*genparts)[partonMatchIndex].mother(0)->phi(),(float)0.001,genparts, 0);
			      if (momIndex >=0 && (*genparts)[momIndex].pdgId()==21){ // double check momidex && momId = gluon
				      for( UInt_t i_dau =0; i_dau < (*genparts)[momIndex].numberOfDaughters(); i_dau++){
					      if( (*genparts)[momIndex].daughter(i_dau)->pdgId()== -MatchedPartonId ){       
						      partonPairIndex=findMatchedParton( (*genparts)[momIndex].daughter(i_dau)->eta(), (*genparts)[momIndex].daughter(i_dau)->phi(),0.001,genparts , 0);
						      break; // terminate for i_dau
					      } 
				      } // end i_dau < (*genparts)[momIndex].numberOfDaughters()
			      } // end if momIndex >=0 && (*genparts)[momIndex].pdgId()==21

			      if(partonPairIndex<=0) {cout<<"event : "<<event<<" ,partonPairIndex = "<<partonPairIndex<<" , momIndex = "<<momIndex<<endl;}
			      if(partonMatchIndex >0 && momIndex >0 && partonPairIndex >0){
				      jets_.refGSP_gpt[jets_.nref]          			=(*genparts)[momIndex].pt();
				      jets_.refGSP_geta [jets_.nref]        			=(*genparts)[momIndex].eta();
				      jets_.refGSP_gphi [jets_.nref]              =(*genparts)[momIndex].phi();
				      jets_.refGSP_gidx [jets_.nref]              =momIndex;
				      jets_.refGSP_b1pt [jets_.nref]              =(*genparts)[partonMatchIndex].pt();
				      jets_.refGSP_b1eta [jets_.nref]				      =(*genparts)[partonMatchIndex].eta();
				      jets_.refGSP_b1phi [jets_.nref]				      =(*genparts)[partonMatchIndex].phi();
				      jets_.refGSP_b2pt [jets_.nref]				      =(*genparts)[partonPairIndex].pt();
				      jets_.refGSP_b2eta [jets_.nref]				      =(*genparts)[partonPairIndex].eta();
				      jets_.refGSP_b2phi [jets_.nref]				      =(*genparts)[partonPairIndex].phi();

				      float b1eta=jets_.refGSP_b1eta [jets_.nref];
				      float b1phi=jets_.refGSP_b1phi [jets_.nref];
				      float b2eta=jets_.refGSP_b2eta [jets_.nref];
				      float b2phi=jets_.refGSP_b2phi [jets_.nref];

				      // jets_.refGSP_b1Match_jtIdx [jets_.nref];

				      jets_.refGSP_b1Match_jtdR [jets_.nref]= pow( pow(b1eta-jet.eta(),2) + pow(deltaPhi(b1phi,jet.phi()),2) , 0.5 ) ;
				      //							jets_.refGSP_b1Match_Subjt1dR [jets_.nref];
				      //							jets_.refGSP_b1Match_Subjt2dR [jets_.nref];

				      // jets_.refGSP_b2Match_jtIdx [jets_.nref];
				      jets_.refGSP_b2Match_jtdR [jets_.nref]= pow( pow(b2eta-jet.eta(),2) + pow(deltaPhi(b2phi,jet.phi()),2) , 0.5 );
				      //							jets_.refGSP_b1Match_Subjt1dR [jets_.nref];
				      //							jets_.refGSP_b1Match_Subjt2dR [jets_.nref];

				      float bbdphi=deltaPhi(b1phi,b2phi);

				      jets_.refGSP_bbdR [jets_.nref] = pow( pow(b1eta-b2eta,2) + pow(bbdphi,2), 0.5);
				      // jets_.refGSP_bbdxy [jets_.nref];
				      // jets_.refGSP_bbdz [jets_.nref];
				      jets_.refGSP_bbzg [jets_.nref] = jets_.refGSP_b2pt[jets_.nref] / (jets_.refGSP_b1pt[jets_.nref]+jets_.refGSP_b2pt[jets_.nref]);
				      if (jets_.refGSP_b2pt[jets_.nref] >jets_.refGSP_b1pt[jets_.nref]){
					      jets_.refGSP_bbzg [jets_.nref] =  jets_.refGSP_b1pt[jets_.nref] / (jets_.refGSP_b1pt[jets_.nref]+jets_.refGSP_b2pt[jets_.nref]);
				      }

				      jets_.refGSP_SubJtMatched [jets_.nref]=-1;
				      if(jets_.refGSP_b1Match_jtdR [jets_.nref] <0.4 && jets_.refGSP_b2Match_jtdR [jets_.nref] <0.4){
					      jets_.refGSP_SubJtMatched [jets_.nref]=1;
				      }

			      } // end if MatchedPartonId >0 && momIndex >0 && partonPairIndex >0  // index check
			      else {jets_.refGSP_SubJtMatched [jets_.nref]=-2;}

		      } // end GSP-bbbar tag

	      } // end if abs(partonFlavor)==4||abs(partonFlavor)==5
	      else jets_.refparton_flavorProcess[jets_.nref] = 0;
      }


      // matched partons
      const reco::GenParticle & parton = *(*patjets)[j].genParton();

      if((*patjets)[j].genParton()){
	jets_.refparton_pt[jets_.nref] = parton.pt();
	jets_.refparton_flavor[jets_.nref] = parton.pdgId();
      } else {
	jets_.refparton_pt[jets_.nref] = -999;
	jets_.refparton_flavor[jets_.nref] = -999;
      }
    }
    jets_.nref++;
  }

  if(isMC_){
  
    if(useHepMC_) {
      edm::Handle<HepMCProduct> hepMCProduct;
      iEvent.getByToken(eventInfoTag_,hepMCProduct);
      const HepMC::GenEvent* MCEvt = hepMCProduct->GetEvent();

      std::pair<HepMC::GenParticle*,HepMC::GenParticle*> beamParticles = MCEvt->beam_particles();
      if(beamParticles.first != 0)jets_.beamId1 = beamParticles.first->pdg_id();
      if(beamParticles.second != 0)jets_.beamId2 = beamParticles.second->pdg_id();
    }
    
    //edm::Handle<GenEventInfoProduct> hEventInfo;
    //iEvent.getByToken(eventGenInfoTag_,hEventInfo);
    //jets_.pthat = hEventInfo->binningValues()[0];

    // binning values and qscale appear to be equivalent, but binning values not always present
    //jets_.pthat = hEventInfo->qScale();

    edm::Handle<vector<reco::GenJet> >genjets;
    //edm::Handle<edm::View<reco::Jet>> genjets;
    iEvent.getByToken(genjetTag_, genjets);
    
    //get gen-level n-jettiness
    // edm::Handle<edm::ValueMap<float> > genTau1s;
    // edm::Handle<edm::ValueMap<float> > genTau2s;
    // edm::Handle<edm::ValueMap<float> > genTau3s;
    // if(useGenTaus) {
    //   Printf("get gen taus");
    //   iEvent.getByToken(tokenGenTau1_,genTau1s);
    //   iEvent.getByToken(tokenGenTau2_,genTau2s);
    //   iEvent.getByToken(tokenGenTau3_,genTau3s);
    // }
    
    jets_.ngen = 0;

    //int igen = 0;
    for(unsigned int igen = 0 ; igen < genjets->size(); ++igen){
      //for ( typename edm::View<reco::Jet>::const_iterator genjetIt = genjets->begin() ; genjetIt != genjets->end() ; ++genjetIt ) {
      const reco::GenJet & genjet = (*genjets)[igen];
      //edm::Ptr<reco::Jet> genjetPtr = genjets->ptrAt(genjetIt - genjets->begin());
      //const reco::GenJet genjet = (*dynamic_cast<const reco::GenJet*>(&(*genjetPtr)));
      float genjet_pt = genjet.pt();

      float tau1 =  -999.;
      float tau2 =  -999.;
      float tau3 =  -9999.;
      if(doGenTaus_) {
        tau1 =  getTau(1,genjet);
        tau2 =  getTau(2,genjet);
        tau3 =  getTau(3,genjet);
      }

      // find matching patJet if there is one
      jets_.gendrjt[jets_.ngen] = -1.0;
      jets_.genmatchindex[jets_.ngen] = -1;
      
      for(int ijet = 0 ; ijet < jets_.nref; ++ijet){
        // poor man's matching, someone fix please

	double deltaPt = fabs(genjet.pt()-jets_.refpt[ijet]); //Note: precision of this ~ .0001, so cut .01
	double deltaEta = fabs(genjet.eta()-jets_.refeta[ijet]); //Note: precision of this is  ~.0000001, but keep it low, .0001 is well below cone size and typical pointing resolution
	double deltaPhi = fabs(reco::deltaPhi(genjet.phi(), jets_.refphi[ijet])); //Note: precision of this is  ~.0000001, but keep it low, .0001 is well below cone size and typical pointing resolution

        if(deltaPt < 0.01 && deltaEta < .0001 && deltaPhi < .0001){
          if(genjet_pt>genPtMin_) {
            jets_.genmatchindex[jets_.ngen] = (int)ijet;
            jets_.gendphijt[jets_.ngen] = reco::deltaPhi(jets_.refphi[ijet],genjet.phi());
            jets_.gendrjt[jets_.ngen] = sqrt(pow(jets_.gendphijt[jets_.ngen],2)+pow(fabs(genjet.eta()-jets_.refeta[ijet]),2));
          }
          if(doGenTaus_) {
            jets_.reftau1[ijet] = tau1;
            jets_.reftau2[ijet] = tau2;
            jets_.reftau3[ijet] = tau3;
          }
          break;
        }
      }

      //reWTA reclustering----------------------------------
      if(doWTARecluster_){
        std::vector<fastjet::PseudoJet> candidates;
        auto daughters = genjet.getJetConstituents();
        for(auto it = daughters.begin(); it!=daughters.end(); ++it){
          candidates.push_back(fastjet::PseudoJet((**it).px(), (**it).py(), (**it).pz(), (**it).energy()));
        }
        auto cs = new fastjet::ClusterSequence(candidates, WTAjtDef);
        std::vector<fastjet::PseudoJet> wtajt = fastjet::sorted_by_pt(cs->inclusive_jets(0));

        jets_.WTAgeneta[jets_.ngen] = (wtajt.size() > 0) ? wtajt[0].eta() : -999;
        jets_.WTAgenphi[jets_.ngen] =  (wtajt.size() > 0) ? wtajt[0].phi_std() : -999;
        delete cs;
      }
      //-------------------------------------------------

      // threshold to reduce size of output in minbias PbPb
      if(genjet_pt>genPtMin_){
	jets_.genpt [jets_.ngen] = genjet_pt;
	jets_.geneta[jets_.ngen] = genjet.eta();
	jets_.genphi[jets_.ngen] = genjet.phi();
        jets_.genm  [jets_.ngen] = genjet.mass();
	jets_.geny  [jets_.ngen] = genjet.eta();

        if(doGenTaus_) {
          jets_.gentau1[jets_.ngen] = tau1;
          jets_.gentau2[jets_.ngen] = tau2;
          jets_.gentau3[jets_.ngen] = tau3;
        }

        if(doGenSubJets_)
          analyzeGenSubjets(genjet);

	if(doSubEvent_){
	  const GenParticle* gencon = genjet.getGenConstituent(0);
	  jets_.gensubid[jets_.ngen] = gencon->collisionId();
	}
	jets_.ngen++;
      }
    }
  }


  t->Fill();

  memset(&jets_,0,sizeof jets_);
}

int
HiInclusiveJetAnalyzer::getPFJetMuon(const pat::Jet& pfJet, const reco::PFCandidateCollection *pfCandidateColl)
{

  int pfMuonIndex = -1;
  float ptMax = 0.;


  for(unsigned icand=0;icand<pfCandidateColl->size(); icand++) {
    const reco::PFCandidate pfCandidate = pfCandidateColl->at(icand);

    int id = pfCandidate.particleId();
    if(abs(id) != 3) continue;

    if(reco::deltaR(pfJet,pfCandidate)>0.5) continue;

    double pt =  pfCandidate.pt();
    if(pt>ptMax){
      ptMax = pt;
      pfMuonIndex = (int) icand;
    }
  }

  return pfMuonIndex;

}


double
HiInclusiveJetAnalyzer::getPtRel(const reco::PFCandidate lep, const pat::Jet& jet )
{

  float lj_x = jet.p4().px();
  float lj_y = jet.p4().py();
  float lj_z = jet.p4().pz();

  // absolute values squared
  float lj2  = lj_x*lj_x+lj_y*lj_y+lj_z*lj_z;
  float lep2 = lep.px()*lep.px()+lep.py()*lep.py()+lep.pz()*lep.pz();

  // projection vec(mu) to lepjet axis
  float lepXlj = lep.px()*lj_x+lep.py()*lj_y+lep.pz()*lj_z;

  // absolute value squared and normalized
  float pLrel2 = lepXlj*lepXlj/lj2;

  // lep2 = pTrel2 + pLrel2
  float pTrel2 = lep2-pLrel2;

  return (pTrel2 > 0) ? std::sqrt(pTrel2) : 0.0;
}


double HiInclusiveJetAnalyzer::getEt(math::XYZPoint pos, double energy){
  double et = energy*sin(pos.theta());
  return et;
}

int HiInclusiveJetAnalyzer::TaggedJet(Jet calojet, Handle<JetTagCollection > jetTags ) {
  double small = 1.e-5;
  int result = -1;

  for (size_t t = 0; t < jetTags->size(); t++) {
    RefToBase<Jet> jet_p = (*jetTags)[t].first;
    if (jet_p.isNull()) {
      continue;
    }
    if (DeltaR<Candidate>()( calojet, *jet_p ) < small) {
      result = (int) t;
    }
  }
  return result;
}
// Matt Flavor Production Identification
// //-------------------------------------------------------------------------------------------------
int HiInclusiveJetAnalyzer::findMatchedParton(float eta, float phi, float maxDr, Handle<GenParticleCollection > genparts, int partonFlavor=0){

	float highestPartonPt =-1.;
	int matchIndex =-1;
	for( size_t i = 0; i < genparts->size(); ++ i ) {
		const GenParticle & genCand = (*genparts)[ i ];

		if(partonFlavor!=0){
//			cout << " candidate " << i << " pdg: "<< genCand.pdgId() << " status: "<< genCand.status() << " dr: "<< deltaR(eta,phi,genCand.eta(),genCand.phi()) << " flavorToMatch: "<< partonFlavor << endl;
			if(abs(genCand.pdgId())!=partonFlavor) continue;
			if(genCand.status()<20) continue;
		}
		double dr = deltaR(eta,phi,genCand.eta(),genCand.phi());
		if(dr>maxDr) continue;
		if(genCand.pt() > highestPartonPt){
			matchIndex = i;
			highestPartonPt = genCand.pt();
		}
	}
	return matchIndex;
}

int HiInclusiveJetAnalyzer::getFlavorProcess(int index, Handle<GenParticleCollection > genparts){

	const GenParticle & constParton = (*genparts)[ index ];
	GenParticle *matchedParton = const_cast<reco::GenParticle*>(&constParton);
	if(matchedParton->numberOfMothers()>1) cout<<" too many parents "<<endl;
	if(matchedParton->numberOfMothers()==0){ /*cout <<" found primary quark of pdg: " << matchedParton->pdgId() << endl;*/ return 1;}
	int momID = matchedParton->mother(0)->pdgId();
	int momIndex = findMatchedParton(matchedParton->mother(0)->eta(),matchedParton->mother(0)->phi(),0.001,genparts);
	if(momIndex==index){ cout << " WARNING! Particle is its own mother??" << endl; return -1; }
	int gmomIdx=-1;
	if(matchedParton->mother(0)->numberOfMothers()>0){
		gmomIdx = findMatchedParton(matchedParton->mother(0)->mother(0)->eta(),matchedParton->mother(0)->mother(0)->phi(),0.001,genparts);
		if(gmomIdx==index) { cout << "WARNING! Particle is its own grandmother" << endl; return -1; }
	}

	while(abs(matchedParton->mother(0)->pdgId())==5 && matchedParton->numberOfMothers()>0){
		if(matchedParton->mother(0)->status()==21) return 1;  // primary b-quark
		else {
			matchedParton = (reco::GenParticle*)(reco::LeafCandidate*)(matchedParton->mother(0));
			//return getFlavorProcess(momIndex,genparts);
		}
	}
	if(abs(momID)==5 && matchedParton->numberOfMothers()==0){ cout << "warning - found orphaned b-quark!" << endl; return -1; }

	if(!isPythia6_){
		if(matchedParton->status()>20 && matchedParton->status()<30) return 2;
		if(matchedParton->status()>30 && matchedParton->status()<40) return 3;
		if(matchedParton->status()>40 && matchedParton->status()<50) return 4;
		if(matchedParton->status()>50){
			if(abs(momID)==21) return 5;
			return 6;
		}
	}
	else{
		if(momIndex<2) return 4; // initial state GSP
		else if(momIndex<4) return 3; // sometimes GSP, sometimes associated to FEX
		else if(momIndex<6) return 2; // primaries
		else if(momIndex<8){
			if(momID==21) return 6;  // final state hard GSP
			else return 5; // final state soft GSP
		}
	}
	//else cout<<" should never get here "<<" momID "<<momID<<" momIndex "<<momIndex<<endl;


	return -1;

}

//--------------------------------------------------------------------------------------------------
float HiInclusiveJetAnalyzer::getTau(unsigned num, const reco::GenJet object) const
{
  std::vector<fastjet::PseudoJet> FJparticles;
  if(object.numberOfDaughters()>0) {
    for (unsigned k = 0; k < object.numberOfDaughters(); ++k)
      {
        const reco::Candidate & dp = *object.daughter(k);
        //const reco::CandidatePtr & dp = object.daughterPtr(k);
        if(dp.pt()>0.) FJparticles.push_back( fastjet::PseudoJet( dp.px(), dp.py(), dp.pz(), dp.energy() ) );
      }
  }
  return routine_->getTau(num, FJparticles);
}


//--------------------------------------------------------------------------------------------------
void HiInclusiveJetAnalyzer::analyzeSubjets(const reco::Jet jet, int idx, edm::Handle<reco::JetFlavourInfoMatchingCollection> theSubjetFlavourInfos, edm::Handle<edm::View<reco::Jet> > groomedJets) {

  std::vector<float> sjpt;
  std::vector<float> sjeta;
  std::vector<float> sjphi;
  std::vector<float> sjm;
  std::vector<float> hadronFlavor;
  std::vector<float> partonFlavor;
  std::vector<std::vector<float>> hadronDR;
  std::vector<std::vector<float>> hadronPt;
  std::vector<std::vector<float>> hadronEta;
  std::vector<std::vector<float>> hadronPhi;
  std::vector<std::vector<float>> hadronPdg;
  std::vector<std::vector<float>> partonDR;
  std::vector<std::vector<float>> partonPt;
  std::vector<std::vector<float>> partonEta;
  std::vector<std::vector<float>> partonPhi;
  std::vector<std::vector<float>> partonPdg;

  if(jet.numberOfDaughters()>0) {
	  //cout << "nsubjets: "<< jet.numberOfDaughters() << endl;
	  for (unsigned k = 0; k < jet.numberOfDaughters(); ++k) {
		  const reco::Candidate & dp = *jet.daughter(k);
		  sjpt.push_back(dp.pt());
		  sjeta.push_back(dp.eta());
		  sjphi.push_back(dp.phi());
		  sjm.push_back(dp.mass());

		  const reco::Jet *subjd = dynamic_cast<const reco::Jet*>(jet.daughter(k));

		  if (doSubJets_ && useSubjets_) {
		    vector<float> hdr, hpt, heta, hphi, hpdg, pdr, ppt, peta, pphi, ppdg;
		    for ( reco::JetFlavourInfoMatchingCollection::const_iterator sj  = theSubjetFlavourInfos->begin(); sj != theSubjetFlavourInfos->end(); sj++ ) { 
		      if( sqrt(reco::deltaR2(subjd->eta(), subjd->phi(), (*sj).first.get()->eta(), (*sj).first.get()->phi() )) <0.01  ){
			
			reco::Jet *aSubjet = const_cast<reco::Jet*>((*sj).first.get());
			
			reco::JetFlavourInfo aInfo = (*sj).second;	
			hadronFlavor.push_back(aInfo.getHadronFlavour());
			partonFlavor.push_back(aInfo.getPartonFlavour());
			const reco::GenParticleRefVector &bHadrons = aInfo.getbHadrons();
			for(reco::GenParticleRefVector::const_iterator it = bHadrons.begin(); it != bHadrons.end(); ++it){
			  hdr.push_back(reco::deltaR(aSubjet->eta(), aSubjet->phi(), (*it)->eta(), (*it)->phi()));
			  hpt.push_back((*it)->pt());
			  heta.push_back((*it)->eta());
			  hphi.push_back((*it)->phi());
			  hpdg.push_back((*it)->pdgId());
			}
			const reco::GenParticleRefVector &cHadrons = aInfo.getcHadrons();
			for(reco::GenParticleRefVector::const_iterator it = cHadrons.begin(); it != cHadrons.end(); ++it){
			  hdr.push_back(reco::deltaR(aSubjet->eta(), aSubjet->phi(), (*it)->eta(), (*it)->phi()));
			  hpt.push_back((*it)->pt());
			  heta.push_back((*it)->eta());
			  hphi.push_back((*it)->phi());
			  hpdg.push_back((*it)->pdgId());
			}
			const reco::GenParticleRefVector & partons = aInfo.getPartons();
			for(reco::GenParticleRefVector::const_iterator it = partons.begin(); it != partons.end(); ++it){
			  pdr.push_back(reco::deltaR( aSubjet->eta(), aSubjet->phi(), (*it)->eta(), (*it)->phi() ));
			  ppt.push_back((*it)->pt());
			  peta.push_back((*it)->eta());
			  pphi.push_back((*it)->phi());
			  ppdg.push_back((*it)->pdgId());
			}
			break;	
		      } // end if reco::deltaR2 subjd (*sj).first.get()
		    } // end for const_iterator sj  = theSubjetFlavourInfos->begin()
		    hadronDR.push_back(hdr);
		    hadronPt.push_back(hpt);
		    hadronEta.push_back(heta);
		    hadronPhi.push_back(hphi);
		    hadronPdg.push_back(hpdg);
		    partonDR.push_back(pdr);
		    partonPt.push_back(ppt);
		    partonEta.push_back(peta);
		    partonPhi.push_back(pphi);
		    partonPdg.push_back(ppdg);
		  }	
	  }	  
	  
  } else {
    sjpt.push_back(-999.);
    sjeta.push_back(-999.);
	  sjphi.push_back(-999.);
	  sjm.push_back(-999.);
	  if(doExtendedFlavorTagging_){
	    hadronFlavor.push_back(-999.);
	    partonFlavor.push_back(-999.);
	  }
  }
  //cout << "subjet pt size: "<< sjpt.size() << endl;
  //cout << "csv size: "<< csvV1.size() << endl;
  //cout << "hadron flavor size: " << hadronFlavor.size() << endl;
  //cout << "subjet SV mass size: "<< subjetVtxMass.size() << endl;
  jets_.jtSubJetPt.push_back(sjpt);
  jets_.jtSubJetEta.push_back(sjeta);
  jets_.jtSubJetPhi.push_back(sjphi);
  jets_.jtSubJetM.push_back(sjm);
  if(doExtendedFlavorTagging_){
	  jets_.jtSubJetHadronFlavor.push_back(hadronFlavor);
	  jets_.jtSubJetPartonFlavor.push_back(partonFlavor); 
	  jets_.jtSubJetHadronDR.push_back(hadronDR);
	  jets_.jtSubJetHadronPt.push_back(hadronPt);
	  jets_.jtSubJetHadronEta.push_back(hadronEta);
	  jets_.jtSubJetHadronPhi.push_back(hadronPhi);
	  jets_.jtSubJetHadronPdg.push_back(hadronPdg);
	  jets_.jtSubJetPartonDR.push_back(partonDR);
	  jets_.jtSubJetPartonPt.push_back(partonPt);
	  jets_.jtSubJetPartonEta.push_back(partonEta);
	  jets_.jtSubJetPartonPhi.push_back(partonPhi);
	  jets_.jtSubJetPartonPdg.push_back(partonPdg);
  }	
}

//--------------------------------------------------------------------------------------------------
int HiInclusiveJetAnalyzer::getGroomedGenJetIndex(const reco::GenJet jet) const {
  //Find closest soft-dropped gen jet
  double drMin = 100;
  int imatch = -1;
  for(unsigned int i = 0 ; i < gensubjets_->size(); ++i) {
    const reco::Jet& mjet = (*gensubjets_)[i];

    double dr = deltaR(jet,mjet);
    if(dr < drMin){
      imatch = i;
      drMin = dr;
    }
  }
  return imatch;
}

//--------------------------------------------------------------------------------------------------
void HiInclusiveJetAnalyzer::analyzeRefSubjets(const reco::GenJet jet) {

  //Find closest soft-dropped gen jet
  int imatch = getGroomedGenJetIndex(jet);
  double dr = 999.;
  if(imatch>-1) {
    const reco::Jet& mjet =  (*gensubjets_)[imatch];
    dr = deltaR(jet,mjet);
  }

  std::vector<float> sjpt;
  std::vector<float> sjeta;
  std::vector<float> sjphi;
  std::vector<float> sjm;
  if(imatch>-1 && dr<0.4) {
    const reco::Jet& mjet =  (*gensubjets_)[imatch];
    jets_.refptG[jets_.nref]  = mjet.pt();
    jets_.refetaG[jets_.nref] = mjet.eta();
    jets_.refphiG[jets_.nref] = mjet.phi();
    jets_.refmG[jets_.nref]   = mjet.mass();

    if(mjet.numberOfDaughters()>0) {
      for (unsigned k = 0; k < mjet.numberOfDaughters(); ++k) {
        const reco::Candidate & dp = *mjet.daughter(k);
        sjpt.push_back(dp.pt());
        sjeta.push_back(dp.eta());
        sjphi.push_back(dp.phi());
        sjm.push_back(dp.mass());
      }
    }
  }
  else {
    jets_.refptG[jets_.nref]  = -999.;
    jets_.refetaG[jets_.nref] = -999.;
    jets_.refphiG[jets_.nref] = -999.;
    jets_.refmG[jets_.nref]   = -999.;

    sjpt.push_back(-999.);
    sjeta.push_back(-999.);
    sjphi.push_back(-999.);
    sjm.push_back(-999.);
  }

  jets_.refSubJetPt.push_back(sjpt);
  jets_.refSubJetEta.push_back(sjeta);
  jets_.refSubJetPhi.push_back(sjphi);
  jets_.refSubJetM.push_back(sjm);
}

//--------------------------------------------------------------------------------------------------
void HiInclusiveJetAnalyzer::analyzeGenSubjets(const reco::GenJet jet) {
  //Find closest soft-dropped gen jet
  int imatch = getGroomedGenJetIndex(jet);
  double dr = 999.;
  if(imatch>-1) {
    const reco::Jet& mjet =  (*gensubjets_)[imatch];
    dr = deltaR(jet,mjet);
  }

  std::vector<float> sjpt;
  std::vector<float> sjeta;
  std::vector<float> sjphi;
  std::vector<float> sjm;
  std::vector<float> sjarea;
  if(imatch>-1 && dr<0.4) {
    const reco::Jet& mjet =  (*gensubjets_)[imatch];
    jets_.genptG[jets_.ngen]  = mjet.pt();
    jets_.genetaG[jets_.ngen] = mjet.eta();
    jets_.genphiG[jets_.ngen] = mjet.phi();
    jets_.genmG[jets_.ngen]   = mjet.mass();
    
    if(mjet.numberOfDaughters()>0) {
      for (unsigned k = 0; k < mjet.numberOfDaughters(); ++k) {
        const reco::Candidate & dp = *mjet.daughter(k);
        sjpt.push_back(dp.pt());
        sjeta.push_back(dp.eta());
        sjphi.push_back(dp.phi());
        sjm.push_back(dp.mass());
        //sjarea.push_back(dp.castTo<reco::JetRef>()->jetArea());
      }
    }
  }
  else {
    jets_.genptG[jets_.ngen]  = -999.;
    jets_.genetaG[jets_.ngen] = -999.;
    jets_.genphiG[jets_.ngen] = -999.;
    jets_.genmG[jets_.ngen]   = -999.;
    
    sjpt.push_back(-999.);
    sjeta.push_back(-999.);
    sjphi.push_back(-999.);
    sjm.push_back(-999.);
    sjarea.push_back(-999.);
  }

  jets_.genSubJetPt.push_back(sjpt);
  jets_.genSubJetEta.push_back(sjeta);
  jets_.genSubJetPhi.push_back(sjphi);
  jets_.genSubJetM.push_back(sjm);
  jets_.genSubJetArea.push_back(sjarea);
}

//--------------------------------------------------------------------------------------------------
float HiInclusiveJetAnalyzer::getAboveCharmThresh(TrackRefVector& selTracks, const TrackIPTagInfo& ipData, int sigOrVal)
{

	const double pdgCharmMass = 1.290;
	btag::SortCriteria sc;
	switch(sigOrVal){
		case 1: //2d significance 
			sc = reco::btag::IP2DSig;
		case 2: //3d significance
			sc = reco::btag::IP3DSig;
		case 3:
			sc = reco::btag::IP2DSig;  //values are not sortable!
		case 4:
			sc = reco::btag::IP3DSig;
	}
	std::vector<std::size_t> indices = ipData.sortedIndexes(sc);
	reco::TrackKinematics kin;
	for(unsigned int i=0; i<indices.size(); i++){
		size_t idx = indices[i];
		const Track track = *(selTracks[idx]);
		const btag::TrackIPData &data = ipData.impactParameterData()[idx];
		kin.add(track);
		if(kin.vectorSum().M() > pdgCharmMass){
			switch(sigOrVal){
				case 1:
					return data.ip2d.significance();
				case 2:
					return data.ip3d.significance();
				case 3:
					return data.ip2d.value();
				case 4:
					return data.ip3d.value();
			}
		}
	}
	return 0;

}


DEFINE_FWK_MODULE(HiInclusiveJetAnalyzer);
