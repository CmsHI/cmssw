import FWCore.ParameterSet.Config as cms

trackAnalyzer = cms.EDAnalyzer('TrackAnalyzer',
    doTrack = cms.untracked.bool(True),
    trackPtMin = cms.untracked.double(0.01),
    vertexSrc = cms.InputTag("unpackedTracksAndVertices"),
    packedCandSrc = cms.InputTag("packedPFCandidates"),
    lostTracksSrc = cms.InputTag("lostTracks"),
    beamSpotSrc = cms.untracked.InputTag('offlineBeamSpot'),
    chi2Map = cms.InputTag("packedPFCandidateTrackChi2"),
    chi2MapLost = cms.InputTag("lostTrackChi2")
)
