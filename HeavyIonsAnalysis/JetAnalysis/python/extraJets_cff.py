import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import PackedPFTowers, hiPuRho, hiFJRhoFlowModulation, ak4PFJetsForFlow
hiPuRho.src = 'PackedPFTowers'

# Configuration for flow subtracted jets
ak4PFJetsForFlow.src = "PackedPFTowers" # Use packed towers as a source if jetty areas are excluded in flow estimate
hiFJRhoFlowModulation.jetTag = "ak4PFJetsForFlow"  # Jet collection used for jetty region exclusion

# Create extra jet sequences
extraJets = cms.Sequence(PackedPFTowers + hiPuRho)
extraFlowJets = cms.Sequence(PackedPFTowers + hiPuRho + ak4PFJetsForFlow + hiFJRhoFlowModulation)
