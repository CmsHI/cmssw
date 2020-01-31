import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.EventAnalysis.dummybranches_cff import *

hltanalysis = cms.EDAnalyzer('HLTBitAnalyzer',
    HLTProcessName = cms.string('HLT'),
    hltresults = cms.InputTag('TriggerResults::HLT'),
    l1results = cms.InputTag('gtStage2Digis'),
    dummyBranches = dummy_branches_for_pp_2017_HLT,
    l1dummyBranches = dummy_branches_for_pp_2017_L1,
    RunParameters = cms.PSet(
        Debug = cms.bool(False),
    ),
)


skimanalysis = cms.EDAnalyzer("FilterAnalyzer",
                              hltresults = cms.InputTag("TriggerResults","","HiForest"),
                              superFilters = cms.vstring("")
)




