import FWCore.ParameterSet.Config as cms

from RecoBTag.ImpactParameter.pfImpactParameterTagInfos_cfi import pfImpactParameterTagInfos
pfImpactParameterTagInfos.jets = "slimmedJets"
pfImpactParameterTagInfos.candidates = "packedPFCandidates"
pfImpactParameterTagInfos.primaryVertex = "offlineSlimmedPrimaryVerticesRecovery"
from RecoBTag.SecondaryVertex.pfSecondaryVertexTagInfos_cfi import pfSecondaryVertexTagInfos
# leave IVF workflow commented out for reference -matt
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import inclusiveCandidateVertexFinder
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import candidateVertexMerger
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import candidateVertexArbitrator
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import inclusiveCandidateSecondaryVertices
from RecoBTag.SecondaryVertex.pfInclusiveSecondaryVertexFinderTagInfos_cfi import pfInclusiveSecondaryVertexFinderTagInfos
inclusiveCandidateVertexFinder.primaryVertices  = "offlineSlimmedPrimaryVerticesRecovery"
inclusiveCandidateVertexFinder.tracks= "packedPFCandidates"
candidateVertexArbitrator.tracks = "packedPFCandidates"
candidateVertexArbitrator.primaryVertices = "offlineSlimmedPrimaryVerticesRecovery"
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *
from RecoBTau.JetTagComputer.jetTagRecord_cfi import *
from RecoBTag.ImpactParameter.candidateJetProbabilityComputer_cfi import  *
from RecoBTag.ImpactParameter.pfJetProbabilityBJetTags_cfi import pfJetProbabilityBJetTags
from RecoBTag.Combined.pfDeepCSVTagInfos_cfi import pfDeepCSVTagInfos
from RecoBTag.Combined.pfDeepCSVJetTags_cfi import pfDeepCSVJetTags
pfDeepCSVTagInfos.svTagInfos = "pfSecondaryVertexTagInfos"

from RecoBTag.ONNXRuntime.pfParticleNetAK4_cff import pfParticleNetAK4TagInfos, pfParticleNetAK4JetTags
from RecoBTag.ONNXRuntime.pfParticleNetAK4DiscriminatorsJetTags_cfi import pfParticleNetAK4DiscriminatorsJetTags
pfParticleNetAK4TagInfos.jets = "updatedPatJets"
pfParticleNetAK4TagInfos.unsubjet_map = "unsubJets"
pfParticleNetAK4TagInfos.use_puppiP4 = False
pfParticleNetAK4TagInfos.pf_candidates = "packedPFCandidates"
pfParticleNetAK4TagInfos.puppi_value_map = ''
pfParticleNetAK4TagInfos.vertex_associator = ""
pfParticleNetAK4TagInfos.vertices = "offlineSlimmedPrimaryVerticesRecovery"

pfParticleNetAK4JetTags.src = "pfParticleNetAK4TagInfos"

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
ak4PFJets = ak4PFJets.clone(rParam = 0.4, src = 'packedPFCandidates')

unsubJets = cms.EDProducer("JetMatcherDR",
    matched = cms.InputTag("ak4PFJets"),
    source = cms.InputTag("updatedPatJets")
)

candidateBtagging = cms.Sequence(
    pfImpactParameterTagInfos +
    pfSecondaryVertexTagInfos +
    inclusiveCandidateVertexFinder +
    candidateVertexMerger +
    candidateVertexArbitrator +
    inclusiveCandidateSecondaryVertices +
    pfInclusiveSecondaryVertexFinderTagInfos +
    ak4PFJets +
    unsubJets +
    pfParticleNetAK4TagInfos +
    pfParticleNetAK4JetTags +  
    pfParticleNetAK4DiscriminatorsJetTags
)
