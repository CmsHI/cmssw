import FWCore.ParameterSet.Config as cms

from RecoBTag.ImpactParameter.pfImpactParameterTagInfos_cfi import pfImpactParameterTagInfos
pfImpactParameterTagInfos.jets = "slimmedJets"
pfImpactParameterTagInfos.candidates = "packedPFCandidates"
pfImpactParameterTagInfos.primaryVertex = "offlineSlimmedPrimaryVertices"
from RecoBTag.SecondaryVertex.pfSecondaryVertexTagInfos_cfi import pfSecondaryVertexTagInfos
# leave IVF workflow commented out for reference -matt
#from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import inclusiveCandidateVertexFinder
#from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import candidateVertexMerger
#from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import candidateVertexArbitrator
#from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import inclusiveCandidateSecondaryVertices
#from RecoBTag.SecondaryVertex.pfInclusiveSecondaryVertexFinderTagInfos_cfi import pfInclusiveSecondaryVertexFinderTagInfos
#inclusiveCandidateVertexFinder.primaryVertices  = "offlineSlimmedPrimaryVertices"
#inclusiveCandidateVertexFinder.tracks= "packedPFCandidates"
#candidateVertexArbitrator.tracks = "packedPFCandidates"
#candidateVertexArbitrator.primaryVertices = "offlineSlimmedPrimaryVertices"
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *
from RecoBTau.JetTagComputer.jetTagRecord_cfi import *
from RecoBTag.ImpactParameter.candidateJetProbabilityComputer_cfi import  *
from RecoBTag.ImpactParameter.pfJetProbabilityBJetTags_cfi import pfJetProbabilityBJetTags
from RecoBTag.Combined.pfDeepCSVTagInfos_cfi import pfDeepCSVTagInfos
from RecoBTag.Combined.pfDeepCSVJetTags_cfi import pfDeepCSVJetTags
pfDeepCSVTagInfos.svTagInfos = "pfSecondaryVertexTagInfos"

candidateBtagging = cms.Sequence(
    pfImpactParameterTagInfos +
    pfSecondaryVertexTagInfos +
    #inclusiveCandidateVertexFinder +
    #candidateVertexMerger +
    #candidateVertexArbitrator +
    #inclusiveCandidateSecondaryVertices +
    #pfInclusiveSecondaryVertexFinderTagInfos +
    pfJetProbabilityBJetTags +
    pfDeepCSVTagInfos + 
    pfDeepCSVJetTags
)
