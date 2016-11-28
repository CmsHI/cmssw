

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter2PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter2PFJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akFilter2PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter2GenJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akFilter2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter2PFJets")
                                                        )

akFilter2PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter2PFJets"),
    payload = "AK2PF_offline"
    )

akFilter2PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter2CaloJets'))

#akFilter2PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2GenJets'))

akFilter2PFbTagger = bTaggers("akFilter2PF",0.2)

#create objects locally since they dont load properly otherwise
#akFilter2PFmatch = akFilter2PFbTagger.match
akFilter2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter2PFJets"), matched = cms.InputTag("genParticles"))
akFilter2PFPatJetFlavourAssociationLegacy = akFilter2PFbTagger.PatJetFlavourAssociationLegacy
akFilter2PFPatJetPartons = akFilter2PFbTagger.PatJetPartons
akFilter2PFJetTracksAssociatorAtVertex = akFilter2PFbTagger.JetTracksAssociatorAtVertex
akFilter2PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter2PFSimpleSecondaryVertexHighEffBJetTags = akFilter2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter2PFSimpleSecondaryVertexHighPurBJetTags = akFilter2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter2PFCombinedSecondaryVertexBJetTags = akFilter2PFbTagger.CombinedSecondaryVertexBJetTags
akFilter2PFCombinedSecondaryVertexV2BJetTags = akFilter2PFbTagger.CombinedSecondaryVertexV2BJetTags
akFilter2PFJetBProbabilityBJetTags = akFilter2PFbTagger.JetBProbabilityBJetTags
akFilter2PFSoftPFMuonByPtBJetTags = akFilter2PFbTagger.SoftPFMuonByPtBJetTags
akFilter2PFSoftPFMuonByIP3dBJetTags = akFilter2PFbTagger.SoftPFMuonByIP3dBJetTags
akFilter2PFTrackCountingHighEffBJetTags = akFilter2PFbTagger.TrackCountingHighEffBJetTags
akFilter2PFTrackCountingHighPurBJetTags = akFilter2PFbTagger.TrackCountingHighPurBJetTags
akFilter2PFPatJetPartonAssociationLegacy = akFilter2PFbTagger.PatJetPartonAssociationLegacy

akFilter2PFImpactParameterTagInfos = akFilter2PFbTagger.ImpactParameterTagInfos
akFilter2PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter2PFJetProbabilityBJetTags = akFilter2PFbTagger.JetProbabilityBJetTags

akFilter2PFSecondaryVertexTagInfos = akFilter2PFbTagger.SecondaryVertexTagInfos
akFilter2PFSimpleSecondaryVertexHighEffBJetTags = akFilter2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter2PFSimpleSecondaryVertexHighPurBJetTags = akFilter2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter2PFCombinedSecondaryVertexBJetTags = akFilter2PFbTagger.CombinedSecondaryVertexBJetTags
akFilter2PFCombinedSecondaryVertexV2BJetTags = akFilter2PFbTagger.CombinedSecondaryVertexV2BJetTags

akFilter2PFSecondaryVertexNegativeTagInfos = akFilter2PFbTagger.SecondaryVertexNegativeTagInfos
akFilter2PFNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter2PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter2PFNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter2PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter2PFNegativeCombinedSecondaryVertexBJetTags = akFilter2PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter2PFPositiveCombinedSecondaryVertexBJetTags = akFilter2PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter2PFNegativeCombinedSecondaryVertexV2BJetTags = akFilter2PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter2PFPositiveCombinedSecondaryVertexV2BJetTags = akFilter2PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter2PFSoftPFMuonsTagInfos = akFilter2PFbTagger.SoftPFMuonsTagInfos
akFilter2PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter2PFSoftPFMuonBJetTags = akFilter2PFbTagger.SoftPFMuonBJetTags
akFilter2PFSoftPFMuonByIP3dBJetTags = akFilter2PFbTagger.SoftPFMuonByIP3dBJetTags
akFilter2PFSoftPFMuonByPtBJetTags = akFilter2PFbTagger.SoftPFMuonByPtBJetTags
akFilter2PFNegativeSoftPFMuonByPtBJetTags = akFilter2PFbTagger.NegativeSoftPFMuonByPtBJetTags
akFilter2PFPositiveSoftPFMuonByPtBJetTags = akFilter2PFbTagger.PositiveSoftPFMuonByPtBJetTags
akFilter2PFPatJetFlavourIdLegacy = cms.Sequence(akFilter2PFPatJetPartonAssociationLegacy*akFilter2PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter2PFPatJetFlavourAssociation = akFilter2PFbTagger.PatJetFlavourAssociation
#akFilter2PFPatJetFlavourId = cms.Sequence(akFilter2PFPatJetPartons*akFilter2PFPatJetFlavourAssociation)

akFilter2PFJetBtaggingIP       = cms.Sequence(akFilter2PFImpactParameterTagInfos *
            (akFilter2PFTrackCountingHighEffBJetTags +
             akFilter2PFTrackCountingHighPurBJetTags +
             akFilter2PFJetProbabilityBJetTags +
             akFilter2PFJetBProbabilityBJetTags 
            )
            )

akFilter2PFJetBtaggingSV = cms.Sequence(akFilter2PFImpactParameterTagInfos
            *
            akFilter2PFSecondaryVertexTagInfos
            * (akFilter2PFSimpleSecondaryVertexHighEffBJetTags+
                akFilter2PFSimpleSecondaryVertexHighPurBJetTags+
                akFilter2PFCombinedSecondaryVertexBJetTags+
                akFilter2PFCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter2PFJetBtaggingNegSV = cms.Sequence(akFilter2PFImpactParameterTagInfos
            *
            akFilter2PFSecondaryVertexNegativeTagInfos
            * (akFilter2PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter2PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter2PFNegativeCombinedSecondaryVertexBJetTags+
                akFilter2PFPositiveCombinedSecondaryVertexBJetTags+
                akFilter2PFNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter2PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter2PFJetBtaggingMu = cms.Sequence(akFilter2PFSoftPFMuonsTagInfos * (akFilter2PFSoftPFMuonBJetTags
                +
                akFilter2PFSoftPFMuonByIP3dBJetTags
                +
                akFilter2PFSoftPFMuonByPtBJetTags
                +
                akFilter2PFNegativeSoftPFMuonByPtBJetTags
                +
                akFilter2PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter2PFJetBtagging = cms.Sequence(akFilter2PFJetBtaggingIP
            *akFilter2PFJetBtaggingSV
            *akFilter2PFJetBtaggingNegSV
#            *akFilter2PFJetBtaggingMu
            )

akFilter2PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter2PFJets"),
        genJetMatch          = cms.InputTag("akFilter2PFmatch"),
        genPartonMatch       = cms.InputTag("akFilter2PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter2PFcorr")),
        JetPartonMapSource   = cms.InputTag("akFilter2PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter2PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter2PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter2PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter2PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter2PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter2PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter2PFJetBProbabilityBJetTags"),
            cms.InputTag("akFilter2PFJetProbabilityBJetTags"),
            #cms.InputTag("akFilter2PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter2PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter2PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter2PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter2PFJetID"),
        addBTagInfo = True,
        addTagInfos = True,
        addDiscriminators = True,
        addAssociatedTracks = True,
        addJetCharge = False,
        addJetID = False,
        getJetMCFlavour = True,
        addGenPartonMatch = True,
        addGenJetMatch = True,
        embedGenJetMatch = True,
        embedGenPartonMatch = True,
        # embedCaloTowers = False,
        # embedPFCandidates = True
        )

akFilter2PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter2PFJets"),
           	    R0  = cms.double( 0.2)
)
akFilter2PFpatJetsWithBtagging.userData.userFloats.src += ['akFilter2PFNjettiness:tau1','akFilter2PFNjettiness:tau2','akFilter2PFNjettiness:tau3']

akFilter2PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter2PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak2GenJets',
                                                             rParam = 0.2,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlow'),
                                                             trackTag = cms.InputTag("generalTracks"),
                                                             fillGenJets = True,
                                                             isMC = True,
							     doSubEvent = True,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akFilter2PF"),
                                                             jetName = cms.untracked.string("akFilter2PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter2GenJets"),
                                                             doGenTaus = True
                                                             )

akFilter2PFJetSequence_mc = cms.Sequence(
                                                  #akFilter2PFclean
                                                  #*
                                                  akFilter2PFmatch
                                                  #*
                                                  #akFilter2PFmatchGroomed
                                                  *
                                                  akFilter2PFparton
                                                  *
                                                  akFilter2PFcorr
                                                  *
                                                  #akFilter2PFJetID
                                                  #*
                                                  akFilter2PFPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter2PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter2PFJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter2PFJetBtagging
                                                  *
                                                  akFilter2PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter2PFpatJetsWithBtagging
                                                  *
                                                  akFilter2PFJetAnalyzer
                                                  )

akFilter2PFJetSequence_data = cms.Sequence(akFilter2PFcorr
                                                    *
                                                    #akFilter2PFJetID
                                                    #*
                                                    akFilter2PFJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter2PFJetBtagging
                                                    *
                                                    akFilter2PFNjettiness 
                                                    *
                                                    akFilter2PFpatJetsWithBtagging
                                                    *
                                                    akFilter2PFJetAnalyzer
                                                    )

akFilter2PFJetSequence_jec = cms.Sequence(akFilter2PFJetSequence_mc)
akFilter2PFJetSequence_mb = cms.Sequence(akFilter2PFJetSequence_mc)

akFilter2PFJetSequence = cms.Sequence(akFilter2PFJetSequence_mc)
