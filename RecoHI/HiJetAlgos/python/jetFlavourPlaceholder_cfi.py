import FWCore.ParameterSet.Config as cms

jetFlavourPlaceholder = cms.EDProducer(
    'JetFlavourPlaceholder',
    jets = cms.InputTag('ak4HiGenJets'),
    )
