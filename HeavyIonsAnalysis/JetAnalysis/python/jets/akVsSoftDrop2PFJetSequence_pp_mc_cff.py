

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop2PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop2PFJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.2
    )

akVsSoftDrop2PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop2GenJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.2
    )

akVsSoftDrop2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop2PFJets")
                                                        )

akVsSoftDrop2PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop2PFJets"),
    payload = "AK2PF_offline"
    )

akVsSoftDrop2PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop2CaloJets'))

#akVsSoftDrop2PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2GenJets'))

akVsSoftDrop2PFbTagger = bTaggers("akVsSoftDrop2PF",0.2)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop2PFmatch = akVsSoftDrop2PFbTagger.match
akVsSoftDrop2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop2PFJets"), matched = cms.InputTag("genParticles"))
akVsSoftDrop2PFPatJetFlavourAssociationLegacy = akVsSoftDrop2PFbTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop2PFPatJetPartons = akVsSoftDrop2PFbTagger.PatJetPartons
akVsSoftDrop2PFJetTracksAssociatorAtVertex = akVsSoftDrop2PFbTagger.JetTracksAssociatorAtVertex
akVsSoftDrop2PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop2PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop2PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop2PFCombinedSecondaryVertexBJetTags = akVsSoftDrop2PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop2PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop2PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop2PFJetBProbabilityBJetTags = akVsSoftDrop2PFbTagger.JetBProbabilityBJetTags
akVsSoftDrop2PFSoftPFMuonByPtBJetTags = akVsSoftDrop2PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop2PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop2PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop2PFTrackCountingHighEffBJetTags = akVsSoftDrop2PFbTagger.TrackCountingHighEffBJetTags
akVsSoftDrop2PFTrackCountingHighPurBJetTags = akVsSoftDrop2PFbTagger.TrackCountingHighPurBJetTags
akVsSoftDrop2PFPatJetPartonAssociationLegacy = akVsSoftDrop2PFbTagger.PatJetPartonAssociationLegacy

akVsSoftDrop2PFImpactParameterTagInfos = akVsSoftDrop2PFbTagger.ImpactParameterTagInfos
akVsSoftDrop2PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop2PFJetProbabilityBJetTags = akVsSoftDrop2PFbTagger.JetProbabilityBJetTags

akVsSoftDrop2PFSecondaryVertexTagInfos = akVsSoftDrop2PFbTagger.SecondaryVertexTagInfos
akVsSoftDrop2PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop2PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop2PFCombinedSecondaryVertexBJetTags = akVsSoftDrop2PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop2PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop2PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop2PFSecondaryVertexNegativeTagInfos = akVsSoftDrop2PFbTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop2PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop2PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop2PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop2PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop2PFNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop2PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop2PFPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop2PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop2PFNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop2PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop2PFPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop2PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop2PFSoftPFMuonsTagInfos = akVsSoftDrop2PFbTagger.SoftPFMuonsTagInfos
akVsSoftDrop2PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop2PFSoftPFMuonBJetTags = akVsSoftDrop2PFbTagger.SoftPFMuonBJetTags
akVsSoftDrop2PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop2PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop2PFSoftPFMuonByPtBJetTags = akVsSoftDrop2PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop2PFNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop2PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop2PFPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop2PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop2PFPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop2PFPatJetPartonAssociationLegacy*akVsSoftDrop2PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop2PFPatJetFlavourAssociation = akVsSoftDrop2PFbTagger.PatJetFlavourAssociation
#akVsSoftDrop2PFPatJetFlavourId = cms.Sequence(akVsSoftDrop2PFPatJetPartons*akVsSoftDrop2PFPatJetFlavourAssociation)

akVsSoftDrop2PFJetBtaggingIP       = cms.Sequence(akVsSoftDrop2PFImpactParameterTagInfos *
            (akVsSoftDrop2PFTrackCountingHighEffBJetTags +
             akVsSoftDrop2PFTrackCountingHighPurBJetTags +
             akVsSoftDrop2PFJetProbabilityBJetTags +
             akVsSoftDrop2PFJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop2PFJetBtaggingSV = cms.Sequence(akVsSoftDrop2PFImpactParameterTagInfos
            *
            akVsSoftDrop2PFSecondaryVertexTagInfos
            * (akVsSoftDrop2PFSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop2PFSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop2PFCombinedSecondaryVertexBJetTags+
                akVsSoftDrop2PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop2PFJetBtaggingNegSV = cms.Sequence(akVsSoftDrop2PFImpactParameterTagInfos
            *
            akVsSoftDrop2PFSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop2PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop2PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop2PFNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop2PFPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop2PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop2PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop2PFJetBtaggingMu = cms.Sequence(akVsSoftDrop2PFSoftPFMuonsTagInfos * (akVsSoftDrop2PFSoftPFMuonBJetTags
                +
                akVsSoftDrop2PFSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop2PFSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop2PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop2PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop2PFJetBtagging = cms.Sequence(akVsSoftDrop2PFJetBtaggingIP
            *akVsSoftDrop2PFJetBtaggingSV
            *akVsSoftDrop2PFJetBtaggingNegSV
#            *akVsSoftDrop2PFJetBtaggingMu
            )

akVsSoftDrop2PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop2PFJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop2PFmatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop2PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop2PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop2PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop2PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop2PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop2PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop2PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop2PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop2PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop2PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop2PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop2PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop2PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop2PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop2PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop2PFJetID"),
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

akVsSoftDrop2PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop2PFJets"),
           	    R0  = cms.double( 0.2)
)
akVsSoftDrop2PFpatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop2PFNjettiness:tau1','akVsSoftDrop2PFNjettiness:tau2','akVsSoftDrop2PFNjettiness:tau3']

akVsSoftDrop2PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop2PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop2PF"),
                                                             jetName = cms.untracked.string("akVsSoftDrop2PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(True),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop2GenJets"),
                                                             doGenTaus = True
                                                             )

akVsSoftDrop2PFJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop2PFclean
                                                  #*
                                                  akVsSoftDrop2PFmatch
                                                  #*
                                                  #akVsSoftDrop2PFmatchGroomed
                                                  *
                                                  akVsSoftDrop2PFparton
                                                  *
                                                  akVsSoftDrop2PFcorr
                                                  *
                                                  #akVsSoftDrop2PFJetID
                                                  #*
                                                  akVsSoftDrop2PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop2PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop2PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop2PFJetBtagging
                                                  *
                                                  akVsSoftDrop2PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop2PFpatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop2PFJetAnalyzer
                                                  )

akVsSoftDrop2PFJetSequence_data = cms.Sequence(akVsSoftDrop2PFcorr
                                                    *
                                                    #akVsSoftDrop2PFJetID
                                                    #*
                                                    akVsSoftDrop2PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop2PFJetBtagging
                                                    *
                                                    akVsSoftDrop2PFNjettiness 
                                                    *
                                                    akVsSoftDrop2PFpatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop2PFJetAnalyzer
                                                    )

akVsSoftDrop2PFJetSequence_jec = cms.Sequence(akVsSoftDrop2PFJetSequence_mc)
akVsSoftDrop2PFJetSequence_mb = cms.Sequence(akVsSoftDrop2PFJetSequence_mc)

akVsSoftDrop2PFJetSequence = cms.Sequence(akVsSoftDrop2PFJetSequence_mc)
