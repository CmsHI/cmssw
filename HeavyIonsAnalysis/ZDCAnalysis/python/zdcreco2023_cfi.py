import FWCore.ParameterSet.Config as cms

zdcrecoRun3 = cms.EDProducer(
    "ZDC2023RecHit",
    zdcDigiSrc = cms.InputTag('hcalDigis', 'ZDC'),
    calZDCDigi = cms.bool(False),
    skipRPD = cms.bool(True)
)
