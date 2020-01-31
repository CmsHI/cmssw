import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.JetAnalysis.rechitanalyzer_cfi import *

rechitanalyzer.vtxSrc = cms.InputTag("offlinePrimaryVerticesWithBS")
rechitanalyzer.JetSrc = cms.InputTag("ak3CaloJets")

pfTowers.vtxSrc = cms.InputTag("offlinePrimaryVerticesWithBS")
pfTowers.JetSrc = cms.InputTag("ak3CaloJets")
