import FWCore.ParameterSet.Config as cms

from RecoEgamma.EgammaTools.calibratedEgammas_cff import *

correctedElectrons = cms.EDProducer(
    "CorrectedElectronProducer",
    semiDeterministic = cms.bool(True),
    src = cms.InputTag("gedGsfElectrons"),
    centrality = cms.InputTag("centralityBin", "HFtowers"),
    epCombConfig = ecalTrkCombinationRegression,
    correctionFile = cms.string(""),
    minPt = cms.double(20.0),
    )
