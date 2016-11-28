#include <iostream>
#include <sstream>
#include <istream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include <functional>
#include <stdlib.h>
#include <string.h>

#include "HLTrigger/HLTanalyzers/interface/HLTStage2Info.h"
#include "FWCore/Common/interface/TriggerNames.h"

// L1 related
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"

HLTStage2Info::HLTStage2Info() {

  //set parameter defaults 
  _Debug=false;
}

void HLTStage2Info::beginRun(const edm::Run& run, const edm::EventSetup& c){ 


  bool changed(true);
  if (hltConfigProvider_->init(run,c,processName_,changed)) {
    // if init returns TRUE, initialisation has succeeded!
    if (changed) {
      // The HLT config has actually changed wrt the previous Run, hence rebook your
      // histograms or do anything else dependent on the revised HLT config
      std::cout << "Initalizing HLTConfigProvider"  << std::endl;
    }
  } else {
    // if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
    // with the file and/or code and needs to be investigated!
    std::cout << " HLT config extraction failure with process name " << processName_ << std::endl;
    // In this case, all access methods will return empty values!
  }
  l1tGlobalUtil_->setUnprescaledUnmasked(!getPrescales_, true);
  l1tGlobalUtil_->retrieveL1Setup(c);

}

/*  Setup the analysis to put the branch-variables into the tree. */
void HLTStage2Info::setup(const edm::ParameterSet& pSet, TTree* HltTree) {

  processName_ = pSet.getParameter<std::string>("HLTProcessName") ;

  edm::ParameterSet myHltParams = pSet.getParameter<edm::ParameterSet>("RunParameters") ;
  std::vector<std::string> parameterNames = myHltParams.getParameterNames() ;
  
  for ( std::vector<std::string>::iterator iParam = parameterNames.begin();
        iParam != parameterNames.end(); iParam++ ){
    if ( (*iParam) == "Debug" ) _Debug =  myHltParams.getParameter<bool>( *iParam );
  }

  getPrescales_ = pSet.getUntrackedParameter<bool>("getPrescales", false);
  getL1InfoFromEventSetup_ = pSet.getUntrackedParameter<bool>("getL1InfoFromEventSetup", true);
  dummyBranches_ = pSet.getUntrackedParameter<std::vector<std::string> >("dummyBranches",std::vector<std::string>(0));

  HltEvtCnt = 0;
  const int kMaxTrigFlag = 10000;
  trigflag = new int[kMaxTrigFlag];
  trigPrescl = new int[kMaxTrigFlag];
  L1TEvtCnt = 0;
  const int kMaxL1TFlag = 10000;
  l1TInitialFlag = new int[kMaxL1TFlag];
  l1TFinalFlag = new int[kMaxL1TFlag];
  l1TPrescl = new int[kMaxL1TFlag];
  const int kMaxHLTPart = 10000;
  hltppt = new float[kMaxHLTPart];
  hltpeta = new float[kMaxHLTPart];
  const int kMaxL1Stage2EG = 10000;
  l1stage2eget = new float[kMaxL1Stage2EG];
  l1stage2ege = new float[kMaxL1Stage2EG];
  l1stage2egeta = new float[kMaxL1Stage2EG];
  l1stage2egphi = new float[kMaxL1Stage2EG];
  l1stage2egiso = new int[kMaxL1Stage2EG];
  l1stage2egbx = new int[kMaxL1Stage2EG];
  const int kMaxL1Stage2Mu = 10000;
  l1stage2mupt = new float[kMaxL1Stage2Mu];
  l1stage2mue = new float[kMaxL1Stage2Mu];
  l1stage2mueta = new float[kMaxL1Stage2Mu];
  l1stage2muphi = new float[kMaxL1Stage2Mu];
  l1stage2muiso = new int[kMaxL1Stage2Mu];
  l1stage2muqul = new int[kMaxL1Stage2Mu];
  l1stage2muchg = new int[kMaxL1Stage2Mu];
  l1stage2mubx = new int[kMaxL1Stage2Mu];
  l1stage2mutfidx = new int[kMaxL1Stage2Mu];
  l1stage2mutfreg = new int[kMaxL1Stage2Mu];
  const int kMaxL1Stage2DiMu = 10000;
  l1stage2dimumass = new float[kMaxL1Stage2DiMu];
  l1stage2dimupt = new float[kMaxL1Stage2DiMu];
  l1stage2dimurap = new float[kMaxL1Stage2DiMu];
  l1stage2dimuphi = new float[kMaxL1Stage2DiMu];
  l1stage2dimudr = new float[kMaxL1Stage2DiMu];
  l1stage2dimuchg = new int[kMaxL1Stage2DiMu];
  l1stage2dimuidx1 = new int[kMaxL1Stage2DiMu];
  l1stage2dimuidx2 = new int[kMaxL1Stage2DiMu];
  const int kMaxL1Stage2Jt = 10000;
  l1stage2jtet = new float[kMaxL1Stage2Jt];
  l1stage2jte = new float[kMaxL1Stage2Jt];
  l1stage2jteta = new float[kMaxL1Stage2Jt];
  l1stage2jtphi = new float[kMaxL1Stage2Jt];
  l1stage2jtbx = new int[kMaxL1Stage2Jt];
  const int kMaxL1Stage2Tau = 10000;
  l1stage2tauet = new float[kMaxL1Stage2Tau];
  l1stage2taue = new float[kMaxL1Stage2Tau];
  l1stage2taueta = new float[kMaxL1Stage2Tau];
  l1stage2tauphi = new float[kMaxL1Stage2Tau];
  l1stage2taubx = new int[kMaxL1Stage2Tau];
  const int kMaxL1Stage2EtS = 10000;
  l1stage2etset = new float[kMaxL1Stage2EtS];
  l1stage2etsphi = new float[kMaxL1Stage2EtS];
  l1stage2etshwet = new int[kMaxL1Stage2EtS];
  l1stage2etshwphi = new int[kMaxL1Stage2EtS];
  l1stage2etstype = new int[kMaxL1Stage2EtS];
  l1stage2etsbx = new int[kMaxL1Stage2EtS];

  algoBitToName.clear();

  HltTree->Branch("NL1EGamma",&nl1stage2eg,"NL1Stage2EGamma/I");
  HltTree->Branch("L1Stage2EGammaEt",l1stage2eget,"L1Stage2EGammaEt[NL1Stage2EGamma]/F");
  HltTree->Branch("L1Stage2EGammaE",l1stage2ege,"L1Stage2EGammaE[NL1Stage2EGamma]/F");
  HltTree->Branch("L1Stage2EGammaEta",l1stage2egeta,"L1Stage2EGammaEta[NL1Stage2EGamma]/F");
  HltTree->Branch("L1Stage2EGammaPhi",l1stage2egphi,"L1Stage2EGammaPhi[NL1Stage2EGamma]/F");
  HltTree->Branch("L1Stage2EGammaIsol",l1stage2egiso,"L1Stage2EGammaIsol[NL1Stage2EGamma]/I");
  HltTree->Branch("L1Stage2EGammaBx",l1stage2egbx,"L1Stage2EGammaBx[NL1Stage2EGamma]/I");
  HltTree->Branch("NL1Stage2Muon",&nl1stage2mu,"NL1Stage2Muon/I");
  HltTree->Branch("L1Stage2MuonPt",l1stage2mupt,"L1Stage2MuonPt[NL1Stage2Muon]/F");
  HltTree->Branch("L1Stage2MuonE",l1stage2mue,"L1Stage2MuonE[NL1Stage2Muon]/F");
  HltTree->Branch("L1Stage2MuonEta",l1stage2mueta,"L1Stage2MuonEta[NL1Stage2Muon]/F");
  HltTree->Branch("L1Stage2MuonPhi",l1stage2muphi,"L1Stage2MuonPhi[NL1Stage2Muon]/F");
  HltTree->Branch("L1Stage2MuonIsol",l1stage2muiso,"L1Stage2MuonIsol[NL1Stage2Muon]/I");
  HltTree->Branch("L1Stage2MuonQual",l1stage2muqul,"L1Stage2MuonQual[NL1Stage2Muon]/I");
  HltTree->Branch("L1Stage2MuonChg",l1stage2muchg,"L1Stage2MuonChg[NL1Stage2Muon]/I");
  HltTree->Branch("L1Stage2MuontfMuonIndex",l1stage2mutfidx,"L1Stage2MuontfMuonIndex[NL1Stage2Muon]/I");
  HltTree->Branch("L1Stage2MuontfRegion",l1stage2mutfreg,"L1Stage2MuontfRegion[NL1Stage2Muon]/I");
  HltTree->Branch("L1Stage2MuonBx",l1stage2mubx,"L1Stage2MuonBx[NL1Stage2Muon]/I");
  HltTree->Branch("NL1Stage2DiMuon",&nl1stage2dimu,"NL1Stage2DiMuon/I");
  HltTree->Branch("L1Stage2DiMuonPt",l1stage2dimupt,"L1Stage2DiMuonPt[NL1Stage2DiMuon]/F");
  HltTree->Branch("L1Stage2DiMuonRap",l1stage2dimurap,"L1Stage2DiMuonRap[NL1Stage2DiMuon]/F");
  HltTree->Branch("L1Stage2DiMuonPhi",l1stage2dimuphi,"L1Stage2DiMuonPhi[NL1Stage2DiMuon]/F");
  HltTree->Branch("L1Stage2DiMuonInvMass",l1stage2dimumass,"L1Stage2DiMuonInvMass[NL1Stage2DiMuon]/F");
  HltTree->Branch("L1Stage2DiMuondR",l1stage2dimudr,"L1Stage2DiMuondR[NL1Stage2DiMuon]/F");
  HltTree->Branch("L1Stage2DiMuonChg",l1stage2dimuchg,"L1Stage2DiMuonChg[NL1Stage2DiMuon]/I");
  HltTree->Branch("L1Stage2DiMuonIdx1",l1stage2dimuidx1,"L1Stage2DiMuonIdx1[NL1Stage2DiMuon]/I");
  HltTree->Branch("L1Stage2DiMuonIdx2",l1stage2dimuidx2,"L1Stage2DiMuonIdx2[NL1Stage2DiMuon]/I");
  HltTree->Branch("NL1Stage2Jet",&nl1stage2jet,"NL1Stage2Jet/I");
  HltTree->Branch("L1Stage2JetEt",l1stage2jtet,"L1Stage2JetEt[NL1Stage2Jet]/F");
  HltTree->Branch("L1Stage2JetE",l1stage2jte,"L1Stage2JetE[NL1Stage2Jet]/F");
  HltTree->Branch("L1Stage2JetEta",l1stage2jteta,"L1Stage2JetEta[NL1Stage2Jet]/F");
  HltTree->Branch("L1Stage2JetPhi",l1stage2jtphi,"L1Stage2JetPhi[NL1Stage2Jet]/F");
  HltTree->Branch("L1Stage2JetBx",l1stage2jtbx,"L1Stage2JetBx[NL1Stage2Jet]/I");
  HltTree->Branch("NL1Stage2Tau",&nl1stage2tau,"NL1Stage2Tau/I");
  HltTree->Branch("L1Stage2TauEt",l1stage2tauet,"L1Stage2TauEt[NL1Stage2Tau]/F");
  HltTree->Branch("L1Stage2TauE",l1stage2taue,"L1Stage2TauE[NL1Stage2Tau]/F");
  HltTree->Branch("L1Stage2TauEta",l1stage2taueta,"L1Stage2TauEta[NL1Stage2Tau]/F");
  HltTree->Branch("L1Stage2TauPhi",l1stage2tauphi,"L1Stage2TauPhi[NL1Stage2Tau]/F");
  HltTree->Branch("L1Stage2TauBx",l1stage2taubx,"L1Stage2TauBx[NL1Stage2Tau]/I");
  HltTree->Branch("NL1Stage2EtSum",&nl1stage2ets,"NL1Stage2EtSum/I");
  HltTree->Branch("L1Stage2EtSumEt",l1stage2etset,"L1Stage2EtSumEt[NL1Stage2EtSum]/F");
  HltTree->Branch("L1Stage2EtSumPhi",l1stage2etsphi,"L1Stage2EtSumPhi[NL1Stage2EtSum]/F");
  HltTree->Branch("L1Stage2EtSumHwEt",l1stage2etshwet,"L1Stage2EtSumHwEt[NL1Stage2EtSum]/I");
  HltTree->Branch("L1Stage2EtSumHwPhi",l1stage2etshwphi,"L1Stage2EtSumHwPhi[NL1Stage2EtSum]/I");
  HltTree->Branch("L1Stage2EtSumType",l1stage2etstype,"L1Stage2EtSumType[NL1Stage2EtSum]/I");
  HltTree->Branch("L1Stage2EtSumBx",l1stage2etsbx,"L1Stage2EtSumBx[NL1Stage2EtSum]/I");
}

/* **Analyze the event** */
void HLTStage2Info::analyze(const edm::Handle<edm::TriggerResults>                 & hltresults,
                            const edm::Handle< BXVector<l1t::EGamma> >             & L1Stage2EGamma,
                            const edm::Handle< BXVector<l1t::Muon> >               & L1Stage2Muon,
                            const edm::Handle< BXVector<l1t::Jet> >                & L1Stage2Jet,
                            const edm::Handle< BXVector<l1t::Tau> >                & L1Stage2Tau,
                            const edm::Handle< BXVector<l1t::EtSum> >              & L1Stage2EtSum,
                            const edm::Handle<GlobalObjectMapRecord>               & L1GOMR,
                            edm::EventSetup const& eventSetup,
                            edm::Event const& iEvent,
                            TTree* HltTree) {
  
  //   std::cout << " Beginning HLTStage2Info " << std::endl;

  l1tGlobalUtil_->retrieveL1Event(iEvent,eventSetup);

  /////////// Analyzing HLT Trigger Results (TriggerResults) //////////
  if (hltresults.isValid()) {
    int ntrigs = hltresults->size();
    if (ntrigs==0){std::cout << "%HLTStage2Info -- No trigger name given in TriggerResults of the input " << std::endl;}

    edm::TriggerNames const& triggerNames = iEvent.triggerNames(*hltresults);

    // 1st event : Book as many branches as trigger paths provided in the input...
    if (HltEvtCnt==0){
      for (int itrig = 0; itrig != ntrigs; ++itrig) {
        TString trigName = triggerNames.triggerName(itrig);
        HltTree->Branch(trigName,trigflag+itrig,trigName+"/I");
        HltTree->Branch(trigName+"_Prescl",trigPrescl+itrig,trigName+"_Prescl/I");
      }

      int itdum = ntrigs;
      for (unsigned int idum = 0; idum < dummyBranches_.size(); ++idum) {
	TString trigName(dummyBranches_[idum].data());
	bool addThisBranch = 1;
	for (int itrig = 0; itrig != ntrigs; ++itrig) {
	  TString realTrigName = triggerNames.triggerName(itrig);
	  if(trigName == realTrigName) addThisBranch = 0;
	}
	if(addThisBranch){
	  HltTree->Branch(trigName,trigflag+itdum,trigName+"/I");
	  HltTree->Branch(trigName+"_Prescl",trigPrescl+itdum,trigName+"_Prescl/I");
	  trigflag[itdum] = 0;
	  trigPrescl[itdum] = 0;
	  ++itdum;
	}
      }

      HltEvtCnt++;
    }
    // ...Fill the corresponding accepts in branch-variables 

    for (int itrig = 0; itrig != ntrigs; ++itrig){

      std::string trigName=triggerNames.triggerName(itrig);
      bool accept = hltresults->accept(itrig);

      trigPrescl[itrig] = hltConfigProvider_->prescaleValue(l1tGlobalUtil_->prescaleColumn(), trigName);


      if (accept){trigflag[itrig] = 1;}
      else {trigflag[itrig] = 0;}

      if (_Debug){
        if (_Debug) std::cout << "%HLTStage2Info --  Number of HLT Triggers: " << ntrigs << std::endl;
        std::cout << "%HLTStage2Info --  HLTTrigger(" << itrig << "): " << trigName << " = " << accept << std::endl;
      }
    }
  }
  else { if (_Debug) std::cout << "%HLTStage2Info -- No Trigger Result" << std::endl;}

  /////////// Analyzing L1 Stage2 objects //////////

  if (L1Stage2EGamma.isValid()) {
    int il1stage2eg = 0;
    typedef std::vector<l1t::EGamma>::const_iterator l1cand;
    for(int iBx = L1Stage2EGamma->getFirstBX(); iBx <= L1Stage2EGamma->getLastBX(); ++iBx) { 
      for (l1cand egItr=L1Stage2EGamma->begin(iBx); egItr!=L1Stage2EGamma->end(iBx); ++egItr) {
        l1stage2eget[il1stage2eg]  = egItr->et();
        l1stage2ege[il1stage2eg]   = egItr->energy();
        l1stage2egeta[il1stage2eg] = egItr->eta();
        l1stage2egphi[il1stage2eg] = egItr->phi();
        l1stage2egiso[il1stage2eg] = egItr->hwIso();
        l1stage2egbx[il1stage2eg]  = iBx;
        il1stage2eg++;
      }
    }
    nl1stage2eg = il1stage2eg;
  }
  else {
    nl1stage2eg = 0;
    if (_Debug) std::cout << "%HLTStage2Info -- No L1 Stage2 EGamma object" << std::endl;
  }

  if (L1Stage2Muon.isValid()) {
    int il1stage2mu = 0, jl1stage2mu = 0, il1stage2dimu = 0;
    typedef std::vector<l1t::Muon>::const_iterator l1cand;
    for(int iBx = L1Stage2Muon->getFirstBX(); iBx <= L1Stage2Muon->getLastBX(); ++iBx) { 
      for (l1cand muItr=L1Stage2Muon->begin(iBx); muItr!=L1Stage2Muon->end(iBx); ++muItr) {
        l1stage2mupt[il1stage2mu]  = muItr->pt();
        l1stage2mue[il1stage2mu]   = muItr->energy();
        l1stage2mueta[il1stage2mu] = muItr->eta();
        l1stage2muphi[il1stage2mu] = muItr->phi();
        l1stage2muiso[il1stage2mu] = muItr->hwIso();
        l1stage2muchg[il1stage2mu] = muItr->charge();
        l1stage2muqul[il1stage2mu] = muItr->hwQual(); // Muon quality at hardware level
        l1stage2mubx[il1stage2mu]  = iBx;
        l1stage2mutfidx[il1stage2mu] = muItr->tfMuonIndex(); // Muon Track Finder Index
        l1stage2mutfreg[il1stage2mu] = -1;
        if ( muItr->tfMuonIndex()>35 && muItr->tfMuonIndex()<72 ) l1stage2mutfreg[il1stage2mu] = 0; // Barrel Muon Track Finder
        else if ( (muItr->tfMuonIndex()>17 && muItr->tfMuonIndex()<36) || (muItr->tfMuonIndex()>71 && muItr->tfMuonIndex()<90) ) l1stage2mutfreg[il1stage2mu] = 1; // Overlap Muon Track Finder 
        else if ( (muItr->tfMuonIndex()<18) || (muItr->tfMuonIndex()>89) ) l1stage2mutfreg[il1stage2mu] = 2; // Endcap Muon
        jl1stage2mu = il1stage2mu + 1;
        for (l1cand mu2Itr=muItr+1; mu2Itr!=L1Stage2Muon->end(iBx); ++mu2Itr) {
            l1stage2dimuidx1[il1stage2dimu] = il1stage2mu;
            l1stage2dimuidx2[il1stage2dimu] = jl1stage2mu;
            // Combined dimuon system
            l1stage2dimuchg[il1stage2dimu] = muItr->charge() + mu2Itr->charge();
            double const MuMass2 = (0.105658*0.105658);
            double e1 = sqrt(muItr->momentum().Mag2()+MuMass2);
            double e2 = sqrt(mu2Itr->momentum().Mag2()+MuMass2);
            reco::Particle::LorentzVector p1 = reco::Particle::LorentzVector(muItr->px(),muItr->py(),muItr->pz(),e1);
            reco::Particle::LorentzVector p2 = reco::Particle::LorentzVector(mu2Itr->px(),mu2Itr->py(),mu2Itr->pz(),e2);
            reco::Particle::LorentzVector p = p1+p2;
            l1stage2dimumass[il1stage2dimu] = p.mass();
            l1stage2dimupt[il1stage2dimu] = p.pt();
            l1stage2dimuphi[il1stage2dimu] = p.Phi();
            l1stage2dimurap[il1stage2dimu] = p.Rapidity();
            Double_t deta = p1.Eta()-p2.Eta();
            Double_t dphi = TVector2::Phi_mpi_pi(p1.Phi()-p2.Phi());
            l1stage2dimudr[il1stage2dimu] = TMath::Sqrt( deta*deta+dphi*dphi );
            il1stage2dimu++;
            jl1stage2mu++;
        }
        il1stage2mu++;
      }
    }
    nl1stage2mu = il1stage2mu;
    nl1stage2dimu = il1stage2dimu;
  }
  else {
    nl1stage2mu = 0;
    nl1stage2dimu = 0;
    if (_Debug) std::cout << "%HLTStage2Info -- No L1 Stage2 Muon object" << std::endl;
  }

  if (L1Stage2Jet.isValid()) {
    int il1stage2jt = 0;
    typedef std::vector<l1t::Jet>::const_iterator l1cand;
    for(int iBx = L1Stage2Jet->getFirstBX(); iBx <= L1Stage2Jet->getLastBX(); ++iBx) { 
      for (l1cand jtItr=L1Stage2Jet->begin(iBx); jtItr!=L1Stage2Jet->end(iBx); ++jtItr) {
        l1stage2jtet[il1stage2jt]  = jtItr->et();
        l1stage2jte[il1stage2jt]   = jtItr->energy();
        l1stage2jteta[il1stage2jt] = jtItr->eta();
        l1stage2jtphi[il1stage2jt] = jtItr->phi();
        l1stage2jtbx[il1stage2jt]  = iBx;
        il1stage2jt++;
      }
    }
    nl1stage2jet = il1stage2jt;
  }
  else {
    nl1stage2jet = 0;
    if (_Debug) std::cout << "%HLTStage2Info -- No L1 Stage2 Jet object" << std::endl;
  }

  if (L1Stage2Tau.isValid()) {
    int il1stage2tau = 0;
    typedef std::vector<l1t::Tau>::const_iterator l1cand;
    for(int iBx = L1Stage2Tau->getFirstBX(); iBx <= L1Stage2Tau->getLastBX(); ++iBx) { 
      for (l1cand tauItr=L1Stage2Tau->begin(iBx); tauItr!=L1Stage2Tau->end(iBx); ++tauItr) {
        l1stage2tauet[il1stage2tau]  = tauItr->et();
        l1stage2taue[il1stage2tau]   = tauItr->energy();
        l1stage2taueta[il1stage2tau] = tauItr->eta();
        l1stage2tauphi[il1stage2tau] = tauItr->phi();
        l1stage2taubx[il1stage2tau]  = iBx;
        il1stage2tau++;
      }
    }
    nl1stage2tau = il1stage2tau;
  }
  else {
    nl1stage2tau = 0;
    if (_Debug) std::cout << "%HLTStage2Info -- No L1 Stage2 Tau object" << std::endl;
  }

  if (L1Stage2EtSum.isValid()) {
    int il1stage2ets = 0;
    typedef std::vector<l1t::EtSum>::const_iterator l1cand;
    for(int iBx = L1Stage2EtSum->getFirstBX(); iBx <= L1Stage2EtSum->getLastBX(); ++iBx) { 
      for (l1cand etsItr=L1Stage2EtSum->begin(iBx); etsItr!=L1Stage2EtSum->end(iBx); ++etsItr) {
        l1stage2etset[il1stage2ets]   = etsItr->et();
        l1stage2etsphi[il1stage2ets]  = etsItr->phi();
        l1stage2etshwet[il1stage2ets]   = etsItr->hwPt();
        l1stage2etshwphi[il1stage2ets]  = etsItr->hwPhi();
        l1stage2etstype[il1stage2ets] = etsItr->getType();
        l1stage2etsbx[il1stage2ets]   = iBx;
        il1stage2ets++;
      }
    }
    nl1stage2ets = il1stage2ets;
  }
  else {
    nl1stage2ets = 0;
    if (_Debug) std::cout << "%HLTStage2Info -- No L1 Stage2 EtSum object" << std::endl;
  }

  //==============L1 Stage2 information=======================================


  if (L1GOMR.isValid() && !getL1InfoFromEventSetup_) {
    // Get the stage2 menu from GlobalObjectMapRecord collection
    if (L1TEvtCnt==0){
      // 1st event : Book as many branches as trigger paths provided in the input...
      const std::vector<GlobalObjectMap> gObjectMapRecord = L1GOMR->gtObjectMap();
      std::vector<GlobalObjectMap>::const_iterator gObjectMap = gObjectMapRecord.begin();
      // Book branches for algo bits
      for (; gObjectMap!=gObjectMapRecord.end(); ++gObjectMap) {
        int itrig = gObjectMap->algoBitNumber();
        algoBitToName[itrig] = TString( gObjectMap->algoName() );
        HltTree->Branch(algoBitToName[itrig]+"_Final",l1TFinalFlag+itrig,algoBitToName[itrig]+"_Final/I");
        HltTree->Branch(algoBitToName[itrig]+"_Prescl",l1TPrescl+itrig,algoBitToName[itrig]+"_Prescl/I");
      }
    }
    // ...Fill the corresponding accepts in branch-variables
    std::map< int, TString >::iterator iL1Trig = algoBitToName.begin();
    for (; iL1Trig!=algoBitToName.end(); ++iL1Trig) {
      std::string name = iL1Trig->second.Data();
      int iBit = iL1Trig->first;
      l1TInitialFlag[iBit] = false; // The Global Object Collection doesn't have initial L1 decisions
      l1TFinalFlag[iBit] = L1GOMR->getObjectMap(name)->algoGtlResult();
      if(!(l1tGlobalUtil_->getPrescaleByName(name, l1TPrescl[iBit]))) l1TPrescl[iBit] = -1;
    }
    L1TEvtCnt++;
  }
  else {
    // Get the stage2 menu from Event Setup
    if (L1TEvtCnt==0){
      // 1st event : Book as many branches as trigger paths provided in the input...
      edm::ESTransientHandle<L1TUtmTriggerMenu> l1GtMenu;
      eventSetup.get<L1TUtmTriggerMenuRcd>().get(l1GtMenu);
      if(l1GtMenu.isValid()) {
        const L1TUtmTriggerMenu* stage2Menu = l1GtMenu.product();
        // Book branches for algo bits
        for (auto const & algo: stage2Menu->getAlgorithmMap()) {
          int itrig = algo.second.getIndex();
          algoBitToName[itrig] = TString( algo.second.getName() );
          HltTree->Branch(algoBitToName[itrig]+"_Initial",l1TInitialFlag+itrig,algoBitToName[itrig]+"_Initial/I");
          HltTree->Branch(algoBitToName[itrig]+"_Final",l1TFinalFlag+itrig,algoBitToName[itrig]+"_Final/I");
          HltTree->Branch(algoBitToName[itrig]+"_Prescl",l1TPrescl+itrig,algoBitToName[itrig]+"_Prescl/I");
        }
      }
    }
    // ...Fill the corresponding accepts in branch-variables
    std::map< int, TString >::iterator iL1Trig = algoBitToName.begin();
    for (; iL1Trig!=algoBitToName.end(); ++iL1Trig) {
      std::string name = iL1Trig->second.Data();
      int iBit = iL1Trig->first;
      bool des = false;
      if (!(l1tGlobalUtil_->getFinalDecisionByName(name, des))) l1TFinalFlag[iBit] = false;
      else l1TFinalFlag[iBit] = des;
      if (!(l1tGlobalUtil_->getInitialDecisionByName(name, des))) l1TInitialFlag[iBit] = false;
      else l1TInitialFlag[iBit] = des;
      if(!(l1tGlobalUtil_->getPrescaleByName(name, l1TPrescl[iBit]))) l1TPrescl[iBit] = -1;
    }
    L1TEvtCnt++;
  }

  if (_Debug) std::cout << "%HLTStage2Info -- Done with routine" << std::endl;
}
