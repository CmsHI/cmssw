#ifndef HLTSTAGE2INFO_H
#define HLTSTAGE2INFO_H

#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TNamed.h"
#include <memory>
#include <vector>
#include <map>
#include "TROOT.h"
#include "TChain.h"
#include "TVector3.h"
#include "TMath.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/L1Trigger/interface/Tau.h"
#include "DataFormats/L1Trigger/interface/EtSum.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/L1TGlobal/interface/GlobalObjectMapRecord.h"
#include "DataFormats/L1TGlobal/interface/GlobalObjectMap.h"

//ccla
#include "FWCore/Framework/interface/EventPrincipal.h"
#include "FWCore/Common/interface/Provenance.h"
#include "FWCore/Framework/interface/ESTransientHandle.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "L1Trigger/L1TGlobal/interface/L1TGlobalUtil.h"

namespace edm {
  class ConsumesCollector;
  class ParameterSet;
}

/** \class HLTStage2Info
  *  
  * $Date: July 2016
  * $Revision:
  * \author A. Stahl - Ecole Polytechnique
  */
class HLTStage2Info {
public:

  template <typename T>
  HLTStage2Info(edm::ParameterSet const& pset,
          edm::ConsumesCollector&& iC,
          T& module);

  template <typename T>
  HLTStage2Info(edm::ParameterSet const& pset,
          edm::ConsumesCollector& iC,
          T& module);

  void setup(const edm::ParameterSet& pSet, TTree* tree);
  void beginRun(const edm::Run& , const edm::EventSetup& );

  /** Analyze the Data */
  void analyze(const edm::Handle<edm::TriggerResults>                 & hltresults,
               const edm::Handle< BXVector<l1t::EGamma> >             & L1Stage2EGamma,
               const edm::Handle< BXVector<l1t::Muon> >               & L1Stage2Muon,
               const edm::Handle< BXVector<l1t::Jet> >                & L1Stage2Jet,
               const edm::Handle< BXVector<l1t::Tau> >                & L1Stage2Tau,
               const edm::Handle< BXVector<l1t::EtSum> >              & L1Stage2EtSum,
               const edm::Handle<GlobalObjectMapRecord>               & L1GOMR,
               edm::EventSetup const& eventSetup,
               edm::Event const& iEvent,
               TTree* HltTree);

private:

  HLTStage2Info();

  // Tree variables
  float *hltppt, *hltpeta;
  float *l1stage2eget, *l1stage2ege, *l1stage2egeta, *l1stage2egphi;
  int   *l1stage2egiso;
  float *l1stage2mupt, *l1stage2mue, *l1stage2mueta, *l1stage2muphi;
  int   *l1stage2muchg, *l1stage2muiso, *l1stage2muqul, *l1stage2mutfidx, *l1stage2mutfreg;
  float *l1stage2dimupt, *l1stage2dimurap, *l1stage2dimuphi, *l1stage2dimumass, *l1stage2dimudr;
  int   *l1stage2dimuchg, *l1stage2dimuidx1, *l1stage2dimuidx2;
  float *l1stage2jtet, *l1stage2jte, *l1stage2jteta, *l1stage2jtphi;
  float *l1stage2tauet, *l1stage2taue, *l1stage2taueta, *l1stage2tauphi;
  int   *l1stage2etshwet, *l1stage2etshwphi;
  float *l1stage2etset, *l1stage2etsphi;
  int   *l1stage2ctetem, *l1stage2cteth, *l1stage2ctetc, *l1stage2cteta, *l1stage2ctphi;
  int   *l1stage2etstype;
  int   *l1stage2egbx, *l1stage2mubx, *l1stage2jtbx, *l1stage2taubx, *l1stage2etsbx, *l1stage2ctbx;
  int   L1TEvtCnt,HltEvtCnt,nl1stage2eg,nl1stage2mu,nl1stage2dimu,nl1stage2jet,nl1stage2tau,nl1stage2ets;

  int   *trigflag, *l1TFinalFlag, *l1TInitialFlag, *trigPrescl, *l1TPrescl;

  std::map<int,TString> algoBitToName;
  std::vector<std::string> dummyBranches_;
  bool getPrescales_;
  bool getL1InfoFromEventSetup_;

  std::unique_ptr<HLTConfigProvider>  hltConfigProvider_;
  std::unique_ptr<l1t::L1TGlobalUtil> l1tGlobalUtil_;
  std::string processName_;

  // input variables
  bool _Debug;
};

template <typename T>
HLTStage2Info::HLTStage2Info(edm::ParameterSet const& pset,
                 edm::ConsumesCollector&& iC,
                 T& module) :
  HLTStage2Info(pset, iC, module) {
}

template <typename T>
HLTStage2Info::HLTStage2Info(edm::ParameterSet const& pset,
                 edm::ConsumesCollector& iC,
                 T& module) :
    HLTStage2Info() {
      hltConfigProvider_.reset(new HLTConfigProvider());
      l1tGlobalUtil_.reset(new l1t::L1TGlobalUtil(pset, iC, module));
}

#endif
