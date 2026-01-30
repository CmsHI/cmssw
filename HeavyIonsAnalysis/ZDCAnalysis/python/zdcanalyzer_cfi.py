import FWCore.ParameterSet.Config as cms

zdcanalyzer = cms.EDAnalyzer(
    "ZDCTreeProducer",
    doZDCRecHit = cms.bool(True),
    doZDCDigi = cms.bool(True),
    zdcRecHitSrc = cms.InputTag("zdcreco"),
    zdcDigiSrc = cms.InputTag('hcalDigis', 'ZDC'),
    calZDCDigi = cms.bool(False),
    skipRPD = cms.bool(True),
    verbose = cms.bool(False),
)
