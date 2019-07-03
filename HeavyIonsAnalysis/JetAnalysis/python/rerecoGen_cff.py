import FWCore.ParameterSet.Config as cms

from RecoJets.Configuration.GenJetParticles_cff import genParticlesForJets

from HeavyIonsAnalysis.JetAnalysis.akGenJets_cfi import (
    ak1GenJets, ak2GenJets, ak3GenJets, ak4GenJets, ak5GenJets, ak6GenJets,
    akSoftDrop1GenJets, akSoftDrop2GenJets, akSoftDrop3GenJets,
    akSoftDrop4GenJets, akSoftDrop5GenJets, akSoftDrop6GenJets)

from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness
ak1GenNjettiness = Njettiness.clone(src = "ak1GenJets", R0 = 0.1)
ak2GenNjettiness = Njettiness.clone(src = "ak2GenJets", R0 = 0.2)
ak3GenNjettiness = Njettiness.clone(src = "ak3GenJets", R0 = 0.3)
ak4GenNjettiness = Njettiness.clone(src = "ak4GenJets", R0 = 0.4)
ak5GenNjettiness = Njettiness.clone(src = "ak5GenJets", R0 = 0.5)
ak6GenNjettiness = Njettiness.clone(src = "ak6GenJets", R0 = 0.6)
