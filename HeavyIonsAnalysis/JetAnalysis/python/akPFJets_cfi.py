import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoHI.HiJetAlgos.HiPFJetParameters_cff import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets

ak4PFJets.jetPtMin = 1.0
ak4PFJets.doAreaFastjet = cms.bool(True)

akPu4PFJets = cms.EDProducer(
    "FastjetJetProducer",
    HiPFJetParameters,
    AnomalousCellParameters,
    MultipleAlgoIteratorBlock,
    jetAlgorithm = cms.string("AntiKt"),
    rParam       = cms.double(0.4)
)
akPu4PFJets.jetType               = cms.string('BasicJet')
akPu4PFJets.doPUOffsetCorr        = True
akPu4PFJets.subtractorName        = cms.string("MultipleAlgoIterator")
akPu4PFJets.src                   = cms.InputTag('PFTowers')
akPu4PFJets.doAreaFastjet         = False
akPu4PFJets.puPtMin               = cms.double(20.0)
akPu4PFJets.minimumTowersFraction = cms.double(0.5)
akPu4PFJets.jetPtMin = 1.0

akCs4PFJets = cms.EDProducer(
    "CSJetProducer",
    HiPFJetParameters,
    AnomalousCellParameters,
    jetAlgorithm        = cms.string("AntiKt"),
    rParam              = cms.double(0.4),
    etaMap              = cms.InputTag('hiFJRhoProducer','mapEtaEdges'),
    rho                 = cms.InputTag('hiFJRhoProducer','mapToRho'),
    rhom                = cms.InputTag('hiFJRhoProducer','mapToRhoM'),
    csRParam            = cms.double(-1.),
    csAlpha             = cms.double(2.),
    useModulatedRho     = cms.bool(False),
    writeJetsWithConst  = cms.bool(True),
    jetCollInstanceName = cms.string("pfParticlesCs")
)
akCs4PFJets.jetPtMin          = cms.double(0.0)
akCs4PFJets.doAreaFastjet     = cms.bool(True)
akCs4PFJets.useExplicitGhosts = cms.bool(True)
akCs4PFJets.GhostArea         = cms.double(0.005)

# hybrid jets with flow correction
akFlowPuCs4PFJets = akCs4PFJets.clone(
    etaMap = cms.InputTag('hiPuRhoR3Producer','mapEtaEdges'),
    rho = cms.InputTag('hiPuRhoR3Producer','mapToRho'),
    rhom = cms.InputTag('hiPuRhoR3Producer','mapToRhoM'),
    rhoFlowFitParams = cms.InputTag('hiFJRhoFlowModulationProducer','rhoFlowFitParams'),
    jetCollInstanceName = cms.string("pfParticlesCs"),
    useModulatedRho = cms.bool(True)
)

# legacy pu subtraction
akULPu4PFJets = akPu4PFJets.clone(
    minimumTowersFraction = cms.double(0.0))

# jets for deriving jec
ak4PFJECJets = ak4PFJets.clone(
    doSubEvent = cms.bool(True))

akPu4PFJECJets = akPu4PFJets.clone(
    doSubEvent = cms.bool(True))

akCs4PFJECJets = akCs4PFJets.clone(
    doSubEvent = cms.bool(True))

# jets for legacy hi reco: using unlinked particle flow objects
ak4HIPFJets = ak4PFJets.clone(
    src = 'particleFlowTmp')

akPu4HIPFJets = akPu4PFJets.clone(
    src = 'particleFlowTmp')

akCs4HIPFJets = cms.EDProducer(
    "CSJetProducer",
    PFJetParameters,
    AnomalousCellParameters,
    jetAlgorithm        = cms.string("AntiKt"),
    rParam              = cms.double(0.4),
    etaMap              = cms.InputTag('hiFJRhoProducer','mapEtaEdges'),
    rho                 = cms.InputTag('hiFJGridEmptyAreaCalculator','mapToRhoCorr1Bin'),
    rhom                = cms.InputTag('hiFJGridEmptyAreaCalculator','mapToRhoMCorr1Bin'),
    csAlpha             = cms.double(1.),
    writeJetsWithConst  = cms.bool(True),
    jetCollInstanceName = cms.string("pfParticlesCs")
)
akCs4HIPFJets.src               = cms.InputTag('particleFlowTmp')
akCs4HIPFJets.jetPtMin          = cms.double(0.0)
akCs4HIPFJets.doAreaFastjet     = cms.bool(True)
akCs4HIPFJets.useExplicitGhosts = cms.bool(True)
akCs4HIPFJets.GhostArea         = cms.double(0.005)

akULPu4HIPFJets = akULPu4PFJets.clone(
    src = 'particleFlowTmp')

# cloning jets for other radii
ak1PFJets = ak4PFJets.clone(rParam = 0.1)
ak2PFJets = ak4PFJets.clone(rParam = 0.2)
ak3PFJets = ak4PFJets.clone(rParam = 0.3)
ak5PFJets = ak4PFJets.clone(rParam = 0.5)
ak6PFJets = ak4PFJets.clone(rParam = 0.6)

akPu1PFJets = akPu4PFJets.clone(rParam = 0.1, puPtMin = cms.double(10.0))
akPu2PFJets = akPu4PFJets.clone(rParam = 0.2, puPtMin = cms.double(10.0))
akPu3PFJets = akPu4PFJets.clone(rParam = 0.3, puPtMin = cms.double(15.0))
akPu5PFJets = akPu4PFJets.clone(rParam = 0.5, puPtMin = cms.double(25.0))
akPu6PFJets = akPu4PFJets.clone(rParam = 0.6, puPtMin = cms.double(30.0))

akCs1PFJets = akCs4PFJets.clone(rParam = 0.1)
akCs2PFJets = akCs4PFJets.clone(rParam = 0.2)
akCs3PFJets = akCs4PFJets.clone(rParam = 0.3)
akCs5PFJets = akCs4PFJets.clone(rParam = 0.5)
akCs6PFJets = akCs4PFJets.clone(rParam = 0.6)

akFlowPuCs1PFJets = akFlowPuCs4PFJets.clone(rParam = 0.1)
akFlowPuCs2PFJets = akFlowPuCs4PFJets.clone(rParam = 0.2)
akFlowPuCs3PFJets = akFlowPuCs4PFJets.clone(rParam = 0.3)
akFlowPuCs5PFJets = akFlowPuCs4PFJets.clone(rParam = 0.5)
akFlowPuCs6PFJets = akFlowPuCs4PFJets.clone(rParam = 0.6)

akULPu1PFJets = akPu1PFJets.clone(minimumTowersFraction = cms.double(0.0))
akULPu2PFJets = akPu2PFJets.clone(minimumTowersFraction = cms.double(0.0))
akULPu3PFJets = akPu3PFJets.clone(minimumTowersFraction = cms.double(0.0))
akULPu5PFJets = akPu5PFJets.clone(minimumTowersFraction = cms.double(0.0))
akULPu6PFJets = akPu6PFJets.clone(minimumTowersFraction = cms.double(0.0))

ak1PFJECJets = ak1PFJets.clone(doSubEvent = cms.bool(True))
ak2PFJECJets = ak2PFJets.clone(doSubEvent = cms.bool(True))
ak3PFJECJets = ak3PFJets.clone(doSubEvent = cms.bool(True))
ak5PFJECJets = ak5PFJets.clone(doSubEvent = cms.bool(True))
ak6PFJECJets = ak6PFJets.clone(doSubEvent = cms.bool(True))

akPu1PFJECJets = akPu1PFJets.clone(doSubEvent = cms.bool(True))
akPu2PFJECJets = akPu2PFJets.clone(doSubEvent = cms.bool(True))
akPu3PFJECJets = akPu3PFJets.clone(doSubEvent = cms.bool(True))
akPu5PFJECJets = akPu5PFJets.clone(doSubEvent = cms.bool(True))
akPu6PFJECJets = akPu6PFJets.clone(doSubEvent = cms.bool(True))

akCs1PFJECJets = akCs1PFJets.clone(doSubEvent = cms.bool(True))
akCs2PFJECJets = akCs2PFJets.clone(doSubEvent = cms.bool(True))
akCs3PFJECJets = akCs3PFJets.clone(doSubEvent = cms.bool(True))
akCs5PFJECJets = akCs5PFJets.clone(doSubEvent = cms.bool(True))
akCs6PFJECJets = akCs6PFJets.clone(doSubEvent = cms.bool(True))

ak1HIPFJets = ak1PFJets.clone(src = 'particleFlowTmp')
ak2HIPFJets = ak2PFJets.clone(src = 'particleFlowTmp')
ak3HIPFJets = ak3PFJets.clone(src = 'particleFlowTmp')
ak5HIPFJets = ak5PFJets.clone(src = 'particleFlowTmp')
ak6HIPFJets = ak6PFJets.clone(src = 'particleFlowTmp')

akCs1HIPFJets = akCs4HIPFJets.clone(rParam = 0.1)
akCs2HIPFJets = akCs4HIPFJets.clone(rParam = 0.2)
akCs3HIPFJets = akCs4HIPFJets.clone(rParam = 0.3)
akCs5HIPFJets = akCs4HIPFJets.clone(rParam = 0.5)
akCs6HIPFJets = akCs4HIPFJets.clone(rParam = 0.6)
