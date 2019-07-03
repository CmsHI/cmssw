import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets

from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

akSoftDrop4GenJets = cms.EDProducer(
    "FastjetJetProducer",
    GenJetParameters,
    AnomalousCellParameters,
    jetAlgorithm        = cms.string("AntiKt"),
    rParam              = cms.double(0.4),
    useSoftDrop         = cms.bool(True),
    zcut                = cms.double(0.1),
    beta                = cms.double(0.0),
    R0                  = cms.double(0.4),
    useExplicitGhosts   = cms.bool(True),
    writeCompound       = cms.bool(True),
    jetCollInstanceName = cms.string("SubJets")
)

ak1GenJets = ak4GenJets.clone(rParam = 0.1)
ak2GenJets = ak4GenJets.clone(rParam = 0.2)
ak3GenJets = ak4GenJets.clone(rParam = 0.3)
ak5GenJets = ak4GenJets.clone(rParam = 0.5)
ak6GenJets = ak4GenJets.clone(rParam = 0.6)

akSoftDrop1GenJets = akSoftDrop4GenJets.clone(rParam = 0.1, R0 = 0.1)
akSoftDrop2GenJets = akSoftDrop4GenJets.clone(rParam = 0.2, R0 = 0.2)
akSoftDrop3GenJets = akSoftDrop4GenJets.clone(rParam = 0.3, R0 = 0.3)
akSoftDrop5GenJets = akSoftDrop4GenJets.clone(rParam = 0.5, R0 = 0.5)
akSoftDrop6GenJets = akSoftDrop4GenJets.clone(rParam = 0.6, R0 = 0.6)
