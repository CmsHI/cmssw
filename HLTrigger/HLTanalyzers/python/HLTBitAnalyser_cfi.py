import FWCore.ParameterSet.Config as cms

hltbitanalysis = cms.EDAnalyzer("HLTBitAnalyzer",
    ### L1 Legacy and Stage 1 objects
    l1GctHFBitCounts                = cms.InputTag("hltGctDigis"),
    l1GctHFRingSums                 = cms.InputTag("hltGctDigis"),
    l1GtReadoutRecord               = cms.InputTag("hltGtDigis::HLT"),
    l1extramc                       = cms.string('hltL1extraParticles'),
    l1extramu                       = cms.string('hltL1extraParticles'),

    ### L1 Stage 2 objects
    l1tAlgBlkInputTag               = cms.InputTag("hltGtStage2Digis"),  # Needed, fix bug of GlobalAlgBlk uninitialized token
    l1tExtBlkInputTag               = cms.InputTag("hltGtStage2Digis"),
    gObjectMapRecord                = cms.InputTag("hltGtStage2ObjectMap"),
    gmtStage2Digis                  = cms.string("hltGmtStage2Digis"),
    caloStage2Digis                 = cms.string("hltCaloStage2Digis"),

    ### HLT
    hltresults                      = cms.InputTag("TriggerResults::HLT"),
    HLTProcessName                  = cms.string("HLT"),

    ### GEN objects
    mctruth                         = cms.InputTag("genParticles::HLT"),
    genEventInfo                    = cms.InputTag("generator::SIM"),

    ### SIM objects
    simhits                         = cms.InputTag("g4SimHits"),
                                
    ## reco vertices
    OfflinePrimaryVertices0         = cms.InputTag('offlinePrimaryVertices'),
                                
    ### Run parameters
    RunParameters = cms.PSet(
        HistogramFile = cms.untracked.string('hltbitanalysis.root'),
        isData         = cms.untracked.bool(False),
        Monte          = cms.bool(True),
        GenTracks      = cms.bool(True),
        UseL1Stage2    = cms.bool(True)
    )
                                
)
