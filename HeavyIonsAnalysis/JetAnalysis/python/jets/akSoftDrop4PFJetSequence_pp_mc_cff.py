

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akSoftDrop4PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop4PFJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akSoftDrop4PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop4GenJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akSoftDrop4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop4PFJets")
                                                        )

akSoftDrop4PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akSoftDrop4PFJets"),
    payload = "AK4PF_offline"
    )

akSoftDrop4PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akSoftDrop4CaloJets'))

#akSoftDrop4PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4GenJets'))

akSoftDrop4PFbTagger = bTaggers("akSoftDrop4PF",0.4)

#create objects locally since they dont load properly otherwise
#akSoftDrop4PFmatch = akSoftDrop4PFbTagger.match
akSoftDrop4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop4PFJets"), matched = cms.InputTag("genParticles"))
akSoftDrop4PFPatJetFlavourAssociationLegacy = akSoftDrop4PFbTagger.PatJetFlavourAssociationLegacy
akSoftDrop4PFPatJetPartons = akSoftDrop4PFbTagger.PatJetPartons
akSoftDrop4PFJetTracksAssociatorAtVertex = akSoftDrop4PFbTagger.JetTracksAssociatorAtVertex
akSoftDrop4PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags = akSoftDrop4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags = akSoftDrop4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop4PFCombinedSecondaryVertexBJetTags = akSoftDrop4PFbTagger.CombinedSecondaryVertexBJetTags
akSoftDrop4PFCombinedSecondaryVertexV2BJetTags = akSoftDrop4PFbTagger.CombinedSecondaryVertexV2BJetTags
akSoftDrop4PFJetBProbabilityBJetTags = akSoftDrop4PFbTagger.JetBProbabilityBJetTags
akSoftDrop4PFSoftPFMuonByPtBJetTags = akSoftDrop4PFbTagger.SoftPFMuonByPtBJetTags
akSoftDrop4PFSoftPFMuonByIP3dBJetTags = akSoftDrop4PFbTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop4PFTrackCountingHighEffBJetTags = akSoftDrop4PFbTagger.TrackCountingHighEffBJetTags
akSoftDrop4PFTrackCountingHighPurBJetTags = akSoftDrop4PFbTagger.TrackCountingHighPurBJetTags
akSoftDrop4PFPatJetPartonAssociationLegacy = akSoftDrop4PFbTagger.PatJetPartonAssociationLegacy

akSoftDrop4PFImpactParameterTagInfos = akSoftDrop4PFbTagger.ImpactParameterTagInfos
akSoftDrop4PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop4PFJetProbabilityBJetTags = akSoftDrop4PFbTagger.JetProbabilityBJetTags

akSoftDrop4PFSecondaryVertexTagInfos = akSoftDrop4PFbTagger.SecondaryVertexTagInfos
akSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags = akSoftDrop4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags = akSoftDrop4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop4PFCombinedSecondaryVertexBJetTags = akSoftDrop4PFbTagger.CombinedSecondaryVertexBJetTags
akSoftDrop4PFCombinedSecondaryVertexV2BJetTags = akSoftDrop4PFbTagger.CombinedSecondaryVertexV2BJetTags

akSoftDrop4PFSecondaryVertexNegativeTagInfos = akSoftDrop4PFbTagger.SecondaryVertexNegativeTagInfos
akSoftDrop4PFNegativeSimpleSecondaryVertexHighEffBJetTags = akSoftDrop4PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akSoftDrop4PFNegativeSimpleSecondaryVertexHighPurBJetTags = akSoftDrop4PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akSoftDrop4PFNegativeCombinedSecondaryVertexBJetTags = akSoftDrop4PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akSoftDrop4PFPositiveCombinedSecondaryVertexBJetTags = akSoftDrop4PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akSoftDrop4PFNegativeCombinedSecondaryVertexV2BJetTags = akSoftDrop4PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akSoftDrop4PFPositiveCombinedSecondaryVertexV2BJetTags = akSoftDrop4PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akSoftDrop4PFSoftPFMuonsTagInfos = akSoftDrop4PFbTagger.SoftPFMuonsTagInfos
akSoftDrop4PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop4PFSoftPFMuonBJetTags = akSoftDrop4PFbTagger.SoftPFMuonBJetTags
akSoftDrop4PFSoftPFMuonByIP3dBJetTags = akSoftDrop4PFbTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop4PFSoftPFMuonByPtBJetTags = akSoftDrop4PFbTagger.SoftPFMuonByPtBJetTags
akSoftDrop4PFNegativeSoftPFMuonByPtBJetTags = akSoftDrop4PFbTagger.NegativeSoftPFMuonByPtBJetTags
akSoftDrop4PFPositiveSoftPFMuonByPtBJetTags = akSoftDrop4PFbTagger.PositiveSoftPFMuonByPtBJetTags
akSoftDrop4PFPatJetFlavourIdLegacy = cms.Sequence(akSoftDrop4PFPatJetPartonAssociationLegacy*akSoftDrop4PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akSoftDrop4PFPatJetFlavourAssociation = akSoftDrop4PFbTagger.PatJetFlavourAssociation
#akSoftDrop4PFPatJetFlavourId = cms.Sequence(akSoftDrop4PFPatJetPartons*akSoftDrop4PFPatJetFlavourAssociation)

akSoftDrop4PFJetBtaggingIP       = cms.Sequence(akSoftDrop4PFImpactParameterTagInfos *
            (akSoftDrop4PFTrackCountingHighEffBJetTags +
             akSoftDrop4PFTrackCountingHighPurBJetTags +
             akSoftDrop4PFJetProbabilityBJetTags +
             akSoftDrop4PFJetBProbabilityBJetTags 
            )
            )

akSoftDrop4PFJetBtaggingSV = cms.Sequence(akSoftDrop4PFImpactParameterTagInfos
            *
            akSoftDrop4PFSecondaryVertexTagInfos
            * (akSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop4PFCombinedSecondaryVertexBJetTags+
                akSoftDrop4PFCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop4PFJetBtaggingNegSV = cms.Sequence(akSoftDrop4PFImpactParameterTagInfos
            *
            akSoftDrop4PFSecondaryVertexNegativeTagInfos
            * (akSoftDrop4PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop4PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop4PFNegativeCombinedSecondaryVertexBJetTags+
                akSoftDrop4PFPositiveCombinedSecondaryVertexBJetTags+
                akSoftDrop4PFNegativeCombinedSecondaryVertexV2BJetTags+
                akSoftDrop4PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop4PFJetBtaggingMu = cms.Sequence(akSoftDrop4PFSoftPFMuonsTagInfos * (akSoftDrop4PFSoftPFMuonBJetTags
                +
                akSoftDrop4PFSoftPFMuonByIP3dBJetTags
                +
                akSoftDrop4PFSoftPFMuonByPtBJetTags
                +
                akSoftDrop4PFNegativeSoftPFMuonByPtBJetTags
                +
                akSoftDrop4PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akSoftDrop4PFJetBtagging = cms.Sequence(akSoftDrop4PFJetBtaggingIP
            *akSoftDrop4PFJetBtaggingSV
            *akSoftDrop4PFJetBtaggingNegSV
#            *akSoftDrop4PFJetBtaggingMu
            )

akSoftDrop4PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akSoftDrop4PFJets"),
        genJetMatch          = cms.InputTag("akSoftDrop4PFmatch"),
        genPartonMatch       = cms.InputTag("akSoftDrop4PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akSoftDrop4PFcorr")),
        JetPartonMapSource   = cms.InputTag("akSoftDrop4PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akSoftDrop4PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akSoftDrop4PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akSoftDrop4PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akSoftDrop4PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akSoftDrop4PFJetBProbabilityBJetTags"),
            cms.InputTag("akSoftDrop4PFJetProbabilityBJetTags"),
            #cms.InputTag("akSoftDrop4PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akSoftDrop4PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akSoftDrop4PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akSoftDrop4PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akSoftDrop4PFJetID"),
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

akSoftDrop4PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akSoftDrop4PFJets"),
           	    R0  = cms.double( 0.4)
)
akSoftDrop4PFpatJetsWithBtagging.userData.userFloats.src += ['akSoftDrop4PFNjettiness:tau1','akSoftDrop4PFNjettiness:tau2','akSoftDrop4PFNjettiness:tau3']

akSoftDrop4PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akSoftDrop4PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak4GenJets',
                                                             rParam = 0.4,
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
                                                             bTagJetName = cms.untracked.string("akSoftDrop4PF"),
                                                             jetName = cms.untracked.string("akSoftDrop4PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(True),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop4GenJets"),
                                                             doGenTaus = True
                                                             )

akSoftDrop4PFJetSequence_mc = cms.Sequence(
                                                  #akSoftDrop4PFclean
                                                  #*
                                                  akSoftDrop4PFmatch
                                                  #*
                                                  #akSoftDrop4PFmatchGroomed
                                                  *
                                                  akSoftDrop4PFparton
                                                  *
                                                  akSoftDrop4PFcorr
                                                  *
                                                  #akSoftDrop4PFJetID
                                                  #*
                                                  akSoftDrop4PFPatJetFlavourIdLegacy
                                                  #*
			                          #akSoftDrop4PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akSoftDrop4PFJetTracksAssociatorAtVertex
                                                  *
                                                  akSoftDrop4PFJetBtagging
                                                  *
                                                  akSoftDrop4PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akSoftDrop4PFpatJetsWithBtagging
                                                  *
                                                  akSoftDrop4PFJetAnalyzer
                                                  )

akSoftDrop4PFJetSequence_data = cms.Sequence(akSoftDrop4PFcorr
                                                    *
                                                    #akSoftDrop4PFJetID
                                                    #*
                                                    akSoftDrop4PFJetTracksAssociatorAtVertex
                                                    *
                                                    akSoftDrop4PFJetBtagging
                                                    *
                                                    akSoftDrop4PFNjettiness 
                                                    *
                                                    akSoftDrop4PFpatJetsWithBtagging
                                                    *
                                                    akSoftDrop4PFJetAnalyzer
                                                    )

akSoftDrop4PFJetSequence_jec = cms.Sequence(akSoftDrop4PFJetSequence_mc)
akSoftDrop4PFJetSequence_mb = cms.Sequence(akSoftDrop4PFJetSequence_mc)

akSoftDrop4PFJetSequence = cms.Sequence(akSoftDrop4PFJetSequence_mc)
