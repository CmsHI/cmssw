import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.JetAnalysis.rerecoGen_cff import *
from HeavyIonsAnalysis.JetAnalysis.rerecoJets_JEC_cff import *
from HeavyIonsAnalysis.JetAnalysis.rerecoTracks_cff import *

from HeavyIonsAnalysis.JetAnalysis.jets.ak4CaloJetSequence_pp_jec_cff import *

from HeavyIonsAnalysis.JetAnalysis.jets.ak1PFJetSequence_pp_jec_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak2PFJetSequence_pp_jec_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak3PFJetSequence_pp_jec_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak4PFJetSequence_pp_jec_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak5PFJetSequence_pp_jec_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak6PFJetSequence_pp_jec_cff import *

genJetSequence = cms.Sequence(
    genParticlesForJets +

    ak1GenJets +
    ak2GenJets +
    ak3GenJets +
    # ak4GenJets +
    ak5GenJets +
    ak6GenJets +

    ak1GenNjettiness +
    ak2GenNjettiness +
    ak3GenNjettiness +
    ak4GenNjettiness +
    ak5GenNjettiness +
    ak6GenNjettiness
)

jetSequence = cms.Sequence(
    # ak4CaloJets +

    ak1PFJets +
    ak2PFJets +
    ak3PFJets +
    # ak4PFJets +
    ak5PFJets +
    ak6PFJets +

    highPurityTracks +

    ak4CaloJetSequence +

    ak1PFJetSequence +
    ak2PFJetSequence +
    ak3PFJetSequence +
    ak4PFJetSequence +
    ak5PFJetSequence +
    ak6PFJetSequence
)
