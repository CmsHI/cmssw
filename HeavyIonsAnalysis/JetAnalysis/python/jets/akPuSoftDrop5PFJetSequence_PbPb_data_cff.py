

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop5PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop5PFJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akPuSoftDrop5PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop5HiGenJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akPuSoftDrop5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop5PFJets")
                                                        )

akPuSoftDrop5PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop5PFJets"),
    payload = "AKPu5PF_offline"
    )

akPuSoftDrop5PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop5CaloJets'))

#akPuSoftDrop5PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5HiSignalGenJets'))

akPuSoftDrop5PFbTagger = bTaggers("akPuSoftDrop5PF",0.5)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop5PFmatch = akPuSoftDrop5PFbTagger.match
akPuSoftDrop5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop5PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuSoftDrop5PFPatJetFlavourAssociationLegacy = akPuSoftDrop5PFbTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop5PFPatJetPartons = akPuSoftDrop5PFbTagger.PatJetPartons
akPuSoftDrop5PFJetTracksAssociatorAtVertex = akPuSoftDrop5PFbTagger.JetTracksAssociatorAtVertex
akPuSoftDrop5PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop5PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop5PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop5PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop5PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop5PFCombinedSecondaryVertexBJetTags = akPuSoftDrop5PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop5PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop5PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop5PFJetBProbabilityBJetTags = akPuSoftDrop5PFbTagger.JetBProbabilityBJetTags
akPuSoftDrop5PFSoftPFMuonByPtBJetTags = akPuSoftDrop5PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop5PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop5PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop5PFTrackCountingHighEffBJetTags = akPuSoftDrop5PFbTagger.TrackCountingHighEffBJetTags
akPuSoftDrop5PFTrackCountingHighPurBJetTags = akPuSoftDrop5PFbTagger.TrackCountingHighPurBJetTags
akPuSoftDrop5PFPatJetPartonAssociationLegacy = akPuSoftDrop5PFbTagger.PatJetPartonAssociationLegacy

akPuSoftDrop5PFImpactParameterTagInfos = akPuSoftDrop5PFbTagger.ImpactParameterTagInfos
akPuSoftDrop5PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop5PFJetProbabilityBJetTags = akPuSoftDrop5PFbTagger.JetProbabilityBJetTags

akPuSoftDrop5PFSecondaryVertexTagInfos = akPuSoftDrop5PFbTagger.SecondaryVertexTagInfos
akPuSoftDrop5PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop5PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop5PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop5PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop5PFCombinedSecondaryVertexBJetTags = akPuSoftDrop5PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop5PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop5PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop5PFSecondaryVertexNegativeTagInfos = akPuSoftDrop5PFbTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop5PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop5PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop5PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop5PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop5PFNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop5PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop5PFPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop5PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop5PFNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop5PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop5PFPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop5PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop5PFSoftPFMuonsTagInfos = akPuSoftDrop5PFbTagger.SoftPFMuonsTagInfos
akPuSoftDrop5PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop5PFSoftPFMuonBJetTags = akPuSoftDrop5PFbTagger.SoftPFMuonBJetTags
akPuSoftDrop5PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop5PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop5PFSoftPFMuonByPtBJetTags = akPuSoftDrop5PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop5PFNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop5PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop5PFPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop5PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop5PFPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop5PFPatJetPartonAssociationLegacy*akPuSoftDrop5PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop5PFPatJetFlavourAssociation = akPuSoftDrop5PFbTagger.PatJetFlavourAssociation
#akPuSoftDrop5PFPatJetFlavourId = cms.Sequence(akPuSoftDrop5PFPatJetPartons*akPuSoftDrop5PFPatJetFlavourAssociation)

akPuSoftDrop5PFJetBtaggingIP       = cms.Sequence(akPuSoftDrop5PFImpactParameterTagInfos *
            (akPuSoftDrop5PFTrackCountingHighEffBJetTags +
             akPuSoftDrop5PFTrackCountingHighPurBJetTags +
             akPuSoftDrop5PFJetProbabilityBJetTags +
             akPuSoftDrop5PFJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop5PFJetBtaggingSV = cms.Sequence(akPuSoftDrop5PFImpactParameterTagInfos
            *
            akPuSoftDrop5PFSecondaryVertexTagInfos
            * (akPuSoftDrop5PFSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop5PFSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop5PFCombinedSecondaryVertexBJetTags+
                akPuSoftDrop5PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop5PFJetBtaggingNegSV = cms.Sequence(akPuSoftDrop5PFImpactParameterTagInfos
            *
            akPuSoftDrop5PFSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop5PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop5PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop5PFNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop5PFPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop5PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop5PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop5PFJetBtaggingMu = cms.Sequence(akPuSoftDrop5PFSoftPFMuonsTagInfos * (akPuSoftDrop5PFSoftPFMuonBJetTags
                +
                akPuSoftDrop5PFSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop5PFSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop5PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop5PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop5PFJetBtagging = cms.Sequence(akPuSoftDrop5PFJetBtaggingIP
            *akPuSoftDrop5PFJetBtaggingSV
            *akPuSoftDrop5PFJetBtaggingNegSV
#            *akPuSoftDrop5PFJetBtaggingMu
            )

akPuSoftDrop5PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop5PFJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop5PFmatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop5PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop5PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop5PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop5PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop5PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop5PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop5PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop5PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop5PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop5PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop5PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop5PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop5PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop5PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop5PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop5PFJetID"),
        addBTagInfo = True,
        addTagInfos = True,
        addDiscriminators = True,
        addAssociatedTracks = True,
        addJetCharge = False,
        addJetID = False,
        getJetMCFlavour = False,
        addGenPartonMatch = False,
        addGenJetMatch = False,
        embedGenJetMatch = False,
        embedGenPartonMatch = False,
        # embedCaloTowers = False,
        # embedPFCandidates = True
        )

akPuSoftDrop5PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop5PFJets"),
           	    R0  = cms.double( 0.5)
)
akPuSoftDrop5PFpatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop5PFNjettiness:tau1','akPuSoftDrop5PFNjettiness:tau2','akPuSoftDrop5PFNjettiness:tau3']

akPuSoftDrop5PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop5PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak5HiGenJets',
                                                             rParam = 0.5,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlowTmp'),
                                                             trackTag = cms.InputTag("hiGeneralTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
							     doSubEvent = False,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop5PF"),
                                                             jetName = cms.untracked.string("akPuSoftDrop5PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop5GenJets"),
                                                             doGenTaus = False
                                                             )

akPuSoftDrop5PFJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop5PFclean
                                                  #*
                                                  akPuSoftDrop5PFmatch
                                                  #*
                                                  #akPuSoftDrop5PFmatchGroomed
                                                  *
                                                  akPuSoftDrop5PFparton
                                                  *
                                                  akPuSoftDrop5PFcorr
                                                  *
                                                  #akPuSoftDrop5PFJetID
                                                  #*
                                                  akPuSoftDrop5PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop5PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop5PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop5PFJetBtagging
                                                  *
                                                  akPuSoftDrop5PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop5PFpatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop5PFJetAnalyzer
                                                  )

akPuSoftDrop5PFJetSequence_data = cms.Sequence(akPuSoftDrop5PFcorr
                                                    *
                                                    #akPuSoftDrop5PFJetID
                                                    #*
                                                    akPuSoftDrop5PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop5PFJetBtagging
                                                    *
                                                    akPuSoftDrop5PFNjettiness 
                                                    *
                                                    akPuSoftDrop5PFpatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop5PFJetAnalyzer
                                                    )

akPuSoftDrop5PFJetSequence_jec = cms.Sequence(akPuSoftDrop5PFJetSequence_mc)
akPuSoftDrop5PFJetSequence_mb = cms.Sequence(akPuSoftDrop5PFJetSequence_mc)

akPuSoftDrop5PFJetSequence = cms.Sequence(akPuSoftDrop5PFJetSequence_data)
