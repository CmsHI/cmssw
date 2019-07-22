import FWCore.ParameterSet.Config as cms

hiPuRhoR3Producer = cms.EDProducer(
    'HiPuRhoProducer',
    src = cms.InputTag('PFTowers'),
    rParam = cms.double(.3),
    nSigmaPU = cms.double(1.0),
    puPtMin = cms.double(15.0),
    radiusPU = cms.double(.5),
    minimumTowersFraction = cms.double(0.7),
    medianWindowWidth = cms.int32(2),
    towSigmaCut = cms.double(5.),
    )
