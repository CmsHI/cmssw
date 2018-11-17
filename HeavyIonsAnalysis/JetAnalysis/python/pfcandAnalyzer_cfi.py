import FWCore.ParameterSet.Config as cms

pfcandAnalyzer = cms.EDAnalyzer(
    'HiPFCandAnalyzer',
    pfCandidateLabel = cms.InputTag("particleFlow"),
    genLabel         = cms.InputTag('genParticles'),
    jetLabel         = cms.InputTag("ak5patJets"),
    pfPtMin          = cms.double(0.0),
    pfAbsEtaMax      = cms.double(5.0),
    genPtMin         = cms.double(0.5),
    jetPtMin         = cms.double(20.0),
    doMC             = cms.bool(False),
    doJets           = cms.bool(False),
    doCaloEnergy     = cms.bool(True),
    skipCharged      = cms.bool(False),
    )

pfcandAnalyzerCS = pfcandAnalyzer.clone(
    pfCandidateLabel = cms.InputTag("akCs4PFJets","pfParticlesCs"),
    doCaloEnergy     = cms.bool(False),
    )
