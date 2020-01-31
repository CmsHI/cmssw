#ifndef MNguyen_HiInclusiveJetAnalyzer_inclusiveJetAnalyzer_
#define MNguyen_HiInclusiveJetAnalyzer_inclusiveJetAnalyzer_

// system include files
#include <memory>
#include <string>
#include <iostream>

// ROOT headers
#include "TTree.h"

// user include files
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include "RecoBTag/SecondaryVertex/interface/TrackKinematics.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "SimDataFormats/JetMatching/interface/JetFlavourInfo.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourInfoMatching.h"
#include "RecoBTag/SecondaryVertex/interface/V0Filter.h"
#include "RecoBTag/SecondaryVertex/interface/TrackSelector.h"

#include "fastjet/contrib/Njettiness.hh"
//

/**\class HiInclusiveJetAnalyzer

   \author Matt Nguyen
   \date   November 2010
*/

class HiInclusiveJetAnalyzer : public edm::EDAnalyzer {
public:

  explicit HiInclusiveJetAnalyzer(const edm::ParameterSet&);

  ~HiInclusiveJetAnalyzer();

  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  virtual void beginRun(const edm::Run & r, const edm::EventSetup & c);

  virtual void beginJob();

  template <typename TYPE>
    void getProduct(const std::string name, edm::Handle<TYPE> &prod,
		    const edm::Event &event) const;

  template <typename TYPE>
    bool getProductSafe(const std::string name, edm::Handle<TYPE> &prod,
			const edm::Event &event) const;

private:

  // for reWTA reclustering-----------------------
  bool doWTARecluster_ = false;
  fastjet::JetDefinition WTAjtDef = fastjet::JetDefinition(fastjet::JetAlgorithm::antikt_algorithm, 2, fastjet::WTA_pt_scheme);
  //--------------------------------------------

  int getPFJetMuon(const pat::Jet& pfJet, const reco::PFCandidateCollection *pfCandidateColl);

  double getPtRel(const reco::PFCandidate lep, const pat::Jet& jet );

  double getEt(math::XYZPoint pos, double energy);
  math::XYZPoint getPosition(const DetId &id, reco::Vertex::Point vtx = reco::Vertex::Point(0,0,0));
  int TaggedJet(reco::Jet calojet, edm::Handle<reco::JetTagCollection > jetTags );
  float getTau(unsigned num, const reco::GenJet object) const;
  void analyzeSubjets(const reco::Jet jet, int idx, edm::Handle<reco::JetFlavourInfoMatchingCollection>, edm::Handle<edm::View<reco::Jet> > );
  void fillNewJetVarsRecoJet(const reco::Jet jet);
  void fillNewJetVarsRefJet(const reco::GenJet jet);
  void fillNewJetVarsGenJet(const reco::GenJet jet);
  int  getGroomedGenJetIndex(const reco::GenJet jet) const;
  void analyzeRefSubjets(const reco::GenJet jet);
  void analyzeGenSubjets(const reco::GenJet jet);
  float getAboveCharmThresh(reco::TrackRefVector& selTracks, const reco::TrackIPTagInfo& ipData, int sigOrVal);

  int findMatchedParton(float eta, float phi, float maxDr, edm::Handle<reco::GenParticleCollection > genparts, int partonFlavor);
  int getFlavorProcess(int index, edm::Handle<reco::GenParticleCollection > genparts);

  reco::TrackSelector                     trackSelector; 
  reco::TrackSelector                     trackPseudoSelector;
  reco::V0Filter                          pseudoVertexV0Filter;
  reco::V0Filter                          trackPairV0Filter;
  std::auto_ptr<fastjet::contrib::Njettiness>   routine_;

  class ExtraInfo : public fastjet::PseudoJet::UserInfoBase {
  public:
  ExtraInfo(int id) : _index(id){}
    int part_id() const { return _index; }
  protected:
    int _index;
  };

  edm::InputTag   jetTagLabel_;
  edm::EDGetTokenT<std::vector<reco::Vertex>>    vtxTag_;
  edm::EDGetTokenT<reco::JetView>                jetTag_;
  edm::EDGetTokenT<pat::JetCollection>           jetTagPat_;
  edm::EDGetTokenT<reco::JetView>                matchTag_;
  edm::EDGetTokenT<pat::JetCollection>           matchTagPat_;
  edm::EDGetTokenT<reco::PFCandidateCollection>  pfCandidateLabel_;
  edm::EDGetTokenT<reco::TrackCollection>        trackTag_;
  edm::EDGetTokenT<reco::GenParticleCollection>  genParticleSrc_;
  edm::EDGetTokenT<std::vector<reco::GenJet>>    genjetTag_;
  edm::EDGetTokenT<reco::JetView>                subjetGenTag_;
  edm::EDGetTokenT<edm::HepMCProduct>            eventInfoTag_;
  edm::EDGetTokenT<GenEventInfoProduct>          eventGenInfoTag_;

  std::string jetName_; //used as prefix for jet structures
  edm::Handle<reco::JetView> gensubjets_;
  /* edm::EDGetTokenT< edm::ValueMap<float> > tokenGenTau1_; */
  /* edm::EDGetTokenT< edm::ValueMap<float> > tokenGenTau2_; */
  /* edm::EDGetTokenT< edm::ValueMap<float> > tokenGenTau3_; */

  // towers
  edm::EDGetTokenT<CaloTowerCollection> TowerSrc_;

  std::vector<float> usedStringPts;

  /// verbose ?
  bool verbose_;
  bool doMatch_;
  bool useVtx_;
  bool useJEC_;
  bool usePat_;
  bool doTower;
  bool isMC_;
  bool useHepMC_;
  bool fillGenJets_;
  bool doTrigger_;
  bool useQuality_;
  std::string trackQuality_;

  bool isPythia6_;

  bool doSubEvent_;
  double genPtMin_;
  bool doLifeTimeTagging_;
  bool doLifeTimeTaggingExtras_;
  bool saveBfragments_;
  bool skipCorrections_;
  bool doExtraCTagging_;

  bool doHiJetID_;
  bool doStandardJetID_;

  double rParam;
  double hardPtMin_;
  double jetPtMin_;
  bool doGenTaus_;
  bool doSubJets_;
  bool doJetConstituents_;
  bool doGenSubJets_;

  TTree *t;
  edm::Service<TFileService> fs1;

  std::string bTagJetName_;
  std::string ipTagInfos_;
  std::string svTagInfos_;
  std::string trackCHEBJetTags_;
  std::string trackCHPBJetTags_;
  std::string jetPBJetTags_;
  std::string jetBPBJetTags_;
  std::string simpleSVHighEffBJetTags_;
  std::string simpleSVHighPurBJetTags_;
  std::string combinedSVV1BJetTags_;
  std::string combinedSVV2BJetTags_;
  std::string deepCSVJetTags_;
  std::string deepCSVDiscriminatorJetTags_;

  bool doExtendedFlavorTagging_;
  edm::EDGetTokenT<reco::JetFlavourInfoMatchingCollection> jetFlavourInfosToken_;
  edm::EDGetTokenT<reco::JetFlavourInfoMatchingCollection> subjetFlavourInfosToken_;
  edm::EDGetTokenT<edm::View<reco::Jet> >                  groomedJetsToken_;
  bool                                                     useSubjets_;

  static const int MAXJETS = 1000;
  static const int MAXTRACKS = 5000;
  static const int MAXBFRAG = 500;

  struct JRA{

    int nref;
    int run;
    int evt;
    int lumi;
    int bin;
    float vx, vy, vz;
    float b;
    float hf;

    float rawpt[MAXJETS];
    float jtpt[MAXJETS];
    float jteta[MAXJETS];
    float jtphi[MAXJETS];

    //reWTA reclusted jet axis
    float WTAeta[MAXJETS];
    float WTAphi[MAXJETS];
    float WTAgeneta[MAXJETS];
    float WTAgenphi[MAXJETS];

    float jty[MAXJETS];
    float jtpu[MAXJETS];
    float jtm[MAXJETS];
    float jtarea[MAXJETS];

    float jtPfCHF[MAXJETS];
    float jtPfNHF[MAXJETS];
    float jtPfCEF[MAXJETS];
    float jtPfNEF[MAXJETS];
    float jtPfMUF[MAXJETS];

    int jtPfCHM[MAXJETS];
    int jtPfNHM[MAXJETS];
    int jtPfCEM[MAXJETS];
    int jtPfNEM[MAXJETS];
    int jtPfMUM[MAXJETS];
    
    float jttau1[MAXJETS];
    float jttau2[MAXJETS];
    float jttau3[MAXJETS];

    float jtHadronFlavor[MAXJETS];
    float jtPartonFlavor[MAXJETS];

    std::vector<std::vector<float>> jtSubJetPt;
    std::vector<std::vector<float>> jtSubJetEta;
    std::vector<std::vector<float>> jtSubJetPhi;
    std::vector<std::vector<float>> jtSubJetM;
    std::vector<std::vector<float>> jtSubJetHadronFlavor;
    std::vector<std::vector<float>> jtSubJetPartonFlavor; 

    std::vector<std::vector<std::vector<float>>> jtSubJetHadronDR;
    std::vector<std::vector<std::vector<float>>> jtSubJetHadronPt;
    std::vector<std::vector<std::vector<float>>> jtSubJetHadronEta;
    std::vector<std::vector<std::vector<float>>> jtSubJetHadronPhi;
    std::vector<std::vector<std::vector<float>>> jtSubJetHadronPdg;
    std::vector<std::vector<std::vector<float>>> jtSubJetPartonDR;
    std::vector<std::vector<std::vector<float>>> jtSubJetPartonPt;
    std::vector<std::vector<std::vector<float>>> jtSubJetPartonEta;
    std::vector<std::vector<std::vector<float>>> jtSubJetPartonPhi;
    std::vector<std::vector<std::vector<float>>> jtSubJetPartonPdg;


    std::vector<std::vector<int>> jtConstituentsId;
    std::vector<std::vector<float>> jtConstituentsE;
    std::vector<std::vector<float>> jtConstituentsPt;
    std::vector<std::vector<float>> jtConstituentsEta;
    std::vector<std::vector<float>> jtConstituentsPhi;
    std::vector<std::vector<float>> jtConstituentsM;
    std::vector<std::vector<int>> jtSDConstituentsId;
    std::vector<std::vector<float>> jtSDConstituentsE;
    std::vector<std::vector<float>> jtSDConstituentsPt;
    std::vector<std::vector<float>> jtSDConstituentsEta;
    std::vector<std::vector<float>> jtSDConstituentsPhi;
    std::vector<std::vector<float>> jtSDConstituentsM;

    float trackMax[MAXJETS];
    float trackSum[MAXJETS];
    int trackN[MAXJETS];

    float chargedMax[MAXJETS];
    float chargedSum[MAXJETS];
    int chargedN[MAXJETS];

    float photonMax[MAXJETS];
    float photonSum[MAXJETS];
    int photonN[MAXJETS];

    float trackHardSum[MAXJETS];
    float chargedHardSum[MAXJETS];
    float photonHardSum[MAXJETS];

    int trackHardN[MAXJETS];
    int chargedHardN[MAXJETS];
    int photonHardN[MAXJETS];

    float neutralMax[MAXJETS];
    float neutralSum[MAXJETS];
    int neutralN[MAXJETS];

    float eMax[MAXJETS];
    float eSum[MAXJETS];
    int eN[MAXJETS];

    float muMax[MAXJETS];
    float muSum[MAXJETS];
    int muN[MAXJETS];

    float genChargedSum[MAXJETS];
    float genHardSum[MAXJETS];
    float signalChargedSum[MAXJETS];
    float signalHardSum[MAXJETS];

    // Update by Raghav, modified to take it from the towers
    float hcalSum[MAXJETS];
    float ecalSum[MAXJETS];

    float fHPD[MAXJETS];
    float fRBX[MAXJETS];
    int n90[MAXJETS];
    float fSubDet1[MAXJETS];
    float fSubDet2[MAXJETS];
    float fSubDet3[MAXJETS];
    float fSubDet4[MAXJETS];
    float restrictedEMF[MAXJETS];
    int nHCAL[MAXJETS];
    int nECAL[MAXJETS];
    float apprHPD[MAXJETS];
    float apprRBX[MAXJETS];

    //    int n90[MAXJETS];
    int n2RPC[MAXJETS];
    int n3RPC[MAXJETS];
    int nRPC[MAXJETS];

    float fEB[MAXJETS];
    float fEE[MAXJETS];
    float fHB[MAXJETS];
    float fHE[MAXJETS];
    float fHO[MAXJETS];
    float fLong[MAXJETS];
    float fShort[MAXJETS];
    float fLS[MAXJETS];
    float fHFOOT[MAXJETS];

    int subid[MAXJETS];

    float matchedPt[MAXJETS];
    float matchedRawPt[MAXJETS];
    float matchedR[MAXJETS];
    float matchedPu[MAXJETS];

    float discr_csvV1[MAXJETS];
    float discr_csvV2[MAXJETS];
    float discr_deepCSV[MAXJETS];
    float discr_muByIp3[MAXJETS];
    float discr_muByPt[MAXJETS];
    float discr_prob[MAXJETS];
    float discr_probb[MAXJETS];
    float discr_tcHighEff[MAXJETS];
    float discr_tcHighPur[MAXJETS];
    float discr_ssvHighEff[MAXJETS];
    float discr_ssvHighPur[MAXJETS];


    int nsvtx[MAXJETS];
    std::vector<std::vector<int> >svType;
    std::vector<std::vector<int> >svtxntrk;
    std::vector<std::vector<float> >svtxdl;
    std::vector<std::vector<float> >svtxdls;
    std::vector<std::vector<float> >svtxdl2d;
    std::vector<std::vector<float> >svtxdls2d;
    std::vector<std::vector<float> >svtxm;
    std::vector<std::vector<float> >svtxpt;
    float svtxmcorr[MAXJETS];
    float svtxnormchi2[MAXJETS];
    std::vector<std::vector<float> >svJetDeltaR;
    float svtxTrkSumChi2[MAXJETS];
    int svtxTrkNetCharge[MAXJETS];
    int svtxNtrkInCone[MAXJETS];

    int nIPtrk[MAXJETS];
    int nselIPtrk[MAXJETS];

    int nIP;
    int ipJetIndex[MAXTRACKS];
    float ipPt[MAXTRACKS];
    float ipEta[MAXTRACKS];
    float ipDxy[MAXTRACKS];
    float ipDz[MAXTRACKS];
    float ipChi2[MAXTRACKS];
    int ipNHit[MAXTRACKS];
    int ipNHitPixel[MAXTRACKS];
    int ipNHitStrip[MAXTRACKS];
    bool ipIsHitL1[MAXTRACKS];
    float ipProb0[MAXTRACKS];
    float ipProb1[MAXTRACKS];
    float ip2d[MAXTRACKS];
    float ip2dSig[MAXTRACKS];
    float ip3d[MAXTRACKS];
    float ip3dSig[MAXTRACKS];
    float ipDist2Jet[MAXTRACKS];
    float ipDist2JetSig[MAXTRACKS];
    float ipClosest2Jet[MAXTRACKS];
  
    float trackPtRel[MAXTRACKS];
    float trackPtRatio[MAXTRACKS];
    float trackPPar[MAXTRACKS];
    float trackPParRatio[MAXTRACKS];
    float trackDeltaR[MAXTRACKS];

    float trackSip2dSigAboveCharm[MAXJETS];
    float trackSip2dValAboveCharm[MAXJETS];
    float trackSip3dValAboveCharm[MAXJETS];
    float trackSip3dSigAboveCharm[MAXJETS];
    float trackSumJetDeltaR[MAXJETS];

    float mue[MAXJETS];
    float mupt[MAXJETS];
    float mueta[MAXJETS];
    float muphi[MAXJETS];
    float mudr[MAXJETS];
    float muptrel[MAXJETS];
    int muchg[MAXJETS];

    int refparton_flavorProcess[MAXJETS];
    float refGSP_gpt [MAXJETS];
    float refGSP_geta [MAXJETS];
    float refGSP_gphi [MAXJETS];
    float refGSP_gidx [MAXJETS];
    float refGSP_b1pt [MAXJETS];
    float refGSP_b1eta [MAXJETS];
    float refGSP_b1phi [MAXJETS];
    float refGSP_b2pt [MAXJETS];
    float refGSP_b2eta [MAXJETS];
    float refGSP_b2phi [MAXJETS];
    float refGSP_b1Match_jtdR [MAXJETS];
    float refGSP_b2Match_jtdR [MAXJETS];
    float refGSP_bbdR [MAXJETS];
    float refGSP_bbzg [MAXJETS];
    int refGSP_SubJtMatched [MAXJETS];

    float refpt[MAXJETS];
    float refeta[MAXJETS];
    float refphi[MAXJETS];
    float refm[MAXJETS];
    float refarea[MAXJETS];
    float refy[MAXJETS];
    float reftau1[MAXJETS];
    float reftau2[MAXJETS];
    float reftau3[MAXJETS];
    float refdphijt[MAXJETS];
    float refdrjt[MAXJETS];
    float refparton_pt[MAXJETS];
    int refparton_flavor[MAXJETS];

    float refptG[MAXJETS];
    float refetaG[MAXJETS];
    float refphiG[MAXJETS];
    float refmG[MAXJETS];
    std::vector<std::vector<float>> refSubJetPt;
    std::vector<std::vector<float>> refSubJetEta;
    std::vector<std::vector<float>> refSubJetPhi;
    std::vector<std::vector<float>> refSubJetM;
    
    std::vector<std::vector<int>> refConstituentsId;
    std::vector<std::vector<float>> refConstituentsE;
    std::vector<std::vector<float>> refConstituentsPt;
    std::vector<std::vector<float>> refConstituentsEta;
    std::vector<std::vector<float>> refConstituentsPhi;
    std::vector<std::vector<float>> refConstituentsM;
    std::vector<std::vector<int>> refSDConstituentsId;
    std::vector<std::vector<float>> refSDConstituentsE;
    std::vector<std::vector<float>> refSDConstituentsPt;
    std::vector<std::vector<float>> refSDConstituentsEta;
    std::vector<std::vector<float>> refSDConstituentsPhi;
    std::vector<std::vector<float>> refSDConstituentsM;

    float pthat;
    int beamId1, beamId2;
    int ngen;
    int genmatchindex[MAXJETS];
    float genpt[MAXJETS];
    float geneta[MAXJETS];
    float genphi[MAXJETS];
    float genm[MAXJETS];
    float geny[MAXJETS];
    float gentau1[MAXJETS];
    float gentau2[MAXJETS];
    float gentau3[MAXJETS];
    float gendphijt[MAXJETS];
    float gendrjt[MAXJETS];
    int gensubid[MAXJETS];

    float genptG[MAXJETS];
    float genetaG[MAXJETS];
    float genphiG[MAXJETS];
    float genmG[MAXJETS];
    std::vector<std::vector<float>> genSubJetPt;
    std::vector<std::vector<float>> genSubJetEta;
    std::vector<std::vector<float>> genSubJetPhi;
    std::vector<std::vector<float>> genSubJetM;
    std::vector<std::vector<float>> genSubJetArea;

    std::vector<std::vector<int>> genConstituentsId;
    std::vector<std::vector<float>> genConstituentsE;
    std::vector<std::vector<float>> genConstituentsPt;
    std::vector<std::vector<float>> genConstituentsEta;
    std::vector<std::vector<float>> genConstituentsPhi;
    std::vector<std::vector<float>> genConstituentsM;
    std::vector<std::vector<int>> genSDConstituentsId;
    std::vector<std::vector<float>> genSDConstituentsE;
    std::vector<std::vector<float>> genSDConstituentsPt;
    std::vector<std::vector<float>> genSDConstituentsEta;
    std::vector<std::vector<float>> genSDConstituentsPhi;
    std::vector<std::vector<float>> genSDConstituentsM;

    int bMult;
    int bJetIndex[MAXBFRAG];
    int bStatus[MAXBFRAG];
    int bPdg[MAXBFRAG];
    int bChg[MAXBFRAG];
    float bVx[MAXBFRAG];
    float bVy[MAXBFRAG];
    float bVz[MAXBFRAG];
    float bPt[MAXBFRAG];
    float bEta[MAXBFRAG];
    float bPhi[MAXBFRAG];
  };

  JRA jets_;

};

#endif
