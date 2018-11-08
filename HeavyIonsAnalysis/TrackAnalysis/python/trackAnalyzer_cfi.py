import FWCore.ParameterSet.Config as cms

ppTrack = cms.EDAnalyzer(
    'TrackAnalyzer',
    trackPtMin = cms.untracked.double(0.01),
    simTrackPtMin = cms.untracked.double(0.1),
    vertexSrc = cms.vstring('offlinePrimaryVertices'),
    trackSrc = cms.InputTag('generalTracks'),
    mvaSrc = cms.InputTag("generalTracks","MVAVals"),
    particleSrc = cms.InputTag('genParticles'),
    pfCandSrc = cms.InputTag('particleFlow'),
    beamSpotSrc = cms.untracked.InputTag('offlineBeamSpot'),
    doPFMatching = cms.untracked.bool(True),
    doSimTrack = cms.untracked.bool(False),
    doSimVertex = cms.untracked.bool(False),
    useQuality = cms.untracked.bool(False),
    qualityString = cms.untracked.string('highPurity'),
    qualityStrings = cms.untracked.vstring('highPurity','tight','loose'),
    tpFakeSrc = cms.untracked.InputTag('mix','MergedTrackTruth'),
    tpEffSrc = cms.untracked.InputTag('mix','MergedTrackTruth'),
    # associateChi2 = cms.bool(False),
    associatorMap = cms.InputTag('tpRecoAssocHiGeneralTracks'),
    doMVA = cms.untracked.bool(False),
    fillSimTrack = cms.untracked.bool(False)
)
