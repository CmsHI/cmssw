#ifndef MNguyen_HiInclusiveJetAnalyzer_inclusiveJetAnalyzer_
#define MNguyen_HiInclusiveJetAnalyzer_inclusiveJetAnalyzer_

// system include files
#include <memory>
#include <string>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "TFile.h"
#include "TVector2.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TH1.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetup.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMapRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMap.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "fastjet/contrib/Njettiness.hh"
#include "TMVA/Reader.h"
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

  void fillL1Bits(const edm::Event &iEvent);

  void fillHLTBits(const edm::Event &iEvent);

  template <typename TYPE>
    void getProduct(const std::string name, edm::Handle<TYPE> &prod,
		    const edm::Event &event) const;
  template <typename TYPE>
    bool getProductSafe(const std::string name, edm::Handle<TYPE> &prod,
			const edm::Event &event) const;



private:

  int getPFJetMuon(const pat::Jet& pfJet, const reco::PFCandidateCollection *pfCandidateColl);

  double getPtRel(const reco::PFCandidate lep, const pat::Jet& jet );

  void saveDaughters( const reco::GenParticle & gen);
  void saveDaughters( const reco::Candidate & gen);
  double getEt(math::XYZPoint pos, double energy);
  math::XYZPoint getPosition(const DetId &id, reco::Vertex::Point vtx = reco::Vertex::Point(0,0,0));
  int TaggedJet(reco::Jet calojet, edm::Handle<reco::JetTagCollection > jetTags );
  float getTau(unsigned num, const reco::GenJet object) const;
  void analyzeSubjets(const reco::Jet jet);
  void fillNewJetVarsRecoJet(const reco::Jet jet);
  void fillNewJetVarsRefJet(const reco::GenJet jet);
  void fillNewJetVarsGenJet(const reco::GenJet jet);
  int  getGroomedGenJetIndex(const reco::GenJet jet) const;
  void analyzeRefSubjets(const reco::GenJet jet);
  void analyzeGenSubjets(const reco::GenJet jet);
  float getAboveCharmThresh(reco::TrackRefVector& selTracks, const reco::TrackIPTagInfo& ipData, int sigOrVal);
 
  std::auto_ptr<fastjet::contrib::Njettiness>   routine_;

  class ExtraInfo : public fastjet::PseudoJet::UserInfoBase {
  public:
  ExtraInfo(int id) : _index(id){}
    int part_id() const { return _index; }
  protected:
    int _index;
  };

  
  // edm::InputTag   jetTag_, vtxTag_, genjetTag_, eventInfoTag_, L1gtReadout_, pfCandidateLabel_, trackTag_, matchTag_;
  edm::InputTag   jetTagLabel_;
  edm::EDGetTokenT<std::vector<reco::Vertex> >       vtxTag_;
  edm::EDGetTokenT<reco::JetView>                    jetTag_;
  edm::EDGetTokenT<pat::JetCollection>               jetTagPat_;
  edm::EDGetTokenT<reco::JetView>                    matchTag_;
  edm::EDGetTokenT<pat::JetCollection>               matchTagPat_;
  edm::EDGetTokenT<reco::PFCandidateCollection>      pfCandidateLabel_;
  edm::EDGetTokenT<reco::TrackCollection>            trackTag_;
  edm::EDGetTokenT<reco::GenParticleCollection>      genParticleSrc_;
  //edm::EDGetTokenT<std::vector<reco::GenJet> >         genjetTag_;
  edm::EDGetTokenT<edm::View<reco::GenJet>>          genjetTag_;
  edm::EDGetTokenT<edm::HepMCProduct>                eventInfoTag_;
  edm::EDGetTokenT<GenEventInfoProduct>              eventGenInfoTag_;
  edm::EDGetTokenT< L1GlobalTriggerReadoutRecord >   L1gtReadout_;
  
  std::string                              jetName_; //used as prefix for jet structures
  edm::EDGetTokenT<edm::View<reco::Jet>>   subjetGenTag_;
  edm::Handle<reco::JetView>               gensubjets_;
  edm::EDGetTokenT< edm::ValueMap<float> > tokenGenTau1_;
  edm::EDGetTokenT< edm::ValueMap<float> > tokenGenTau2_;
  edm::EDGetTokenT< edm::ValueMap<float> > tokenGenTau3_;
  edm::EDGetTokenT< edm::ValueMap<float> > tokenGenSym_;
  edm::Handle<edm::ValueMap<float> >       genSymVM_;
  edm::EDGetTokenT< edm::ValueMap<int> >   tokenGenDroppedBranches_;
  edm::Handle<edm::ValueMap<int> >         genDroppedBranchesVM_;
  
  // towers
  edm::EDGetTokenT<CaloTowerCollection> TowerSrc_;

  std::vector<float> usedStringPts;

  //for the JetID BDT
  std::unique_ptr<TMVA::Reader> reader;
  std::unique_ptr<float[]> varAddr;

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
  double jetAbsEtaMax_;
  bool doGenTaus_;
  bool doGenSym_;
  bool doSubJets_;
  bool doJetConstituents_;
  bool doNewJetVars_;
  bool doGenSubJets_;

  TTree *t;
  edm::Service<TFileService> fs1;

  const CaloGeometry *geo;

  edm::EDGetTokenT<edm::TriggerResults> hltResName_;         //HLT trigger results name
  std::vector<std::string>      hltProcNames_;       //HLT process name(s)
  std::vector<std::string>      hltTrgNames_;        //HLT trigger name(s)

  std::vector<int>              hltTrgBits_;         //HLT trigger bit(s)
  std::vector<bool>             hltTrgDeci_;         //HLT trigger descision(s)
  std::vector<std::string>      hltTrgUsedNames_;    //HLT used trigger name(s)
  std::string                   hltUsedResName_;     //used HLT trigger results name
  std::string			jetIDweightFile_;

  std::string bTagJetName_;
  edm::EDGetTokenT<std::vector<reco::TrackIPTagInfo> > ImpactParameterTagInfos_;
  edm::EDGetTokenT<reco::JetTagCollection> TrackCountingHighEffBJetTags_;
  edm::EDGetTokenT<reco::JetTagCollection> TrackCountingHighPurBJetTags_;
  edm::EDGetTokenT<reco::JetTagCollection> JetProbabilityBJetTags_;
  edm::EDGetTokenT<reco::JetTagCollection> JetBProbabilityBJetTags_;
  edm::EDGetTokenT<std::vector<reco::SecondaryVertexTagInfo> > SecondaryVertexTagInfos_;
  edm::EDGetTokenT<reco::JetTagCollection> SimpleSecondaryVertexHighEffBJetTags_;
  edm::EDGetTokenT<reco::JetTagCollection> SimpleSecondaryVertexHighPurBJetTags_;
  edm::EDGetTokenT<reco::JetTagCollection> CombinedSecondaryVertexBJetTags_;
  edm::EDGetTokenT<reco::JetTagCollection> CombinedSecondaryVertexV2BJetTags_;

  static const int MAXJETS = 1000;
  static const int MAXTRACKS = 5000;
  static const int MAXHLTBITS = 5000;
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
    float jty[MAXJETS];
    float jtpu[MAXJETS];
    float jtm[MAXJETS];
    float jtarea[MAXJETS];
    int jtnCands[MAXJETS];
    int jtnChCands[MAXJETS];
    int jtnNeCands[MAXJETS];
    float jtchargedSumConst[MAXJETS];
    int   jtchargedNConst  [MAXJETS];
    float jteSumConst      [MAXJETS];
    int   jteNConst        [MAXJETS];
    float jtmuSumConst     [MAXJETS];
    int   jtmuNConst       [MAXJETS];
    float jtphotonSumConst [MAXJETS];
    int   jtphotonNConst   [MAXJETS];
    float jtneutralSumConst[MAXJETS];
    int   jtneutralNConst  [MAXJETS];
    float jthfhadSumConst  [MAXJETS];
    int   jthfhadNConst    [MAXJETS];
    float jthfemSumConst   [MAXJETS];
    int   jthfemNConst     [MAXJETS];

    float jtMByPt[MAXJETS];
    float jtRMSCand[MAXJETS];
    float jtAxis1[MAXJETS];
    float jtAxis2[MAXJETS];
    float jtSigma[MAXJETS];
    float jtR[MAXJETS];
    float jtpTD[MAXJETS];
    float jtrm0p5[MAXJETS];
    float jtrm1[MAXJETS];
    float jtrm2[MAXJETS];
    float jtrm3[MAXJETS];
    float jtpull[MAXJETS];
    float jtSDm[MAXJETS];
    float jtSDpt[MAXJETS];
    float jtSDeta[MAXJETS];
    float jtSDphi[MAXJETS];
    float jtSDptFrac[MAXJETS];
    float jtSDrm0p5[MAXJETS];
    float jtSDrm1[MAXJETS];
    float jtSDrm2[MAXJETS];
    float jtSDrm3[MAXJETS];
    
    float jtTbeta20p2[MAXJETS];
    float jtTbeta20p3[MAXJETS];
    float jtTbeta20p4[MAXJETS];
    float jtTbeta20p5[MAXJETS];
    float jtTbeta30p2[MAXJETS];
    float jtTbeta30p3[MAXJETS];
    float jtTbeta30p4[MAXJETS];
    float jtTbeta30p5[MAXJETS];
    float jtCbeta20p2[MAXJETS];
    float jtCbeta20p3[MAXJETS];
    float jtCbeta20p4[MAXJETS];
    float jtCbeta20p5[MAXJETS];
    float jtZ11[MAXJETS];
    float jtZ20[MAXJETS];
    float jtZ22[MAXJETS];
    float jtZ31[MAXJETS];
    float jtZ33[MAXJETS];
    float jtZ40[MAXJETS];
    float jtZ42[MAXJETS];
    float jtZ44[MAXJETS];
    float jtZ51[MAXJETS];
    float jtZ53[MAXJETS];
    float jtZ55[MAXJETS];
    float jtPhi1[MAXJETS];
    float jtPhi2[MAXJETS];
    float jtPhi3[MAXJETS];
    float jtPhi4[MAXJETS];
    float jtPhi5[MAXJETS];
    float jtPhi6[MAXJETS];
    float jtPhi7[MAXJETS];
    float jtSkx[MAXJETS];
    float jtSky[MAXJETS];


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

    float jtsym[MAXJETS];
    int   jtdroppedBranches[MAXJETS];
    
    std::vector<std::vector<float>> jtSubJetPt;
    std::vector<std::vector<float>> jtSubJetEta;
    std::vector<std::vector<float>> jtSubJetPhi;
    std::vector<std::vector<float>> jtSubJetM;

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
    float discr_muByIp3[MAXJETS];
    float discr_muByPt[MAXJETS];
    float discr_prob[MAXJETS];
    float discr_probb[MAXJETS];
    float discr_tcHighEff[MAXJETS];
    float discr_tcHighPur[MAXJETS];
    float discr_ssvHighEff[MAXJETS];
    float discr_ssvHighPur[MAXJETS];

    float ndiscr_ssvHighEff[MAXJETS];
    float ndiscr_ssvHighPur[MAXJETS];
    float ndiscr_csvV1[MAXJETS];
    float ndiscr_csvV2[MAXJETS];
    float ndiscr_muByPt[MAXJETS];

    float pdiscr_csvV1[MAXJETS];
    float pdiscr_csvV2[MAXJETS];

    int nsvtx[MAXJETS];
    int svtxntrk[MAXJETS];
    float svtxdl[MAXJETS];
    float svtxdls[MAXJETS];
    float svtxdl2d[MAXJETS];
    float svtxdls2d[MAXJETS];
    float svtxm[MAXJETS];
    float svtxpt[MAXJETS];
    float svtxmcorr[MAXJETS];
    float svtxnormchi2[MAXJETS];
    float svJetDeltaR[MAXJETS];
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

    float discr_fr01[MAXJETS];
    float discr_jetID_cuts[MAXJETS];
    float discr_jetID_bdt[MAXJETS];

    float refpt[MAXJETS];
    float refeta[MAXJETS];
    float refphi[MAXJETS];
    float refm[MAXJETS];
    float refarea[MAXJETS];
    float refy[MAXJETS];
    float reftau1[MAXJETS];
    float reftau2[MAXJETS];
    float reftau3[MAXJETS];
    float refsym[MAXJETS];
    int   refdroppedBranches[MAXJETS];
    float refdphijt[MAXJETS];
    float refdrjt[MAXJETS];
    float refparton_pt[MAXJETS];
    int refparton_flavor[MAXJETS];
    int refparton_flavorForB[MAXJETS];
    int refnCands[MAXJETS];
    int refnChCands[MAXJETS];
    int refnNeCands[MAXJETS];
    float refchargedSumConst[MAXJETS];
    int   refchargedNConst  [MAXJETS];
    float refeSumConst      [MAXJETS];
    int   refeNConst        [MAXJETS];
    float refmuSumConst     [MAXJETS];
    int   refmuNConst       [MAXJETS];
    float refphotonSumConst [MAXJETS];
    int   refphotonNConst   [MAXJETS];
    float refneutralSumConst[MAXJETS];
    int   refneutralNConst  [MAXJETS];
    float refhfhadSumConst  [MAXJETS];
    int   refhfhadNConst    [MAXJETS];
    float refhfemSumConst   [MAXJETS];
    int   refhfemNConst     [MAXJETS];

    float refMByPt[MAXJETS];
    float refRMSCand[MAXJETS];
    float refAxis1[MAXJETS];
    float refAxis2[MAXJETS];
    float refSigma[MAXJETS];
    float refR[MAXJETS];
    float refpTD[MAXJETS];
    float refrm0p5[MAXJETS];
    float refrm1[MAXJETS];
    float refrm2[MAXJETS];
    float refrm3[MAXJETS];
    float refpull[MAXJETS];
    float refSDm[MAXJETS];
    float refSDpt[MAXJETS];
    float refSDeta[MAXJETS];
    float refSDphi[MAXJETS];
    float refSDptFrac[MAXJETS];
    float refSDrm0p5[MAXJETS];
    float refSDrm1[MAXJETS];
    float refSDrm2[MAXJETS];
    float refSDrm3[MAXJETS];
    float refTbeta20p2[MAXJETS];
    float refTbeta20p3[MAXJETS];
    float refTbeta20p4[MAXJETS];
    float refTbeta20p5[MAXJETS];
    float refTbeta30p2[MAXJETS];
    float refTbeta30p3[MAXJETS];
    float refTbeta30p4[MAXJETS];
    float refTbeta30p5[MAXJETS];
    float refCbeta20p2[MAXJETS];
    float refCbeta20p3[MAXJETS];
    float refCbeta20p4[MAXJETS];
    float refCbeta20p5[MAXJETS];
    float refZ11[MAXJETS];
    float refZ20[MAXJETS];
    float refZ22[MAXJETS];
    float refZ31[MAXJETS];
    float refZ33[MAXJETS];
    float refZ40[MAXJETS];
    float refZ42[MAXJETS];
    float refZ44[MAXJETS];
    float refZ51[MAXJETS];
    float refZ53[MAXJETS];
    float refZ55[MAXJETS];
    float refPhi1[MAXJETS];
    float refPhi2[MAXJETS];
    float refPhi3[MAXJETS];
    float refPhi4[MAXJETS];
    float refPhi5[MAXJETS];
    float refPhi6[MAXJETS];
    float refPhi7[MAXJETS];
    float refSkx[MAXJETS];
    float refSky[MAXJETS];
    
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

    int gennCands[MAXJETS];
    int gennChCands[MAXJETS];
    int gennNeCands[MAXJETS];
    float genchargedSumConst[MAXJETS];
    int   genchargedNConst  [MAXJETS];
    float geneSumConst      [MAXJETS];
    int   geneNConst        [MAXJETS];
    float genmuSumConst     [MAXJETS];
    int   genmuNConst       [MAXJETS];
    float genphotonSumConst [MAXJETS];
    int   genphotonNConst   [MAXJETS];
    float genneutralSumConst[MAXJETS];
    int   genneutralNConst  [MAXJETS];
    float genhfhadSumConst  [MAXJETS];
    int   genhfhadNConst    [MAXJETS];
    float genhfemSumConst   [MAXJETS];
    int   genhfemNConst     [MAXJETS];

    float genMByPt[MAXJETS];
    float genRMSCand[MAXJETS];
    float genAxis1[MAXJETS];
    float genAxis2[MAXJETS];
    float genSigma[MAXJETS];
    float genR[MAXJETS];
    float genpTD[MAXJETS];
    float genrm0p5[MAXJETS];
    float genrm1[MAXJETS];
    float genrm2[MAXJETS];
    float genrm3[MAXJETS];
    float genpull[MAXJETS];

    float genSDm[MAXJETS];
    float genSDpt[MAXJETS];
    float genSDeta[MAXJETS];
    float genSDphi[MAXJETS];
    float genSDptFrac[MAXJETS];
    float genSDrm0p5[MAXJETS];
    float genSDrm1[MAXJETS];
    float genSDrm2[MAXJETS];
    float genSDrm3[MAXJETS];

    float genTbeta20p2[MAXJETS];
    float genTbeta20p3[MAXJETS];
    float genTbeta20p4[MAXJETS];
    float genTbeta20p5[MAXJETS];
    float genTbeta30p2[MAXJETS];
    float genTbeta30p3[MAXJETS];
    float genTbeta30p4[MAXJETS];
    float genTbeta30p5[MAXJETS];
    float genCbeta20p2[MAXJETS];
    float genCbeta20p3[MAXJETS];
    float genCbeta20p4[MAXJETS];
    float genCbeta20p5[MAXJETS];
    float genZ11[MAXJETS];
    float genZ20[MAXJETS];
    float genZ22[MAXJETS];
    float genZ31[MAXJETS];
    float genZ33[MAXJETS];
    float genZ40[MAXJETS];
    float genZ42[MAXJETS];
    float genZ44[MAXJETS];
    float genZ51[MAXJETS];
    float genZ53[MAXJETS];
    float genZ55[MAXJETS];
    float genPhi1[MAXJETS];
    float genPhi2[MAXJETS];
    float genPhi3[MAXJETS];
    float genPhi4[MAXJETS];
    float genPhi5[MAXJETS];
    float genPhi6[MAXJETS];
    float genPhi7[MAXJETS];
    float genSkx[MAXJETS];
    float genSky[MAXJETS];
    
    float genptG[MAXJETS];
    float genetaG[MAXJETS];
    float genphiG[MAXJETS];
    float genmG[MAXJETS];
    std::vector<std::vector<float>> genSubJetPt;
    std::vector<std::vector<float>> genSubJetEta;
    std::vector<std::vector<float>> genSubJetPhi;
    std::vector<std::vector<float>> genSubJetM;
    std::vector<std::vector<float>> genSubJetArea;
    float gensym[MAXJETS];
    int   gendroppedBranches[MAXJETS];
    
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

    // hlt
    int nHLTBit;
    bool hltBit[MAXHLTBITS];

    // l1
    int nL1TBit;
    bool l1TBit[MAXHLTBITS];
    int nL1ABit;
    bool l1ABit[MAXHLTBITS];

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
