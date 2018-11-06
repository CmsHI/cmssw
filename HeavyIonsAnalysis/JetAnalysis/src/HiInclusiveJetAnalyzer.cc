/*
  Based on the jet response analyzer
  Modified by Matt Nguyen, November 2010

*/

#include "HeavyIonsAnalysis/JetAnalysis/interface/HiInclusiveJetAnalyzer.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include <Math/DistFunc.h>
#include "TMath.h"

#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "DataFormats/Common/interface/View.h"

#include "DataFormats/CaloTowers/interface/CaloTowerCollection.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "SimDataFormats/HiGenData/interface/GenHIEvent.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetup.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMapRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMap.h"
#include "L1Trigger/GlobalTrigger/plugins/L1GlobalTrigger.h"

#include "RecoBTag/SecondaryVertex/interface/TrackKinematics.h"

//#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
//#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"

#include "fastjet/contrib/Njettiness.hh"
#include "fastjet/AreaDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/contrib/SoftDrop.hh"

using namespace std;
using namespace edm;
using namespace reco;


// class ExtraInfo : public fastjet::PseudoJet::UserInfoBase {
// public:
//   ExtraInfo(int id) : _index(id){}
//   int part_id() const { return _index; }
// protected:
//   int _index;
// };



HiInclusiveJetAnalyzer::HiInclusiveJetAnalyzer(const edm::ParameterSet& iConfig) :
  geo(0)
{

  doMatch_ = iConfig.getUntrackedParameter<bool>("matchJets",false);
  jetTagLabel_ = iConfig.getParameter<InputTag>("jetTag");
  jetTag_ = consumes<reco::JetView> (jetTagLabel_);
  jetTagPat_ = consumes<pat::JetCollection> (jetTagLabel_);
  matchTag_ = consumes<reco::JetView> (iConfig.getUntrackedParameter<InputTag>("matchTag"));
  matchTagPat_ = consumes<pat::JetCollection> (iConfig.getUntrackedParameter<InputTag>("matchTag"));
  
  // vtxTag_ = iConfig.getUntrackedParameter<edm::InputTag>("vtxTag",edm::InputTag("hiSelectedVertex"));
  vtxTag_ = consumes<vector<reco::Vertex> >        (iConfig.getUntrackedParameter<edm::InputTag>("vtxTag",edm::InputTag("hiSelectedVertex")));  
  // iConfig.getUntrackedParameter<edm::InputTag>("vtxTag",edm::InputTag("hiSelectedVertex"));
  trackTag_ = consumes<reco::TrackCollection> (iConfig.getParameter<InputTag>("trackTag"));
  useQuality_ = iConfig.getUntrackedParameter<bool>("useQuality",1);
  trackQuality_ = iConfig.getUntrackedParameter<string>("trackQuality","highPurity");

  jetName_ = iConfig.getUntrackedParameter<string>("jetName");
  doGenTaus_ = iConfig.getUntrackedParameter<bool>("doGenTaus",0);
  doGenSym_ = iConfig.getUntrackedParameter<bool>("doGenSym",0);
  doSubJets_ = iConfig.getUntrackedParameter<bool>("doSubJets",0);
  doJetConstituents_ = iConfig.getUntrackedParameter<bool>("doJetConstituents", false);
  doNewJetVars_ = iConfig.getUntrackedParameter<bool>("doNewJetVars", false);
  doGenSubJets_ = iConfig.getUntrackedParameter<bool>("doGenSubJets", false);
  subjetGenTag_ = consumes<reco::JetView> (iConfig.getUntrackedParameter<InputTag>("subjetGenTag"));

  if (iConfig.exists("genTau1"))
    tokenGenTau1_          = consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("genTau1"));
  if (iConfig.exists("genTau2"))
    tokenGenTau2_          = consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("genTau2"));
  if (iConfig.exists("genTau3"))
    tokenGenTau3_          = consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("genTau3"));

  if (iConfig.exists("genSym"))
    tokenGenSym_          = consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("genSym"));
  if (iConfig.exists("genDroppedBranches"))
    tokenGenDroppedBranches_          = consumes<edm::ValueMap<int> >(iConfig.getParameter<edm::InputTag>("genDroppedBranches"));

  isMC_ = iConfig.getUntrackedParameter<bool>("isMC",false);
  useHepMC_ = iConfig.getUntrackedParameter<bool> ("useHepMC",false);
  fillGenJets_ = iConfig.getUntrackedParameter<bool>("fillGenJets",false);

  doTrigger_ = iConfig.getUntrackedParameter<bool>("doTrigger",false);
  doHiJetID_ = iConfig.getUntrackedParameter<bool>("doHiJetID",false);
  if(doHiJetID_) jetIDweightFile_ = iConfig.getUntrackedParameter<string>("jetIDWeight","weights.xml");
  doStandardJetID_ = iConfig.getUntrackedParameter<bool>("doStandardJetID",false);

  rParam = iConfig.getParameter<double>("rParam");
  hardPtMin_ = iConfig.getUntrackedParameter<double>("hardPtMin",4);
  jetPtMin_ = iConfig.getParameter<double>("jetPtMin");
  jetAbsEtaMax_ = iConfig.getUntrackedParameter<double>("jetAbsEtaMax", 5.1);

  if(isMC_){
    //genjetTag_ = consumes<vector<reco::GenJet> > (iConfig.getParameter<InputTag>("genjetTag"));
    genjetTag_ = consumes<edm::View<reco::GenJet>>(iConfig.getParameter<InputTag>("genjetTag"));
    if(useHepMC_) eventInfoTag_ = consumes<HepMCProduct> (iConfig.getParameter<InputTag>("eventInfoTag"));
    eventGenInfoTag_ = consumes<GenEventInfoProduct> (iConfig.getParameter<InputTag>("eventInfoTag"));
  }
  verbose_ = iConfig.getUntrackedParameter<bool>("verbose",false);

  useVtx_ = iConfig.getUntrackedParameter<bool>("useVtx",false);
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
  
  doExtraCTagging_ = iConfig.getUntrackedParameter<bool>("doExtraCTagging",false);

  genParticleSrc_ = consumes<reco::GenParticleCollection> (iConfig.getUntrackedParameter<edm::InputTag>("genParticles",edm::InputTag("hiGenParticles")));

  if(doTrigger_){
    L1gtReadout_ = consumes< L1GlobalTriggerReadoutRecord > (iConfig.getParameter<edm::InputTag>("L1gtReadout"));
    hltResName_ = consumes< TriggerResults >(iConfig.getUntrackedParameter<string>("hltTrgResults","TriggerResults::HLT"));


    if (iConfig.exists("hltTrgNames"))
      hltTrgNames_ = iConfig.getUntrackedParameter<vector<string> >("hltTrgNames");

    if (iConfig.exists("hltProcNames"))
      hltProcNames_ = iConfig.getUntrackedParameter<vector<string> >("hltProcNames");
    else {
      hltProcNames_.push_back("FU");
      hltProcNames_.push_back("HLT");
    }
  }
  if(doLifeTimeTagging_){
    bTagJetName_ = iConfig.getUntrackedParameter<string>("bTagJetName");
    ImpactParameterTagInfos_ = consumes<vector<TrackIPTagInfo> > (iConfig.getUntrackedParameter<string>("ImpactParameterTagInfos",(bTagJetName_+"ImpactParameterTagInfos")));
    TrackCountingHighEffBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("TrackCountingHighEffBJetTags",(bTagJetName_+"TrackCountingHighEffBJetTags")));
    TrackCountingHighPurBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("TrackCountingHighPurBJetTags",(bTagJetName_+"TrackCountingHighPurBJetTags")));
    JetProbabilityBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("JetProbabilityBJetTags",(bTagJetName_+"JetProbabilityBJetTags")));
    JetBProbabilityBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("JetBProbabilityBJetTags",(bTagJetName_+"JetBProbabilityBJetTags")));
    SecondaryVertexTagInfos_ = consumes<vector<SecondaryVertexTagInfo> > (iConfig.getUntrackedParameter<string>("SecondaryVertexTagInfos",(bTagJetName_+"SecondaryVertexTagInfos")));
    SecondaryVertexNegativeTagInfos_ = consumes<vector<SecondaryVertexTagInfo> > (iConfig.getUntrackedParameter<string>("SecondaryVertexNegativeTagInfos",(bTagJetName_+"SecondaryVertexNegativeTagInfos")));
    SimpleSecondaryVertexHighEffBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("SimpleSecondaryVertexHighEffBJetTags",(bTagJetName_+"SimpleSecondaryVertexHighEffBJetTags")));
    NegativeSimpleSecondaryVertexHighEffBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("NegativeSimpleSecondaryVertexHighEffBJetTags",(bTagJetName_+"NegativeSimpleSecondaryVertexHighEffBJetTags")));
    SimpleSecondaryVertexHighPurBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("SimpleSecondaryVertexHighPurBJetTags",(bTagJetName_+"SimpleSecondaryVertexHighPurBJetTags")));
    NegativeSimpleSecondaryVertexHighPurBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("NegativeSimpleSecondaryVertexHighPurBJetTags",(bTagJetName_+"NegativeSimpleSecondaryVertexHighPurBJetTags")));
    CombinedSecondaryVertexBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("CombinedSecondaryVertexBJetTags",(bTagJetName_+"CombinedSecondaryVertexBJetTags")));
    NegativeCombinedSecondaryVertexBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("NegativeCombinedSecondaryVertexBJetTags",(bTagJetName_+"NegativeCombinedSecondaryVertexBJetTags")));
    PositiveCombinedSecondaryVertexBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("PositiveCombinedSecondaryVertexBJetTags",(bTagJetName_+"PositiveCombinedSecondaryVertexBJetTags")));
    CombinedSecondaryVertexV2BJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("CombinedSecondaryVertexV2BJetTags",(bTagJetName_+"CombinedSecondaryVertexV2BJetTags")));
    NegativeCombinedSecondaryVertexV2BJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("NegativeCombinedSecondaryVertexV2BJetTags",(bTagJetName_+"NegativeCombinedSecondaryVertexV2BJetTags")));
    PositiveCombinedSecondaryVertexV2BJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("PositiveCombinedSecondaryVertexV2BJetTags",(bTagJetName_+"PositiveCombinedSecondaryVertexV2BJetTags")));
    NegativeSoftPFMuonByPtBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("NegativeSoftPFMuonByPtBJetTags",(bTagJetName_+"NegativeSoftPFMuonByPtBJetTags")));
    PositiveSoftPFMuonByPtBJetTags_ = consumes<JetTagCollection> (iConfig.getUntrackedParameter<string>("PositiveSoftPFMuonByPtBJetTags",(bTagJetName_+"PositiveSoftPFMuonByPtBJetTags")));
  }

  doSubEvent_ = 0;

  if(isMC_){
    genPtMin_ = iConfig.getUntrackedParameter<double>("genPtMin",10);
    doSubEvent_ = iConfig.getUntrackedParameter<bool>("doSubEvent",0);
  }

  fastjet::contrib::OnePass_KT_Axes     onepass_kt_axes;
  fastjet::contrib::NormalizedMeasure normalizedMeasure(1.,rParam);
  routine_ = std::auto_ptr<fastjet::contrib::Njettiness> ( new fastjet::contrib::Njettiness( onepass_kt_axes, normalizedMeasure) );

  if(doHiJetID_){
	  string inputArrs[] = { "trackMax/jtpt", "trackHardSum/jtpt", "trackHardN/jtpt", "chargedN/jtpt", "chargedHardSum/jtpt", "chargedHardN/jtpt", "photonN/jtpt", "photonHardSum/jtpt", "photonHardN/jtpt", "neutralN/jtpt", "hcalSum/jtpt", "ecalSum/jtpt", "chargedMax/jtpt", "chargedSum/jtpt", "neutralMax/jtpt", "neutralSum/jtpt", "photonMax/jtpt", "photonSum/jtpt", "eSum/jtpt", "muSum/jtpt" };
	  varAddr = std::unique_ptr<float[]> (new float[sizeof(inputArrs)/sizeof(inputArrs[0])]);

	  reader = std::unique_ptr<TMVA::Reader> (new TMVA::Reader("V:Color:!Silent"));
	  for(unsigned int ivar=0; ivar< (sizeof(inputArrs)/sizeof(inputArrs[0])); ivar++){ reader->AddVariable(inputArrs[ivar].c_str(), &(varAddr.get()[ivar])); }
	  edm::FileInPath fp(jetIDweightFile_.data());
	  std::string transFileName = fp.fullPath(); 
	  reader->BookMVA("BDTG",transFileName.c_str());
   }
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

  if(doNewJetVars_){
    t->Branch("jtnCands",jets_.jtnCands,"jtnCands[nref]/I");
    t->Branch("jtnChCands",jets_.jtnChCands,"jtnChCands[nref]/I");
    t->Branch("jtnNeCands",jets_.jtnNeCands,"jtnNeCands[nref]/I");
    t->Branch("jtchargedSumConst",jets_.jtchargedSumConst,"jtchargedSumConst[nref]/F");
    t->Branch("jtchargedNConst"  ,jets_.jtchargedNConst  ,"jtchargedNConst  [nref]/I");  
    t->Branch("jteSumConst"      ,jets_.jteSumConst      ,"jteSumConst      [nref]/F");  
    t->Branch("jteNConst"        ,jets_.jteNConst        ,"jteNConst        [nref]/I");  
    t->Branch("jtmuSumConst"     ,jets_.jtmuSumConst     ,"jtmuSumConst     [nref]/F");  
    t->Branch("jtmuNConst"       ,jets_.jtmuNConst       ,"jtmuNConst       [nref]/I");  
    t->Branch("jtphotonSumConst" ,jets_.jtphotonSumConst ,"jtphotonSumConst [nref]/F"); 
    t->Branch("jtphotonNConst"   ,jets_.jtphotonNConst   ,"jtphotonNConst   [nref]/I");  
    t->Branch("jtneutralSumConst",jets_.jtneutralSumConst,"jtneutralSumConst[nref]/F");
    t->Branch("jtneutralNConst"  ,jets_.jtneutralNConst  ,"jtneutralNConst  [nref]/I");  
    t->Branch("jthfhadSumConst"  ,jets_.jthfhadSumConst  ,"jthfhadSumConst[nref]/F");
    t->Branch("jthfhadNConst"    ,jets_.jthfhadNConst    ,"jthfhadNConst  [nref]/I");  
    t->Branch("jthfemSumConst"   ,jets_.jthfemSumConst   ,"jthfemSumConst[nref]/F");
    t->Branch("jthfemNConst"     ,jets_.jthfemNConst     ,"jthfemNConst  [nref]/I");  
    t->Branch("jtMByPt",jets_.jtMByPt,"jtMByPt[nref]/F");
    t->Branch("jtRMSCand",jets_.jtRMSCand,"jtRMSCand[nref]/F");
    t->Branch("jtAxis1",jets_.jtAxis1,"jtAxis1[nref]/F");
    t->Branch("jtAxis2",jets_.jtAxis2,"jtAxis2[nref]/F");
    t->Branch("jtSigma",jets_.jtSigma,"jtSigma[nref]/F");
    t->Branch("jtR",jets_.jtR,"jtR[nref]/F");
    t->Branch("jtpTD",jets_.jtpTD,"jtpTD[nref]/F");
    t->Branch("jtpull",jets_.jtpull,"jtpull[nref]/F");
    t->Branch("jtrm0p5",jets_.jtrm0p5,"jtrm0p5[nref]/F");
    t->Branch("jtrm1",jets_.jtrm1,"jtrm1[nref]/F");
    t->Branch("jtrm2",jets_.jtrm2,"jtrm2[nref]/F");
    t->Branch("jtrm3",jets_.jtrm3,"jtrm3[nref]/F");
    t->Branch("jtSDm",jets_.jtSDm, "jtSDm[nref]/F");
    t->Branch("jtSDpt",jets_.jtSDpt, "jtSDpt[nref]/F");
    t->Branch("jtSDeta",jets_.jtSDeta, "jtSDeta[nref]/F");
    t->Branch("jtSDphi",jets_.jtSDphi, "jtSDphi[nref]/F");
    t->Branch("jtSDptFrac",jets_.jtSDptFrac, "jtSDptFrac[nref]/F");
    t->Branch("jtSDrm0p5",jets_.jtSDrm0p5, "jtSDrm0p5[nref]/F");
    t->Branch("jtSDrm1",jets_.jtSDrm1, "jtSDrm1[nref]/F");
    t->Branch("jtSDrm2",jets_.jtSDrm2, "jtSDrm2[nref]/F");
    t->Branch("jtSDrm3",jets_.jtSDrm3, "jtSDrm3[nref]/F");
  
    t->Branch("jtTbeta20p2",jets_.jtTbeta20p2,"jtTbeta20p2[nref]/F"); 
    t->Branch("jtTbeta20p3",jets_.jtTbeta20p3,"jtTbeta20p3[nref]/F"); 
    t->Branch("jtTbeta20p4",jets_.jtTbeta20p4,"jtTbeta20p4[nref]/F"); 
    t->Branch("jtTbeta20p5",jets_.jtTbeta20p5,"jtTbeta20p5[nref]/F"); 

    t->Branch("jtTbeta30p2",jets_.jtTbeta30p2,"jtTbeta30p2[nref]/F"); 
    t->Branch("jtTbeta30p3",jets_.jtTbeta30p3,"jtTbeta30p3[nref]/F"); 
    t->Branch("jtTbeta30p4",jets_.jtTbeta30p4,"jtTbeta30p4[nref]/F"); 
    t->Branch("jtTbeta30p5",jets_.jtTbeta30p5,"jtTbeta30p5[nref]/F"); 
      
    t->Branch("jtCbeta20p2",jets_.jtCbeta20p2,"jtCbeta20p2[nref]/F"); 
    t->Branch("jtCbeta20p3",jets_.jtCbeta20p3,"jtCbeta20p3[nref]/F"); 
    t->Branch("jtCbeta20p4",jets_.jtCbeta20p4,"jtCbeta20p4[nref]/F"); 
    t->Branch("jtCbeta20p5",jets_.jtCbeta20p5,"jtCbeta20p5[nref]/F"); 
			 
    t->Branch("jtZ11",jets_.jtZ11,"jtZ11[nref]/F");
    t->Branch("jtZ20",jets_.jtZ20,"jtZ20[nref]/F");
    t->Branch("jtZ22",jets_.jtZ22,"jtZ22[nref]/F");
    t->Branch("jtZ31",jets_.jtZ31,"jtZ31[nref]/F");
    t->Branch("jtZ33",jets_.jtZ33,"jtZ33[nref]/F");
    t->Branch("jtZ40",jets_.jtZ40,"jtZ40[nref]/F");
    t->Branch("jtZ42",jets_.jtZ42,"jtZ42[nref]/F");
    t->Branch("jtZ44",jets_.jtZ44,"jtZ44[nref]/F");
    t->Branch("jtZ51",jets_.jtZ51,"jtZ51[nref]/F");
    t->Branch("jtZ53",jets_.jtZ53,"jtZ53[nref]/F");
    t->Branch("jtZ55",jets_.jtZ55,"jtZ55[nref]/F");


    t->Branch("jtPhi1",jets_.jtPhi1,"jtPhi1[nref]/F");
    t->Branch("jtPhi2",jets_.jtPhi2,"jtPhi2[nref]/F");
    t->Branch("jtPhi3",jets_.jtPhi3,"jtPhi3[nref]/F");
    t->Branch("jtPhi4",jets_.jtPhi4,"jtPhi4[nref]/F");
    t->Branch("jtPhi5",jets_.jtPhi5,"jtPhi5[nref]/F");
    t->Branch("jtPhi6",jets_.jtPhi6,"jtPhi6[nref]/F");
    t->Branch("jtPhi7",jets_.jtPhi7,"jtPhi7[nref]/F");

    t->Branch("jtSkx",jets_.jtSkx,"jtSkx[nref]/F");
    t->Branch("jtSky",jets_.jtSky,"jtSky[nref]/F");


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
  
  if(doSubJets_) {
    t->Branch("jtSubJetPt",&jets_.jtSubJetPt);
    t->Branch("jtSubJetEta",&jets_.jtSubJetEta);
    t->Branch("jtSubJetPhi",&jets_.jtSubJetPhi);
    t->Branch("jtSubJetM",&jets_.jtSubJetM);
    t->Branch("jtsym",jets_.jtsym,"jtsym[nref]/F");
    t->Branch("jtdroppedBranches",jets_.jtdroppedBranches,"jtdroppedBranches[nref]/I");
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
    t->Branch("discr_jetID_cuts", jets_.discr_jetID_cuts,"discr_jetID_cuts[nref]/F");
    t->Branch("discr_jetID_bdt", jets_.discr_jetID_bdt,"discr_jetID_bdt[nref]/F");

    t->Branch("discr_fr01", jets_.discr_fr01,"discr_fr01[nref]/F");

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
    t->Branch("discr_muByIp3",jets_.discr_muByIp3,"discr_muByIp3[nref]/F");
    t->Branch("discr_muByPt",jets_.discr_muByPt,"discr_muByPt[nref]/F");
    t->Branch("discr_prob",jets_.discr_prob,"discr_prob[nref]/F");
    t->Branch("discr_probb",jets_.discr_probb,"discr_probb[nref]/F");
    t->Branch("discr_tcHighEff",jets_.discr_tcHighEff,"discr_tcHighEff[nref]/F");
    t->Branch("discr_tcHighPur",jets_.discr_tcHighPur,"discr_tcHighPur[nref]/F");

    t->Branch("ndiscr_ssvHighEff",jets_.ndiscr_ssvHighEff,"ndiscr_ssvHighEff[nref]/F");
    t->Branch("ndiscr_ssvHighPur",jets_.ndiscr_ssvHighPur,"ndiscr_ssvHighPur[nref]/F");
    t->Branch("ndiscr_csvV1",jets_.ndiscr_csvV1,"ndiscr_csvV1[nref]/F");
    t->Branch("ndiscr_csvV2",jets_.ndiscr_csvV2,"ndiscr_csvV2[nref]/F");
    t->Branch("ndiscr_muByPt",jets_.ndiscr_muByPt,"ndiscr_muByPt[nref]/F");

    t->Branch("pdiscr_csvV1",jets_.pdiscr_csvV1,"pdiscr_csvV1[nref]/F");
    t->Branch("pdiscr_csvV2",jets_.pdiscr_csvV2,"pdiscr_csvV2[nref]/F");

    t->Branch("nsvtx",    jets_.nsvtx,    "nsvtx[nref]/I");
    t->Branch("svtxntrk", jets_.svtxntrk, "svtxntrk[nref]/I");
    t->Branch("svtxdl",   jets_.svtxdl,   "svtxdl[nref]/F");
    t->Branch("svtxdls",  jets_.svtxdls,  "svtxdls[nref]/F");
    t->Branch("svtxdl2d", jets_.svtxdl2d, "svtxdl2d[nref]/F");
    t->Branch("svtxdls2d", jets_.svtxdls2d, "svtxdls2d[nref]/F");
    t->Branch("svtxm",    jets_.svtxm,    "svtxm[nref]/F");
    t->Branch("svtxpt",   jets_.svtxpt,   "svtxpt[nref]/F");
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
      
      t->Branch("svJetDeltaR", jets_.svJetDeltaR, "svJetDeltaR[nref]/F");
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

    if(doNewJetVars_){
      t->Branch("refnCands",jets_.refnCands,"refnCands[nref]/I");
      t->Branch("refnChCands",jets_.refnChCands,"refnChCands[nref]/I");
      t->Branch("refnNeCands",jets_.refnNeCands,"refnNeCands[nref]/I");
      t->Branch("refchargedSumConst",jets_.refchargedSumConst,"refchargedSumConst[nref]/F");
      t->Branch("refchargedNConst"  ,jets_.refchargedNConst  ,"refchargedNConst  [nref]/I");  
      t->Branch("refeSumConst"      ,jets_.refeSumConst      ,"refeSumConst      [nref]/F");  
      t->Branch("refeNConst"        ,jets_.refeNConst        ,"refeNConst        [nref]/I");  
      t->Branch("refmuSumConst"     ,jets_.refmuSumConst     ,"refmuSumConst     [nref]/F");  
      t->Branch("refmuNConst"       ,jets_.refmuNConst       ,"refmuNConst       [nref]/I");  
      t->Branch("refphotonSumConst" ,jets_.refphotonSumConst ,"refphotonSumConst [nref]/F"); 
      t->Branch("refphotonNConst"   ,jets_.refphotonNConst   ,"refphotonNConst   [nref]/I");  
      t->Branch("refneutralSumConst",jets_.refneutralSumConst,"refneutralSumConst[nref]/F");
      t->Branch("refneutralNConst"  ,jets_.refneutralNConst  ,"refneutralNConst  [nref]/I");  
      t->Branch("refhfhadSumConst"  ,jets_.refhfhadSumConst  ,"refhfhadSumConst  [nref]/F");
      t->Branch("refhfhadNConst"    ,jets_.refhfhadNConst    ,"refhfhadNConst    [nref]/I");  
      t->Branch("refhfemSumConst"   ,jets_.refhfemSumConst   ,"refhfemSumConst   [nref]/F");
      t->Branch("refhfemNConst"     ,jets_.refhfemNConst     ,"refhfemNConst     [nref]/I");  

      t->Branch("refMByPt",jets_.refMByPt,"refMByPt[nref]/F");
      t->Branch("refRMSCand",jets_.refRMSCand,"refRMSCand[nref]/F");
      t->Branch("refAxis1",jets_.refAxis1,"refAxis1[nref]/F");
      t->Branch("refAxis2",jets_.refAxis2,"refAxis2[nref]/F");
      t->Branch("refSigma",jets_.refSigma,"refSigma[nref]/F");
      t->Branch("refR",jets_.refR,"refR[nref]/F");
      t->Branch("refpTD",jets_.refpTD,"refpTD[nref]/F");
      t->Branch("refpull",jets_.refpull,"refpull[nref]/F");
      t->Branch("refrm0p5",jets_.refrm0p5,"refrm0p5[nref]/F");
      t->Branch("refrm1",jets_.refrm1,"refrm1[nref]/F");
      t->Branch("refrm2",jets_.refrm2,"refrm2[nref]/F");
      t->Branch("refrm3",jets_.refrm3,"refrm3[nref]/F");

      t->Branch("refSDm",jets_.refSDm, "refSDm[nref]/F");
      t->Branch("refSDpt",jets_.refSDpt, "refSDpt[nref]/F");
      t->Branch("refSDeta",jets_.refSDeta, "refSDeta[nref]/F");
      t->Branch("refSDphi",jets_.refSDphi, "refSDphi[nref]/F");
      t->Branch("refSDptFrac",jets_.refSDptFrac, "refSDptFrac[nref]/F");
      t->Branch("refSDrm0p5",jets_.refSDrm0p5, "refSDrm0p5[nref]/F");
      t->Branch("refSDrm1",jets_.refSDrm1, "refSDrm1[nref]/F");
      t->Branch("refSDrm2",jets_.refSDrm2, "refSDrm2[nref]/F");
      t->Branch("refSDrm3",jets_.refSDrm3, "refSDrm3[nref]/F");

      t->Branch("refTbeta20p2",jets_.refTbeta20p2,"refTbeta20p2[nref]/F"); 
      t->Branch("refTbeta20p3",jets_.refTbeta20p3,"refTbeta20p3[nref]/F"); 
      t->Branch("refTbeta20p4",jets_.refTbeta20p4,"refTbeta20p4[nref]/F"); 
      t->Branch("refTbeta20p5",jets_.refTbeta20p5,"refTbeta20p5[nref]/F"); 

      t->Branch("refTbeta30p2",jets_.refTbeta30p2,"refTbeta30p2[nref]/F"); 
      t->Branch("refTbeta30p3",jets_.refTbeta30p3,"refTbeta30p3[nref]/F"); 
      t->Branch("refTbeta30p4",jets_.refTbeta30p4,"refTbeta30p4[nref]/F"); 
      t->Branch("refTbeta30p5",jets_.refTbeta30p5,"refTbeta30p5[nref]/F"); 
      
      t->Branch("refCbeta20p2",jets_.refCbeta20p2,"refCbeta20p2[nref]/F"); 
      t->Branch("refCbeta20p3",jets_.refCbeta20p3,"refCbeta20p3[nref]/F"); 
      t->Branch("refCbeta20p4",jets_.refCbeta20p4,"refCbeta20p4[nref]/F"); 
      t->Branch("refCbeta20p5",jets_.refCbeta20p5,"refCbeta20p5[nref]/F"); 
			 
      t->Branch("refZ11",jets_.refZ11,"refZ11[nref]/F");
      t->Branch("refZ20",jets_.refZ20,"refZ20[nref]/F");
      t->Branch("refZ22",jets_.refZ22,"refZ22[nref]/F");
      t->Branch("refZ31",jets_.refZ31,"refZ31[nref]/F");
      t->Branch("refZ33",jets_.refZ33,"refZ33[nref]/F");
      t->Branch("refZ40",jets_.refZ40,"refZ40[nref]/F");
      t->Branch("refZ42",jets_.refZ42,"refZ42[nref]/F");
      t->Branch("refZ44",jets_.refZ44,"refZ44[nref]/F");
      t->Branch("refZ51",jets_.refZ51,"refZ51[nref]/F");
      t->Branch("refZ53",jets_.refZ53,"refZ53[nref]/F");
      t->Branch("refZ55",jets_.refZ55,"refZ55[nref]/F");


      t->Branch("refPhi1",jets_.refPhi1,"refPhi1[nref]/F");
      t->Branch("refPhi2",jets_.refPhi2,"refPhi2[nref]/F");
      t->Branch("refPhi3",jets_.refPhi3,"refPhi3[nref]/F");
      t->Branch("refPhi4",jets_.refPhi4,"refPhi4[nref]/F");
      t->Branch("refPhi5",jets_.refPhi5,"refPhi5[nref]/F");
      t->Branch("refPhi6",jets_.refPhi6,"refPhi6[nref]/F");
      t->Branch("refPhi7",jets_.refPhi7,"refPhi7[nref]/F");

      t->Branch("refSkx",jets_.refSkx,"refSkx[nref]/F");
      t->Branch("refSky",jets_.refSky,"refSky[nref]/F");
    }
    
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
    t->Branch("refparton_flavorForB",jets_.refparton_flavorForB,"refparton_flavorForB[nref]/I");

    if(doGenSubJets_) {
      t->Branch("refptG",jets_.refptG,"refptG[nref]/F");
      t->Branch("refetaG",jets_.refetaG,"refetaG[nref]/F");
      t->Branch("refphiG",jets_.refphiG,"refphiG[nref]/F");
      t->Branch("refmG",jets_.refmG,"refmG[nref]/F");
      t->Branch("refSubJetPt",&jets_.refSubJetPt);
      t->Branch("refSubJetEta",&jets_.refSubJetEta);
      t->Branch("refSubJetPhi",&jets_.refSubJetPhi);
      t->Branch("refSubJetM",&jets_.refSubJetM);
      t->Branch("refsym",jets_.refsym,"refsym[nref]/F");
      t->Branch("refdroppedBranches",jets_.refdroppedBranches,"refdroppedBranches[nref]/I");
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

      if(doNewJetVars_){
	t->Branch("gennCands",jets_.gennCands,"gennCands[ngen]/I");
	t->Branch("gennChCands",jets_.gennChCands,"gennChCands[ngen]/I");
	t->Branch("gennNeCands",jets_.gennNeCands,"gennNeCands[ngen]/I");
	t->Branch("genchargedNConst"  ,jets_.genchargedNConst  ,"genchargedNConst  [ngen]/I");  
	t->Branch("geneSumConst"      ,jets_.geneSumConst      ,"geneSumConst      [ngen]/F");  
	t->Branch("geneNConst"        ,jets_.geneNConst        ,"geneNConst        [ngen]/I");  
	t->Branch("genmuSumConst"     ,jets_.genmuSumConst     ,"genmuSumConst     [ngen]/F");  
	t->Branch("genmuNConst"       ,jets_.genmuNConst       ,"genmuNConst       [ngen]/I");  
	t->Branch("genphotonSumConst" ,jets_.genphotonSumConst ,"genphotonSumConst [ngen]/F"); 
	t->Branch("genphotonNConst"   ,jets_.genphotonNConst   ,"genphotonNConst   [ngen]/I");  
	t->Branch("genneutralSumConst",jets_.genneutralSumConst,"genneutralSumConst[ngen]/F");
	t->Branch("genneutralNConst"  ,jets_.genneutralNConst  ,"genneutralNConst  [ngen]/I");  
	t->Branch("genhfhadSumConst"  ,jets_.genhfhadSumConst  ,"genhfhadSumConst  [ngen]/F");
	t->Branch("genhfhadNConst"    ,jets_.genhfhadNConst    ,"genhfhadNConst    [ngen]/I");  
	t->Branch("genhfemSumConst"   ,jets_.genhfemSumConst   ,"genhfemSumConst   [ngen]/F");
	t->Branch("genhfemNConst"     ,jets_.genhfemNConst     ,"genhfemNConst     [ngen]/I");  

	t->Branch("genMByPt",jets_.genMByPt,"genMByPt[ngen]/F");
	t->Branch("genRMSCand",jets_.genRMSCand,"genRMSCand[ngen]/F");
	t->Branch("genAxis1",jets_.genAxis1,"genAxis1[ngen]/F");
	t->Branch("genAxis2",jets_.genAxis2,"genAxis2[ngen]/F");
	t->Branch("genSigma",jets_.genSigma,"genSigma[ngen]/F");
	t->Branch("genR",jets_.genR,"genR[ngen]/F");
	t->Branch("genpTD",jets_.genpTD,"genpTD[ngen]/F");
	t->Branch("genpull",jets_.genpull,"genpull[ngen]/F");
	t->Branch("genrm0p5",jets_.genrm0p5,"genrm0p5[ngen]/F");
	t->Branch("genrm1",jets_.genrm1,"genrm1[ngen]/F");
	t->Branch("genrm2",jets_.genrm2,"genrm2[ngen]/F");
	t->Branch("genrm3",jets_.genrm3,"genrm3[ngen]/F");

	t->Branch("genSDm",jets_.genSDm, "genSDm[ngen]/F");
	t->Branch("genSDpt",jets_.genSDpt, "genSDpt[ngen]/F");
	t->Branch("genSDeta",jets_.genSDeta, "genSDeta[ngen]/F");
	t->Branch("genSDphi",jets_.genSDphi, "genSDphi[ngen]/F");
	t->Branch("genSDptFrac",jets_.genSDptFrac, "genSDptFrac[ngen]/F");
	t->Branch("genSDrm0p5",jets_.genSDrm0p5, "genSDrm0p5[ngen]/F");
	t->Branch("genSDrm1",jets_.genSDrm1, "genSDrm1[ngen]/F");
	t->Branch("genSDrm2",jets_.genSDrm2, "genSDrm2[ngen]/F");
	t->Branch("genSDrm3",jets_.genSDrm3, "genSDrm3[ngen]/F");

	t->Branch("genTbeta20p2",jets_.genTbeta20p2,"genTbeta20p2[ngen]/F"); 
	t->Branch("genTbeta20p3",jets_.genTbeta20p3,"genTbeta20p3[ngen]/F"); 
	t->Branch("genTbeta20p4",jets_.genTbeta20p4,"genTbeta20p4[ngen]/F"); 
	t->Branch("genTbeta20p5",jets_.genTbeta20p5,"genTbeta20p5[ngen]/F"); 
      
	t->Branch("genTbeta30p2",jets_.genTbeta30p2,"genTbeta30p2[ngen]/F"); 
	t->Branch("genTbeta30p3",jets_.genTbeta30p3,"genTbeta30p3[ngen]/F"); 
	t->Branch("genTbeta30p4",jets_.genTbeta30p4,"genTbeta30p4[ngen]/F"); 
	t->Branch("genTbeta30p5",jets_.genTbeta30p5,"genTbeta30p5[ngen]/F"); 

	t->Branch("genCbeta20p2",jets_.genCbeta20p2,"genCbeta20p2[ngen]/F"); 
	t->Branch("genCbeta20p3",jets_.genCbeta20p3,"genCbeta20p3[ngen]/F"); 
	t->Branch("genCbeta20p4",jets_.genCbeta20p4,"genCbeta20p4[ngen]/F"); 
	t->Branch("genCbeta20p5",jets_.genCbeta20p5,"genCbeta20p5[ngen]/F"); 

	t->Branch("genZ11",jets_.genZ11,"genZ11[ngen]/F");
	t->Branch("genZ20",jets_.genZ20,"genZ20[ngen]/F");
	t->Branch("genZ22",jets_.genZ22,"genZ22[ngen]/F");
	t->Branch("genZ31",jets_.genZ31,"genZ31[ngen]/F");
	t->Branch("genZ33",jets_.genZ33,"genZ33[ngen]/F");
	t->Branch("genZ40",jets_.genZ40,"genZ40[ngen]/F");
	t->Branch("genZ42",jets_.genZ42,"genZ42[ngen]/F");
	t->Branch("genZ44",jets_.genZ44,"genZ44[ngen]/F");
	t->Branch("genZ51",jets_.genZ51,"genZ51[ngen]/F");
	t->Branch("genZ53",jets_.genZ53,"genZ53[ngen]/F");
	t->Branch("genZ55",jets_.genZ55,"genZ55[ngen]/F");


	t->Branch("genPhi1",jets_.genPhi1,"genPhi1[ngen]/F");
	t->Branch("genPhi2",jets_.genPhi2,"genPhi2[ngen]/F");
	t->Branch("genPhi3",jets_.genPhi3,"genPhi3[ngen]/F");
	t->Branch("genPhi4",jets_.genPhi4,"genPhi4[ngen]/F");
	t->Branch("genPhi5",jets_.genPhi5,"genPhi5[ngen]/F");
	t->Branch("genPhi6",jets_.genPhi6,"genPhi6[ngen]/F");
	t->Branch("genPhi7",jets_.genPhi7,"genPhi7[ngen]/F");

	t->Branch("genSkx",jets_.genSkx,"genSkx[ngen]/F");
	t->Branch("genSky",jets_.genSky,"genSky[ngen]/F");
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
        t->Branch("gensym",jets_.gensym,"gensym[ngen]/F");
        t->Branch("gendroppedBranches",jets_.gendroppedBranches,"gendroppedBranches[ngen]/I");
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
  /*
    if(!isMC_){
    t->Branch("nL1TBit",&jets_.nL1TBit,"nL1TBit/I");
    t->Branch("l1TBit",jets_.l1TBit,"l1TBit[nL1TBit]/O");

    t->Branch("nL1ABit",&jets_.nL1ABit,"nL1ABit/I");
    t->Branch("l1ABit",jets_.l1ABit,"l1ABit[nL1ABit]/O");

    t->Branch("nHLTBit",&jets_.nHLTBit,"nHLTBit/I");
    t->Branch("hltBit",jets_.hltBit,"hltBit[nHLTBit]/O");

    }
  */
  TH1D::SetDefaultSumw2();

  if (doLifeTimeTagging_) {
    /* clear arrays */
    memset(jets_.discr_csvV1, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_csvV2, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_muByIp3, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_muByPt, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_prob, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_probb, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_tcHighEff, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_tcHighPur, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_ssvHighEff, 0, MAXJETS * sizeof(float));
    memset(jets_.discr_ssvHighPur, 0, MAXJETS * sizeof(float));

    memset(jets_.ndiscr_ssvHighEff, 0, MAXJETS * sizeof(float));
    memset(jets_.ndiscr_ssvHighPur, 0, MAXJETS * sizeof(float));
    memset(jets_.ndiscr_csvV1, 0, MAXJETS * sizeof(float));
    memset(jets_.ndiscr_csvV2, 0, MAXJETS * sizeof(float));
    memset(jets_.ndiscr_muByPt, 0, MAXJETS * sizeof(float));

    memset(jets_.pdiscr_csvV1, 0, MAXJETS * sizeof(float));
    memset(jets_.pdiscr_csvV2, 0, MAXJETS * sizeof(float));

    memset(jets_.nsvtx, 0, MAXJETS * sizeof(int));
    memset(jets_.svtxntrk, 0, MAXJETS * sizeof(int));
    memset(jets_.svtxdl, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxdls, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxdl2d, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxdls2d, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxm, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxpt, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxmcorr, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxnormchi2, 0, MAXJETS * sizeof(float));
    memset(jets_.svJetDeltaR, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxTrkSumChi2, 0, MAXJETS * sizeof(float));
    memset(jets_.svtxTrkNetCharge, 0, MAXJETS * sizeof(int));
    memset(jets_.svtxNtrkInCone, 0, MAXJETS * sizeof(int));
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

  if(doHiJetID_ && !geo){
    edm::ESHandle<CaloGeometry> pGeo;
    iSetup.get<CaloGeometryRecord>().get(pGeo);
    geo = pGeo.product();
  }

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
  if(doGenSym_) {
    iEvent.getByToken(tokenGenSym_,genSymVM_);
    iEvent.getByToken(tokenGenDroppedBranches_,genDroppedBranchesVM_);
  }
  
  edm::Handle<reco::JetView> jets;
  iEvent.getByToken(jetTag_, jets);

  edm::Handle<reco::PFCandidateCollection> pfCandidates;
  iEvent.getByToken(pfCandidateLabel_,pfCandidates);

  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByToken(trackTag_,tracks);

  edm::Handle<reco::GenParticleCollection> genparts;
  iEvent.getByToken(genParticleSrc_,genparts);

  //Get all the b-tagging handles
  // Track Counting Taggers
  //------------------------------------------------------
  Handle<JetTagCollection> jetTags_TCHighEff;
  Handle<JetTagCollection> jetTags_TCHighPur;

  //------------------------------------------------------
  // Jet Probability tagger
  //------------------------------------------------------
  Handle<vector<TrackIPTagInfo> > tagInfo;
  Handle<JetTagCollection> jetTags_JP;
  Handle<JetTagCollection> jetTags_JB;

  //------------------------------------------------------
  // Secondary vertex taggers
  //------------------------------------------------------
  Handle<vector<SecondaryVertexTagInfo> > tagInfoSVx;
  Handle<vector<SecondaryVertexTagInfo> > tagInfoNegSVx;
  Handle<JetTagCollection> jetTags_SvtxHighEff;
  Handle<JetTagCollection> jetTags_negSvtxHighEff;
  Handle<JetTagCollection> jetTags_SvtxHighPur;
  Handle<JetTagCollection> jetTags_negSvtxHighPur;
  Handle<JetTagCollection> jetTags_CombinedSvtx;
  Handle<JetTagCollection> jetTags_negCombinedSvtx;
  Handle<JetTagCollection> jetTags_posCombinedSvtx;
  Handle<JetTagCollection> jetTags_CombinedSvtxV2;
  Handle<JetTagCollection> jetTags_negCombinedSvtxV2;
  Handle<JetTagCollection> jetTags_posCombinedSvtxV2;

  //------------------------------------------------------
  // Soft muon tagger
  //------------------------------------------------------

  //Handle<SoftLeptonTagInfoCollection> tagInos_softmuon;
  //Handle<JetTagCollection> jetTags_softMu;
  //Handle<JetTagCollection> jetTags_softMuneg;

  if(doLifeTimeTagging_){
    iEvent.getByToken(ImpactParameterTagInfos_, tagInfo);
    iEvent.getByToken(TrackCountingHighEffBJetTags_, jetTags_TCHighEff);
    iEvent.getByToken(TrackCountingHighPurBJetTags_, jetTags_TCHighPur);
    iEvent.getByToken(JetProbabilityBJetTags_, jetTags_JP);
    iEvent.getByToken(JetBProbabilityBJetTags_, jetTags_JB);
    iEvent.getByToken(SecondaryVertexTagInfos_, tagInfoSVx);
    iEvent.getByToken(SecondaryVertexNegativeTagInfos_, tagInfoNegSVx);
    iEvent.getByToken(SimpleSecondaryVertexHighEffBJetTags_, jetTags_SvtxHighEff);
    iEvent.getByToken(NegativeSimpleSecondaryVertexHighEffBJetTags_, jetTags_negSvtxHighEff);
    iEvent.getByToken(SimpleSecondaryVertexHighPurBJetTags_, jetTags_SvtxHighPur);
    iEvent.getByToken(NegativeSimpleSecondaryVertexHighEffBJetTags_, jetTags_negSvtxHighPur);
    iEvent.getByToken(CombinedSecondaryVertexBJetTags_, jetTags_CombinedSvtx);
    iEvent.getByToken(NegativeCombinedSecondaryVertexBJetTags_, jetTags_negCombinedSvtx);
    iEvent.getByToken(PositiveCombinedSecondaryVertexBJetTags_, jetTags_posCombinedSvtx);
    iEvent.getByToken(CombinedSecondaryVertexV2BJetTags_, jetTags_CombinedSvtxV2);
    iEvent.getByToken(NegativeCombinedSecondaryVertexV2BJetTags_, jetTags_negCombinedSvtxV2);
    iEvent.getByToken(PositiveCombinedSecondaryVertexV2BJetTags_, jetTags_posCombinedSvtxV2);
    //iEvent.getByToken(NegativeSoftPFMuonByPtBJetTags_, jetTags_softMuneg);
    //iEvent.getByToken(PositiveSoftPFMuonByPtBJetTags_, jetTags_softMu);
  }


  // get tower information
  edm::Handle<CaloTowerCollection> towers;
  if(doTower){
    iEvent.getByToken(TowerSrc_,towers);
  }

  // FILL JRA TREE
  jets_.b = b;
  jets_.nref = 0;

  if(doTrigger_){
    fillL1Bits(iEvent);
    fillHLTBits(iEvent);
  }

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
    if(TMath::Abs(jet.eta()) > jetAbsEtaMax_) continue;
    if (useJEC_ && usePat_){
      jets_.rawpt[jets_.nref]=(*patjets)[j].correctedJet("Uncorrected").pt();
    }

    math::XYZVector jetDir = jet.momentum().Unit();

    if(doLifeTimeTagging_){
      int ith_tagged =    this->TaggedJet(jet,jetTags_SvtxHighEff);
      if(ith_tagged >= 0){
	jets_.discr_ssvHighEff[jets_.nref] = (*jetTags_SvtxHighEff)[ith_tagged].second;
	const SecondaryVertexTagInfo &tagInfoSV = (*tagInfoSVx)[ith_tagged];
	jets_.nsvtx[jets_.nref]     = tagInfoSV.nVertices();

	if ( jets_.nsvtx[jets_.nref] > 0) {

	  jets_.svtxntrk[jets_.nref]  = tagInfoSV.nVertexTracks(0);
	  if(doExtraCTagging_) jets_.svJetDeltaR[jets_.nref] = reco::deltaR(tagInfoSV.flightDirection(0),jetDir);

	  // this is the 3d flight distance, for 2-D use (0,true)
	  Measurement1D m1D = tagInfoSV.flightDistance(0);
	  jets_.svtxdl[jets_.nref]    = m1D.value();
	  jets_.svtxdls[jets_.nref]   = m1D.significance();
	  Measurement1D m2D = tagInfoSV.flightDistance(0,true);
          jets_.svtxdl2d[jets_.nref] = m2D.value();
          jets_.svtxdls2d[jets_.nref] = m2D.significance();
          const Vertex& svtx = tagInfoSV.secondaryVertex(0);
	  
	  double svtxM = svtx.p4().mass();
          double svtxPt = svtx.p4().pt();
	  jets_.svtxm[jets_.nref]    = svtxM; 
	  jets_.svtxpt[jets_.nref]   = svtxPt;
	 
	  if(doExtraCTagging_){
	    double trkSumChi2=0;
	    int trkNetCharge=0;
	    int nTrkInCone=0;
	    int nsvtxtrks=0;
	    TrackRefVector svtxTracks = tagInfoSV.vertexTracks(0);
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
	    double sinth = svtx.p4().Vect().Unit().Cross(tagInfoSV.flightDirection(0).unit()).Mag2();
	    sinth = sqrt(sinth);
	    jets_.svtxmcorr[jets_.nref] = sqrt(pow(svtxM,2)+(pow(svtxPt,2)*pow(sinth,2)))+svtxPt*sinth;
	  }	
	  
	  if(svtx.ndof()>0)jets_.svtxnormchi2[jets_.nref]  = svtx.chi2()/svtx.ndof();
	}
      }
      ith_tagged    = this->TaggedJet(jet,jetTags_negSvtxHighEff);
      if(ith_tagged >= 0) jets_.ndiscr_ssvHighEff[jets_.nref]   = (*jetTags_negSvtxHighEff)[ith_tagged].second;
      ith_tagged    = this->TaggedJet(jet,jetTags_SvtxHighPur);
      if(ith_tagged >= 0) jets_.discr_ssvHighPur[jets_.nref]  = (*jetTags_SvtxHighPur)[ith_tagged].second;
      ith_tagged    = this->TaggedJet(jet,jetTags_negSvtxHighPur);
      if(ith_tagged >= 0) jets_.ndiscr_ssvHighPur[jets_.nref] = (*jetTags_negSvtxHighPur)[ith_tagged].second;

      ith_tagged          = this->TaggedJet(jet,jetTags_CombinedSvtx);
      if(ith_tagged >= 0) jets_.discr_csvV1[jets_.nref]  = (*jetTags_CombinedSvtx)[ith_tagged].second;
      ith_tagged          = this->TaggedJet(jet,jetTags_negCombinedSvtx);
      if(ith_tagged >= 0) jets_.ndiscr_csvV1[jets_.nref] = (*jetTags_negCombinedSvtx)[ith_tagged].second;
      ith_tagged  = this->TaggedJet(jet,jetTags_posCombinedSvtx);
      if(ith_tagged >= 0) jets_.pdiscr_csvV1[jets_.nref] = (*jetTags_posCombinedSvtx)[ith_tagged].second;

      ith_tagged          = this->TaggedJet(jet,jetTags_CombinedSvtxV2);
      if(ith_tagged >= 0) jets_.discr_csvV2[jets_.nref]  = (*jetTags_CombinedSvtxV2)[ith_tagged].second;
      ith_tagged          = this->TaggedJet(jet,jetTags_negCombinedSvtxV2);
      if(ith_tagged >= 0) jets_.ndiscr_csvV2[jets_.nref] = (*jetTags_negCombinedSvtxV2)[ith_tagged].second;
      ith_tagged  = this->TaggedJet(jet,jetTags_posCombinedSvtxV2);
      if(ith_tagged >= 0) jets_.pdiscr_csvV2[jets_.nref] = (*jetTags_posCombinedSvtxV2)[ith_tagged].second;

      if(ith_tagged >= 0){
	ith_tagged = this->TaggedJet(jet,jetTags_JP);
	jets_.discr_prob[jets_.nref]  = (*jetTags_JP)[ith_tagged].second;

	const TrackIPTagInfo& tagInfoIP= (*tagInfo)[ith_tagged];

	jets_.nIPtrk[jets_.nref] = tagInfoIP.tracks().size();
	jets_.nselIPtrk[jets_.nref] = tagInfoIP.selectedTracks().size();
	if (doLifeTimeTaggingExtras_) {

	  TrackRefVector selTracks=tagInfoIP.selectedTracks();

	  GlobalPoint pv(tagInfoIP.primaryVertex()->position().x(),tagInfoIP.primaryVertex()->position().y(),tagInfoIP.primaryVertex()->position().z());

  	  reco::TrackKinematics allKinematics;	 
 
	  for(int it=0;it<jets_.nselIPtrk[jets_.nref] ;it++){
	    jets_.ipJetIndex[jets_.nIP + it]= jets_.nref;
	    reco::btag::TrackIPData data = tagInfoIP.impactParameterData()[it];
	    jets_.ipPt[jets_.nIP + it] = selTracks[it]->pt();
	    jets_.ipEta[jets_.nIP + it] = selTracks[it]->eta();
	    jets_.ipDxy[jets_.nIP + it] = selTracks[it]->dxy(tagInfoIP.primaryVertex()->position());
	    jets_.ipDz[jets_.nIP + it] = selTracks[it]->dz(tagInfoIP.primaryVertex()->position());
	    jets_.ipChi2[jets_.nIP + it] = selTracks[it]->normalizedChi2();
	    jets_.ipNHit[jets_.nIP + it] = selTracks[it]->numberOfValidHits();
	    jets_.ipNHitPixel[jets_.nIP + it] = selTracks[it]->hitPattern().numberOfValidPixelHits();
	    jets_.ipNHitStrip[jets_.nIP + it] = selTracks[it]->hitPattern().numberOfValidStripHits();
	    jets_.ipIsHitL1[jets_.nIP + it]  = selTracks[it]->hitPattern().hasValidHitInPixelLayer(
		PixelSubdetector::SubDetector::PixelBarrel, 1);
	    jets_.ipProb0[jets_.nIP + it] = tagInfoIP.probabilities(0)[it];
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
	    jets_.trackSip2dSigAboveCharm[jets_.nref] = getAboveCharmThresh(selTracks, tagInfoIP, 1);
	    jets_.trackSip3dSigAboveCharm[jets_.nref] = getAboveCharmThresh(selTracks, tagInfoIP, 2);
	    jets_.trackSip2dValAboveCharm[jets_.nref] = getAboveCharmThresh(selTracks, tagInfoIP, 3);
	    jets_.trackSip3dValAboveCharm[jets_.nref] = getAboveCharmThresh(selTracks, tagInfoIP, 4);
	  }
	  jets_.nIP += jets_.nselIPtrk[jets_.nref];
	}
      }

      ith_tagged = this->TaggedJet(jet,jetTags_JB);
      if(ith_tagged >= 0) jets_.discr_probb[jets_.nref]  = (*jetTags_JB)[ith_tagged].second;

      ith_tagged    = this->TaggedJet(jet,jetTags_TCHighEff);
      if(ith_tagged >= 0) jets_.discr_tcHighEff[jets_.nref]   = (*jetTags_TCHighEff)[ith_tagged].second;
      ith_tagged    = this->TaggedJet(jet,jetTags_TCHighPur);
      if(ith_tagged >= 0) jets_.discr_tcHighPur[jets_.nref]   = (*jetTags_TCHighPur)[ith_tagged].second;

      //ith_tagged = this->TaggedJet(jet,jetTags_softMu);
      //if(ith_tagged >= 0){
      //  if ( (*jetTags_softMu)[ith_tagged].second     > -100000 )
      //    jets_.discr_muByPt[jets_.nref]  = (*jetTags_softMu)[ith_tagged].second;
      //}
      //ith_tagged = this->TaggedJet(jet,jetTags_softMuneg);
      //if(ith_tagged >= 0){
      //  float SoftMN = 0;
      //  if ( (*jetTags_softMuneg)[ith_tagged].second  > -100000 )
      //    SoftMN = ((*jetTags_softMuneg)[ith_tagged].second);
      //  if ( SoftMN > 0 ) SoftMN = -SoftMN;
      //  jets_.ndiscr_muByPt[jets_.nref] = SoftMN;
      //}

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
    //     if(etrk.quality(reco::TrackBase::qualityByName(qualityString_))) pev_.trkQual[pev_.nTrk]=1;

    if(doHiJetID_){

      // JetID Selections for 5 TeV PbPb
      // Cuts by Yen-Jie Lee, BDT by Kurt Jung
      double rawpt = jets_.rawpt[jets_.nref];
      float jtpt = jet.pt();
      int ijet = jets_.nref;
      jets_.discr_jetID_cuts[jets_.nref] = jets_.neutralMax[ijet]/rawpt*0.085 + 
					   jets_.photonMax[ijet]/rawpt*0.337 + 
					   jets_.chargedMax[ijet]/rawpt*0.584 + 
					   jets_.neutralSum[ijet]/rawpt*-0.454 + 
					   jets_.photonSum[ijet]/rawpt*-0.127 + 
					   jets_.chargedSum[ijet]/rawpt*(-0.239) + 
					   jets_.jtpu[ijet]/rawpt*(-0.184) + 0.173;
      //begin bdt - TMVA requires you to load in all input vars and names into separate containers (eyeroll)
      float tempVarAddr[] = {jets_.trackMax[ijet]/jtpt, jets_.trackHardSum[ijet]/jtpt, jets_.trackHardN[ijet]/jtpt, jets_.chargedN[ijet]/jtpt, jets_.chargedHardSum[ijet]/jtpt, jets_.chargedHardN[ijet]/jtpt, jets_.photonN[ijet]/jtpt, jets_.photonHardSum[ijet]/jtpt, jets_.photonHardN[ijet]/jtpt, jets_.neutralN[ijet]/jtpt, jets_.hcalSum[ijet]/jtpt, jets_.ecalSum[ijet]/jtpt, jets_.chargedMax[ijet]/jtpt, jets_.chargedSum[ijet], jets_.neutralMax[ijet]/jtpt, jets_.neutralSum[ijet]/jtpt, jets_.photonMax[ijet]/jtpt, jets_.photonSum[ijet]/jtpt, jets_.eSum[ijet]/jtpt, jets_.muSum[ijet]/jtpt};
      for(unsigned int ivar=0; ivar<(sizeof(tempVarAddr)/sizeof(tempVarAddr[0])); ivar++){ varAddr[ivar] = tempVarAddr[ivar]; }
      jets_.discr_jetID_bdt[jets_.nref] = reader->EvaluateMVA("BDTG");

      /////////////////////////////////////////////////////////////////
      // Jet core pt^2 discriminant for fake jets
      // Edited by Yue Shi Lai <ylai@mit.edu>

      // Initial value is 0
      jets_.discr_fr01[jets_.nref] = 0;
      // Start with no directional adaption, i.e. the fake rejection
      // axis is the jet axis
      float pseudorapidity_adapt = jets_.jteta[jets_.nref];
      float azimuth_adapt = jets_.jtphi[jets_.nref];

      // Unadapted discriminant with adaption search
      for (size_t iteration = 0; iteration < 2; iteration++) {
	float pseudorapidity_adapt_new = pseudorapidity_adapt;
	float azimuth_adapt_new = azimuth_adapt;
	float max_weighted_perp = 0;
	float perp_square_sum = 0;

	for (size_t index_pf_candidate = 0;
	     index_pf_candidate < pfCandidates->size();
	     index_pf_candidate++) {
	  const reco::PFCandidate &p =
	    (*pfCandidates)[index_pf_candidate];

	  switch (p.particleId()) {
	    //case 1:	// Charged hadron
	    //case 3:	// Muon
	  case 4:	// Photon
	    {
	      const float dpseudorapidity =
		p.eta() - pseudorapidity_adapt;
	      const float dazimuth =
		reco::deltaPhi(p.phi(), azimuth_adapt);
	      // The Gaussian scale factor is 0.5 / (0.1 * 0.1)
	      // = 50
	      const float angular_weight =
		exp(-50.0F * (dpseudorapidity * dpseudorapidity +
			      dazimuth * dazimuth));
	      const float weighted_perp =
		angular_weight * p.pt() * p.pt();
	      const float weighted_perp_square =
		weighted_perp * p.pt();

	      perp_square_sum += weighted_perp_square;
	      if (weighted_perp >= max_weighted_perp) {
		pseudorapidity_adapt_new = p.eta();
		azimuth_adapt_new = p.phi();
		max_weighted_perp = weighted_perp;
	      }
	    }
	  default:
	    break;
	  }
	}
	// Update the fake rejection value
	jets_.discr_fr01[jets_.nref] = std::max(
						jets_.discr_fr01[jets_.nref], perp_square_sum);
	// Update the directional adaption
	pseudorapidity_adapt = pseudorapidity_adapt_new;
	azimuth_adapt = azimuth_adapt_new;
      }
    }
    jets_.jtpt[jets_.nref] = jet.pt();
    jets_.jteta[jets_.nref] = jet.eta();
    jets_.jtphi[jets_.nref] = jet.phi();
    jets_.jty[jets_.nref] = jet.eta();
    jets_.jtpu[jets_.nref] = jet.pileup();
    jets_.jtm[jets_.nref] = jet.mass();
    jets_.jtarea[jets_.nref] = jet.jetArea();

    //! fill in the new jet varibles
    if(doNewJetVars_)
      fillNewJetVarsRecoJet(jet);

    jets_.jttau1[jets_.nref] = -999.;
    jets_.jttau2[jets_.nref] = -999.;
    jets_.jttau3[jets_.nref] = -999.;

    jets_.jtsym[jets_.nref] = -999.;
    jets_.jtdroppedBranches[jets_.nref] = -999;
    
    if(doSubJets_) analyzeSubjets(jet);

    if(usePat_){
      if( (*patjets)[j].hasUserFloat(jetName_+"Njettiness:tau1") )
        jets_.jttau1[jets_.nref] = (*patjets)[j].userFloat(jetName_+"Njettiness:tau1");
      if( (*patjets)[j].hasUserFloat(jetName_+"Njettiness:tau2") )
        jets_.jttau2[jets_.nref] = (*patjets)[j].userFloat(jetName_+"Njettiness:tau2");
      if( (*patjets)[j].hasUserFloat(jetName_+"Njettiness:tau3") )
        jets_.jttau3[jets_.nref] = (*patjets)[j].userFloat(jetName_+"Njettiness:tau3");

      if( (*patjets)[j].hasUserFloat(jetName_+"Jets:sym") )
        jets_.jtsym[jets_.nref] = (*patjets)[j].userFloat(jetName_+"Jets:sym");
      //std::cout << "jets_.nref: " << jets_.nref << "  jtsym: " << jets_.jtsym[jets_.nref] << endl;
      if( (*patjets)[j].hasUserInt(jetName_+"Jets:droppedBranches") )
        jets_.jtdroppedBranches[jets_.nref] = (*patjets)[j].userInt(jetName_+"Jets:droppedBranches");

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
      } else {
        jets_.jtPfCHF[jets_.nref] = 0;
        jets_.jtPfNHF[jets_.nref] = 0;
        jets_.jtPfCEF[jets_.nref] = 0;
        jets_.jtPfNEF[jets_.nref] = 0;
        jets_.jtPfMUF[jets_.nref] = 0;

        jets_.jtPfCHM[jets_.nref] = 0;
        jets_.jtPfNHM[jets_.nref] = 0;
        jets_.jtPfCEM[jets_.nref] = 0;
        jets_.jtPfNEM[jets_.nref] = 0;
        jets_.jtPfMUM[jets_.nref] = 0;
      }
        
      if(doStandardJetID_){
	jets_.fHPD[jets_.nref] = (*patjets)[j].jetID().fHPD;
	jets_.fRBX[jets_.nref] = (*patjets)[j].jetID().fRBX;
	jets_.n90[jets_.nref] = (*patjets)[j].n90();

	jets_.fSubDet1[jets_.nref] = (*patjets)[j].jetID().fSubDetector1;
	jets_.fSubDet2[jets_.nref] = (*patjets)[j].jetID().fSubDetector2;
	jets_.fSubDet3[jets_.nref] = (*patjets)[j].jetID().fSubDetector3;
	jets_.fSubDet4[jets_.nref] = (*patjets)[j].jetID().fSubDetector4;
	jets_.restrictedEMF[jets_.nref] = (*patjets)[j].jetID().restrictedEMF;
	jets_.nHCAL[jets_.nref] = (*patjets)[j].jetID().nHCALTowers;
	jets_.nECAL[jets_.nref] = (*patjets)[j].jetID().nECALTowers;
	jets_.apprHPD[jets_.nref] = (*patjets)[j].jetID().approximatefHPD;
	jets_.apprRBX[jets_.nref] = (*patjets)[j].jetID().approximatefRBX;

	//       jets_.n90[jets_.nref] = (*patjets)[j].jetID().hitsInN90;
	jets_.n2RPC[jets_.nref] = (*patjets)[j].jetID().numberOfHits2RPC;
	jets_.n3RPC[jets_.nref] = (*patjets)[j].jetID().numberOfHits3RPC;
	jets_.nRPC[jets_.nref] = (*patjets)[j].jetID().numberOfHitsRPC;

	jets_.fEB[jets_.nref] = (*patjets)[j].jetID().fEB;
	jets_.fEE[jets_.nref] = (*patjets)[j].jetID().fEE;
	jets_.fHB[jets_.nref] = (*patjets)[j].jetID().fHB;
	jets_.fHE[jets_.nref] = (*patjets)[j].jetID().fHE;
	jets_.fHO[jets_.nref] = (*patjets)[j].jetID().fHO;
	jets_.fLong[jets_.nref] = (*patjets)[j].jetID().fLong;
	jets_.fShort[jets_.nref] = (*patjets)[j].jetID().fShort;
	jets_.fLS[jets_.nref] = (*patjets)[j].jetID().fLS;
	jets_.fHFOOT[jets_.nref] = (*patjets)[j].jetID().fHFOOT;
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

	if(doNewJetVars_)
	  fillNewJetVarsRefJet(*genjet);
	
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

	if(doNewJetVars_){
	  jets_.refnCands[jets_.nref] = -999;
	  jets_.refnChCands[jets_.nref] = -999;
	  jets_.refnNeCands[jets_.nref] = -999;
	  jets_.refchargedSumConst[jets_.nref] = -999;
	  jets_.refchargedNConst  [jets_.nref] = -999;  
	  jets_.refeSumConst      [jets_.nref] = -999;  
	  jets_.refeNConst        [jets_.nref] = -999;  
	  jets_.refmuSumConst     [jets_.nref] = -999;  
	  jets_.refmuNConst       [jets_.nref] = -999;  
	  jets_.refphotonSumConst [jets_.nref] = -999; 
	  jets_.refphotonNConst   [jets_.nref] = -999;  
	  jets_.refneutralSumConst[jets_.nref] = -999;
	  jets_.refneutralNConst  [jets_.nref] = -999;  
	  jets_.refMByPt[jets_.nref] = -999.;
	  jets_.refRMSCand[jets_.nref] = -999.;
	  jets_.refAxis1[jets_.nref] = -999.;
	  jets_.refAxis2[jets_.nref] = -999.;
	  jets_.refSigma[jets_.nref] = -999.;
	  jets_.refrm3[jets_.nref] = -999.;
	  jets_.refrm2[jets_.nref] = -999.;
	  jets_.refrm1[jets_.nref] = -999.;
	  jets_.refrm0p5[jets_.nref] = -999.;
	  jets_.refR[jets_.nref] = -999.;
	  jets_.refpull[jets_.nref] = -999.;
	  jets_.refpTD[jets_.nref] = -999.;
	  jets_.refSDm[jets_.nref] = -999;
	  jets_.refSDpt[jets_.nref] = -999;
	  jets_.refSDeta[jets_.nref] = -999;
	  jets_.refSDphi[jets_.nref] = -999;
	  jets_.refSDptFrac[jets_.nref] = -999;
	  jets_.refSDrm0p5[jets_.nref] = -999;
	  jets_.refSDrm1[jets_.nref] = -999;
	  jets_.refSDrm2[jets_.nref] = -999;
	  jets_.refSDrm3[jets_.nref] = -999;

	  jets_.refTbeta20p2[jets_.nref] = -999; 
	  jets_.refTbeta20p3[jets_.nref] = -999; 
	  jets_.refTbeta20p4[jets_.nref] = -999; 
	  jets_.refTbeta20p5[jets_.nref] = -999; 

	  jets_.refTbeta30p2[jets_.nref] = -999; 
	  jets_.refTbeta30p3[jets_.nref] = -999; 
	  jets_.refTbeta30p4[jets_.nref] = -999; 
	  jets_.refTbeta30p5[jets_.nref] = -999; 
			       
	  jets_.refCbeta20p2[jets_.nref] = -999; 
	  jets_.refCbeta20p3[jets_.nref] = -999; 
	  jets_.refCbeta20p4[jets_.nref] = -999; 
	  jets_.refCbeta20p5[jets_.nref] = -999; 

	  jets_.refZ11[jets_.nref] = -999;
	  jets_.refZ20[jets_.nref] = -999;
	  jets_.refZ22[jets_.nref] = -999;
	  jets_.refZ31[jets_.nref] = -999;
	  jets_.refZ33[jets_.nref] = -999;
	  jets_.refZ40[jets_.nref] = -999;
	  jets_.refZ42[jets_.nref] = -999;
	  jets_.refZ44[jets_.nref] = -999;
	  jets_.refZ51[jets_.nref] = -999;
	  jets_.refZ53[jets_.nref] = -999;
	  jets_.refZ55[jets_.nref] = -999;


	  jets_.refPhi1[jets_.nref] = -999;
	  jets_.refPhi2[jets_.nref] = -999;
	  jets_.refPhi3[jets_.nref] = -999;
	  jets_.refPhi4[jets_.nref] = -999;
	  jets_.refPhi5[jets_.nref] = -999;
	  jets_.refPhi6[jets_.nref] = -999;
	  jets_.refPhi7[jets_.nref] = -999;

	  jets_.refSkx[jets_.nref] = -999;
	  jets_.refSky[jets_.nref] = -999;
	}
	
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
          jets_.refsym[jets_.nref]  = -999.;
          jets_.refdroppedBranches[jets_.nref]  = -999;
          
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
      
      jets_.refparton_flavorForB[jets_.nref] = (*patjets)[j].partonFlavour();
      // matched partons
      const reco::GenParticle & parton = *(*patjets)[j].genParton();

      if((*patjets)[j].genParton()){
	jets_.refparton_pt[jets_.nref] = parton.pt();
	jets_.refparton_flavor[jets_.nref] = parton.pdgId();

	if(saveBfragments_ && abs(jets_.refparton_flavorForB[jets_.nref])==5){

	  usedStringPts.clear();

	  // uncomment this if you want to know the ugly truth about parton matching -matt
	  //if(jet.pt() > 50 &&abs(parton.pdgId())!=5 && parton.pdgId()!=21)
	  // cout<<" Identified as a b, but doesn't match b or gluon, id = "<<parton.pdgId()<<endl;

	  jets_.bJetIndex[jets_.bMult] = jets_.nref;
	  jets_.bStatus[jets_.bMult] = parton.status();
	  jets_.bVx[jets_.bMult] = parton.vx();
	  jets_.bVy[jets_.bMult] = parton.vy();
	  jets_.bVz[jets_.bMult] = parton.vz();
	  jets_.bPt[jets_.bMult] = parton.pt();
	  jets_.bEta[jets_.bMult] = parton.eta();
	  jets_.bPhi[jets_.bMult] = parton.phi();
	  jets_.bPdg[jets_.bMult] = parton.pdgId();
	  jets_.bChg[jets_.bMult] = parton.charge();
	  jets_.bMult++;
	  saveDaughters(parton);
	}
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
    
    edm::Handle<GenEventInfoProduct> hEventInfo;
    iEvent.getByToken(eventGenInfoTag_,hEventInfo);
    //jets_.pthat = hEventInfo->binningValues()[0];

    // binning values and qscale appear to be equivalent, but binning values not always present
    jets_.pthat = hEventInfo->qScale();

    //edm::Handle<vector<reco::GenJet> >genjets;
    edm::Handle<edm::View<reco::GenJet>> genjets;
    iEvent.getByToken(genjetTag_, genjets);

    //get gen-level n-jettiness
    edm::Handle<edm::ValueMap<float> > genTau1s;
    edm::Handle<edm::ValueMap<float> > genTau2s;
    edm::Handle<edm::ValueMap<float> > genTau3s;
    if(doGenTaus_) {
      iEvent.getByToken(tokenGenTau1_,genTau1s);
      iEvent.getByToken(tokenGenTau2_,genTau2s);
      iEvent.getByToken(tokenGenTau3_,genTau3s);
    }
    
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
      float tau3 =  -999.;
      Ptr<reco::GenJet> genJetPtr = genjets->ptrAt(igen);
      if(doGenTaus_) {
        tau1 = (*genTau1s)[genJetPtr];
        tau2 = (*genTau2s)[genJetPtr];
        tau3 = (*genTau3s)[genJetPtr];
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

      // threshold to reduce size of output in minbias PbPb
      if(genjet_pt>genPtMin_){
	jets_.genpt [jets_.ngen] = genjet_pt;
	jets_.geneta[jets_.ngen] = genjet.eta();
	jets_.genphi[jets_.ngen] = genjet.phi();
        jets_.genm  [jets_.ngen] = genjet.mass();
	jets_.geny  [jets_.ngen] = genjet.eta();

	if(doNewJetVars_)
	  fillNewJetVarsGenJet(genjet);      

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


//--------------------------------------------------------------------------------------------------
void HiInclusiveJetAnalyzer::fillL1Bits(const edm::Event &iEvent)
{
  edm::Handle< L1GlobalTriggerReadoutRecord >  L1GlobalTrigger;

  iEvent.getByToken(L1gtReadout_, L1GlobalTrigger);
  const TechnicalTriggerWord&  technicalTriggerWordBeforeMask = L1GlobalTrigger->technicalTriggerWord();

  for (int i=0; i<64;i++)
    {
      jets_.l1TBit[i] = technicalTriggerWordBeforeMask.at(i);
    }
  jets_.nL1TBit = 64;

  int ntrigs = L1GlobalTrigger->decisionWord().size();
  jets_.nL1ABit = ntrigs;

  for (int i=0; i != ntrigs; i++) {
    bool accept = L1GlobalTrigger->decisionWord()[i];
    //jets_.l1ABit[i] = (accept == true)? 1:0;
    if(accept== true){
      jets_.l1ABit[i] = 1;
    }
    else{
      jets_.l1ABit[i] = 0;
    }

  }
}

//--------------------------------------------------------------------------------------------------
void HiInclusiveJetAnalyzer::fillHLTBits(const edm::Event &iEvent)
{
  // Fill HLT trigger bits.
  Handle<TriggerResults> triggerResultsHLT;
  iEvent.getByToken(hltResName_, triggerResultsHLT);

  const TriggerResults *hltResults = triggerResultsHLT.product();
  const TriggerNames & triggerNames = iEvent.triggerNames(*hltResults);

  jets_.nHLTBit = hltTrgNames_.size();

  for(size_t i=0;i<hltTrgNames_.size();i++){

    for(size_t j=0;j<triggerNames.size();++j) {

      if(triggerNames.triggerName(j) == hltTrgNames_[i]){

	//cout <<"hltTrgNames_(i) "<<hltTrgNames_[i]<<endl;
	//cout <<"triggerName(j) "<<triggerNames.triggerName(j)<<endl;
	//cout<<" result "<<triggerResultsHLT->accept(j)<<endl;
	jets_.hltBit[i] = triggerResultsHLT->accept(j);
      }

    }
  }
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

// Recursive function, but this version gets called only the first time
void
HiInclusiveJetAnalyzer::saveDaughters(const reco::GenParticle &gen){

  for(unsigned i=0;i<gen.numberOfDaughters();i++){
    const reco::Candidate & daughter = *gen.daughter(i);
    double daughterPt = daughter.pt();
    if(daughterPt<1.) continue;
    double daughterEta = daughter.eta();
    if(fabs(daughterEta)>3.) continue;
    int daughterPdgId = daughter.pdgId();
    int daughterStatus = daughter.status();
    // Special case when b->b+string, both b and string contain all daughters, so only take the string
    if(gen.pdgId()==daughterPdgId && gen.status()==3 && daughterStatus==2) continue;

    // cheesy way of finding strings which were already used
    if(daughter.pdgId()==92){
      for(unsigned ist=0;ist<usedStringPts.size();ist++){
	if(fabs(daughter.pt() - usedStringPts[ist]) < 0.0001) return;
      }
      usedStringPts.push_back(daughter.pt());
    }
    jets_.bJetIndex[jets_.bMult] = jets_.nref;
    jets_.bStatus[jets_.bMult] = daughterStatus;
    jets_.bVx[jets_.bMult] = daughter.vx();
    jets_.bVy[jets_.bMult] = daughter.vy();
    jets_.bVz[jets_.bMult] = daughter.vz();
    jets_.bPt[jets_.bMult] = daughterPt;
    jets_.bEta[jets_.bMult] = daughterEta;
    jets_.bPhi[jets_.bMult] = daughter.phi();
    jets_.bPdg[jets_.bMult] = daughterPdgId;
    jets_.bChg[jets_.bMult] = daughter.charge();
    jets_.bMult++;
    saveDaughters(daughter);
  }
}

// This version called for all subsequent calls
void
HiInclusiveJetAnalyzer::saveDaughters(const reco::Candidate &gen){

  for(unsigned i=0;i<gen.numberOfDaughters();i++){
    const reco::Candidate & daughter = *gen.daughter(i);
    double daughterPt = daughter.pt();
    if(daughterPt<1.) continue;
    double daughterEta = daughter.eta();
    if(fabs(daughterEta)>3.) continue;
    int daughterPdgId = daughter.pdgId();
    int daughterStatus = daughter.status();
    // Special case when b->b+string, both b and string contain all daughters, so only take the string
    if(gen.pdgId()==daughterPdgId && gen.status()==3 && daughterStatus==2) continue;

    // cheesy way of finding strings which were already used
    if(daughter.pdgId()==92){
      for(unsigned ist=0;ist<usedStringPts.size();ist++){
	if(fabs(daughter.pt() - usedStringPts[ist]) < 0.0001) return;
      }
      usedStringPts.push_back(daughter.pt());
    }

    jets_.bJetIndex[jets_.bMult] = jets_.nref;
    jets_.bStatus[jets_.bMult] = daughterStatus;
    jets_.bVx[jets_.bMult] = daughter.vx();
    jets_.bVy[jets_.bMult] = daughter.vy();
    jets_.bVz[jets_.bMult] = daughter.vz();
    jets_.bPt[jets_.bMult] = daughterPt;
    jets_.bEta[jets_.bMult] = daughterEta;
    jets_.bPhi[jets_.bMult] = daughter.phi();
    jets_.bPdg[jets_.bMult] = daughterPdgId;
    jets_.bChg[jets_.bMult] = daughter.charge();
    jets_.bMult++;
    saveDaughters(daughter);
  }
}

double HiInclusiveJetAnalyzer::getEt(math::XYZPoint pos, double energy){
  double et = energy*sin(pos.theta());
  return et;
}

math::XYZPoint HiInclusiveJetAnalyzer::getPosition(const DetId &id, reco::Vertex::Point vtx){
  const GlobalPoint& pos=geo->getPosition(id);
  math::XYZPoint posV(pos.x() - vtx.x(),pos.y() - vtx.y(),pos.z() - vtx.z());
  return posV;
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
void HiInclusiveJetAnalyzer::analyzeSubjets(const reco::Jet jet) {

  std::vector<float> sjpt;
  std::vector<float> sjeta;
  std::vector<float> sjphi;
  std::vector<float> sjm;
  if(jet.numberOfDaughters()>0) {
    for (unsigned k = 0; k < jet.numberOfDaughters(); ++k) {
      const reco::Candidate & dp = *jet.daughter(k);
      sjpt.push_back(dp.pt());
      sjeta.push_back(dp.eta());
      sjphi.push_back(dp.phi());
      sjm.push_back(dp.mass());
    }
  } else {
    sjpt.push_back(-999.);
    sjeta.push_back(-999.);
    sjphi.push_back(-999.);
    sjm.push_back(-999.);
  }
  jets_.jtSubJetPt.push_back(sjpt);
  jets_.jtSubJetEta.push_back(sjeta);
  jets_.jtSubJetPhi.push_back(sjphi);
  jets_.jtSubJetM.push_back(sjm);
  
}


//--------------------------------------------------------------------------------------------------
void HiInclusiveJetAnalyzer::fillNewJetVarsRecoJet(const reco::Jet jet){

  int nCands = 0;
  int nChCands = 0;
  int nNeCands = 0;

  float jetMByPt = (jet.mass()>0 && jet.pt()!=0) ? jet.mass()/jet.pt() : -999;

  float tot_wt=0;
      
  float RMSCand = 0.0;
  float rmscand_n=0;
  float rmscand_d=0;
      
  float M11=0,M22=0,M12=0,M21=0;
  float Axis1 = 0.0;
  float Axis2 = 0.0;
  float Sigma = 0.0;
      
  float maxCandPt=-999;
  float sumCandPt=0;
  float sumCandPtSq=0;
  float R = 0.0;
  float pTD = 0.0;

  float rm0p5 = 0.0;
  float rm1 = 0.0;
  float rm2 = 0.0;
  float rm3 = 0.0;
      
  TVector2 t_Vect(0,0);
  TVector2 r(0,0);
  float pull = 0.0;

  float sd_m = 0.0;
  float sd_pt = 0.0;
  float sd_eta = 0.0;
  float sd_phi = 0.0;
  float sd_ptfrac = 0.0;
  float sd_rm0p5 = 0.0;
  float sd_rm1 = 0.0;
  float sd_rm2 = 0.0;
  float sd_rm3 = 0.0;

  float Tbeta20p2 = 0.0;
  float Tbeta20p3 = 0.0;
  float Tbeta20p4 = 0.0;
  float Tbeta20p5 = 0.0;

  float Tbeta30p2 = 0.0;
  float Tbeta30p3 = 0.0;
  float Tbeta30p4 = 0.0;
  float Tbeta30p5 = 0.0;

  //! Double ratio of the moments
  //!  Cbeta2 = (Tbeta3 * Tbeta0)/pow(Tbeta2,2);
  //! Tbeta0 = sumpT_{i};
  float Cbeta20p2 = 0.0;
  float Cbeta20p3 = 0.0;
  float Cbeta20p4 = 0.0;
  float Cbeta20p5 = 0.0;

  // //! Moments shifted to centriod
  float Mu00=0.0, Mu01=0.0, Mu10=0.0, Mu11=0.0;
  float Mu20=0.0, Mu02=0.0, Mu12=0.0, Mu21=0.0;
  float Mu30=0.0, Mu03=0.0;

  float Phi1 = 0.0;
  float Phi2 = 0.0;
  float Phi3 = 0.0;
  float Phi4 = 0.0;
  float Phi5 = 0.0;
  float Phi6 = 0.0;
  float Phi7 = 0.0;

  float Skx=0.0;
  float Sky=0.0;

  float Z11=0.0;
  float Z20=0.0;
  float Z22=0.0;
  float Z31=0.0;
  float Z33=0.0;
  float Z40=0.0;
  float Z42=0.0;
  float Z44=0.0;
  float Z51=0.0;
  float Z53=0.0;
  float Z55=0.0;

  TVector2 tmp_Z11(0,0);
  TVector2 tmp_Z20(0,0);
  TVector2 tmp_Z22(0,0);
  TVector2 tmp_Z31(0,0);
  TVector2 tmp_Z33(0,0);
  TVector2 tmp_Z40(0,0);
  TVector2 tmp_Z42(0,0);
  TVector2 tmp_Z44(0,0);
  TVector2 tmp_Z51(0,0);
  TVector2 tmp_Z53(0,0);
  TVector2 tmp_Z55(0,0);

  
  vector<fastjet::PseudoJet> jetconsts;
  std::vector<int>   jcid;
  std::vector<float> jcE;
  std::vector<float> jcpt;
  std::vector<float> jceta;
  std::vector<float> jcphi;
  std::vector<float> jcm;
  std::vector<int>   jcSDid;
  std::vector<float> jcSDE;
  std::vector<float> jcSDpt;
  std::vector<float> jcSDeta;
  std::vector<float> jcSDphi;
  std::vector<float> jcSDm;

  float chargedSumConst = 0;
  int   chargedNConst = 0;
  float eSumConst = 0;
  int   eNConst = 0;
  float muSumConst = 0;
  int   muNConst = 0;
  float photonSumConst = 0;
  int   photonNConst = 0;
  float neutralSumConst = 0;
  int   neutralNConst = 0;
  float hfhadSumConst = 0;
  int   hfhadNConst = 0;
  float hfemSumConst = 0;
  int   hfemNConst = 0;
  if(jet.numberOfDaughters()>0) {
    nCands = jet.numberOfDaughters();
    for (unsigned k = 0; k < jet.numberOfDaughters(); ++k) {
      const reco::Candidate & dp = *jet.daughter(k);
      if(dp.charge() == 0){
	nNeCands++;
      }else{
	nChCands++;
      }

      float ptcand = dp.pt();
      int pfid     = dp.pdgId();

      switch(std::abs(pfid)){
      case 211:  //PFCandidate::h charged hadron
      case 321:
      case 2212:
	chargedSumConst += ptcand;
	chargedNConst++;
	break;
      case 11:  //PFCandidate::e // electron
	eSumConst += ptcand;
	eNConst++;
	break;
      case 13: //PFCandidate::mu // muon
	muSumConst += ptcand;
	muNConst++;
	break;
      case 22: //PFCandidate:gamma // gamma
	photonSumConst += ptcand;
	photonNConst++;
	break;
      case 130:  //PFCandidate::h0 //Neutral hadron
      case 2112:
	neutralSumConst += ptcand;
	neutralNConst++;
	break;
      case 1:  //PFCandidate::h_HF //hadron in HF
	hfhadSumConst += ptcand; 
	hfhadNConst++;
      case 2:  //PFCandidate::egamma_HF //electromagnetic in HF
	hfemSumConst += ptcand; 
	hfemNConst++;
      default:
	break;
      }

      if( dp.pt() > maxCandPt )	maxCandPt=dp.pt();
      sumCandPt   += dp.pt();
      sumCandPtSq += pow(dp.pt(),2);
	
      float wt = pow(dp.pt(),2);
      tot_wt += wt;
	
      //! RMSCand
      float deta = dp.eta()- jet.eta();
      float dphi = deltaPhi(dp.phi(), jet.phi());
      float dr = deltaR(dp.eta(), dp.phi(), jet.eta(), jet.phi());
      rmscand_n += wt*dr*dr;
      rmscand_d += wt; 
	
      M11 += wt*deta*deta;
      M22 += wt*dphi*dphi;
      M12 += wt*deta*dphi;
      M21 += wt*deta*dphi;
	
      //! Pull
      TLorentzVector pfvec;
      pfvec.SetPtEtaPhiE(dp.pt(), dp.eta(), dp.phi(), dp.energy());
      fastjet::PseudoJet jc = fastjet::PseudoJet(dp.px(), dp.py(), dp.pz(), dp.energy());
      jc.set_user_info(new ExtraInfo(dp.pdgId()));
      jetconsts.push_back(jc);

      jcid.push_back(dp.pdgId());
      jcE.push_back(jc.e());
      jcpt.push_back(jc.pt());
      jcphi.push_back(jc.phi_std());
      jceta.push_back(jc.eta());
      jcm.push_back(jc.m());
      
      float pfy = pfvec.Rapidity();
      float dy = pfy - jet.y();
      r.Set( dy, dphi );
      float r_mag = r.Mod();
      t_Vect += ( dp.pt() /  jet.pt() ) * r_mag *r;

      rm0p5+=(dp.pt()*pow(dr,0.5))/jet.pt();
      rm1+=(dp.pt()*pow(dr,1))/jet.pt();
      rm2+=(dp.pt()*pow(dr,2))/jet.pt();
      rm3+=(dp.pt()*pow(dr,3))/jet.pt();      


      //! Added by Pawan ZM 
      tmp_Z11 += ( ( dp.pt() /  jet.pt() ) * r_mag * r );

      tmp_Z20 += ( ( dp.pt() /  jet.pt() ) * (2.*r_mag*r_mag - 1) * r );
      tmp_Z22 += ( ( dp.pt() /  jet.pt() ) * r_mag * r_mag * r);

      tmp_Z31 += ( ( dp.pt() /  jet.pt() ) * ( (3. * r_mag * r_mag * r_mag) - 2.*r_mag ) * r );
      tmp_Z33 += ( ( dp.pt() /  jet.pt() ) * r_mag * r_mag * r_mag * r );

      tmp_Z40 += ( ( dp.pt() /  jet.pt() ) * ( 6.*pow(r_mag,4) - 6.*pow(r_mag,2) + 1 ) * r );
      tmp_Z42 += ( ( dp.pt() /  jet.pt() ) * ( 4.*pow(r_mag,4) - 3.*pow(r_mag,2)) * r );
      tmp_Z44 += ( ( dp.pt() /  jet.pt() ) * pow(r_mag,4) * r);

      tmp_Z51 += ( ( dp.pt() /  jet.pt() ) * ( 10.*pow(r_mag,5) - 12.*pow(r_mag,3) + 3.*r_mag ) * r );
      tmp_Z53 += ( ( dp.pt() /  jet.pt() ) * ( 5.*pow(r_mag,5) - 4.*pow(r_mag,3)) * r );
      tmp_Z55 += ( ( dp.pt() /  jet.pt() ) * pow(r_mag,5) * r );


      //! For two-point moment
      for (unsigned l = k+1; l < jet.numberOfDaughters(); ++l) {
        const reco::Candidate & dl = *jet.daughter(l);
        float dr_kl = deltaR(dl.eta(), dl.phi(), dp.eta(), dp.phi());
	
        Tbeta20p2 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.2) );
        Tbeta20p3 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.3) );
        Tbeta20p4 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.4) );
        Tbeta20p5 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.5) );

	//! For three-point moment
	for (unsigned m = l+1; m < jet.numberOfDaughters(); ++m) {
	  const reco::Candidate & dm = *jet.daughter(m);
	  float dr_km = deltaR(dm.eta(), dm.phi(), dp.eta(), dp.phi());
	  float dr_lm = deltaR(dm.eta(), dm.phi(), dl.eta(), dl.phi());
	  
	  Tbeta30p2 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.2) );
	  Tbeta30p3 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.3) );
	  Tbeta30p4 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.4) );
	  Tbeta30p5 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.5) );
	}
      }

      //! Hu Moment Calculation 
      Mu00 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu01 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));
      Mu10 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu11 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));

      Mu20 += (pow(dp.eta()-jet.eta(),2)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu02 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),2)*(dp.pt()/jet.pt()));
      Mu12 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),2)*(dp.pt()/jet.pt()));
      Mu21 += (pow(dp.eta()-jet.eta(),2)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));

      Mu30 += (pow(dp.eta()-jet.eta(),3)*pow(dp.eta()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu03 += (pow(dp.eta()-jet.eta(),0)*pow(dp.eta()-jet.phi(),3)*(dp.pt()/jet.pt()));
    }
  }
  fastjet::JetDefinition jetDef(fastjet::antikt_algorithm, 999);
  fastjet::ClusterSequence thisClustering_basic(jetconsts, jetDef);
  std::vector<fastjet::PseudoJet> out_jets_basic = thisClustering_basic.inclusive_jets(0);
  if(out_jets_basic.size() == 1){ 
    fastjet::contrib::RecursiveSymmetryCutBase::SymmetryMeasure  symmetry_measure = fastjet::contrib::RecursiveSymmetryCutBase::scalar_z;
    fastjet::contrib::SoftDrop sd(0, 0.1, symmetry_measure, rParam);
    fastjet::PseudoJet sd_jet = sd(out_jets_basic[0]);
    if(sd_jet != 0){
      sd_m = sd_jet.m();
      sd_pt = sd_jet.pt();
      sd_eta = sd_jet.eta();
      sd_phi = sd_jet.phi();
      sd_ptfrac = sd_jet.pt()/jet.pt();    
      std::vector<fastjet::PseudoJet> sd_jetconsts = sd_jet.constituents();
      if(sd_jetconsts.size()!=0){
	for (unsigned k = 0; k < sd_jetconsts.size(); ++k) {
	  const fastjet::PseudoJet dp = sd_jetconsts.at(k);
	  jcSDid.push_back(dp.user_info<ExtraInfo>().part_id());
	  jcSDE.push_back(dp.e());
	  jcSDpt.push_back(dp.pt());
	  jcSDphi.push_back(dp.phi());
	  jcSDeta.push_back(dp.eta());
	  jcSDm.push_back(dp.m());
	  float dr = deltaR(dp.eta(), dp.phi(), jet.eta(), jet.phi());
	  sd_rm0p5+=(dp.pt()*pow(dr,0.5))/sd_jet.pt();
	  sd_rm1+=(dp.pt()*pow(dr,1))/sd_jet.pt();
	  sd_rm2+=(dp.pt()*pow(dr,2))/sd_jet.pt();
	  sd_rm3+=(dp.pt()*pow(dr,3))/sd_jet.pt();
	}
      }
    }
  }

  RMSCand = (rmscand_d > 0 ) ? sqrt ( rmscand_n / rmscand_d ) : -999;
      
  M12 = -1.*M12;
  M21 = -1.*M21;
      
  //! eign values
  float trace = M11 + M22;
  float detrm = (M11*M22) - (M12*M21);
      
  float lam1 = trace/2. + sqrt( pow(trace,2)/4. - detrm );
  float lam2 = trace/2. - sqrt( pow(trace,2)/4. - detrm );
      
  Axis1 = (tot_wt > 0 && lam1 >= 0) ? sqrt( lam1 / tot_wt ) : -999;
  Axis2 = (tot_wt > 0 && lam2 >=0 ) ? sqrt( lam2 / tot_wt ) : -999;
  
  Sigma = (tot_wt > 0 ) ? sqrt( pow(Axis1,2) + pow(Axis2,2) ) : -999;
      
  R = (sumCandPt > 0 ) ? maxCandPt / sumCandPt : -999;
      
  pTD = (sumCandPt > 0 ) ? sqrt( sumCandPtSq ) / sumCandPt : -999;
  
  pull = t_Vect.Mod();



  Tbeta20p2 /= pow(jet.pt(),2); 
  Tbeta20p3 /= pow(jet.pt(),2); 
  Tbeta20p4 /= pow(jet.pt(),2); 
  Tbeta20p5 /= pow(jet.pt(),2); 

  Tbeta30p2 /= pow(jet.pt(),3); 
  Tbeta30p3 /= pow(jet.pt(),3); 
  Tbeta30p4 /= pow(jet.pt(),3); 
  Tbeta30p5 /= pow(jet.pt(),3); 

  Cbeta20p2 = ( Tbeta20p2 > 0 ) ? Tbeta30p2 / Tbeta20p2 : -999;
  Cbeta20p3 = ( Tbeta20p3 > 0 ) ? Tbeta30p3 / Tbeta20p3 : -999;
  Cbeta20p4 = ( Tbeta20p4 > 0 ) ? Tbeta30p4 / Tbeta20p4 : -999;
  Cbeta20p5 = ( Tbeta20p5 > 0 ) ? Tbeta30p5 / Tbeta20p5 : -999;

  //! Hu Moments
  float Eta02 = Mu20/pow(Mu00,(0+2+1));
  float Eta20 = Mu20/pow(Mu00,(2+0+1));
  float Eta11 = Mu11/pow(Mu00,(1+1+1));
  float Eta12 = Mu12/pow(Mu00,(1+2+1));
  float Eta21 = Mu21/pow(Mu00,(2+1+1));
  float Eta03 = Mu03/pow(Mu00,(0+3+1));
  float Eta30 = Mu30/pow(Mu00,(3+0+1));
  
  if( Mu00 > 0 ){
    Phi1 = (Eta20 + Eta02);
    Phi2 = pow((Eta20 - Eta02),2) + 4.*pow(Eta11,2);
    Phi3 = pow((Eta30 - 3.*Eta12),2) + pow((3.*Eta21 - Eta03),2);
    Phi4 = pow((Eta30 + Eta12),2) + pow((Eta21 + Eta03),2);
    
    Phi5 = (Eta30 - 3.*Eta12)*(Eta30 + Eta12)*(pow((Eta30 + Eta12),2) - 3.*pow((Eta21 + Eta03),2)) + (3.*Eta21 - Eta03)*(Eta21 + Eta03)*(3.*pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2));
    
    Phi6 = ((Eta20 - Eta02 )*(pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2))) + 4.*Eta11*(Eta30 + Eta12)*(Eta21 + Eta03);
    
    Phi7 = (3.*Eta21 - Eta03)*(Eta30 + Eta12)*(pow((Eta30 + Eta12),2) - 3.*pow((Eta21 + Eta03),2)) - (Eta30 - 3.*Eta12)*(Eta21 + Eta03)*(3.*pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2));
  }else{
    Phi1 = Phi2 = Phi3 = Phi4 = Phi5 = Phi6 = Phi7 = -999;
  }
  
  Skx = ( Mu20 > 0 ) ? Mu30/pow(Mu20,1.5) : -999;
  Sky = ( Mu02 > 0 ) ? Mu03/pow(Mu02,1.5) : -999;
  
  Z11 += tmp_Z11.Mod();
  Z20 += tmp_Z20.Mod();
  Z22 += tmp_Z22.Mod();
  Z31 += tmp_Z31.Mod();
  Z33 += tmp_Z33.Mod();
  Z40 += tmp_Z40.Mod();
  Z42 += tmp_Z42.Mod();
  Z44 += tmp_Z44.Mod();
  Z51 += tmp_Z51.Mod();
  Z53 += tmp_Z53.Mod();
  Z55 += tmp_Z55.Mod();


  
  jets_.jtnCands[jets_.nref] = nCands;
  jets_.jtnChCands[jets_.nref] = nChCands;
  jets_.jtnNeCands[jets_.nref] = nNeCands;
  
  jets_.jtchargedSumConst[jets_.nref] = chargedSumConst;
  jets_.jtchargedNConst  [jets_.nref] = chargedNConst;  
  jets_.jteSumConst      [jets_.nref] = eSumConst;      
  jets_.jteNConst        [jets_.nref] = eNConst;        
  jets_.jtmuSumConst     [jets_.nref] = muSumConst;     
  jets_.jtmuNConst       [jets_.nref] = muNConst;       
  jets_.jtphotonSumConst [jets_.nref] = photonSumConst; 
  jets_.jtphotonNConst   [jets_.nref] = photonNConst;   
  jets_.jtneutralSumConst[jets_.nref] = neutralSumConst;
  jets_.jtneutralNConst  [jets_.nref] = neutralNConst;  
  jets_.jthfhadSumConst  [jets_.nref] = hfhadSumConst;
  jets_.jthfhadNConst    [jets_.nref] = hfhadNConst;
  jets_.jthfemSumConst   [jets_.nref] = hfemSumConst;
  jets_.jthfemNConst     [jets_.nref] = hfemNConst;

  jets_.jtMByPt[jets_.nref] = jetMByPt;
  jets_.jtRMSCand[jets_.nref] = RMSCand;
  jets_.jtAxis1[jets_.nref] = Axis1;
  jets_.jtAxis2[jets_.nref] = Axis2;
  jets_.jtSigma[jets_.nref] = Sigma;
  jets_.jtrm3[jets_.nref] = rm3;
  jets_.jtrm2[jets_.nref] = rm2;
  jets_.jtrm1[jets_.nref] = rm1;
  jets_.jtrm0p5[jets_.nref] = rm0p5;
  jets_.jtR[jets_.nref] = R;
  jets_.jtpull[jets_.nref] = pull;
  jets_.jtpTD[jets_.nref] = pTD;
  jets_.jtSDm[jets_.nref] = sd_m;
  jets_.jtSDpt[jets_.nref] = sd_pt;
  jets_.jtSDeta[jets_.nref] = sd_eta;
  jets_.jtSDphi[jets_.nref] = sd_phi;
  jets_.jtSDptFrac[jets_.nref] = sd_ptfrac;
  jets_.jtSDrm0p5[jets_.nref] = sd_rm0p5;
  jets_.jtSDrm1[jets_.nref] = sd_rm1;
  jets_.jtSDrm2[jets_.nref] = sd_rm2;
  jets_.jtSDrm3[jets_.nref] = sd_rm3;

  jets_.jtConstituentsId.push_back(jcid);
  jets_.jtConstituentsE.push_back(jcE);
  jets_.jtConstituentsPt.push_back(jcpt);
  jets_.jtConstituentsEta.push_back(jceta);
  jets_.jtConstituentsPhi.push_back(jcphi);
  jets_.jtConstituentsM.push_back(jcm);
  jets_.jtSDConstituentsId.push_back(jcSDid);
  jets_.jtSDConstituentsE.push_back(jcSDE);
  jets_.jtSDConstituentsPt.push_back(jcSDpt);
  jets_.jtSDConstituentsEta.push_back(jcSDeta);
  jets_.jtSDConstituentsPhi.push_back(jcSDphi);
  jets_.jtSDConstituentsM.push_back(jcSDm);
  
  jets_.jtTbeta20p2[jets_.nref] = Tbeta20p2; 
  jets_.jtTbeta20p3[jets_.nref] = Tbeta20p3; 
  jets_.jtTbeta20p4[jets_.nref] = Tbeta20p4; 
  jets_.jtTbeta20p5[jets_.nref] = Tbeta20p5; 

  jets_.jtTbeta30p2[jets_.nref] = Tbeta30p2; 
  jets_.jtTbeta30p3[jets_.nref] = Tbeta30p3; 
  jets_.jtTbeta30p4[jets_.nref] = Tbeta30p4; 
  jets_.jtTbeta30p5[jets_.nref] = Tbeta30p5; 

  jets_.jtCbeta20p2[jets_.nref] = Cbeta20p2; 
  jets_.jtCbeta20p3[jets_.nref] = Cbeta20p3; 
  jets_.jtCbeta20p4[jets_.nref] = Cbeta20p4; 
  jets_.jtCbeta20p5[jets_.nref] = Cbeta20p5; 
			       

  jets_.jtZ11[jets_.nref] = Z11;
  jets_.jtZ20[jets_.nref] = Z20;
  jets_.jtZ22[jets_.nref] = Z22;
  jets_.jtZ31[jets_.nref] = Z31;
  jets_.jtZ33[jets_.nref] = Z33;
  jets_.jtZ40[jets_.nref] = Z40;
  jets_.jtZ42[jets_.nref] = Z42;
  jets_.jtZ44[jets_.nref] = Z44;
  jets_.jtZ51[jets_.nref] = Z51;
  jets_.jtZ53[jets_.nref] = Z53;
  jets_.jtZ55[jets_.nref] = Z55;


  jets_.jtPhi1[jets_.nref] = Phi1;
  jets_.jtPhi2[jets_.nref] = Phi2;
  jets_.jtPhi3[jets_.nref] = Phi3;
  jets_.jtPhi4[jets_.nref] = Phi4;
  jets_.jtPhi5[jets_.nref] = Phi5;
  jets_.jtPhi6[jets_.nref] = Phi6;
  jets_.jtPhi7[jets_.nref] = Phi7;

  jets_.jtSkx[jets_.nref] = Skx;
  jets_.jtSky[jets_.nref] = Sky;
}			       
			       
//--------------------------------------------------------------------------------------------------
void HiInclusiveJetAnalyzer::fillNewJetVarsRefJet(const reco::GenJet jet){
			       
  int nCands = 0;	       
  int nChCands = 0;	       
  int nNeCands = 0;	       

  float jetMByPt = (jet.mass()>0 && jet.pt()!=0) ? jet.mass()/jet.pt() : -999;

  float tot_wt=0;
      
  float RMSCand = 0.0;
  float rmscand_n=0;
  float rmscand_d=0;
      
  float M11=0,M22=0,M12=0,M21=0;
  float Axis1 = 0.0;
  float Axis2 = 0.0;
  float Sigma = 0.0;
      
  float maxCandPt=-999;
  float sumCandPt=0;
  float sumCandPtSq=0;
  float R = 0.0;
  float pTD = 0.0;

  float rm0p5 = 0.0;
  float rm1 = 0.0;
  float rm2 = 0.0;
  float rm3 = 0.0;
      
  TVector2 t_Vect(0,0);
  TVector2 r(0,0);
  float pull = 0.0;

  float sd_m = 0.0;
  float sd_pt = 0.0;
  float sd_eta = 0.0;
  float sd_phi = 0.0;
  float sd_ptfrac = 0.0;
  float sd_rm0p5 = 0.0;
  float sd_rm1 = 0.0;
  float sd_rm2 = 0.0;
  float sd_rm3 = 0.0;

  float Tbeta20p2 = 0.0;
  float Tbeta20p3 = 0.0;
  float Tbeta20p4 = 0.0;
  float Tbeta20p5 = 0.0;

  float Tbeta30p2 = 0.0;
  float Tbeta30p3 = 0.0;
  float Tbeta30p4 = 0.0;
  float Tbeta30p5 = 0.0;

  float Cbeta20p2 = 0.0;
  float Cbeta20p3 = 0.0;
  float Cbeta20p4 = 0.0;
  float Cbeta20p5 = 0.0;

  // //! Moments shifted to centriod
  float Mu00=0.0, Mu01=0.0, Mu10=0.0, Mu11=0.0;
  float Mu20=0.0, Mu02=0.0, Mu12=0.0, Mu21=0.0;
  float Mu30=0.0, Mu03=0.0;

  float Phi1 = 0.0;
  float Phi2 = 0.0;
  float Phi3 = 0.0;
  float Phi4 = 0.0;
  float Phi5 = 0.0;
  float Phi6 = 0.0;
  float Phi7 = 0.0;

  float Skx=0.0;
  float Sky=0.0;

  float Z11=0.0;
  float Z20=0.0;
  float Z22=0.0;
  float Z31=0.0;
  float Z33=0.0;
  float Z40=0.0;
  float Z42=0.0;
  float Z44=0.0;
  float Z51=0.0;
  float Z53=0.0;
  float Z55=0.0;

  TVector2 tmp_Z11(0,0);
  TVector2 tmp_Z20(0,0);
  TVector2 tmp_Z22(0,0);
  TVector2 tmp_Z31(0,0);
  TVector2 tmp_Z33(0,0);
  TVector2 tmp_Z40(0,0);
  TVector2 tmp_Z42(0,0);
  TVector2 tmp_Z44(0,0);
  TVector2 tmp_Z51(0,0);
  TVector2 tmp_Z53(0,0);
  TVector2 tmp_Z55(0,0);


  float chargedSumConst = 0;
  int   chargedNConst = 0;
  float eSumConst = 0;
  int   eNConst = 0;
  float muSumConst = 0;
  int   muNConst = 0;
  float photonSumConst = 0;
  int   photonNConst = 0;
  float neutralSumConst = 0;
  int   neutralNConst = 0;
  float hfhadSumConst = 0;
  int   hfhadNConst = 0;
  float hfemSumConst = 0;
  int   hfemNConst = 0;


  vector<fastjet::PseudoJet> jetconsts;
  std::vector<int> jcid;
  std::vector<float> jcE;
  std::vector<float> jcpt;
  std::vector<float> jceta;
  std::vector<float> jcphi;
  std::vector<float> jcm;
  std::vector<int> jcSDid;
  std::vector<float> jcSDE;
  std::vector<float> jcSDpt;
  std::vector<float> jcSDeta;
  std::vector<float> jcSDphi;
  std::vector<float> jcSDm;

  if(jet.numberOfDaughters()>0) {
    nCands = jet.numberOfDaughters();
    for (unsigned k = 0; k < jet.numberOfDaughters(); ++k) {
      const reco::Candidate & dp = *jet.daughter(k);

      if(dp.charge() == 0){
	nNeCands++;
      }else{
	nChCands++;
      }

      float ptcand = dp.pt();
      int pfid     = dp.pdgId();
      
      switch(std::abs(pfid)){
      case 211:  //PFCandidate::h charged hadron
      case 321:
      case 2212:
	chargedSumConst += ptcand;
	chargedNConst++;
	break;
      case 11:  //PFCandidate::e // electron
	eSumConst += ptcand;
	eNConst++;
	break;
      case 13: //PFCandidate::mu // muon
	muSumConst += ptcand;
	muNConst++;
	break;
      case 22: //PFCandidate:gamma // gamma
	photonSumConst += ptcand;
	photonNConst++;
	break;
      case 130:  //PFCandidate::h0 //Neutral hadron
      case 2112:
	neutralSumConst += ptcand;
	neutralNConst++;
	break;
      case 1:  //PFCandidate::h_HF //hadron in HF
	hfhadSumConst += ptcand; 
	hfhadNConst++;
      case 2:  //PFCandidate::egamma_HF //electromagnetic in HF
	hfemSumConst += ptcand; 
	hfemNConst++;
      default:
	break;
      }


      if( dp.pt() > maxCandPt )maxCandPt=dp.pt();
      sumCandPt   += dp.pt();
      sumCandPtSq += pow(dp.pt(),2);
	
      float wt = pow(dp.pt(),2);
      tot_wt += wt;
	
      //! RMSCand
      float deta = dp.eta()- jet.eta();
      float dphi = deltaPhi(dp.phi(), jet.phi());
      float dr = deltaR(dp.eta(), dp.phi(), jet.eta(), jet.phi());
      rmscand_n += wt*dr*dr;
      rmscand_d += wt; 
	
      M11 += wt*deta*deta;
      M22 += wt*dphi*dphi;
      M12 += wt*deta*dphi;
      M21 += wt*deta*dphi;
	
      //! Pull
      TLorentzVector pfvec;
      pfvec.SetPtEtaPhiE(dp.pt(), dp.eta(), dp.phi(), dp.energy());
      fastjet::PseudoJet jc = fastjet::PseudoJet(dp.px(), dp.py(), dp.pz(), dp.energy());
      jc.set_user_info(new ExtraInfo(dp.pdgId()));
      jetconsts.push_back(jc);
      jcid.push_back(dp.pdgId());
      jcE.push_back(jc.e());
      jcpt.push_back(jc.pt());
      jcphi.push_back(jc.phi_std());
      jceta.push_back(jc.eta());
      jcm.push_back(jc.m());

      float pfy = pfvec.Rapidity();
      float dy = pfy - jet.y();
      r.Set( dy, dphi );
      float r_mag = r.Mod();
      t_Vect += ( dp.pt() /  jet.pt() ) * r_mag *r;

      rm0p5+=(dp.pt()*pow(dr,0.5))/jet.pt();
      rm1+=(dp.pt()*pow(dr,1))/jet.pt();
      rm2+=(dp.pt()*pow(dr,2))/jet.pt();
      rm3+=(dp.pt()*pow(dr,3))/jet.pt();      
      
      //! Added by Pawan ZM 
      tmp_Z11 += ( ( dp.pt() /  jet.pt() ) * r_mag * r);

      tmp_Z20 += ( ( dp.pt() /  jet.pt() ) * (2.*r_mag*r_mag - 1) * r);
      tmp_Z22 += ( ( dp.pt() /  jet.pt() ) * r_mag * r_mag * r);

      tmp_Z31 += ( ( dp.pt() /  jet.pt() ) * ( (3. * r_mag * r_mag * r_mag) - 2.*r_mag ) * r);
      tmp_Z33 += ( ( dp.pt() /  jet.pt() ) * r_mag * r_mag * r_mag * r );

      tmp_Z40 += (( dp.pt() /  jet.pt() ) * ( 6.*pow(r_mag,4) - 6.*pow(r_mag,2) + 1 ) * r);
      tmp_Z42 += (( dp.pt() /  jet.pt() ) * ( 4.*pow(r_mag,4) - 3.*pow(r_mag,2)) * r );
      tmp_Z44 += (( dp.pt() /  jet.pt() ) * pow(r_mag,4) * r);

      tmp_Z51 += (( dp.pt() /  jet.pt() ) * ( 10.*pow(r_mag,5) - 12.*pow(r_mag,3) + 3.*r_mag ) * r);
      tmp_Z53 += (( dp.pt() /  jet.pt() ) * ( 5.*pow(r_mag,5) - 4.*pow(r_mag,3)) * r );
      tmp_Z55 += (( dp.pt() /  jet.pt() ) * pow(r_mag,5) * r );


      //! For two-point moment
      for (unsigned l = k+1; l < jet.numberOfDaughters(); ++l) {
        const reco::Candidate & dl = *jet.daughter(l);
        float dr_kl = deltaR(dl.eta(), dl.phi(), dp.eta(), dp.phi());
	
        Tbeta20p2 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.2) );
        Tbeta20p3 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.3) );
        Tbeta20p4 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.4) );
        Tbeta20p5 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.5) );

	//! For three-point moment
	for (unsigned m = l+1; m < jet.numberOfDaughters(); ++m) {
	  const reco::Candidate & dm = *jet.daughter(m);
	  float dr_km = deltaR(dm.eta(), dm.phi(), dp.eta(), dp.phi());
	  float dr_lm = deltaR(dm.eta(), dm.phi(), dl.eta(), dl.phi());
	  
	  Tbeta30p2 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.2) );
	  Tbeta30p3 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.3) );
	  Tbeta30p4 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.4) );
	  Tbeta30p5 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.5) );
	}
      }

      //! Hu Moment Calculation 
      Mu00 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu01 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));
      Mu10 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu11 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));

      Mu20 += (pow(dp.eta()-jet.eta(),2)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu02 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),2)*(dp.pt()/jet.pt()));
      Mu12 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),2)*(dp.pt()/jet.pt()));
      Mu21 += (pow(dp.eta()-jet.eta(),2)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));

      Mu30 += (pow(dp.eta()-jet.eta(),3)*pow(dp.eta()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu03 += (pow(dp.eta()-jet.eta(),0)*pow(dp.eta()-jet.phi(),3)*(dp.pt()/jet.pt()));
    }
  }

  fastjet::JetDefinition jetDef(fastjet::antikt_algorithm, 999);
  fastjet::ClusterSequence thisClustering_basic(jetconsts, jetDef);
  std::vector<fastjet::PseudoJet> out_jets_basic = thisClustering_basic.inclusive_jets(0);
  if(out_jets_basic.size() == 1){ 
    fastjet::contrib::RecursiveSymmetryCutBase::SymmetryMeasure  symmetry_measure = fastjet::contrib::RecursiveSymmetryCutBase::scalar_z;
    fastjet::contrib::SoftDrop sd(0, 0.1, symmetry_measure, rParam);
    fastjet::PseudoJet sd_jet = sd(out_jets_basic[0]);
    if(sd_jet != 0){
      sd_m = sd_jet.m();
      sd_pt = sd_jet.pt();
      sd_eta = sd_jet.eta();
      sd_phi = sd_jet.phi();
      sd_ptfrac = sd_jet.pt()/jet.pt();    
      std::vector<fastjet::PseudoJet> sd_jetconsts = sd_jet.constituents();
      if(sd_jetconsts.size()!=0){
	for (unsigned k = 0; k < sd_jetconsts.size(); ++k) {
	  const fastjet::PseudoJet dp = sd_jetconsts.at(k);
	  jcSDid.push_back(dp.user_info<ExtraInfo>().part_id());
	  jcSDE.push_back(dp.e());
	  jcSDpt.push_back(dp.pt());
	  jcSDphi.push_back(dp.phi());
	  jcSDeta.push_back(dp.eta());
	  jcSDm.push_back(dp.m());
	  float dr = deltaR(dp.eta(), dp.phi(), jet.eta(), jet.phi());
	  sd_rm0p5+=(dp.pt()*pow(dr,0.5))/sd_jet.pt();
	  sd_rm1+=(dp.pt()*pow(dr,1))/sd_jet.pt();
	  sd_rm2+=(dp.pt()*pow(dr,2))/sd_jet.pt();
	  sd_rm3+=(dp.pt()*pow(dr,3))/sd_jet.pt();
	}
      }
    }
  }
  
  RMSCand = (rmscand_d > 0 ) ? sqrt ( rmscand_n / rmscand_d ) : -999;
      
  M12 = -1.*M12;
  M21 = -1.*M21;
      
  //! eign values
  float trace = M11 + M22;
  float detrm = (M11*M22) - (M12*M21);
      
  float lam1 = trace/2. + sqrt( pow(trace,2)/4. - detrm );
  float lam2 = trace/2. - sqrt( pow(trace,2)/4. - detrm );
      
  Axis1 = (tot_wt > 0 && lam1>=0 ) ? sqrt( lam1 / tot_wt ) : -999;
  Axis2 = (tot_wt > 0 && lam2>=0 ) ? sqrt( lam2 / tot_wt ) : -999;
  
  Sigma = (tot_wt > 0 ) ? sqrt( pow(Axis1,2) + pow(Axis2,2) ) : -999;
      
  R = (sumCandPt > 0 ) ? maxCandPt / sumCandPt : -999;
      
  pTD = (sumCandPt > 0 ) ? sqrt( sumCandPtSq ) / sumCandPt : -999;

      
  pull = t_Vect.Mod();
    
  Tbeta20p2 /= pow(jet.pt(),2); 
  Tbeta20p3 /= pow(jet.pt(),2); 
  Tbeta20p4 /= pow(jet.pt(),2); 
  Tbeta20p5 /= pow(jet.pt(),2); 

  Tbeta30p2 /= pow(jet.pt(),3); 
  Tbeta30p3 /= pow(jet.pt(),3); 
  Tbeta30p4 /= pow(jet.pt(),3); 
  Tbeta30p5 /= pow(jet.pt(),3); 

  Cbeta20p2 = ( Tbeta20p2 > 0 ) ? Tbeta30p2 / Tbeta20p2 : -999;
  Cbeta20p3 = ( Tbeta20p3 > 0 ) ? Tbeta30p3 / Tbeta20p3 : -999;
  Cbeta20p4 = ( Tbeta20p4 > 0 ) ? Tbeta30p4 / Tbeta20p4 : -999;
  Cbeta20p5 = ( Tbeta20p5 > 0 ) ? Tbeta30p5 / Tbeta20p5 : -999;

  //! Hu Moments
  if( Mu00 > 0 ){
    float Eta02 = Mu20/pow(Mu00,(0+2+1));
    float Eta20 = Mu20/pow(Mu00,(2+0+1));
    float Eta11 = Mu11/pow(Mu00,(1+1+1));
    float Eta12 = Mu12/pow(Mu00,(1+2+1));
    float Eta21 = Mu21/pow(Mu00,(2+1+1));
    float Eta03 = Mu03/pow(Mu00,(0+3+1));
    float Eta30 = Mu30/pow(Mu00,(3+0+1));
    
    
    Phi1 = (Eta20 + Eta02);
    Phi2 = pow((Eta20 - Eta02),2) + 4.*pow(Eta11,2);
    Phi3 = pow((Eta30 - 3.*Eta12),2) + pow((3.*Eta21 - Eta03),2);
    Phi4 = pow((Eta30 + Eta12),2) + pow((Eta21 + Eta03),2);
    
    Phi5 = (Eta30 - 3.*Eta12)*(Eta30 + Eta12)*(pow((Eta30 + Eta12),2) - 3.*pow((Eta21 + Eta03),2)) + (3.*Eta21 - Eta03)*(Eta21 + Eta03)*(3.*pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2));
    
    Phi6 = ((Eta20 - Eta02 )*(pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2))) + 4.*Eta11*(Eta30 + Eta12)*(Eta21 + Eta03);
    
    Phi7 = (3.*Eta21 - Eta03)*(Eta30 + Eta12)*(pow((Eta30 + Eta12),2) - 3.*pow((Eta21 + Eta03),2)) - (Eta30 - 3.*Eta12)*(Eta21 + Eta03)*(3.*pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2));
  }else{
    Phi1 = Phi2 = Phi3 = Phi4 = Phi5 = Phi6 = Phi7 = -999;
  }

  Skx = ( Mu20 > 0 ) ? Mu30/pow(Mu20,1.5) : -999;
  Sky = ( Mu02 > 0 ) ? Mu03/pow(Mu02,1.5) : -999;

  
  Z11 += tmp_Z11.Mod();
  Z20 += tmp_Z20.Mod();
  Z22 += tmp_Z22.Mod();
  Z31 += tmp_Z31.Mod();
  Z33 += tmp_Z33.Mod();
  Z40 += tmp_Z40.Mod();
  Z42 += tmp_Z42.Mod();
  Z44 += tmp_Z44.Mod();
  Z51 += tmp_Z51.Mod();
  Z53 += tmp_Z53.Mod();
  Z55 += tmp_Z55.Mod();



  jets_.refnCands[jets_.nref] = nCands;
  jets_.refnChCands[jets_.nref] = nChCands;
  jets_.refnNeCands[jets_.nref] = nNeCands;
  jets_.refchargedSumConst[jets_.nref] = chargedSumConst;
  jets_.refchargedNConst  [jets_.nref] = chargedNConst;  
  jets_.refeSumConst      [jets_.nref] = eSumConst;      
  jets_.refeNConst        [jets_.nref] = eNConst;        
  jets_.refmuSumConst     [jets_.nref] = muSumConst;     
  jets_.refmuNConst       [jets_.nref] = muNConst;       
  jets_.refphotonSumConst [jets_.nref] = photonSumConst; 
  jets_.refphotonNConst   [jets_.nref] = photonNConst;   
  jets_.refneutralSumConst[jets_.nref] = neutralSumConst;
  jets_.refneutralNConst  [jets_.nref] = neutralNConst;  
  jets_.refhfhadSumConst  [jets_.nref] = hfhadSumConst;
  jets_.refhfhadNConst    [jets_.nref] = hfhadNConst;
  jets_.refhfemSumConst   [jets_.nref] = hfemSumConst;
  jets_.refhfemNConst     [jets_.nref] = hfemNConst;

  jets_.refMByPt[jets_.nref] = jetMByPt;
  jets_.refRMSCand[jets_.nref] = RMSCand;
  jets_.refAxis1[jets_.nref] = Axis1;
  jets_.refAxis2[jets_.nref] = Axis2;
  jets_.refSigma[jets_.nref] = Sigma;
  jets_.refrm3[jets_.nref] = rm3;
  jets_.refrm2[jets_.nref] = rm2;
  jets_.refrm1[jets_.nref] = rm1;
  jets_.refrm0p5[jets_.nref] = rm0p5;
  jets_.refR[jets_.nref] = R;
  jets_.refpull[jets_.nref] = pull;
  jets_.refpTD[jets_.nref] = pTD;
  jets_.refSDm[jets_.nref] = sd_m;
  jets_.refSDpt[jets_.nref] = sd_pt;
  jets_.refSDeta[jets_.nref] = sd_eta;
  jets_.refSDphi[jets_.nref] = sd_phi;
  jets_.refSDptFrac[jets_.nref] = sd_ptfrac;
  jets_.refSDrm0p5[jets_.nref] = sd_rm0p5;
  jets_.refSDrm1[jets_.nref] = sd_rm1;
  jets_.refSDrm2[jets_.nref] = sd_rm2;
  jets_.refSDrm3[jets_.nref] = sd_rm3;    

  jets_.refConstituentsId.push_back(jcid);
  jets_.refConstituentsE.push_back(jcE);
  jets_.refConstituentsPt.push_back(jcpt);
  jets_.refConstituentsEta.push_back(jceta);
  jets_.refConstituentsPhi.push_back(jcphi);
  jets_.refConstituentsM.push_back(jcm);
  jets_.refSDConstituentsId.push_back(jcSDid);
  jets_.refSDConstituentsE.push_back(jcSDE);
  jets_.refSDConstituentsPt.push_back(jcSDpt);
  jets_.refSDConstituentsEta.push_back(jcSDeta);
  jets_.refSDConstituentsPhi.push_back(jcSDphi);
  jets_.refSDConstituentsM.push_back(jcSDm);

  jets_.refTbeta20p2[jets_.nref] = Tbeta20p2; 
  jets_.refTbeta20p3[jets_.nref] = Tbeta20p3; 
  jets_.refTbeta20p4[jets_.nref] = Tbeta20p4; 
  jets_.refTbeta20p5[jets_.nref] = Tbeta20p5; 

  jets_.refTbeta30p2[jets_.nref] = Tbeta30p2; 
  jets_.refTbeta30p3[jets_.nref] = Tbeta30p3; 
  jets_.refTbeta30p4[jets_.nref] = Tbeta30p4; 
  jets_.refTbeta30p5[jets_.nref] = Tbeta30p5; 

  jets_.refCbeta20p2[jets_.nref] = Cbeta20p2; 
  jets_.refCbeta20p3[jets_.nref] = Cbeta20p3; 
  jets_.refCbeta20p4[jets_.nref] = Cbeta20p4; 
  jets_.refCbeta20p5[jets_.nref] = Cbeta20p5; 

  jets_.refZ11[jets_.nref] = Z11;
  jets_.refZ20[jets_.nref] = Z20;
  jets_.refZ22[jets_.nref] = Z22;
  jets_.refZ31[jets_.nref] = Z31;
  jets_.refZ33[jets_.nref] = Z33;
  jets_.refZ40[jets_.nref] = Z40;
  jets_.refZ42[jets_.nref] = Z42;
  jets_.refZ44[jets_.nref] = Z44;
  jets_.refZ51[jets_.nref] = Z51;
  jets_.refZ53[jets_.nref] = Z53;
  jets_.refZ55[jets_.nref] = Z55;


  jets_.refPhi1[jets_.nref] = Phi1;
  jets_.refPhi2[jets_.nref] = Phi2;
  jets_.refPhi3[jets_.nref] = Phi3;
  jets_.refPhi4[jets_.nref] = Phi4;
  jets_.refPhi5[jets_.nref] = Phi5;
  jets_.refPhi6[jets_.nref] = Phi6;
  jets_.refPhi7[jets_.nref] = Phi7;

  jets_.refSkx[jets_.nref] = Skx;
  jets_.refSky[jets_.nref] = Sky;
}

//--------------------------------------------------------------------------------------------------
void HiInclusiveJetAnalyzer::fillNewJetVarsGenJet(const reco::GenJet jet){

  int nCands = 0;
  int nChCands = 0;
  int nNeCands = 0;

  float jetMByPt = (jet.mass()>0 && jet.pt()!=0) ? jet.mass()/jet.pt() : -999;

  float tot_wt=0;
      
  float RMSCand = 0.0;
  float rmscand_n=0;
  float rmscand_d=0;
      
  float M11=0,M22=0,M12=0,M21=0;
  float Axis1 = 0.0;
  float Axis2 = 0.0;
  float Sigma = 0.0;
      
  float maxCandPt=-999;
  float sumCandPt=0;
  float sumCandPtSq=0;
  float R = 0.0;
  float pTD = 0.0;

  float rm0p5 = 0.0;
  float rm1 = 0.0;
  float rm2 = 0.0;
  float rm3 = 0.0;
      
  TVector2 t_Vect(0,0);
  TVector2 r(0,0);
  float pull = 0.0;
  

  float sd_m = 0.0;
  float sd_pt = 0.0;
  float sd_eta = 0.0;
  float sd_phi = 0.0;
  float sd_ptfrac = 0.0;
  float sd_rm0p5 = 0.0;
  float sd_rm1 = 0.0;
  float sd_rm2 = 0.0;
  float sd_rm3 = 0.0;

  float Tbeta20p2 = 0.0;
  float Tbeta20p3 = 0.0;
  float Tbeta20p4 = 0.0;
  float Tbeta20p5 = 0.0;

  float Tbeta30p2 = 0.0;
  float Tbeta30p3 = 0.0;
  float Tbeta30p4 = 0.0;
  float Tbeta30p5 = 0.0;

  float Cbeta20p2 = 0.0;
  float Cbeta20p3 = 0.0;
  float Cbeta20p4 = 0.0;
  float Cbeta20p5 = 0.0;

  //! Moments shifted to centriod
  float Mu00=0.0, Mu01=0.0, Mu10=0.0, Mu11=0.0;
  float Mu20=0.0, Mu02=0.0, Mu12=0.0, Mu21=0.0;
  float Mu30=0.0, Mu03=0.0;

  float Phi1 = 0.0;
  float Phi2 = 0.0;
  float Phi3 = 0.0;
  float Phi4 = 0.0;
  float Phi5 = 0.0;
  float Phi6 = 0.0;
  float Phi7 = 0.0;

  float Skx=0.0;
  float Sky=0.0;

  float Z11=0.0;
  float Z20=0.0;
  float Z22=0.0;
  float Z31=0.0;
  float Z33=0.0;
  float Z40=0.0;
  float Z42=0.0;
  float Z44=0.0;
  float Z51=0.0;
  float Z53=0.0;
  float Z55=0.0;

  TVector2 tmp_Z11(0,0);
  TVector2 tmp_Z20(0,0);
  TVector2 tmp_Z22(0,0);
  TVector2 tmp_Z31(0,0);
  TVector2 tmp_Z33(0,0);
  TVector2 tmp_Z40(0,0);
  TVector2 tmp_Z42(0,0);
  TVector2 tmp_Z44(0,0);
  TVector2 tmp_Z51(0,0);
  TVector2 tmp_Z53(0,0);
  TVector2 tmp_Z55(0,0);

  float chargedSumConst = 0;
  int   chargedNConst = 0;
  float eSumConst = 0;
  int   eNConst = 0;
  float muSumConst = 0;
  int   muNConst = 0;
  float photonSumConst = 0;
  int   photonNConst = 0;
  float neutralSumConst = 0;
  int   neutralNConst = 0;
  float hfhadSumConst = 0;
  int   hfhadNConst = 0;
  float hfemSumConst = 0;
  int   hfemNConst = 0;

  vector<fastjet::PseudoJet> jetconsts;
  std::vector<int> jcid;
  std::vector<float> jcE;
  std::vector<float> jcpt;
  std::vector<float> jceta;
  std::vector<float> jcphi;
  std::vector<float> jcm;
  std::vector<int> jcSDid;
  std::vector<float> jcSDE;
  std::vector<float> jcSDpt;
  std::vector<float> jcSDeta;
  std::vector<float> jcSDphi;
  std::vector<float> jcSDm;
  
  if(jet.numberOfDaughters()>0) {
    nCands = jet.numberOfDaughters();
    for (unsigned k = 0; k < jet.numberOfDaughters(); ++k) {
      const reco::Candidate & dp = *jet.daughter(k);

      if(dp.charge() == 0){
	nNeCands++;
      }else{
	nChCands++;
      }

      float ptcand = dp.pt();
      int pfid     = dp.pdgId();

      switch(std::abs(pfid)){
      case 211:  //PFCandidate::h charged hadron
      case 321:
      case 2212:
	chargedSumConst += ptcand;
	chargedNConst++;
	break;
      case 11:  //PFCandidate::e // electron
	eSumConst += ptcand;
	eNConst++;
	break;
      case 13: //PFCandidate::mu // muon
	muSumConst += ptcand;
	muNConst++;
	break;
      case 22: //PFCandidate:gamma // gamma
	photonSumConst += ptcand;
	photonNConst++;
	break;
      case 130:  //PFCandidate::h0 //Neutral hadron
      case 2112:
	neutralSumConst += ptcand;
	neutralNConst++;
	break;
      case 1:  //PFCandidate::h_HF //hadron in HF
	hfhadSumConst += ptcand; 
	hfhadNConst++;
      case 2:  //PFCandidate::egamma_HF //electromagnetic in HF
	hfemSumConst += ptcand; 
	hfemNConst++;
      default:
	break;
      }


      if( dp.pt() > maxCandPt )maxCandPt=dp.pt();
      sumCandPt   += dp.pt();
      sumCandPtSq += pow(dp.pt(),2);
	
      float wt = pow(dp.pt(),2);
      tot_wt += wt;
	
      //! RMSCand
      float deta = dp.eta()- jet.eta();
      float dphi = deltaPhi(dp.phi(), jet.phi());
      float dr = deltaR(dp.eta(), dp.phi(), jet.eta(), jet.phi());
      rmscand_n += wt*dr*dr;
      rmscand_d += wt; 
	
      M11 += wt*deta*deta;
      M22 += wt*dphi*dphi;
      M12 += wt*deta*dphi;
      M21 += wt*deta*dphi;
	
      //! Pull
      TLorentzVector pfvec;
      pfvec.SetPtEtaPhiE(dp.pt(), dp.eta(), dp.phi(), dp.energy());
      fastjet::PseudoJet jc = fastjet::PseudoJet(dp.px(), dp.py(), dp.pz(), dp.energy());
      jc.set_user_info(new ExtraInfo(dp.pdgId()));
      jetconsts.push_back(jc);

      jcid.push_back(dp.pdgId());
      jcE.push_back(jc.e());
      jcpt.push_back(jc.pt());
      jcphi.push_back(jc.phi_std());
      jceta.push_back(jc.eta());
      jcm.push_back(jc.m());

      float pfy = pfvec.Rapidity();
      float dy = pfy - jet.y();
      r.Set( dy, dphi );
      float r_mag = r.Mod();
      t_Vect += ( dp.pt() /  jet.pt() ) * r_mag *r;

      rm0p5+=(dp.pt()*pow(dr,0.5))/jet.pt();
      rm1+=(dp.pt()*pow(dr,1))/jet.pt();
      rm2+=(dp.pt()*pow(dr,2))/jet.pt();
      rm3+=(dp.pt()*pow(dr,3))/jet.pt();      

      //! Added by Pawan ZM 
      tmp_Z11 += ( ( dp.pt() /  jet.pt() ) * r_mag * r );

      tmp_Z20 += ( ( dp.pt() /  jet.pt() ) * (2.*r_mag*r_mag - 1) * r );
      tmp_Z22 += ( ( dp.pt() /  jet.pt() ) * r_mag * r_mag * r );

      tmp_Z31 += ( ( dp.pt() /  jet.pt() ) * ( (3. * r_mag * r_mag * r_mag) - 2.*r_mag ) * r );
      tmp_Z33 += ( ( dp.pt() /  jet.pt() ) * r_mag * r_mag * r_mag * r );

      tmp_Z40 += (( dp.pt() /  jet.pt() ) * ( 6.*pow(r_mag,4) - 6.*pow(r_mag,2) + 1 ) * r );
      tmp_Z42 += (( dp.pt() /  jet.pt() ) * ( 4.*pow(r_mag,4) - 3.*pow(r_mag,2)) * r );
      tmp_Z44 += (( dp.pt() /  jet.pt() ) * pow(r_mag,4) * r);

      tmp_Z51 += (( dp.pt() /  jet.pt() ) * ( 10.*pow(r_mag,5) - 12.*pow(r_mag,3) + 3.*r_mag ) * r );
      tmp_Z53 += (( dp.pt() /  jet.pt() ) * ( 5.*pow(r_mag,5) - 4.*pow(r_mag,3)) * r );
      tmp_Z55 += (( dp.pt() /  jet.pt() ) * pow(r_mag,5) * r );


      //! For two-point moment
      for (unsigned l = k+1; l < jet.numberOfDaughters(); ++l) {
        const reco::Candidate & dl = *jet.daughter(l);
        float dr_kl = deltaR(dl.eta(), dl.phi(), dp.eta(), dp.phi());
	
        Tbeta20p2 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.2) );
        Tbeta20p3 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.3) );
        Tbeta20p4 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.4) );
        Tbeta20p5 += ( dp.pt() * dl.pt() * pow(dr_kl, 0.5) );

	//! For three-point moment
	for (unsigned m = l+1; m < jet.numberOfDaughters(); ++m) {
	  const reco::Candidate & dm = *jet.daughter(m);
	  float dr_km = deltaR(dm.eta(), dm.phi(), dp.eta(), dp.phi());
	  float dr_lm = deltaR(dm.eta(), dm.phi(), dl.eta(), dl.phi());
	  
	  Tbeta30p2 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.2) );
	  Tbeta30p3 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.3) );
	  Tbeta30p4 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.4) );
	  Tbeta30p5 += ( dp.pt() * dl.pt() * dm.pt() * pow(dr_kl*dr_km*dr_lm, 0.5) );
	}
      }

      //! Hu Moment Calculation 
      Mu00 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu01 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));
      Mu10 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu11 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));

      Mu20 += (pow(dp.eta()-jet.eta(),2)*pow(dp.phi()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu02 += (pow(dp.eta()-jet.eta(),0)*pow(dp.phi()-jet.phi(),2)*(dp.pt()/jet.pt()));
      Mu12 += (pow(dp.eta()-jet.eta(),1)*pow(dp.phi()-jet.phi(),2)*(dp.pt()/jet.pt()));
      Mu21 += (pow(dp.eta()-jet.eta(),2)*pow(dp.phi()-jet.phi(),1)*(dp.pt()/jet.pt()));

      Mu30 += (pow(dp.eta()-jet.eta(),3)*pow(dp.eta()-jet.phi(),0)*(dp.pt()/jet.pt()));
      Mu03 += (pow(dp.eta()-jet.eta(),0)*pow(dp.eta()-jet.phi(),3)*(dp.pt()/jet.pt()));
    }
  }
  fastjet::JetDefinition jetDef(fastjet::antikt_algorithm, 999);
  fastjet::ClusterSequence thisClustering_basic(jetconsts, jetDef);
  std::vector<fastjet::PseudoJet> out_jets_basic = thisClustering_basic.inclusive_jets(0);
  if(out_jets_basic.size() == 1){ 
    fastjet::contrib::RecursiveSymmetryCutBase::SymmetryMeasure  symmetry_measure = fastjet::contrib::RecursiveSymmetryCutBase::scalar_z;
    fastjet::contrib::SoftDrop sd(0, 0.1, symmetry_measure, rParam);
    fastjet::PseudoJet sd_jet = sd(out_jets_basic[0]);
    if(sd_jet != 0){
      sd_m = sd_jet.m();
      sd_pt = sd_jet.pt();
      sd_eta = sd_jet.eta();
      sd_phi = sd_jet.phi();
      sd_ptfrac = sd_jet.pt()/jet.pt();    
      std::vector<fastjet::PseudoJet> sd_jetconsts = sd_jet.constituents();
      if(sd_jetconsts.size()!=0){
	for (unsigned k = 0; k < sd_jetconsts.size(); ++k) {
	  const fastjet::PseudoJet dp = sd_jetconsts.at(k);
	  jcSDid.push_back(dp.user_info<ExtraInfo>().part_id());
	  jcSDE.push_back(dp.e());
	  jcSDpt.push_back(dp.pt());
	  jcSDphi.push_back(dp.phi());
	  jcSDeta.push_back(dp.eta());
	  jcSDm.push_back(dp.m());
	  float dr = deltaR(dp.eta(), dp.phi(), jet.eta(), jet.phi());
	  sd_rm0p5+=(dp.pt()*pow(dr,0.5))/sd_jet.pt();
	  sd_rm1+=(dp.pt()*pow(dr,1))/sd_jet.pt();
	  sd_rm2+=(dp.pt()*pow(dr,2))/sd_jet.pt();
	  sd_rm3+=(dp.pt()*pow(dr,3))/sd_jet.pt();
	}
      }
    }
  }

  RMSCand = (rmscand_d > 0 ) ? sqrt ( rmscand_n / rmscand_d ) : -999;
      
  M12 = -1.*M12;
  M21 = -1.*M21;
      
  //! eign values
  float trace = M11 + M22;
  float detrm = (M11*M22) - (M12*M21);
      
  float lam1 = trace/2. + sqrt( pow(trace,2)/4. - detrm );
  float lam2 = trace/2. - sqrt( pow(trace,2)/4. - detrm );
      
  Axis1 = (tot_wt > 0 && lam1>=0 ) ? sqrt( lam1 / tot_wt ) : -999;
  Axis2 = (tot_wt > 0 && lam2>=0 ) ? sqrt( lam2 / tot_wt ) : -999;
  
  Sigma = (tot_wt > 0 ) ? sqrt( pow(Axis1,2) + pow(Axis2,2) ) : -999;
      
  R = (sumCandPt > 0 ) ? maxCandPt / sumCandPt : -999;
      
  pTD = (sumCandPt > 0 ) ? sqrt( sumCandPtSq ) / sumCandPt : -999;
      
  pull = t_Vect.Mod();
    
  Tbeta20p2 /= pow(jet.pt(),2); 
  Tbeta20p3 /= pow(jet.pt(),2); 
  Tbeta20p4 /= pow(jet.pt(),2); 
  Tbeta20p5 /= pow(jet.pt(),2); 

  Tbeta30p2 /= pow(jet.pt(),3); 
  Tbeta30p3 /= pow(jet.pt(),3); 
  Tbeta30p4 /= pow(jet.pt(),3); 
  Tbeta30p5 /= pow(jet.pt(),3); 

  Cbeta20p2 = ( Tbeta20p2 > 0 ) ? Tbeta30p2 / Tbeta20p2 : -999;
  Cbeta20p3 = ( Tbeta20p3 > 0 ) ? Tbeta30p3 / Tbeta20p3 : -999;
  Cbeta20p4 = ( Tbeta20p4 > 0 ) ? Tbeta30p4 / Tbeta20p4 : -999;
  Cbeta20p5 = ( Tbeta20p5 > 0 ) ? Tbeta30p5 / Tbeta20p5 : -999;

  //! Hu Moments
  if( Mu00 > 0 ){
    float Eta02 = Mu20/pow(Mu00,(0+2+1));
    float Eta20 = Mu20/pow(Mu00,(2+0+1));
    float Eta11 = Mu11/pow(Mu00,(1+1+1));
    float Eta12 = Mu12/pow(Mu00,(1+2+1));
    float Eta21 = Mu21/pow(Mu00,(2+1+1));
    float Eta03 = Mu03/pow(Mu00,(0+3+1));
    float Eta30 = Mu30/pow(Mu00,(3+0+1));
    
    Phi1 = (Eta20 + Eta02);
    Phi2 = pow((Eta20 - Eta02),2) + 4.*pow(Eta11,2);
    Phi3 = pow((Eta30 - 3.*Eta12),2) + pow((3.*Eta21 - Eta03),2);
    Phi4 = pow((Eta30 + Eta12),2) + pow((Eta21 + Eta03),2);
    
    Phi5 = (Eta30 - 3.*Eta12)*(Eta30 + Eta12)*(pow((Eta30 + Eta12),2) - 3.*pow((Eta21 + Eta03),2)) + (3.*Eta21 - Eta03)*(Eta21 + Eta03)*(3.*pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2));
    
    Phi6 = ((Eta20 - Eta02 )*(pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2))) + 4.*Eta11*(Eta30 + Eta12)*(Eta21 + Eta03);
    
    Phi7 = (3.*Eta21 - Eta03)*(Eta30 + Eta12)*(pow((Eta30 + Eta12),2) - 3.*pow((Eta21 + Eta03),2)) - (Eta30 - 3.*Eta12)*(Eta21 + Eta03)*(3.*pow((Eta30 + Eta12),2) - pow((Eta21 + Eta03),2));
  }else{
    Phi1 = Phi2 = Phi3 = Phi4 = Phi5 = Phi6 = Phi7 = -999;
  }

  Skx = ( Mu20 > 0 ) ? Mu30/pow(Mu20,1.5) : -999;
  Sky = ( Mu02 > 0 ) ? Mu03/pow(Mu02,1.5) : -999;

  
  Z11 += tmp_Z11.Mod();
  Z20 += tmp_Z20.Mod();
  Z22 += tmp_Z22.Mod();
  Z31 += tmp_Z31.Mod();
  Z33 += tmp_Z33.Mod();
  Z40 += tmp_Z40.Mod();
  Z42 += tmp_Z42.Mod();
  Z44 += tmp_Z44.Mod();
  Z51 += tmp_Z51.Mod();
  Z53 += tmp_Z53.Mod();
  Z55 += tmp_Z55.Mod();


  jets_.gennCands[jets_.ngen] = nCands;
  jets_.gennChCands[jets_.ngen] = nChCands;
  jets_.gennNeCands[jets_.ngen] = nNeCands;
  jets_.genchargedSumConst[jets_.ngen] = chargedSumConst;
  jets_.genchargedNConst  [jets_.ngen] = chargedNConst;  
  jets_.geneSumConst      [jets_.ngen] = eSumConst;      
  jets_.geneNConst        [jets_.ngen] = eNConst;        
  jets_.genmuSumConst     [jets_.ngen] = muSumConst;     
  jets_.genmuNConst       [jets_.ngen] = muNConst;       
  jets_.genphotonSumConst [jets_.ngen] = photonSumConst; 
  jets_.genphotonNConst   [jets_.ngen] = photonNConst;   
  jets_.genneutralSumConst[jets_.ngen] = neutralSumConst;
  jets_.genneutralNConst  [jets_.ngen] = neutralNConst;  
  jets_.genhfhadSumConst  [jets_.ngen] = hfhadSumConst;
  jets_.genhfhadNConst    [jets_.ngen] = hfhadNConst;
  jets_.genhfemSumConst   [jets_.ngen] = hfemSumConst;
  jets_.genhfemNConst     [jets_.ngen] = hfemNConst;

  jets_.genMByPt[jets_.ngen] = jetMByPt;
  jets_.genRMSCand[jets_.ngen] = RMSCand;
  jets_.genAxis1[jets_.ngen] = Axis1;
  jets_.genAxis2[jets_.ngen] = Axis2;
  jets_.genSigma[jets_.ngen] = Sigma;
  jets_.genrm3[jets_.ngen] = rm3;
  jets_.genrm2[jets_.ngen] = rm2;
  jets_.genrm1[jets_.ngen] = rm1;
  jets_.genrm0p5[jets_.ngen] = rm0p5;
  jets_.genR[jets_.ngen] = R;
  jets_.genpull[jets_.ngen] = pull;
  jets_.genpTD[jets_.ngen] = pTD;
  jets_.genSDm[jets_.ngen] = sd_m;
  jets_.genSDpt[jets_.ngen] = sd_pt;
  jets_.genSDeta[jets_.ngen] = sd_eta;  
  jets_.genSDphi[jets_.ngen] = sd_phi;
  jets_.genSDptFrac[jets_.ngen] = sd_ptfrac;
  jets_.genSDrm0p5[jets_.ngen] = sd_rm0p5;
  jets_.genSDrm1[jets_.ngen] = sd_rm1;
  jets_.genSDrm2[jets_.ngen] = sd_rm2;
  jets_.genSDrm3[jets_.ngen] = sd_rm3; 

  jets_.genConstituentsId.push_back(jcid);
  jets_.genConstituentsE.push_back(jcE);
  jets_.genConstituentsPt.push_back(jcpt);
  jets_.genConstituentsEta.push_back(jceta);
  jets_.genConstituentsPhi.push_back(jcphi);
  jets_.genConstituentsM.push_back(jcm);
  jets_.genSDConstituentsId.push_back(jcSDid);
  jets_.genSDConstituentsE.push_back(jcSDE);
  jets_.genSDConstituentsPt.push_back(jcSDpt);
  jets_.genSDConstituentsEta.push_back(jcSDeta);
  jets_.genSDConstituentsPhi.push_back(jcSDphi);
  jets_.genSDConstituentsM.push_back(jcSDm);

  jets_.genTbeta20p2[jets_.ngen] = Tbeta20p2; 
  jets_.genTbeta20p3[jets_.ngen] = Tbeta20p3; 
  jets_.genTbeta20p4[jets_.ngen] = Tbeta20p4; 
  jets_.genTbeta20p5[jets_.ngen] = Tbeta20p5; 

  jets_.genTbeta30p2[jets_.ngen] = Tbeta30p2; 
  jets_.genTbeta30p3[jets_.ngen] = Tbeta30p3; 
  jets_.genTbeta30p4[jets_.ngen] = Tbeta30p4; 
  jets_.genTbeta30p5[jets_.ngen] = Tbeta30p5; 
			       
  jets_.genCbeta20p2[jets_.ngen] = Cbeta20p2; 
  jets_.genCbeta20p3[jets_.ngen] = Cbeta20p3; 
  jets_.genCbeta20p4[jets_.ngen] = Cbeta20p4; 
  jets_.genCbeta20p5[jets_.ngen] = Cbeta20p5; 

  jets_.genZ11[jets_.ngen] = Z11;
  jets_.genZ20[jets_.ngen] = Z20;
  jets_.genZ22[jets_.ngen] = Z22;
  jets_.genZ31[jets_.ngen] = Z31;
  jets_.genZ33[jets_.ngen] = Z33;
  jets_.genZ40[jets_.ngen] = Z40;
  jets_.genZ42[jets_.ngen] = Z42;
  jets_.genZ44[jets_.ngen] = Z44;
  jets_.genZ51[jets_.ngen] = Z51;
  jets_.genZ53[jets_.ngen] = Z53;
  jets_.genZ55[jets_.ngen] = Z55;


  jets_.genPhi1[jets_.ngen] = Phi1;
  jets_.genPhi2[jets_.ngen] = Phi2;
  jets_.genPhi3[jets_.ngen] = Phi3;
  jets_.genPhi4[jets_.ngen] = Phi4;
  jets_.genPhi5[jets_.ngen] = Phi5;
  jets_.genPhi6[jets_.ngen] = Phi6;
  jets_.genPhi7[jets_.ngen] = Phi7;

  jets_.genSkx[jets_.ngen] = Skx;
  jets_.genSky[jets_.ngen] = Sky;
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

  jets_.refptG[jets_.nref]  = -999.;
  jets_.refetaG[jets_.nref] = -999.;
  jets_.refphiG[jets_.nref] = -999.;
  jets_.refmG[jets_.nref]   = -999.;
  jets_.refsym[jets_.nref]  = -999.;
  jets_.refdroppedBranches[jets_.nref]  = -999;

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
    Ptr<reco::Jet> genJetPtr = gensubjets_->ptrAt(imatch);
    if(genSymVM_.isValid()) {
      float gensym = (*genSymVM_)[genJetPtr];
      jets_.refsym[jets_.nref] = gensym;
    }

    if(genDroppedBranchesVM_.isValid()) {
      int db = (*genDroppedBranchesVM_)[genJetPtr];
      jets_.refdroppedBranches[jets_.nref] = db;
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

  jets_.genptG[jets_.ngen]  = -999.;
  jets_.genetaG[jets_.ngen] = -999.;
  jets_.genphiG[jets_.ngen] = -999.;
  jets_.genmG[jets_.ngen]   = -999.;
  jets_.gensym[jets_.ngen]  = -999.;
  jets_.gendroppedBranches[jets_.ngen]  = -999;

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
    Ptr<reco::Jet> genJetPtr = gensubjets_->ptrAt(imatch);
    if(genSymVM_.isValid()) {
      float gensym = (*genSymVM_)[genJetPtr];
      jets_.gensym[jets_.ngen] = gensym;
      //std::cout << "gensym " << gensym << std::endl;
    }

    if(genDroppedBranchesVM_.isValid()) {
      int db = (*genDroppedBranchesVM_)[genJetPtr];
      jets_.gendroppedBranches[jets_.ngen] = db;
      //std::cout << "genDroppedBranches " << db << std::endl;
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
