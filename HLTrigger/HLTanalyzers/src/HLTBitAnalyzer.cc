// File: HLTBitAnalyzer.cc
// Description:  Example of Analysis driver originally from Jeremy Mans,
// Date:  13-October-2006

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "HLTrigger/HLTanalyzers/interface/HLTBitAnalyzer.h"

// Boiler-plate constructor definition of an analyzer module:
HLTBitAnalyzer::HLTBitAnalyzer(edm::ParameterSet const& conf) :
  hlt_analysis_(conf, consumesCollector(), *this) {

  // If your module takes parameters, here is where you would define
  // their names and types, and access them to initialize internal
  // variables. Example as follows:
  std::cout << " Beginning HLTBitAnalyzer Analysis " << std::endl;

  hltresults_ = conf.getParameter<edm::InputTag>("hltresults");
  l1results_ = conf.getParameter<edm::InputTag>("l1results");

  hltresultsToken_ = consumes<edm::TriggerResults>(hltresults_);
  l1resultsToken_ = consumes<GlobalAlgBlkBxCollection>(l1results_);

  // open the tree file and initialize the tree
  edm::Service<TFileService> fs;
  HltTree = fs->make<TTree>("HltTree", "");

  // Setup the different analysis
  hlt_analysis_.setup(conf, HltTree);
  evt_header_.setup(consumesCollector(), HltTree);
}

// Boiler-plate "analyze" method declaration for an analyzer module.
void HLTBitAnalyzer::analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup) {

  edm::Handle<edm::TriggerResults> hltresults;
  edm::Handle<GlobalAlgBlkBxCollection> l1results;

  iEvent.getByToken(hltresultsToken_, hltresults);
  iEvent.getByToken(l1resultsToken_, l1results);

  // run the analysis, passing required event fragments
  hlt_analysis_.analyze(hltresults, l1results, iSetup, iEvent, HltTree);
  evt_header_.analyze(iEvent, HltTree);

  // After analysis, fill the variables tree
  HltTree->Fill();
}

// ------------ method called when starting to processes a run  ------------
void
HLTBitAnalyzer::beginRun(edm::Run const& run, edm::EventSetup const& es) {
   hlt_analysis_.beginRun(run, es);
}

// "endJob" is an inherited method that you may implement to do post-EOF processing and produce final output.
void HLTBitAnalyzer::endJob() { }


// declare this class as a framework plugin
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(HLTBitAnalyzer);
