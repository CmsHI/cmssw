import FWCore.ParameterSet.Config as cms

### PP RECO does not include R=3 or R=5 jets.
### re-RECO is only possible for PF, RECO is missing calotowers
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
ak3PFJets = ak4PFJets.clone(rParam = 0.3)
ak5PFJets = ak4PFJets.clone(rParam = 0.5)
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
ak5GenJets = ak4GenJets.clone(rParam = 0.5)

from HeavyIonsAnalysis.JetAnalysis.jets.HiRecoPFJets_cff import *
#from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
#from RecoHI.HiJetAlgos.hiFJRhoProducer import hiFJRhoProducer
PFTowers.src = cms.InputTag("particleFlow")
from RecoHI.HiJetAlgos.hiFJGridEmptyAreaCalculator_cff import hiFJGridEmptyAreaCalculator
hiFJGridEmptyAreaCalculator.doCentrality = cms.bool(False)
kt4PFJetsForRho.src = cms.InputTag('particleFlow')
kt4PFJetsForRho.doAreaFastjet = True
kt4PFJetsForRho.jetPtMin      = cms.double(0.0)
kt4PFJetsForRho.GhostArea     = cms.double(0.005)
#kt2PFJets = kt4PFJets.clone(rParam       = cms.double(0.2))
akCs4PFJets.src           = cms.InputTag('particleFlow')

#SoftDrop PF jets
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
akSoftDrop4PFJets = cms.EDProducer(
    "FastjetJetProducer",
    PFJetParameters,
    AnomalousCellParameters,
    jetAlgorithm = cms.string("AntiKt"),
    rParam       = cms.double(0.4),
    useSoftDrop = cms.bool(True),
    zcut = cms.double(0.1),
    beta = cms.double(0.0),
    R0   = cms.double(0.4),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
)

from HeavyIonsAnalysis.JetAnalysis.akSoftDrop4GenJets_cfi import akSoftDrop4GenJets

#Filter PF jets
akFilter4PFJets = cms.EDProducer(
    "FastjetJetProducer",
    PFJetParameters,
    AnomalousCellParameters,
    jetAlgorithm = cms.string("AntiKt"),
    rParam       = cms.double(0.4),
    useFiltering = cms.bool(True),
    nFilt = cms.int32(4),
    rFilt = cms.double(0.15),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
)

from RecoJets.Configuration.GenJetParticles_cff import *
from RecoHI.HiJetAlgos.HiGenJets_cff import *
from HeavyIonsAnalysis.JetAnalysis.makePartons_cff import myPartons

from HeavyIonsAnalysis.JetAnalysis.jets.ak3PFJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak4PFJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak5PFJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak4CaloJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akPu4PFJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akCs4PFJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akSoftDrop4PFJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akSoftDrop5PFJetSequence_pp_mc_cff import *

highPurityTracks = cms.EDFilter("TrackSelector",
                                src = cms.InputTag("generalTracks"),
                                cut = cms.string('quality("highPurity")')
)

# Other radii jets and calo jets need to be reconstructed
jetSequences = cms.Sequence(
    myPartons +
    genParticlesForJets +
    ak4GenJets +
    kt4PFJetsForRho*hiFJRhoProducer +
    hiFJGridEmptyAreaCalculator +
    PFTowers +
    akPu4PFJets +
    akCs4PFJets +
    akSoftDrop4PFJets +
    akFilter4PFJets +
    akSoftDrop4GenJets +
    highPurityTracks +
    ak4PFJetSequence +
#    ak4CaloJetSequence +
#    akSoftDrop4PFJetSequence +
    akPu4PFJetSequence +
    akCs4PFJetSequence
)
