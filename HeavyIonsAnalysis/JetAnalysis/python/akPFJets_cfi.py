import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets

from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

ak4PFJECJets = ak4PFJets.clone(
    doAreaFastjet = True, jetPtMin = 1)

akSoftDrop4PFJets = cms.EDProducer(
    "FastjetJetProducer",
    PFJetParameters,
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

akFilter4PFJets = cms.EDProducer(
    "FastjetJetProducer",
    PFJetParameters,
    AnomalousCellParameters,
    jetAlgorithm        = cms.string("AntiKt"),
    rParam              = cms.double(0.4),
    useFiltering        = cms.bool(True),
    nFilt               = cms.int32(4),
    rFilt               = cms.double(0.15),
    useExplicitGhosts   = cms.bool(True),
    writeCompound       = cms.bool(True),
    jetCollInstanceName = cms.string("SubJets")
)

ak1PFJets = ak4PFJets.clone(rParam = 0.1)
ak2PFJets = ak4PFJets.clone(rParam = 0.2)
ak3PFJets = ak4PFJets.clone(rParam = 0.3)
ak5PFJets = ak4PFJets.clone(rParam = 0.5)
ak6PFJets = ak4PFJets.clone(rParam = 0.6)

ak1PFJECJets = ak4PFJECJets.clone(rParam = 0.1)
ak2PFJECJets = ak4PFJECJets.clone(rParam = 0.2)
ak3PFJECJets = ak4PFJECJets.clone(rParam = 0.3)
ak5PFJECJets = ak4PFJECJets.clone(rParam = 0.5)
ak6PFJECJets = ak4PFJECJets.clone(rParam = 0.6)

akSoftDrop1PFJets = akSoftDrop4PFJets.clone(rParam = 0.1, R0 = 0.1)
akSoftDrop2PFJets = akSoftDrop4PFJets.clone(rParam = 0.2, R0 = 0.2)
akSoftDrop3PFJets = akSoftDrop4PFJets.clone(rParam = 0.3, R0 = 0.3)
akSoftDrop5PFJets = akSoftDrop4PFJets.clone(rParam = 0.5, R0 = 0.5)
akSoftDrop6PFJets = akSoftDrop4PFJets.clone(rParam = 0.6, R0 = 0.6)

akFilter1PFJets = akFilter4PFJets.clone(rParam = 0.1)
akFilter2PFJets = akFilter4PFJets.clone(rParam = 0.2)
akFilter3PFJets = akFilter4PFJets.clone(rParam = 0.3)
akFilter5PFJets = akFilter4PFJets.clone(rParam = 0.5)
akFilter6PFJets = akFilter4PFJets.clone(rParam = 0.6)
