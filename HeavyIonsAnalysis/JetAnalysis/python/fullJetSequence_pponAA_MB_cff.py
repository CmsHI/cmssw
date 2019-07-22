import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.JetAnalysis.rerecoGen_cff import *
from HeavyIonsAnalysis.JetAnalysis.rerecoRho_cff import *
from HeavyIonsAnalysis.JetAnalysis.rerecoJets_cff import *
from HeavyIonsAnalysis.JetAnalysis.rerecoTracks_cff import *

from HeavyIonsAnalysis.JetAnalysis.jets.akPu3CaloJetSequence_pponPbPb_mb_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akPu3PFJetSequence_pponPbPb_mb_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akCs3PFJetSequence_pponPbPb_mb_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akFlowPuCs3PFJetSequence_pponPbPb_mb_cff import *

from HeavyIonsAnalysis.JetAnalysis.jets.akPu4CaloJetSequence_pponPbPb_mb_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akPu4PFJetSequence_pponPbPb_mb_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akCs4PFJetSequence_pponPbPb_mb_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akFlowPuCs4PFJetSequence_pponPbPb_mb_cff import *

genSignalSequence = cms.Sequence(
    genParticlesForJets +

    hiSignalGenParticles +
    genParticlesForJetsSignal +

    ak3HiGenJets +
    ak4HiGenJets +

    signalPartons +

    ak3HiSignalGenJets +
    ak4HiSignalGenJets +

    ak3HiGenNjettiness +
    ak4HiGenNjettiness
)

genCleanedSequence = cms.Sequence(
    genParticlesForJets +

    ak3HiGenJets +
    ak4HiGenJets +

    myPartons +
    cleanedPartons +

    ak3HiCleanedGenJets +
    ak4HiCleanedGenJets
)

jetSequence = cms.Sequence(
    rhoSequence +

    highPurityTracks +

    akPu3CaloJets +
    akPu3PFJets +
    akCs3PFJets +
    akFlowPuCs3PFJets +

    akPu4CaloJets +
    akPu4PFJets +
    akCs4PFJets +
    akFlowPuCs4PFJets +

    akPu3CaloJetSequence +
    akPu3PFJetSequence +
    akCs3PFJetSequence +
    akFlowPuCs3PFJetSequence +

    akPu4CaloJetSequence +
    akPu4PFJetSequence +
    akCs4PFJetSequence +
    akFlowPuCs4PFJetSequence
)
