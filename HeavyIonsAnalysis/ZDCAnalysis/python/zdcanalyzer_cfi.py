import FWCore.ParameterSet.Config as cms

zdcanalyzer = cms.EDAnalyzer("ZDCTreeProducer",
    doZDCRecHit = cms.bool(True),
    doZDCDigi = cms.bool(True),

    zdcRecHitSrc = cms.InputTag("zdcreco"),
    #zdcDigiSrc = cms.InputTag("hcalDigis"),
    zdcDigiSrc = cms.InputTag('hcalDigis', 'ZDC'),

    nZdcTs = cms.int32(10),
    calZDCDigi = cms.bool(False),#True
	verbose = cms.bool(True),
    )
