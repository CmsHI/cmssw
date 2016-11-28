

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter2PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter2PFJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.2
    )

akVsFilter2PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter2GenJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.2
    )

akVsFilter2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter2PFJets")
                                                        )

akVsFilter2PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter2PFJets"),
    payload = "AK2PF_offline"
    )

akVsFilter2PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter2CaloJets'))

#akVsFilter2PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2GenJets'))

akVsFilter2PFbTagger = bTaggers("akVsFilter2PF",0.2)

#create objects locally since they dont load properly otherwise
#akVsFilter2PFmatch = akVsFilter2PFbTagger.match
akVsFilter2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter2PFJets"), matched = cms.InputTag("genParticles"))
akVsFilter2PFPatJetFlavourAssociationLegacy = akVsFilter2PFbTagger.PatJetFlavourAssociationLegacy
akVsFilter2PFPatJetPartons = akVsFilter2PFbTagger.PatJetPartons
akVsFilter2PFJetTracksAssociatorAtVertex = akVsFilter2PFbTagger.JetTracksAssociatorAtVertex
akVsFilter2PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter2PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter2PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter2PFCombinedSecondaryVertexBJetTags = akVsFilter2PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter2PFCombinedSecondaryVertexV2BJetTags = akVsFilter2PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter2PFJetBProbabilityBJetTags = akVsFilter2PFbTagger.JetBProbabilityBJetTags
akVsFilter2PFSoftPFMuonByPtBJetTags = akVsFilter2PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter2PFSoftPFMuonByIP3dBJetTags = akVsFilter2PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter2PFTrackCountingHighEffBJetTags = akVsFilter2PFbTagger.TrackCountingHighEffBJetTags
akVsFilter2PFTrackCountingHighPurBJetTags = akVsFilter2PFbTagger.TrackCountingHighPurBJetTags
akVsFilter2PFPatJetPartonAssociationLegacy = akVsFilter2PFbTagger.PatJetPartonAssociationLegacy

akVsFilter2PFImpactParameterTagInfos = akVsFilter2PFbTagger.ImpactParameterTagInfos
akVsFilter2PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter2PFJetProbabilityBJetTags = akVsFilter2PFbTagger.JetProbabilityBJetTags

akVsFilter2PFSecondaryVertexTagInfos = akVsFilter2PFbTagger.SecondaryVertexTagInfos
akVsFilter2PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter2PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter2PFCombinedSecondaryVertexBJetTags = akVsFilter2PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter2PFCombinedSecondaryVertexV2BJetTags = akVsFilter2PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter2PFSecondaryVertexNegativeTagInfos = akVsFilter2PFbTagger.SecondaryVertexNegativeTagInfos
akVsFilter2PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter2PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter2PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter2PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter2PFNegativeCombinedSecondaryVertexBJetTags = akVsFilter2PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter2PFPositiveCombinedSecondaryVertexBJetTags = akVsFilter2PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter2PFNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter2PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter2PFPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter2PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter2PFSoftPFMuonsTagInfos = akVsFilter2PFbTagger.SoftPFMuonsTagInfos
akVsFilter2PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter2PFSoftPFMuonBJetTags = akVsFilter2PFbTagger.SoftPFMuonBJetTags
akVsFilter2PFSoftPFMuonByIP3dBJetTags = akVsFilter2PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter2PFSoftPFMuonByPtBJetTags = akVsFilter2PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter2PFNegativeSoftPFMuonByPtBJetTags = akVsFilter2PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter2PFPositiveSoftPFMuonByPtBJetTags = akVsFilter2PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter2PFPatJetFlavourIdLegacy = cms.Sequence(akVsFilter2PFPatJetPartonAssociationLegacy*akVsFilter2PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter2PFPatJetFlavourAssociation = akVsFilter2PFbTagger.PatJetFlavourAssociation
#akVsFilter2PFPatJetFlavourId = cms.Sequence(akVsFilter2PFPatJetPartons*akVsFilter2PFPatJetFlavourAssociation)

akVsFilter2PFJetBtaggingIP       = cms.Sequence(akVsFilter2PFImpactParameterTagInfos *
            (akVsFilter2PFTrackCountingHighEffBJetTags +
             akVsFilter2PFTrackCountingHighPurBJetTags +
             akVsFilter2PFJetProbabilityBJetTags +
             akVsFilter2PFJetBProbabilityBJetTags 
            )
            )

akVsFilter2PFJetBtaggingSV = cms.Sequence(akVsFilter2PFImpactParameterTagInfos
            *
            akVsFilter2PFSecondaryVertexTagInfos
            * (akVsFilter2PFSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter2PFSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter2PFCombinedSecondaryVertexBJetTags+
                akVsFilter2PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter2PFJetBtaggingNegSV = cms.Sequence(akVsFilter2PFImpactParameterTagInfos
            *
            akVsFilter2PFSecondaryVertexNegativeTagInfos
            * (akVsFilter2PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter2PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter2PFNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter2PFPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter2PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter2PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter2PFJetBtaggingMu = cms.Sequence(akVsFilter2PFSoftPFMuonsTagInfos * (akVsFilter2PFSoftPFMuonBJetTags
                +
                akVsFilter2PFSoftPFMuonByIP3dBJetTags
                +
                akVsFilter2PFSoftPFMuonByPtBJetTags
                +
                akVsFilter2PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter2PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter2PFJetBtagging = cms.Sequence(akVsFilter2PFJetBtaggingIP
            *akVsFilter2PFJetBtaggingSV
            *akVsFilter2PFJetBtaggingNegSV
#            *akVsFilter2PFJetBtaggingMu
            )

akVsFilter2PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter2PFJets"),
        genJetMatch          = cms.InputTag("akVsFilter2PFmatch"),
        genPartonMatch       = cms.InputTag("akVsFilter2PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter2PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter2PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter2PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter2PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter2PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter2PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter2PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter2PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter2PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter2PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter2PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter2PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter2PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter2PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter2PFJetID"),
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

akVsFilter2PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter2PFJets"),
           	    R0  = cms.double( 0.2)
)
akVsFilter2PFpatJetsWithBtagging.userData.userFloats.src += ['akVsFilter2PFNjettiness:tau1','akVsFilter2PFNjettiness:tau2','akVsFilter2PFNjettiness:tau3']

akVsFilter2PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter2PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak2GenJets',
                                                             rParam = 0.2,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlow'),
                                                             trackTag = cms.InputTag("generalTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
							     doSubEvent = False,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akVsFilter2PF"),
                                                             jetName = cms.untracked.string("akVsFilter2PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter2GenJets"),
                                                             doGenTaus = False
                                                             )

akVsFilter2PFJetSequence_mc = cms.Sequence(
                                                  #akVsFilter2PFclean
                                                  #*
                                                  akVsFilter2PFmatch
                                                  #*
                                                  #akVsFilter2PFmatchGroomed
                                                  *
                                                  akVsFilter2PFparton
                                                  *
                                                  akVsFilter2PFcorr
                                                  *
                                                  #akVsFilter2PFJetID
                                                  #*
                                                  akVsFilter2PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter2PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter2PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter2PFJetBtagging
                                                  *
                                                  akVsFilter2PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter2PFpatJetsWithBtagging
                                                  *
                                                  akVsFilter2PFJetAnalyzer
                                                  )

akVsFilter2PFJetSequence_data = cms.Sequence(akVsFilter2PFcorr
                                                    *
                                                    #akVsFilter2PFJetID
                                                    #*
                                                    akVsFilter2PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter2PFJetBtagging
                                                    *
                                                    akVsFilter2PFNjettiness 
                                                    *
                                                    akVsFilter2PFpatJetsWithBtagging
                                                    *
                                                    akVsFilter2PFJetAnalyzer
                                                    )

akVsFilter2PFJetSequence_jec = cms.Sequence(akVsFilter2PFJetSequence_mc)
akVsFilter2PFJetSequence_mb = cms.Sequence(akVsFilter2PFJetSequence_mc)

akVsFilter2PFJetSequence = cms.Sequence(akVsFilter2PFJetSequence_data)
