

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop1PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop1PFJets"),
    matched = cms.InputTag("ak1HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.1
    )

akVsSoftDrop1PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop1HiGenJets"),
    matched = cms.InputTag("ak1HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.1
    )

akVsSoftDrop1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop1PFJets")
                                                        )

akVsSoftDrop1PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop1PFJets"),
    payload = "AK1PF_offline"
    )

akVsSoftDrop1PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop1CaloJets'))

#akVsSoftDrop1PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1HiCleanedGenJets'))

akVsSoftDrop1PFbTagger = bTaggers("akVsSoftDrop1PF",0.1)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop1PFmatch = akVsSoftDrop1PFbTagger.match
akVsSoftDrop1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop1PFJets"), matched = cms.InputTag("selectedPartons"))
akVsSoftDrop1PFPatJetFlavourAssociationLegacy = akVsSoftDrop1PFbTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop1PFPatJetPartons = akVsSoftDrop1PFbTagger.PatJetPartons
akVsSoftDrop1PFJetTracksAssociatorAtVertex = akVsSoftDrop1PFbTagger.JetTracksAssociatorAtVertex
akVsSoftDrop1PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop1PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop1PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop1PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop1PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop1PFCombinedSecondaryVertexBJetTags = akVsSoftDrop1PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop1PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop1PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop1PFJetBProbabilityBJetTags = akVsSoftDrop1PFbTagger.JetBProbabilityBJetTags
akVsSoftDrop1PFSoftPFMuonByPtBJetTags = akVsSoftDrop1PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop1PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop1PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop1PFTrackCountingHighEffBJetTags = akVsSoftDrop1PFbTagger.TrackCountingHighEffBJetTags
akVsSoftDrop1PFTrackCountingHighPurBJetTags = akVsSoftDrop1PFbTagger.TrackCountingHighPurBJetTags
akVsSoftDrop1PFPatJetPartonAssociationLegacy = akVsSoftDrop1PFbTagger.PatJetPartonAssociationLegacy

akVsSoftDrop1PFImpactParameterTagInfos = akVsSoftDrop1PFbTagger.ImpactParameterTagInfos
akVsSoftDrop1PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop1PFJetProbabilityBJetTags = akVsSoftDrop1PFbTagger.JetProbabilityBJetTags

akVsSoftDrop1PFSecondaryVertexTagInfos = akVsSoftDrop1PFbTagger.SecondaryVertexTagInfos
akVsSoftDrop1PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop1PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop1PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop1PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop1PFCombinedSecondaryVertexBJetTags = akVsSoftDrop1PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop1PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop1PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop1PFSecondaryVertexNegativeTagInfos = akVsSoftDrop1PFbTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop1PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop1PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop1PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop1PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop1PFNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop1PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop1PFPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop1PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop1PFNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop1PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop1PFPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop1PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop1PFSoftPFMuonsTagInfos = akVsSoftDrop1PFbTagger.SoftPFMuonsTagInfos
akVsSoftDrop1PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop1PFSoftPFMuonBJetTags = akVsSoftDrop1PFbTagger.SoftPFMuonBJetTags
akVsSoftDrop1PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop1PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop1PFSoftPFMuonByPtBJetTags = akVsSoftDrop1PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop1PFNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop1PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop1PFPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop1PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop1PFPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop1PFPatJetPartonAssociationLegacy*akVsSoftDrop1PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop1PFPatJetFlavourAssociation = akVsSoftDrop1PFbTagger.PatJetFlavourAssociation
#akVsSoftDrop1PFPatJetFlavourId = cms.Sequence(akVsSoftDrop1PFPatJetPartons*akVsSoftDrop1PFPatJetFlavourAssociation)

akVsSoftDrop1PFJetBtaggingIP       = cms.Sequence(akVsSoftDrop1PFImpactParameterTagInfos *
            (akVsSoftDrop1PFTrackCountingHighEffBJetTags +
             akVsSoftDrop1PFTrackCountingHighPurBJetTags +
             akVsSoftDrop1PFJetProbabilityBJetTags +
             akVsSoftDrop1PFJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop1PFJetBtaggingSV = cms.Sequence(akVsSoftDrop1PFImpactParameterTagInfos
            *
            akVsSoftDrop1PFSecondaryVertexTagInfos
            * (akVsSoftDrop1PFSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop1PFSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop1PFCombinedSecondaryVertexBJetTags+
                akVsSoftDrop1PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop1PFJetBtaggingNegSV = cms.Sequence(akVsSoftDrop1PFImpactParameterTagInfos
            *
            akVsSoftDrop1PFSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop1PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop1PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop1PFNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop1PFPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop1PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop1PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop1PFJetBtaggingMu = cms.Sequence(akVsSoftDrop1PFSoftPFMuonsTagInfos * (akVsSoftDrop1PFSoftPFMuonBJetTags
                +
                akVsSoftDrop1PFSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop1PFSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop1PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop1PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop1PFJetBtagging = cms.Sequence(akVsSoftDrop1PFJetBtaggingIP
            *akVsSoftDrop1PFJetBtaggingSV
            *akVsSoftDrop1PFJetBtaggingNegSV
#            *akVsSoftDrop1PFJetBtaggingMu
            )

akVsSoftDrop1PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop1PFJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop1PFmatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop1PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop1PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop1PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop1PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop1PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop1PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop1PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop1PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop1PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop1PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop1PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop1PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop1PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop1PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop1PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop1PFJetID"),
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

akVsSoftDrop1PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop1PFJets"),
           	    R0  = cms.double( 0.1)
)
akVsSoftDrop1PFpatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop1PFNjettiness:tau1','akVsSoftDrop1PFNjettiness:tau2','akVsSoftDrop1PFNjettiness:tau3']

akVsSoftDrop1PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop1PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak1HiGenJets',
                                                             rParam = 0.1,
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop1PF"),
                                                             jetName = cms.untracked.string("akVsSoftDrop1PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop1GenJets"),
                                                             doGenTaus = True
                                                             )

akVsSoftDrop1PFJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop1PFclean
                                                  #*
                                                  akVsSoftDrop1PFmatch
                                                  #*
                                                  #akVsSoftDrop1PFmatchGroomed
                                                  *
                                                  akVsSoftDrop1PFparton
                                                  *
                                                  akVsSoftDrop1PFcorr
                                                  *
                                                  #akVsSoftDrop1PFJetID
                                                  #*
                                                  akVsSoftDrop1PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop1PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop1PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop1PFJetBtagging
                                                  *
                                                  akVsSoftDrop1PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop1PFpatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop1PFJetAnalyzer
                                                  )

akVsSoftDrop1PFJetSequence_data = cms.Sequence(akVsSoftDrop1PFcorr
                                                    *
                                                    #akVsSoftDrop1PFJetID
                                                    #*
                                                    akVsSoftDrop1PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop1PFJetBtagging
                                                    *
                                                    akVsSoftDrop1PFNjettiness 
                                                    *
                                                    akVsSoftDrop1PFpatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop1PFJetAnalyzer
                                                    )

akVsSoftDrop1PFJetSequence_jec = cms.Sequence(akVsSoftDrop1PFJetSequence_mc)
akVsSoftDrop1PFJetSequence_mb = cms.Sequence(akVsSoftDrop1PFJetSequence_mc)

akVsSoftDrop1PFJetSequence = cms.Sequence(akVsSoftDrop1PFJetSequence_mb)
