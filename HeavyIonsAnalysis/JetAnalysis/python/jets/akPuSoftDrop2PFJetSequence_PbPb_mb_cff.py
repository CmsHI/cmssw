

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop2PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop2PFJets"),
    matched = cms.InputTag("ak2HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akPuSoftDrop2PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop2HiGenJets"),
    matched = cms.InputTag("ak2HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akPuSoftDrop2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop2PFJets")
                                                        )

akPuSoftDrop2PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop2PFJets"),
    payload = "AKPu2PF_offline"
    )

akPuSoftDrop2PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop2CaloJets'))

#akPuSoftDrop2PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2HiCleanedGenJets'))

akPuSoftDrop2PFbTagger = bTaggers("akPuSoftDrop2PF",0.2)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop2PFmatch = akPuSoftDrop2PFbTagger.match
akPuSoftDrop2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop2PFJets"), matched = cms.InputTag("selectedPartons"))
akPuSoftDrop2PFPatJetFlavourAssociationLegacy = akPuSoftDrop2PFbTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop2PFPatJetPartons = akPuSoftDrop2PFbTagger.PatJetPartons
akPuSoftDrop2PFJetTracksAssociatorAtVertex = akPuSoftDrop2PFbTagger.JetTracksAssociatorAtVertex
akPuSoftDrop2PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop2PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop2PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop2PFCombinedSecondaryVertexBJetTags = akPuSoftDrop2PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop2PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop2PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop2PFJetBProbabilityBJetTags = akPuSoftDrop2PFbTagger.JetBProbabilityBJetTags
akPuSoftDrop2PFSoftPFMuonByPtBJetTags = akPuSoftDrop2PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop2PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop2PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop2PFTrackCountingHighEffBJetTags = akPuSoftDrop2PFbTagger.TrackCountingHighEffBJetTags
akPuSoftDrop2PFTrackCountingHighPurBJetTags = akPuSoftDrop2PFbTagger.TrackCountingHighPurBJetTags
akPuSoftDrop2PFPatJetPartonAssociationLegacy = akPuSoftDrop2PFbTagger.PatJetPartonAssociationLegacy

akPuSoftDrop2PFImpactParameterTagInfos = akPuSoftDrop2PFbTagger.ImpactParameterTagInfos
akPuSoftDrop2PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop2PFJetProbabilityBJetTags = akPuSoftDrop2PFbTagger.JetProbabilityBJetTags

akPuSoftDrop2PFSecondaryVertexTagInfos = akPuSoftDrop2PFbTagger.SecondaryVertexTagInfos
akPuSoftDrop2PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop2PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop2PFCombinedSecondaryVertexBJetTags = akPuSoftDrop2PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop2PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop2PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop2PFSecondaryVertexNegativeTagInfos = akPuSoftDrop2PFbTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop2PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop2PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop2PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop2PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop2PFNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop2PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop2PFPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop2PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop2PFNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop2PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop2PFPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop2PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop2PFSoftPFMuonsTagInfos = akPuSoftDrop2PFbTagger.SoftPFMuonsTagInfos
akPuSoftDrop2PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop2PFSoftPFMuonBJetTags = akPuSoftDrop2PFbTagger.SoftPFMuonBJetTags
akPuSoftDrop2PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop2PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop2PFSoftPFMuonByPtBJetTags = akPuSoftDrop2PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop2PFNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop2PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop2PFPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop2PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop2PFPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop2PFPatJetPartonAssociationLegacy*akPuSoftDrop2PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop2PFPatJetFlavourAssociation = akPuSoftDrop2PFbTagger.PatJetFlavourAssociation
#akPuSoftDrop2PFPatJetFlavourId = cms.Sequence(akPuSoftDrop2PFPatJetPartons*akPuSoftDrop2PFPatJetFlavourAssociation)

akPuSoftDrop2PFJetBtaggingIP       = cms.Sequence(akPuSoftDrop2PFImpactParameterTagInfos *
            (akPuSoftDrop2PFTrackCountingHighEffBJetTags +
             akPuSoftDrop2PFTrackCountingHighPurBJetTags +
             akPuSoftDrop2PFJetProbabilityBJetTags +
             akPuSoftDrop2PFJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop2PFJetBtaggingSV = cms.Sequence(akPuSoftDrop2PFImpactParameterTagInfos
            *
            akPuSoftDrop2PFSecondaryVertexTagInfos
            * (akPuSoftDrop2PFSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop2PFSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop2PFCombinedSecondaryVertexBJetTags+
                akPuSoftDrop2PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop2PFJetBtaggingNegSV = cms.Sequence(akPuSoftDrop2PFImpactParameterTagInfos
            *
            akPuSoftDrop2PFSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop2PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop2PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop2PFNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop2PFPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop2PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop2PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop2PFJetBtaggingMu = cms.Sequence(akPuSoftDrop2PFSoftPFMuonsTagInfos * (akPuSoftDrop2PFSoftPFMuonBJetTags
                +
                akPuSoftDrop2PFSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop2PFSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop2PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop2PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop2PFJetBtagging = cms.Sequence(akPuSoftDrop2PFJetBtaggingIP
            *akPuSoftDrop2PFJetBtaggingSV
            *akPuSoftDrop2PFJetBtaggingNegSV
#            *akPuSoftDrop2PFJetBtaggingMu
            )

akPuSoftDrop2PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop2PFJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop2PFmatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop2PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop2PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop2PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop2PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop2PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop2PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop2PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop2PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop2PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop2PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop2PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop2PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop2PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop2PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop2PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop2PFJetID"),
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

akPuSoftDrop2PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop2PFJets"),
           	    R0  = cms.double( 0.2)
)
akPuSoftDrop2PFpatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop2PFNjettiness:tau1','akPuSoftDrop2PFNjettiness:tau2','akPuSoftDrop2PFNjettiness:tau3']

akPuSoftDrop2PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop2PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak2HiGenJets',
                                                             rParam = 0.2,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlowTmp'),
                                                             trackTag = cms.InputTag("hiGeneralTracks"),
                                                             fillGenJets = True,
                                                             isMC = True,
							     doSubEvent = True,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop2PF"),
                                                             jetName = cms.untracked.string("akPuSoftDrop2PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop2GenJets"),
                                                             doGenTaus = True
                                                             )

akPuSoftDrop2PFJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop2PFclean
                                                  #*
                                                  akPuSoftDrop2PFmatch
                                                  #*
                                                  #akPuSoftDrop2PFmatchGroomed
                                                  *
                                                  akPuSoftDrop2PFparton
                                                  *
                                                  akPuSoftDrop2PFcorr
                                                  *
                                                  #akPuSoftDrop2PFJetID
                                                  #*
                                                  akPuSoftDrop2PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop2PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop2PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop2PFJetBtagging
                                                  *
                                                  akPuSoftDrop2PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop2PFpatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop2PFJetAnalyzer
                                                  )

akPuSoftDrop2PFJetSequence_data = cms.Sequence(akPuSoftDrop2PFcorr
                                                    *
                                                    #akPuSoftDrop2PFJetID
                                                    #*
                                                    akPuSoftDrop2PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop2PFJetBtagging
                                                    *
                                                    akPuSoftDrop2PFNjettiness 
                                                    *
                                                    akPuSoftDrop2PFpatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop2PFJetAnalyzer
                                                    )

akPuSoftDrop2PFJetSequence_jec = cms.Sequence(akPuSoftDrop2PFJetSequence_mc)
akPuSoftDrop2PFJetSequence_mb = cms.Sequence(akPuSoftDrop2PFJetSequence_mc)

akPuSoftDrop2PFJetSequence = cms.Sequence(akPuSoftDrop2PFJetSequence_mb)
