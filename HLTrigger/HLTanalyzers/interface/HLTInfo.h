#ifndef HLTINFO_H
#define HLTINFO_H

#include <map>
#include <string>
#include <vector>

// ROOT
#include <TTree.h>

// CMSSW
#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "DataFormats/L1TGlobal/interface/GlobalExtBlk.h"
#include "FWCore/Common/interface/Provenance.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"

namespace edm {
  class ConsumesCollector;
  class ParameterSet;
}

constexpr int kMaxTrigFlag = 1000;
constexpr int kMaxL1Flag = 1000;

/** \class HLTInfo
  *
  * $Date: November 2006
  * $Revision:
  * \author P. Bargassa - Rice U.
  * $Date: April 2016
  * $Revision:
  * \author G. Karapostoli - ULB
  */
class HLTInfo {
public:
  template <typename T>
    HLTInfo(edm::ParameterSet const& pset,
	    edm::ConsumesCollector&& iC,
	    T& module);

  template <typename T>
    HLTInfo(edm::ParameterSet const& pset,
	    edm::ConsumesCollector& iC,
	    T& module);

  void setup(const edm::ParameterSet& pSet, TTree* tree);
  void beginRun(const edm::Run& , const edm::EventSetup&);

  /** Analyze the Data */
  void analyze(const edm::Handle<edm::TriggerResults>& hltresults,
	       const edm::Handle<GlobalAlgBlkBxCollection>& l1results,
	       edm::EventSetup const& eventSetup,
	       edm::Event const& iEvent,
	       TTree* tree);

private:
  HLTInfo();

  // Tree variables
  int L1EvtCnt,HltEvtCnt;
  int *trigflag, *l1flag;
  int *trigPrescl, *l1Prescl;

  std::vector<std::string> dummyBranches_;
  std::vector<std::string> l1dummies;

  std::map<std::string, int> pathtoindex;

  std::unique_ptr<HLTPrescaleProvider> hltPrescaleProvider_;
  std::string processName_;

  bool _Debug;
};

template <typename T>
HLTInfo::HLTInfo(edm::ParameterSet const& pset,
		 edm::ConsumesCollector&& iC,
		 T& module) :
    HLTInfo(pset, iC, module) {
}

template <typename T>
HLTInfo::HLTInfo(edm::ParameterSet const& pset,
		 edm::ConsumesCollector& iC,
		 T& module) :
    HLTInfo() {
    hltPrescaleProvider_.reset(new HLTPrescaleProvider(pset, iC, module));
}

#endif
