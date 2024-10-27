import FWCore.ParameterSet.Config as cms

zdcanalyzer = cms.EDAnalyzer(
   "ZDCRecHitAnalyzerHC",
   ZDCRecHitSource    = cms.InputTag('zdcrecoRun3'),
   ZDCDigiSource    = cms.InputTag('hcalDigis', 'ZDC'),
   AuxZDCRecHitSource    = cms.InputTag('zdcrecoRun3'),
   doZdcRecHits = cms.bool(True),
   doZdcDigis = cms.bool(True),
   doAuxZdcRecHits = cms.bool(False),
   skipRPD = cms.bool(True),
   doHardcodedRecHitsRPD = cms.bool(True),
   doHardcodedDigisRPD = cms.bool(True)
 )

