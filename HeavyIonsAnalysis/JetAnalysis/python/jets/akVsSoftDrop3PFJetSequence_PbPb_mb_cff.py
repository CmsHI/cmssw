

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop3PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop3PFJets"),
    matched = cms.InputTag("ak3HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.3
    )

akVsSoftDrop3PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop3HiGenJets"),
    matched = cms.InputTag("ak3HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.3
    )

akVsSoftDrop3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop3PFJets")
                                                        )

akVsSoftDrop3PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop3PFJets"),
    payload = "AK3PF_offline"
    )

akVsSoftDrop3PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop3CaloJets'))

#akVsSoftDrop3PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiCleanedGenJets'))

akVsSoftDrop3PFbTagger = bTaggers("akVsSoftDrop3PF",0.3)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop3PFmatch = akVsSoftDrop3PFbTagger.match
akVsSoftDrop3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop3PFJets"), matched = cms.InputTag("selectedPartons"))
akVsSoftDrop3PFPatJetFlavourAssociationLegacy = akVsSoftDrop3PFbTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop3PFPatJetPartons = akVsSoftDrop3PFbTagger.PatJetPartons
akVsSoftDrop3PFJetTracksAssociatorAtVertex = akVsSoftDrop3PFbTagger.JetTracksAssociatorAtVertex
akVsSoftDrop3PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop3PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop3PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop3PFCombinedSecondaryVertexBJetTags = akVsSoftDrop3PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop3PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop3PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop3PFJetBProbabilityBJetTags = akVsSoftDrop3PFbTagger.JetBProbabilityBJetTags
akVsSoftDrop3PFSoftPFMuonByPtBJetTags = akVsSoftDrop3PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop3PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop3PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop3PFTrackCountingHighEffBJetTags = akVsSoftDrop3PFbTagger.TrackCountingHighEffBJetTags
akVsSoftDrop3PFTrackCountingHighPurBJetTags = akVsSoftDrop3PFbTagger.TrackCountingHighPurBJetTags
akVsSoftDrop3PFPatJetPartonAssociationLegacy = akVsSoftDrop3PFbTagger.PatJetPartonAssociationLegacy

akVsSoftDrop3PFImpactParameterTagInfos = akVsSoftDrop3PFbTagger.ImpactParameterTagInfos
akVsSoftDrop3PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop3PFJetProbabilityBJetTags = akVsSoftDrop3PFbTagger.JetProbabilityBJetTags

akVsSoftDrop3PFSecondaryVertexTagInfos = akVsSoftDrop3PFbTagger.SecondaryVertexTagInfos
akVsSoftDrop3PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop3PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop3PFCombinedSecondaryVertexBJetTags = akVsSoftDrop3PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop3PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop3PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop3PFSecondaryVertexNegativeTagInfos = akVsSoftDrop3PFbTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop3PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop3PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop3PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop3PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop3PFNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop3PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop3PFPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop3PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop3PFNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop3PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop3PFPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop3PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop3PFSoftPFMuonsTagInfos = akVsSoftDrop3PFbTagger.SoftPFMuonsTagInfos
akVsSoftDrop3PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop3PFSoftPFMuonBJetTags = akVsSoftDrop3PFbTagger.SoftPFMuonBJetTags
akVsSoftDrop3PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop3PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop3PFSoftPFMuonByPtBJetTags = akVsSoftDrop3PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop3PFNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop3PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop3PFPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop3PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop3PFPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop3PFPatJetPartonAssociationLegacy*akVsSoftDrop3PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop3PFPatJetFlavourAssociation = akVsSoftDrop3PFbTagger.PatJetFlavourAssociation
#akVsSoftDrop3PFPatJetFlavourId = cms.Sequence(akVsSoftDrop3PFPatJetPartons*akVsSoftDrop3PFPatJetFlavourAssociation)

akVsSoftDrop3PFJetBtaggingIP       = cms.Sequence(akVsSoftDrop3PFImpactParameterTagInfos *
            (akVsSoftDrop3PFTrackCountingHighEffBJetTags +
             akVsSoftDrop3PFTrackCountingHighPurBJetTags +
             akVsSoftDrop3PFJetProbabilityBJetTags +
             akVsSoftDrop3PFJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop3PFJetBtaggingSV = cms.Sequence(akVsSoftDrop3PFImpactParameterTagInfos
            *
            akVsSoftDrop3PFSecondaryVertexTagInfos
            * (akVsSoftDrop3PFSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop3PFSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop3PFCombinedSecondaryVertexBJetTags+
                akVsSoftDrop3PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop3PFJetBtaggingNegSV = cms.Sequence(akVsSoftDrop3PFImpactParameterTagInfos
            *
            akVsSoftDrop3PFSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop3PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop3PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop3PFNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop3PFPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop3PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop3PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop3PFJetBtaggingMu = cms.Sequence(akVsSoftDrop3PFSoftPFMuonsTagInfos * (akVsSoftDrop3PFSoftPFMuonBJetTags
                +
                akVsSoftDrop3PFSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop3PFSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop3PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop3PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop3PFJetBtagging = cms.Sequence(akVsSoftDrop3PFJetBtaggingIP
            *akVsSoftDrop3PFJetBtaggingSV
            *akVsSoftDrop3PFJetBtaggingNegSV
#            *akVsSoftDrop3PFJetBtaggingMu
            )

akVsSoftDrop3PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop3PFJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop3PFmatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop3PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop3PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop3PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop3PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop3PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop3PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop3PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop3PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop3PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop3PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop3PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop3PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop3PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop3PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop3PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop3PFJetID"),
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

akVsSoftDrop3PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop3PFJets"),
           	    R0  = cms.double( 0.3)
)
akVsSoftDrop3PFpatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop3PFNjettiness:tau1','akVsSoftDrop3PFNjettiness:tau2','akVsSoftDrop3PFNjettiness:tau3']

akVsSoftDrop3PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop3PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop3PF"),
                                                             jetName = cms.untracked.string("akVsSoftDrop3PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop3GenJets"),
                                                             doGenTaus = True
                                                             )

akVsSoftDrop3PFJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop3PFclean
                                                  #*
                                                  akVsSoftDrop3PFmatch
                                                  #*
                                                  #akVsSoftDrop3PFmatchGroomed
                                                  *
                                                  akVsSoftDrop3PFparton
                                                  *
                                                  akVsSoftDrop3PFcorr
                                                  *
                                                  #akVsSoftDrop3PFJetID
                                                  #*
                                                  akVsSoftDrop3PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop3PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop3PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop3PFJetBtagging
                                                  *
                                                  akVsSoftDrop3PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop3PFpatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop3PFJetAnalyzer
                                                  )

akVsSoftDrop3PFJetSequence_data = cms.Sequence(akVsSoftDrop3PFcorr
                                                    *
                                                    #akVsSoftDrop3PFJetID
                                                    #*
                                                    akVsSoftDrop3PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop3PFJetBtagging
                                                    *
                                                    akVsSoftDrop3PFNjettiness 
                                                    *
                                                    akVsSoftDrop3PFpatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop3PFJetAnalyzer
                                                    )

akVsSoftDrop3PFJetSequence_jec = cms.Sequence(akVsSoftDrop3PFJetSequence_mc)
akVsSoftDrop3PFJetSequence_mb = cms.Sequence(akVsSoftDrop3PFJetSequence_mc)

akVsSoftDrop3PFJetSequence = cms.Sequence(akVsSoftDrop3PFJetSequence_mb)
