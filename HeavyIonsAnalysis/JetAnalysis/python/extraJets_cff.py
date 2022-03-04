import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import PFTowers, hiPuRho, hiSignalGenParticles, allPartons
PFTowers.src = "packedPFCandidates"
PFTowers.useHF = True
hiSignalGenParticles.src = "prunedGenParticles"

extraJetsData = cms.Sequence(PFTowers + hiPuRho)
extraJetsMC = cms.Sequence(PFTowers + hiPuRho + hiSignalGenParticles + allPartons)

from RecoHI.HiJetAlgos.EventConstSub_cfi import EventConstSub
extraECSJetsData = cms.Sequence(PFTowers + hiPuRho + EventConstSub)
extraECSJetsMC = cms.Sequence(PFTowers + hiPuRho + EventConstSub + hiSignalGenParticles + allPartons)
