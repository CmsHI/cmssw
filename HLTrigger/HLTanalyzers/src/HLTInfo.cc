#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "HLTrigger/HLTanalyzers/interface/HLTInfo.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "L1Trigger/L1TGlobal/interface/L1TGlobalUtil.h"

HLTInfo::HLTInfo() {
  //set parameter defaults
  _Debug = false;
}

void HLTInfo::beginRun(const edm::Run& run, const edm::EventSetup& c) {
  bool changed(true);
  if (hltPrescaleProvider_->init(run, c, processName_, changed)) {
    // if init returns TRUE, initialisation has succeeded!
    if (changed) {
      // The HLT config has actually changed wrt the previous Run, hence rebook your
      // histograms or do anything else dependent on the revised HLT config
      edm::LogInfo("HLTInfo") << "Initalizing HLTConfigProvider" << std::endl;
    }
  } else {
    // if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
    // with the file and/or code and needs to be investigated!
    edm::LogInfo("HLTInfo") << " HLT config extraction failure with process name " << processName_ << std::endl;
    // In this case, all access methods will return empty values!
  }
}

/*  Setup the analysis to put the branch-variables into the tree. */
void HLTInfo::setup(const edm::ParameterSet& pSet, TTree* HltTree) {
  processName_ = pSet.getParameter<std::string>("HLTProcessName");

  edm::ParameterSet myHltParams = pSet.getParameter<edm::ParameterSet>("RunParameters");
  std::vector<std::string> parameterNames = myHltParams.getParameterNames();

  for (auto const& parameterName : parameterNames) {
    if (parameterName == "Debug") _Debug = myHltParams.getParameter<bool>(parameterName);
  }

  dummyBranches_ = pSet.getUntrackedParameter<std::vector<std::string>>("dummyBranches",std::vector<std::string>(0));
  l1dummies = pSet.getUntrackedParameter<std::vector<std::string>>("l1dummyBranches",std::vector<std::string>(0));

  HltEvtCnt = 0;
  trigflag = new int[kMaxTrigFlag];
  trigPrescl = new int[kMaxTrigFlag];

  L1EvtCnt = 0;
  l1flag = new int[kMaxL1Flag];
  l1Prescl = new int[kMaxL1Flag];
}

/* **Analyze the event** */
void HLTInfo::analyze(const edm::Handle<edm::TriggerResults>& hltresults,
                      const edm::Handle<GlobalAlgBlkBxCollection>& l1results,
                      edm::EventSetup const& eventSetup,
                      edm::Event const& iEvent,
                      TTree* HltTree) {

  /////////// Analyzing HLT Trigger Results (TriggerResults) //////////
  if (hltresults.isValid()) {
    /* reset accept status to -1 */
    for (int i = 0; i < kMaxTrigFlag; ++i) {
      trigflag[i] = -1;
      trigPrescl[i] = -1;
    }

    int ntrigs = hltresults->size();
    if (ntrigs == 0) { edm::LogInfo("HLTInfo") << "-- No trigger name given in TriggerResults of the input " << std::endl; }

    edm::TriggerNames const& triggerNames = iEvent.triggerNames(*hltresults);

    // 1st event : Book as many branches as trigger paths provided in the input...
    if (HltEvtCnt == 0) {
      int itdum = 0;
      for (auto & dummyBranche : dummyBranches_) {
        TString trigName(dummyBranche.data());
        HltTree->Branch(trigName,trigflag+itdum,trigName+"/I");
        HltTree->Branch(trigName+"_Prescl",trigPrescl+itdum,trigName+"_Prescl/I");
        pathtoindex[dummyBranche] = itdum;
        ++itdum;
      }

      for (int itrig = 0; itrig != ntrigs; ++itrig) {
        const std::string& trigName = triggerNames.triggerName(itrig);
        if (pathtoindex.find(trigName) == pathtoindex.end()) {
          TString TSname = trigName;
          HltTree->Branch(TSname,trigflag+itdum+itrig,TSname+"/I");
          HltTree->Branch(TSname+"_Prescl",trigPrescl+itdum+itrig,TSname+"_Prescl/I");
          pathtoindex[trigName] = itdum + itrig;
        }
      }

      HltEvtCnt++;
    }
    // ...Fill the corresponding accepts in branch-variables

    for (int itrig = 0; itrig != ntrigs; ++itrig) {
      const std::string& trigName=triggerNames.triggerName(itrig);
      bool accept = hltresults->accept(itrig);

      int index = pathtoindex[trigName];
      trigPrescl[index] = hltPrescaleProvider_->prescaleValue(iEvent, eventSetup, trigName);

      trigflag[index] = accept;

      if (_Debug) {
        edm::LogInfo("HLTInfo") << "--  Number of HLT Triggers: " << ntrigs << std::endl;
        edm::LogInfo("HLTInfo") << "--  HLTTrigger(" << itrig << "): " << trigName << " = " << accept << std::endl;
      }
    }
  }
  else { edm::LogInfo("HLTInfo") << "-- No Trigger Result" << std::endl; }



  //==============L1 information=======================================

  // L1 Triggers from Menu
  auto& l1GtUtils = const_cast<l1t::L1TGlobalUtil&>(hltPrescaleProvider_->l1tGlobalUtil());

  l1GtUtils.retrieveL1(iEvent,eventSetup);

  edm::ESHandle<L1TUtmTriggerMenu> menu;
  eventSetup.get<L1TUtmTriggerMenuRcd>().get(menu);

  if (l1results.isValid() && l1results->size() != 0) {
    /* reset accept status to -1 */
    for (int i = 0; i < kMaxL1Flag; ++i) {
      l1flag[i] = -1;
      l1Prescl[i] = -1;
    }

    // 1st event : Book as many branches as trigger paths provided in the input...
    if (L1EvtCnt == 0) {
      int itdum = 0;
      for (auto & dummy : l1dummies) {
        TString trigName(dummy.data());
        HltTree->Branch(trigName,l1flag+itdum, trigName+"/I");
        HltTree->Branch(trigName+"_Prescl",l1Prescl+itdum,trigName+"_Prescl/I");
        pathtoindex[dummy] = itdum;
        ++itdum;
      }

      int il1 = 0;
      // get the bit/name association
      for (auto const & keyval: menu->getAlgorithmMap()) {
        std::string const & l1trigName  = keyval.second.getName();

        if (pathtoindex.find(l1trigName) == pathtoindex.end()) {
          TString l1TSname = l1trigName;
          HltTree->Branch(l1TSname,l1flag+itdum+il1,l1TSname+"/I");
          HltTree->Branch(l1TSname+"_Prescl",l1Prescl+itdum+il1,l1TSname+"_Prescl/I");
          pathtoindex[l1trigName] = itdum + il1;
          ++il1;
        }

      } // end algo Map

      L1EvtCnt++;
    } // end l1evtCnt=0

    GlobalAlgBlk const& result = l1results->at(0, 0);

    // get the individual decisions from the GlobalAlgBlk
    for (auto const& keyval : menu->getAlgorithmMap()) {
      auto const& l1pathname = keyval.second.getName();
      int l1index = keyval.second.getIndex();

      int index = pathtoindex[l1pathname];

      bool accept = result.getAlgoDecisionFinal(l1index);
      l1flag[index] = accept;

      l1GtUtils.getPrescaleByBit(l1index, l1Prescl[index]);
    }

    edm::LogInfo("HLTInfo") << "%L1Info -- Done with routine" << std::endl;

  } // l1results.isValid
  else { edm::LogWarning("HLTInfo") << "%L1Results -- No L1 Results" << std::endl; }
}
