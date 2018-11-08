import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.TrackAnalysis.trackAnalyzer_cfi import *

anaTrack = ppTrack.clone(
    trackPtMin = 0.49,
    trackSrc = cms.InputTag("hiGeneralTracks"),
    vertexSrc = cms.vstring('hiSelectedVertex'),
    mvaSrc = cms.InputTag('hiGeneralTracks','MVAVals'),
    pfCandSrc = cms.InputTag("particleFlowTmp"))

pixelTrack = anaTrack.clone(
    trackPtMin = 0.4,
    trackSrc = cms.InputTag("hiConformalPixelTracks"),
    qualityStrings = cms.untracked.vstring('highPurity'))

trackSequencesPbPb = cms.Sequence(anaTrack)

trackSequencesPP = cms.Sequence(ppTrack)
