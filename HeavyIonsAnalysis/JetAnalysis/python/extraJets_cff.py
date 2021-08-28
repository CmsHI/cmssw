import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import PFTowers, hiPuRho, hiSignalGenParticles, allPartons
PFTowers.src = "packedPFCandidates"
PFTowers.useHF = True
hiSignalGenParticles.src = "prunedGenParticles"

extraJetsData = cms.Sequence(PFTowers + hiPuRho)
extraJetsMC = cms.Sequence(PFTowers + hiPuRho + hiSignalGenParticles + allPartons)

