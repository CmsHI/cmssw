import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.JetAnalysis.rerecoGen_cff import *
from HeavyIonsAnalysis.JetAnalysis.rerecoJets_cff import *
from HeavyIonsAnalysis.JetAnalysis.rerecoTracks_cff import *

from HeavyIonsAnalysis.JetAnalysis.jets.ak4CaloJetSequence_pp_mc_cff import *

from HeavyIonsAnalysis.JetAnalysis.jets.ak3PFJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak4PFJetSequence_pp_mc_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak5PFJetSequence_pp_mc_cff import *

genJetSequence = cms.Sequence(
    genParticlesForJets +

    ak3GenJets +
    # ak4GenJets +

    ak3GenNjettiness +
    ak4GenNjettiness
)

jetSequence = cms.Sequence(
    # ak4CaloJets +

    ak3PFJets +
    # ak4PFJets +

    highPurityTracks +

    ak4CaloJetSequence +

    ak3PFJetSequence +
    ak4PFJetSequence
)
