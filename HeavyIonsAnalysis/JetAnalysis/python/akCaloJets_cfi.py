import FWCore.ParameterSet.Config as cms

from RecoHI.HiJetAlgos.HiCaloJetParameters_cff import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

ak4CaloJets = cms.EDProducer(
    "FastjetJetProducer",
    HiCaloJetParameters,
    AnomalousCellParameters,
    MultipleAlgoIteratorBlock,
    jetAlgorithm = cms.string("AntiKt"),
    rParam       = cms.double(0.4)
    )

ak4CaloJets.doPUOffsetCorr = False

ak4CaloJECJets = ak4CaloJets.clone(
    doAreaFastjet = True, jetPtMin = 1)

ak1CaloJets = ak4CaloJets.clone(rParam = 0.1)
ak2CaloJets = ak4CaloJets.clone(rParam = 0.2)
ak3CaloJets = ak4CaloJets.clone(rParam = 0.3)
ak5CaloJets = ak4CaloJets.clone(rParam = 0.5)
ak6CaloJets = ak4CaloJets.clone(rParam = 0.6)

ak1CaloJECJets = ak4CaloJECJets.clone(rParam = 0.1)
ak2CaloJECJets = ak4CaloJECJets.clone(rParam = 0.2)
ak3CaloJECJets = ak4CaloJECJets.clone(rParam = 0.3)
ak5CaloJECJets = ak4CaloJECJets.clone(rParam = 0.5)
ak6CaloJECJets = ak4CaloJECJets.clone(rParam = 0.6)
