

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop3PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop3PFJets"),
    matched = cms.InputTag("ak3HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akPuSoftDrop3PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop3HiGenJets"),
    matched = cms.InputTag("ak3HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akPuSoftDrop3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop3PFJets")
                                                        )

akPuSoftDrop3PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop3PFJets"),
    payload = "AKPu3PF_offline"
    )

akPuSoftDrop3PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop3CaloJets'))

#akPuSoftDrop3PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiSignalGenJets'))

akPuSoftDrop3PFbTagger = bTaggers("akPuSoftDrop3PF",0.3)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop3PFmatch = akPuSoftDrop3PFbTagger.match
akPuSoftDrop3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop3PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuSoftDrop3PFPatJetFlavourAssociationLegacy = akPuSoftDrop3PFbTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop3PFPatJetPartons = akPuSoftDrop3PFbTagger.PatJetPartons
akPuSoftDrop3PFJetTracksAssociatorAtVertex = akPuSoftDrop3PFbTagger.JetTracksAssociatorAtVertex
akPuSoftDrop3PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop3PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop3PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop3PFCombinedSecondaryVertexBJetTags = akPuSoftDrop3PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop3PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop3PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop3PFJetBProbabilityBJetTags = akPuSoftDrop3PFbTagger.JetBProbabilityBJetTags
akPuSoftDrop3PFSoftPFMuonByPtBJetTags = akPuSoftDrop3PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop3PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop3PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop3PFTrackCountingHighEffBJetTags = akPuSoftDrop3PFbTagger.TrackCountingHighEffBJetTags
akPuSoftDrop3PFTrackCountingHighPurBJetTags = akPuSoftDrop3PFbTagger.TrackCountingHighPurBJetTags
akPuSoftDrop3PFPatJetPartonAssociationLegacy = akPuSoftDrop3PFbTagger.PatJetPartonAssociationLegacy

akPuSoftDrop3PFImpactParameterTagInfos = akPuSoftDrop3PFbTagger.ImpactParameterTagInfos
akPuSoftDrop3PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop3PFJetProbabilityBJetTags = akPuSoftDrop3PFbTagger.JetProbabilityBJetTags

akPuSoftDrop3PFSecondaryVertexTagInfos = akPuSoftDrop3PFbTagger.SecondaryVertexTagInfos
akPuSoftDrop3PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop3PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop3PFCombinedSecondaryVertexBJetTags = akPuSoftDrop3PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop3PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop3PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop3PFSecondaryVertexNegativeTagInfos = akPuSoftDrop3PFbTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop3PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop3PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop3PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop3PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop3PFNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop3PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop3PFPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop3PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop3PFNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop3PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop3PFPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop3PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop3PFSoftPFMuonsTagInfos = akPuSoftDrop3PFbTagger.SoftPFMuonsTagInfos
akPuSoftDrop3PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop3PFSoftPFMuonBJetTags = akPuSoftDrop3PFbTagger.SoftPFMuonBJetTags
akPuSoftDrop3PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop3PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop3PFSoftPFMuonByPtBJetTags = akPuSoftDrop3PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop3PFNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop3PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop3PFPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop3PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop3PFPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop3PFPatJetPartonAssociationLegacy*akPuSoftDrop3PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop3PFPatJetFlavourAssociation = akPuSoftDrop3PFbTagger.PatJetFlavourAssociation
#akPuSoftDrop3PFPatJetFlavourId = cms.Sequence(akPuSoftDrop3PFPatJetPartons*akPuSoftDrop3PFPatJetFlavourAssociation)

akPuSoftDrop3PFJetBtaggingIP       = cms.Sequence(akPuSoftDrop3PFImpactParameterTagInfos *
            (akPuSoftDrop3PFTrackCountingHighEffBJetTags +
             akPuSoftDrop3PFTrackCountingHighPurBJetTags +
             akPuSoftDrop3PFJetProbabilityBJetTags +
             akPuSoftDrop3PFJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop3PFJetBtaggingSV = cms.Sequence(akPuSoftDrop3PFImpactParameterTagInfos
            *
            akPuSoftDrop3PFSecondaryVertexTagInfos
            * (akPuSoftDrop3PFSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop3PFSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop3PFCombinedSecondaryVertexBJetTags+
                akPuSoftDrop3PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop3PFJetBtaggingNegSV = cms.Sequence(akPuSoftDrop3PFImpactParameterTagInfos
            *
            akPuSoftDrop3PFSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop3PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop3PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop3PFNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop3PFPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop3PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop3PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop3PFJetBtaggingMu = cms.Sequence(akPuSoftDrop3PFSoftPFMuonsTagInfos * (akPuSoftDrop3PFSoftPFMuonBJetTags
                +
                akPuSoftDrop3PFSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop3PFSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop3PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop3PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop3PFJetBtagging = cms.Sequence(akPuSoftDrop3PFJetBtaggingIP
            *akPuSoftDrop3PFJetBtaggingSV
            *akPuSoftDrop3PFJetBtaggingNegSV
#            *akPuSoftDrop3PFJetBtaggingMu
            )

akPuSoftDrop3PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop3PFJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop3PFmatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop3PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop3PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop3PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop3PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop3PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop3PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop3PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop3PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop3PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop3PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop3PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop3PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop3PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop3PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop3PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop3PFJetID"),
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

akPuSoftDrop3PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop3PFJets"),
           	    R0  = cms.double( 0.3)
)
akPuSoftDrop3PFpatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop3PFNjettiness:tau1','akPuSoftDrop3PFNjettiness:tau2','akPuSoftDrop3PFNjettiness:tau3']

akPuSoftDrop3PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop3PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak3HiGenJets',
                                                             rParam = 0.3,
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop3PF"),
                                                             jetName = cms.untracked.string("akPuSoftDrop3PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(True),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop3GenJets"),
                                                             doGenTaus = True
                                                             )

akPuSoftDrop3PFJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop3PFclean
                                                  #*
                                                  akPuSoftDrop3PFmatch
                                                  #*
                                                  #akPuSoftDrop3PFmatchGroomed
                                                  *
                                                  akPuSoftDrop3PFparton
                                                  *
                                                  akPuSoftDrop3PFcorr
                                                  *
                                                  #akPuSoftDrop3PFJetID
                                                  #*
                                                  akPuSoftDrop3PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop3PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop3PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop3PFJetBtagging
                                                  *
                                                  akPuSoftDrop3PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop3PFpatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop3PFJetAnalyzer
                                                  )

akPuSoftDrop3PFJetSequence_data = cms.Sequence(akPuSoftDrop3PFcorr
                                                    *
                                                    #akPuSoftDrop3PFJetID
                                                    #*
                                                    akPuSoftDrop3PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop3PFJetBtagging
                                                    *
                                                    akPuSoftDrop3PFNjettiness 
                                                    *
                                                    akPuSoftDrop3PFpatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop3PFJetAnalyzer
                                                    )

akPuSoftDrop3PFJetSequence_jec = cms.Sequence(akPuSoftDrop3PFJetSequence_mc)
akPuSoftDrop3PFJetSequence_mb = cms.Sequence(akPuSoftDrop3PFJetSequence_mc)

akPuSoftDrop3PFJetSequence = cms.Sequence(akPuSoftDrop3PFJetSequence_mc)
