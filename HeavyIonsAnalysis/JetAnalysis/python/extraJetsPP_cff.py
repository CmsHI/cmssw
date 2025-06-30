import FWCore.ParameterSet.Config as cms


from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import hiSignalGenParticles, allPartons
hiSignalGenParticles.src = "prunedGenParticles"

# Create extra jet sequences
extraJets = cms.Sequence(hiSignalGenParticles + allPartons)
