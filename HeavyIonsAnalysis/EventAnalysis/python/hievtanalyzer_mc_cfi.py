import FWCore.ParameterSet.Config as cms

hiEvtAnalyzer = cms.EDAnalyzer('HiEvtAnalyzer',
   CentralitySrc    = cms.InputTag("hiCentrality"),
   CentralityBinSrc = cms.InputTag("centralityBin","HFtowers"),
   addPileupInfo    = cms.InputTag("slimmedAddPileupInfo"),
   pfCandidateSrc   = cms.InputTag('packedPFCandidates'),
   EvtPlane         = cms.InputTag("hiEvtPlane"),
   EvtPlaneFlat     = cms.InputTag("hiEvtPlaneFlat",""),
   HiMC             = cms.InputTag("heavyIon"),
   Vertex           = cms.InputTag("offlineSlimmedPrimaryVertices"),
   HFfilters        = cms.InputTag("hiHFfilters","hiHFfilters"),
   met              = cms.InputTag("slimmedMETs"),
   doCentrality     = cms.bool(True),
   doEvtPlane       = cms.bool(True),
   doEvtPlaneFlat   = cms.bool(True),
   doVertex         = cms.bool(True),
   doMET            = cms.bool(False),
   doMC             = cms.bool(True),
   doHiMC           = cms.bool(True),
   useHepMC         = cms.bool(False),
   doHFfilters      = cms.bool(True),
   evtPlaneLevel    = cms.int32(0)
)
