import FWCore.ParameterSet.Config as cms

from RecoHI.HiJetAlgos.HiRecoPFJets_cff import PFTowers, pfNoPileUpJMEHI, ak4PFJetsForFlow
from RecoHI.HiJetAlgos.hiPFCandCleaner_cfi import hiPFCandCleaner
from RecoHI.HiJetAlgos.hiFJRhoFlowModulationProducer_cfi import hiFJRhoFlowModulationProducer
from RecoHI.HiJetAlgos.hiPuRhoProducer_cfi import hiPuRhoProducer

recoPFJetsHIpostAODTask = cms.Task(
    PFTowers,
    pfNoPileUpJMEHI,
    hiPFCandCleaner,
    ak4PFJetsForFlow,
    hiFJRhoFlowModulationProducer,
    hiPuRhoProducer,
    )

