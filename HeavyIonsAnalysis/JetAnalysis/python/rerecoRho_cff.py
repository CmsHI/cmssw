import FWCore.ParameterSet.Config as cms

# import kt jets for rho estimators
from HeavyIonsAnalysis.JetAnalysis.ktPFJets_cfi import PFTowers, kt4PFJets, kt4PFJetsForRho

from RecoHI.HiJetAlgos.hiFJRhoProducer import hiFJRhoProducer, hiFJRhoProducerFinerBins
from RecoHI.HiJetAlgos.hiFJGridEmptyAreaCalculator_cff import hiFJGridEmptyAreaCalculator, hiFJGridEmptyAreaCalculatorFinerBins

from RecoHI.HiJetAlgos.hiPuRhoProducer_cfi import hiPuRhoR3Producer
from RecoHI.HiJetAlgos.hiFJRhoFlowModulationProducer_cff import hiFJRhoFlowModulationProducer

ak4PFJetsForFlow = cms.EDProducer("FastjetJetProducer",
    Active_Area_Repeats = cms.int32(1),
    GhostArea = cms.double(0.01),
    Ghost_EtaMax = cms.double(5.0),
    Rho_EtaMax = cms.double(4.4),
    doAreaDiskApprox = cms.bool(False),
    doAreaFastjet = cms.bool(True),
#    doOutputJets = cms.bool(True),
    doPUOffsetCorr = cms.bool(False),
    doPVCorrection = cms.bool(False),
    doRhoFastjet = cms.bool(False),
    inputEMin = cms.double(0.0),
    inputEtMin = cms.double(0.0),
    jetAlgorithm = cms.string('AntiKt'),
    jetPtMin = cms.double(15.0),
    jetType = cms.string('PFJet'),
    maxBadEcalCells = cms.uint32(9999999),
    maxBadHcalCells = cms.uint32(9999999),
    maxProblematicEcalCells = cms.uint32(9999999),
    maxProblematicHcalCells = cms.uint32(9999999),
    maxRecoveredEcalCells = cms.uint32(9999999),
    maxRecoveredHcalCells = cms.uint32(9999999),
    minSeed = cms.uint32(14327),
    nSigmaPU = cms.double(1.0),
    rParam = cms.double(0.4),
    radiusPU = cms.double(0.5),
    src = cms.InputTag("pfcandCleanerPt4Eta2", "particleFlowCleaned"),
    srcPVs = cms.InputTag(""),
    useDeterministicSeed = cms.bool(True),
    voronoiRfact = cms.double(-0.9)
)

# We will also need some cleaned candidates for our jets, declare directly
pfcandCleanerPt4Eta2 = cms.EDProducer(
    "HiPFCandCleaner",
    pfPtMin = cms.double(4.),
    pfAbsEtaMax = cms.double(2.),
    pfCandidateLabel = cms.InputTag("particleFlow")
)

hiFJRhoFlowModulationProducer.jetTag = cms.InputTag("ak4PFJetsForFlow")
hiFJRhoFlowModulationProducer.doFlatTest = cms.bool(True)

rhoSequence = cms.Sequence(
    PFTowers +
    kt4PFJets +
    kt4PFJetsForRho +
    hiFJRhoProducer +
    hiFJRhoProducerFinerBins +
    hiFJGridEmptyAreaCalculator +
    hiFJGridEmptyAreaCalculatorFinerBins +

    hiPuRhoR3Producer +
    # flow modulator
    pfcandCleanerPt4Eta2 +
    ak4PFJetsForFlow +
    hiFJRhoFlowModulationProducer
)
