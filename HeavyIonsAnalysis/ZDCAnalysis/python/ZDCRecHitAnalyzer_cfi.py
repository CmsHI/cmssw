import FWCore.ParameterSet.Config as cms

zdcanalyzer = cms.EDAnalyzer(
   "ZDCRecHitAnalyzer",
   ZDCRecHitSource    = cms.InputTag('zdcrecoRun3'),
   ZDCDigiSource    = cms.InputTag('hcalDigis', 'ZDC'),
   doZdcRecHits = cms.bool(True),
   doZdcDigis = cms.bool(True),
   skipRPD = cms.bool(True)
 ) # zdcreco

