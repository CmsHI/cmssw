import FWCore.ParameterSet.Config as cms

from RecoJets.Configuration.GenJetParticles_cff import genParticlesForJets
from RecoHI.HiJetAlgos.HiSignalParticleProducer_cfi import hiSignalGenParticles
from RecoHI.HiJetAlgos.HiGenCleaner_cff import hiPartons

allPartons = cms.EDProducer(
    "PartonSelector",
    src = cms.InputTag('genParticles'),
    withLeptons = cms.bool(False),
    )

cleanedPartons = hiPartons.clone(
    src = 'allPartons',
    )

cleanedGenJetsTask = cms.Task(
    genParticlesForJets,
    cleanedPartons,
)

signalPartons = allPartons.clone(
    src = 'hiSignalGenParticles',
    )

signalGenJetsTask = cms.Task(
    genParticlesForJets,
    hiSignalGenParticles,
    signalPartons,
    )

from RecoHI.HiJetAlgos.jetFlavourPlaceholder_cfi import jetFlavourPlaceholder

slimmedGenJetsFlavourPlaceholder = jetFlavourPlaceholder.clone(
    jets = 'ak4HiGenJets',
    )

from RecoHI.HiJetAlgos.HiRecoPFJets_cff import PFTowers, pfNoPileUpJMEHI, ak4PFJetsForFlow
from RecoHI.HiJetAlgos.hiPFCandCleaner_cfi import hiPFCandCleaner
from RecoHI.HiJetAlgos.hiFJRhoFlowModulationProducer_cfi import hiFJRhoFlowModulationProducer
from RecoHI.HiJetAlgos.hiPuRhoProducer_cfi import hiPuRhoProducer
from RecoHI.HiTracking.highPurityTracks_cfi import highPurityTracks

recoPFJetsHIpostAODTask = cms.Task(
    PFTowers,
    pfNoPileUpJMEHI,
    hiPFCandCleaner,
    ak4PFJetsForFlow,
    hiFJRhoFlowModulationProducer,
    hiPuRhoProducer,
    highPurityTracks,
    )

recoJetsHIpostAODTask = cms.Task(
    recoPFJetsHIpostAODTask,
    allPartons,
    cleanedGenJetsTask,
    signalGenJetsTask,
    slimmedGenJetsFlavourPlaceholder,
    )
