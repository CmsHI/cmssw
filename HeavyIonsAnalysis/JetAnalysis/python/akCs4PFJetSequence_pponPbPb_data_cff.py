import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *

akCs4PFJetAnalyzer = inclusiveJetAnalyzer.clone(
    jetTag = cms.InputTag("slimmedJets"),
    rParam = 0.4,
    fillGenJets = False,
    isMC = False,
    bTagJetName = cms.untracked.string("akCs4PF"),
    jetName = cms.untracked.string("akCs4PF"),
    hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
    )

akCs4PFJetSequence_mc = cms.Sequence(

    akCs4PFJetAnalyzer
    )

akCs4PFJetSequence_data = cms.Sequence(

    akCs4PFJetAnalyzer
    )

akCs4PFJetSequence_mb = cms.Sequence(
    akCs4PFJetSequence_mc)
akCs4PFJetSequence_jec = cms.Sequence(
    akCs4PFJetSequence_mc)

akCs4PFJetSequence = cms.Sequence(
    akCs4PFJetSequence_data)
