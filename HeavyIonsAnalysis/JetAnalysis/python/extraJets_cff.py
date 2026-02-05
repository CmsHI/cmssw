import FWCore.ParameterSet.Config as cms

from RecoHI.HiJetAlgos.PackedPFTowers_cfi import PackedPFTowers
from RecoHI.HiJetAlgos.HiRecoPFJets_cff import hiPuRho, hiFJRhoFlowModulation, ak4PFJetsForFlow, hiFJRhoFlowModulationIteration, akCs4PFJetsForFlow
from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import hiSignalGenParticles, allPartons
hiSignalGenParticles.src = "prunedGenParticles"
hiPuRho.src = 'PackedPFTowers'

# Configuration for flow subtracted jets
ak4PFJetsForFlow.src = "PackedPFTowers" # Use packed towers as a source if jetty areas are excluded in flow estimate
hiFJRhoFlowModulation.jetTag = "ak4PFJetsForFlow"  # Jet collection used for jetty region exclusion in final iteration
akCs4PFJetsForFlow.src = "packedPFCandidates" # Packed candidates as a source for jets for flow subtraction in first iteration if two iterations are done

# Create extra jet sequences
extraJetsData = cms.Sequence(PackedPFTowers + hiPuRho)
extraFlowJetsData = cms.Sequence(PackedPFTowers + hiPuRho + ak4PFJetsForFlow + hiFJRhoFlowModulation)
extraIterativeFlowJetsData = cms.Sequence(PackedPFTowers + hiPuRho + ak4PFJetsForFlow + hiFJRhoFlowModulationIteration + akCs4PFJetsForFlow + hiFJRhoFlowModulation)
extraJetsMC = cms.Sequence(PackedPFTowers + hiPuRho + hiSignalGenParticles + allPartons)
extraFlowJetsMC = cms.Sequence(PackedPFTowers + hiPuRho + hiSignalGenParticles + allPartons + ak4PFJetsForFlow + hiFJRhoFlowModulation)
extraIterativeFlowJetsMC = cms.Sequence(PackedPFTowers + hiPuRho + hiSignalGenParticles + allPartons + ak4PFJetsForFlow + hiFJRhoFlowModulationIteration + akCs4PFJetsForFlow + hiFJRhoFlowModulation)
