#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1TUtmAlgorithm.h"
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "DataFormats/L1TGlobal/interface/GlobalExtBlk.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/Registry.h"

#include "EventHeader.h"
#include "HLTInfo.h"

/** \class HLTBitAnalyzer
  *
  * $Date: November 2006
  * $Revision:
  * \author P. Bargassa - Rice U.

  * $Date: April 2016
  * $Revision:
  * \author G. Karapostoli - ULB
  */

class HLTBitAnalyzer : public edm::EDAnalyzer {
public:
  explicit HLTBitAnalyzer(edm::ParameterSet const& conf);
  void analyze(edm::Event const& e, edm::EventSetup const& iSetup) override;
  void endJob() override;
  void beginRun(edm::Run const&, edm::EventSetup const&) override;

  //  static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

  // Analysis tree to be filled
  TTree* HltTree;

private:
  // variables persistent across events should be declared here.
  //
  ///Default analyses

  EventHeader evt_header_;
  HLTInfo     hlt_analysis_;

  edm::InputTag hltresults_;
  edm::InputTag l1results_;

  edm::EDGetTokenT<edm::TriggerResults> hltresultsToken_;
  edm::EDGetTokenT<GlobalAlgBlkBxCollection> l1resultsToken_;
};
