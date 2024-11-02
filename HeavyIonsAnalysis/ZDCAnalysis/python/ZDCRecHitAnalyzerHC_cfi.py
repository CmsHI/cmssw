import FWCore.ParameterSet.Config as cms

zdcanalyzer = cms.EDAnalyzer(
   "ZDCRecHitAnalyzerHC",
   ZDCRecHitSource    = cms.InputTag('zdcrecoRun3'),
   ZDCDigiSource    = cms.InputTag('hcalDigis', 'ZDC'),
   AuxZDCRecHitSource    = cms.InputTag('zdcrecoRun3'),
   doZdcRecHits = cms.bool(True),
   doZdcDigis = cms.bool(True),
   doAuxZdcRecHits = cms.bool(False),
   skipRpdRecHits = cms.bool(False),
   doHardcodedRPD = cms.bool(True)
)

