import FWCore.ParameterSet.Config as cms

hltanalysis = cms.EDAnalyzer('HLTBitAnalyzer',
    HLTProcessName = cms.string('HLT'),
    hltresults = cms.InputTag('TriggerResults::HLT'),
    l1results = cms.InputTag('gtStage2Digis'),
    UseTFileService = cms.untracked.bool(True),
    RunParameters = cms.PSet(
        isData = cms.untracked.bool(True)),
    dummyBranches = cms.untracked.vstring(),

    mctruth = cms.InputTag(''),
    genEventInfo = cms.InputTag(''),
    OfflinePrimaryVertices0 = cms.InputTag(''),
    simhits = cms.InputTag(''),
)
