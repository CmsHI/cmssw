import FWCore.ParameterSet.Config as cms

hltMuTree = cms.EDAnalyzer("HLTMuTree",
                           muons = cms.InputTag("slimmedMuons"),
                           vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
                           doReco = cms.untracked.bool(True),
                           doGen = cms.untracked.bool(False),
                           genparticle = cms.InputTag("genParticles")
)
