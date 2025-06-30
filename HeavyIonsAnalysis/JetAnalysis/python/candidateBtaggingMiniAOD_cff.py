import FWCore.ParameterSet.Config as cms

from RecoBTag.ImpactParameter.pfImpactParameterTagInfos_cfi import pfImpactParameterTagInfos
pfImpactParameterTagInfos.jets = "akCs0PFpatJets"
pfImpactParameterTagInfos.candidates = "packedPFCandidates"
pfImpactParameterTagInfos.primaryVertex = "offlineSlimmedPrimaryVertices"
from RecoBTag.SecondaryVertex.pfSecondaryVertexTagInfos_cfi import pfSecondaryVertexTagInfos

from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import inclusiveCandidateVertexFinder
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import candidateVertexMerger
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import candidateVertexArbitrator
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import inclusiveCandidateSecondaryVertices
from RecoBTag.SecondaryVertex.pfInclusiveSecondaryVertexFinderTagInfos_cfi import pfInclusiveSecondaryVertexFinderTagInfos
inclusiveCandidateVertexFinder.primaryVertices  = "offlineSlimmedPrimaryVertices"
inclusiveCandidateVertexFinder.tracks= "packedPFCandidates"
inclusiveCandidateVertexFinder.minHits = 0
inclusiveCandidateVertexFinder.minPt = 0.8
candidateVertexArbitrator.tracks = "packedPFCandidates"
candidateVertexArbitrator.primaryVertices = "offlineSlimmedPrimaryVertices"

from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *
from RecoBTau.JetTagComputer.jetTagRecord_cfi import *
from RecoBTag.ImpactParameter.candidateJetProbabilityComputer_cfi import  *
from RecoBTag.ImpactParameter.pfJetProbabilityBJetTags_cfi import pfJetProbabilityBJetTags

from RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK4_cff import pfParticleNetFromMiniAODAK4CHSCentralTagInfos,pfParticleNetFromMiniAODAK4CHSCentralJetTags,pfParticleNetFromMiniAODAK4CHSCentralDiscriminatorsJetTags
from RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK4_cff import pfParticleNetFromMiniAODAK4CHSForwardTagInfos,pfParticleNetFromMiniAODAK4CHSForwardJetTags,pfParticleNetFromMiniAODAK4CHSForwardDiscriminatorsJetTags

from RecoBTag.FeatureTools.pfParticleTransformerAK4TagInfos_cfi import pfParticleTransformerAK4TagInfos
pfParticleTransformerAK4TagInfosSlimmedDeepFlavour = pfParticleTransformerAK4TagInfos.clone(
    fallback_puppi_weight = True,
    fallback_vertex_association = True,
    jets = cms.InputTag("akCs0PFpatJets"),
    unsubjet_map = cms.InputTag("ak4PFMatchedForakCs0PFpatJets"),
    puppi_value_map = cms.InputTag(""),
    secondary_vertices = cms.InputTag("inclusiveCandidateSecondaryVertices"),
    vertex_associator = cms.InputTag(""),
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices")
)

from RecoBTag.ONNXRuntime.pfParticleTransformerAK4JetTags_cfi import pfParticleTransformerAK4JetTags
pfParticleTransformerAK4JetTagsSlimmedDeepFlavour = pfParticleTransformerAK4JetTags.clone(src = cms.InputTag("pfParticleTransformerAK4TagInfosSlimmedDeepFlavour"))

candidateBtagging = cms.Sequence(
    pfImpactParameterTagInfos +
    pfSecondaryVertexTagInfos +
    inclusiveCandidateVertexFinder +
    candidateVertexMerger +
    candidateVertexArbitrator +
    inclusiveCandidateSecondaryVertices +
    pfInclusiveSecondaryVertexFinderTagInfos +
    pfParticleTransformerAK4TagInfosSlimmedDeepFlavour +
    pfJetProbabilityBJetTags +
    pfParticleTransformerAK4JetTagsSlimmedDeepFlavour
)
