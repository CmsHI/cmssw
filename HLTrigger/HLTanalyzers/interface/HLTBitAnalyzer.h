#include <iostream>

#include "HLTrigger/HLTanalyzers/interface/EventHeader.h"
#include "HLTrigger/HLTanalyzers/interface/HLTStage2Info.h"
#include "HLTrigger/HLTanalyzers/interface/HLTInfo.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetupFwd.h"
#include "DataFormats/L1TGlobal/interface/GlobalObjectMapRecord.h"
#include "DataFormats/L1TGlobal/interface/GlobalObjectMap.h"


/** \class HLTBitAnalyzer
  *  
  * $Date: November 2006
  * $Revision: 
  * \author P. Bargassa - Rice U.
  * $Date: July 2016
  * $Revision: Updated for L1 Stage 2 
  * \author A. Stahl - Ecole Polytechnique
  */

class HLTBitAnalyzer : public edm::EDAnalyzer {
public:
  explicit HLTBitAnalyzer(edm::ParameterSet const& conf);
  virtual void analyze(edm::Event const& e, edm::EventSetup const& iSetup);
  virtual void endJob();
  virtual void beginRun(edm::Run const&, edm::EventSetup const&);

  //  static void fillDescriptions(edm::ConfigurationDescriptions & descriptions); 

  // Analysis tree to be filled
  TTree *HltTree;

private:
  // variables persistent across events should be declared here.
  //
  ///Default analyses

  EventHeader    evt_header_;
  HLTStage2Info  hlt_stage2_analysis_;
  HLTInfo        hlt_analysis_;

  // HLT
  edm::InputTag hltresults_;

  edm::EDGetTokenT<edm::TriggerResults>                  hltresultsToken_;

  // L1 Legacy and Stage 1  
  std::string l1extramc_, l1extramu_;
  edm::InputTag m_l1extramu;
  edm::InputTag m_l1extraemi;
  edm::InputTag m_l1extraemn;
  edm::InputTag m_l1extrajetc;
  edm::InputTag m_l1extrajetf;
  edm::InputTag m_l1extrajet;
  edm::InputTag m_l1extrataujet;
  edm::InputTag m_l1extramet;
  edm::InputTag m_l1extramht;
  edm::InputTag gtReadoutRecord_;
  edm::InputTag gctBitCounts_,gctRingSums_;

  edm::EDGetTokenT<l1extra::L1MuonParticleCollection>    l1extramuToken_;
  edm::EDGetTokenT<l1extra::L1EmParticleCollection>      l1extraemiToken_, l1extraemnToken_;
  edm::EDGetTokenT<l1extra::L1JetParticleCollection>     l1extrajetcToken_, l1extrajetfToken_, l1extrajetToken_, l1extrataujetToken_;
  edm::EDGetTokenT<l1extra::L1EtMissParticleCollection>  l1extrametToken_,l1extramhtToken_;
  edm::EDGetTokenT<L1GlobalTriggerReadoutRecord>         gtReadoutRecordToken_;
  edm::EDGetTokenT< L1GctHFBitCountsCollection >         gctBitCountsToken_;
  edm::EDGetTokenT< L1GctHFRingEtSumsCollection >        gctRingSumsToken_;

  // L1 Stage 2
  std::string gmtstage2_, calostage2_;
  edm::InputTag gObjectMapRecord_;
  edm::InputTag m_l1stage2mu;
  edm::InputTag m_l1stage2eg;
  edm::InputTag m_l1stage2jet;
  edm::InputTag m_l1stage2tau;
  edm::InputTag m_l1stage2ets;

  edm::EDGetTokenT<GlobalObjectMapRecord>                gObjectMapRecordToken_;
  edm::EDGetTokenT< BXVector<l1t::Muon> >                l1stage2muToken_;
  edm::EDGetTokenT< BXVector<l1t::EGamma> >              l1stage2egToken_;
  edm::EDGetTokenT< BXVector<l1t::Jet> >                 l1stage2jetToken_; 
  edm::EDGetTokenT< BXVector<l1t::Tau> >                 l1stage2tauToken_;
  edm::EDGetTokenT< BXVector<l1t::EtSum> >               l1stage2etsToken_;

  int errCnt;
  static int errMax() { return 5; }

  std::string _HistName; // Name of histogram file
  TFile* m_file; // pointer to Histogram file
  bool _UseTFileService;
  bool _UseL1Stage2;
  bool _getL1InfoFromEventSetup;

};
