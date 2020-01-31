import FWCore.ParameterSet.Config as cms

#from PhysicsTools.PatAlgos.patHeavyIonSequences_cff import *
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import *
from PhysicsTools.PatAlgos.mcMatchLayer0.jetFlavourId_cff import *


from RecoJets.JetAssociationProducers.ak5JTA_cff import *
from RecoBTag.Configuration.RecoBTag_cff import *

class bTaggers:
    def __init__(self,jetname,rParam,ispp,doSubjets):
        self.JetTracksAssociatorAtVertex = ak5JetTracksAssociatorAtVertex.clone()
        self.JetTracksAssociatorAtVertex.jets = cms.InputTag(jetname+"Jets")
	if(ispp):
		self.JetTracksAssociatorAtVertex.tracks = cms.InputTag("generalTracks")
	else:
        	self.JetTracksAssociatorAtVertex.tracks = cms.InputTag("hiGeneralTracks")
        self.ImpactParameterTagInfos = impactParameterTagInfos.clone()
        self.ImpactParameterTagInfos.jetTracks = cms.InputTag(jetname+"JetTracksAssociatorAtVertex")
        self.PfImpactParameterTagInfos = pfImpactParameterTagInfos.clone()
        self.PfImpactParameterTagInfos.jets = cms.InputTag(jetname+"Jets")
        self.TrackCountingHighEffBJetTags          = trackCountingHighEffBJetTags.clone()
        self.TrackCountingHighEffBJetTags.tagInfos = cms.VInputTag(cms.InputTag(jetname+"ImpactParameterTagInfos"))
        self.TrackCountingHighPurBJetTags          = trackCountingHighPurBJetTags.clone()
        self.TrackCountingHighPurBJetTags.tagInfos = cms.VInputTag(cms.InputTag(jetname+"ImpactParameterTagInfos"))
        self.JetProbabilityBJetTags                = jetProbabilityBJetTags.clone()
        self.JetProbabilityBJetTags.tagInfos       = cms.VInputTag(cms.InputTag(jetname+"ImpactParameterTagInfos"))
        self.JetBProbabilityBJetTags               = jetBProbabilityBJetTags.clone()
        self.JetBProbabilityBJetTags.tagInfos      = cms.VInputTag(cms.InputTag(jetname+"ImpactParameterTagInfos"))

        # secondary vertex b-tag
        self.SecondaryVertexTagInfos                     = secondaryVertexTagInfos.clone()
        self.SecondaryVertexTagInfos.trackIPTagInfos     = cms.InputTag(jetname+"ImpactParameterTagInfos")
        self.PfInclusiveSecondaryVertexFinderTagInfos                     = pfInclusiveSecondaryVertexFinderTagInfos.clone()
        self.PfInclusiveSecondaryVertexFinderTagInfos.trackIPTagInfos     = cms.InputTag(jetname+"PfImpactParameterTagInfos")
        self.PfDeepCSVTagInfos = pfDeepCSVTagInfos.clone()
        self.PfDeepCSVTagInfos.svTagInfos = cms.InputTag(jetname+"PfInclusiveSecondaryVertexFinderTagInfos")
        self.SimpleSecondaryVertexHighEffBJetTags               = simpleSecondaryVertexHighEffBJetTags.clone()
        self.SimpleSecondaryVertexHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag(jetname+"SecondaryVertexTagInfos"))
        self.SimpleSecondaryVertexHighPurBJetTags               = simpleSecondaryVertexHighPurBJetTags.clone()
        self.SimpleSecondaryVertexHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag(jetname+"SecondaryVertexTagInfos"))
        self.CombinedSecondaryVertexBJetTags             = combinedSecondaryVertexV2BJetTags.clone()
        self.CombinedSecondaryVertexBJetTags.tagInfos    = cms.VInputTag(cms.InputTag(jetname+"ImpactParameterTagInfos"),
                cms.InputTag(jetname+"SecondaryVertexTagInfos"))
        self.CombinedSecondaryVertexV2BJetTags          = combinedSecondaryVertexV2BJetTags.clone()
        self.CombinedSecondaryVertexV2BJetTags.tagInfos = cms.VInputTag(cms.InputTag(jetname+"ImpactParameterTagInfos"),
                cms.InputTag(jetname+"SecondaryVertexTagInfos"))
        self.PfDeepCSVJetTags          = pfDeepCSVJetTags.clone()
        self.PfDeepCSVJetTags.src = cms.InputTag(jetname+"PfDeepCSVTagInfos")
        self.PfDeepCSVJetTags.NNConfig = cms.FileInPath('RecoBTag/Combined/data/DeepCSV_PhaseI.json')
        self.PfDeepCSVJetTags.checkSVForDefaults = cms.bool(True)
        self.PfDeepCSVJetTags.meanPadding = cms.bool(True)
        self.PfDeepCSVJetTags.toAdd = cms.PSet()

        self.SoftPFMuonsTagInfos                = softPFMuonsTagInfos.clone()
        self.SoftPFMuonsTagInfos.jets           = cms.InputTag(jetname+"Jets")
        #self.SoftPFMuonsTagInfos.primaryVertex  = cms.InputTag("offlinePrimaryVertices")
        self.SoftPFMuonBJetTags                = softPFMuonBJetTags.clone()
        self.SoftPFMuonBJetTags.tagInfos       = cms.VInputTag(cms.InputTag(jetname+"SoftPFMuonsTagInfos"))
        self.SoftPFMuonByIP3dBJetTags          = softPFMuonByIP3dBJetTags.clone()
        self.SoftPFMuonByIP3dBJetTags.tagInfos = cms.VInputTag(cms.InputTag(jetname+"SoftPFMuonsTagInfos"))
        self.SoftPFMuonByPtBJetTags            = softPFMuonByPtBJetTags.clone()
        self.SoftPFMuonByPtBJetTags.tagInfos   = cms.VInputTag(cms.InputTag(jetname+"SoftPFMuonsTagInfos"))



	if doSubjets:
		self.SubjetImpactParameterTagInfos = impactParameterTagInfos.clone()
		self.SubjetImpactParameterTagInfos.jetTracks = cms.InputTag(jetname+"SubjetJetTracksAssociatorAtVertex")
		self.SubjetJetProbabilityBJetTags = jetProbabilityBJetTags.clone()
		self.SubjetJetProbabilityBJetTags.tagInfos = cms.VInputTag(cms.InputTag(jetname+"SubjetImpactParameterTagInfos"))
		self.SubjetSecondaryVertexTagInfos = secondaryVertexTagInfos.clone() 
		self.SubjetSecondaryVertexTagInfos.trackIPTagInfos = cms.InputTag(jetname+'SubjetImpactParameterTagInfos')
		self.SubjetSecondaryVertexTagInfos.fatJets = cms.InputTag('ak4PFJets')
		self.SubjetSecondaryVertexTagInfos.groomedFatJets = cms.InputTag(jetname+'Jets')
		self.SubjetSecondaryVertexTagInfos.useSVClustering = cms.bool(True)
		self.SubjetSecondaryVertexTagInfos.useExternalSV = cms.bool(True)
		self.SubjetSecondaryVertexTagInfos.jetAlgorithm = cms.string('AntiKt')
		self.SubjetSecondaryVertexTagInfos.useSVMomentum = cms.bool(True)
		self.SubjetSecondaryVertexTagInfos.rParam = cms.double(0.4)
		self.SubjetSecondaryVertexTagInfos.extSVCollection = cms.InputTag('inclusiveSecondaryVertices')
		self.SubjetSecondaryVertexTagInfos.vertexCuts.maxDeltaRToJetAxis = cms.double(0.1)

		self.SubjetJetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorExplicit",
			jets = cms.InputTag(jetname+'Jets','SubJets')
		)
		if ispp:
			self.SubjetJetTracksAssociatorAtVertex.tracks = cms.InputTag('highPurityTracks')
		else:
			self.SubjetJetTracksAssociatorAtVertex.tracks = cms.InputTag('highPurityTracks')

		self.CombinedSubjetSecondaryVertexV2BJetTags = combinedSecondaryVertexV2BJetTags.clone(
			tagInfos = cms.VInputTag(cms.InputTag(jetname+"SubjetImpactParameterTagInfos"),
			cms.InputTag(jetname+"SubjetSecondaryVertexTagInfos"))
		)
		self.CombinedSubjetSecondaryVertexBJetTags = combinedSecondaryVertexV2BJetTags.clone(
			tagInfos = cms.VInputTag(cms.InputTag(jetname+"SubjetImpactParameterTagInfos"),
			cms.InputTag(jetname+"SubjetSecondaryVertexTagInfos"))
		)


        self.JetTracksAssociator = cms.Sequence(self.JetTracksAssociatorAtVertex)
        self.JetBtaggingIP       = cms.Sequence(self.ImpactParameterTagInfos * self.PfImpactParameterTagInfos *(
                self.TrackCountingHighEffBJetTags +
                self.TrackCountingHighPurBJetTags +
                self.JetProbabilityBJetTags +
                self.JetBProbabilityBJetTags 
                )
                                                )

        self.JetBtaggingSV = cms.Sequence(self.ImpactParameterTagInfos * self.PfImpactParameterTagInfos *
                                          self.SecondaryVertexTagInfos * (self.SimpleSecondaryVertexHighEffBJetTags +
                                                                          self.SimpleSecondaryVertexHighPurBJetTags +
                                                                          self.CombinedSecondaryVertexBJetTags +
                                                                          self.CombinedSecondaryVertexV2BJetTags
                                                                          ) 
                                          * self.PfInclusiveSecondaryVertexFinderTagInfos
                                          * self.PfDeepCSVTagInfos
                                          * self.PfDeepCSVJetTags
                )



        self.JetBtaggingMu = cms.Sequence(self.SoftPFMuonsTagInfos 
                                          * (self.SoftPFMuonBJetTags +
                                             self.SoftPFMuonByIP3dBJetTags +
                                             self.SoftPFMuonByPtBJetTags 
            )
                                          )

        self.JetBtagging = cms.Sequence(self.JetBtaggingIP
                *self.JetBtaggingSV
                *self.JetBtaggingMu
                )

        self.PatJetPartonAssociationLegacy       = patJetPartonAssociationLegacy.clone(
            jets = cms.InputTag(jetname+"Jets"),
            partons = cms.InputTag("myPartons")
            )

        self.PatJetFlavourAssociationLegacy      = patJetFlavourAssociationLegacy.clone(
            srcByReference = cms.InputTag(jetname+"PatJetPartonAssociationLegacy")
            )

        self.patJetFlavourIdLegacy = cms.Sequence( self.PatJetPartonAssociationLegacy * self.PatJetFlavourAssociationLegacy)

        self.PatJetPartons = patJetPartons.clone()
        self.PatJetFlavourAssociation = patJetFlavourAssociation.clone(
            jets = cms.InputTag(jetname+"Jets"),
            rParam = rParam,
            bHadrons = cms.InputTag(jetname+"PatJetPartons","bHadrons"),
            cHadrons = cms.InputTag(jetname+"PatJetPartons","cHadrons"),
            partons = cms.InputTag(jetname+"PatJetPartons","algorithmicPartons"),
            leptons = cms.InputTag(jetname+"PatJetPartons","leptons"),
            )

	if doSubjets:
		self.PatJetFlavourAssociation.jets="ak4PFJets"
		self.PatJetFlavourAssociation.groomedJets = cms.InputTag(jetname+'Jets')
		self.PatJetFlavourAssociation.subjets = cms.InputTag(jetname+'Jets', 'SubJets')

        self.PatJetFlavourId               = cms.Sequence(self.PatJetPartons*self.PatJetFlavourAssociation)
        #self.match   = patJetGenJetMatch.clone(
        #    src      = cms.InputTag(jetname+"Jets"),
        #    matched  = cms.InputTag(jetname+"clean"),
        #    maxDeltaR = rParam 
        #    )
        self.parton  = patJetPartonMatch.clone(src      = cms.InputTag(jetname+"Jets"),
                                                matched = cms.InputTag("genParticles")
                                                )

