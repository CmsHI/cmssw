

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop4PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop4PFJets"),
    matched = cms.InputTag("ak4HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akPuSoftDrop4PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop4HiGenJets"),
    matched = cms.InputTag("ak4HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akPuSoftDrop4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop4PFJets")
                                                        )

akPuSoftDrop4PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop4PFJets"),
    payload = "AKPu4PF_offline"
    )

akPuSoftDrop4PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop4CaloJets'))

#akPuSoftDrop4PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4HiSignalGenJets'))

akPuSoftDrop4PFbTagger = bTaggers("akPuSoftDrop4PF",0.4)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop4PFmatch = akPuSoftDrop4PFbTagger.match
akPuSoftDrop4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop4PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuSoftDrop4PFPatJetFlavourAssociationLegacy = akPuSoftDrop4PFbTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop4PFPatJetPartons = akPuSoftDrop4PFbTagger.PatJetPartons
akPuSoftDrop4PFJetTracksAssociatorAtVertex = akPuSoftDrop4PFbTagger.JetTracksAssociatorAtVertex
akPuSoftDrop4PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop4PFCombinedSecondaryVertexBJetTags = akPuSoftDrop4PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop4PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop4PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop4PFJetBProbabilityBJetTags = akPuSoftDrop4PFbTagger.JetBProbabilityBJetTags
akPuSoftDrop4PFSoftPFMuonByPtBJetTags = akPuSoftDrop4PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop4PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop4PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop4PFTrackCountingHighEffBJetTags = akPuSoftDrop4PFbTagger.TrackCountingHighEffBJetTags
akPuSoftDrop4PFTrackCountingHighPurBJetTags = akPuSoftDrop4PFbTagger.TrackCountingHighPurBJetTags
akPuSoftDrop4PFPatJetPartonAssociationLegacy = akPuSoftDrop4PFbTagger.PatJetPartonAssociationLegacy

akPuSoftDrop4PFImpactParameterTagInfos = akPuSoftDrop4PFbTagger.ImpactParameterTagInfos
akPuSoftDrop4PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop4PFJetProbabilityBJetTags = akPuSoftDrop4PFbTagger.JetProbabilityBJetTags

akPuSoftDrop4PFSecondaryVertexTagInfos = akPuSoftDrop4PFbTagger.SecondaryVertexTagInfos
akPuSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop4PFCombinedSecondaryVertexBJetTags = akPuSoftDrop4PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop4PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop4PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop4PFSecondaryVertexNegativeTagInfos = akPuSoftDrop4PFbTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop4PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop4PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop4PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop4PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop4PFNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop4PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop4PFPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop4PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop4PFNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop4PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop4PFPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop4PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop4PFSoftPFMuonsTagInfos = akPuSoftDrop4PFbTagger.SoftPFMuonsTagInfos
akPuSoftDrop4PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop4PFSoftPFMuonBJetTags = akPuSoftDrop4PFbTagger.SoftPFMuonBJetTags
akPuSoftDrop4PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop4PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop4PFSoftPFMuonByPtBJetTags = akPuSoftDrop4PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop4PFNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop4PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop4PFPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop4PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop4PFPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop4PFPatJetPartonAssociationLegacy*akPuSoftDrop4PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop4PFPatJetFlavourAssociation = akPuSoftDrop4PFbTagger.PatJetFlavourAssociation
#akPuSoftDrop4PFPatJetFlavourId = cms.Sequence(akPuSoftDrop4PFPatJetPartons*akPuSoftDrop4PFPatJetFlavourAssociation)

akPuSoftDrop4PFJetBtaggingIP       = cms.Sequence(akPuSoftDrop4PFImpactParameterTagInfos *
            (akPuSoftDrop4PFTrackCountingHighEffBJetTags +
             akPuSoftDrop4PFTrackCountingHighPurBJetTags +
             akPuSoftDrop4PFJetProbabilityBJetTags +
             akPuSoftDrop4PFJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop4PFJetBtaggingSV = cms.Sequence(akPuSoftDrop4PFImpactParameterTagInfos
            *
            akPuSoftDrop4PFSecondaryVertexTagInfos
            * (akPuSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop4PFCombinedSecondaryVertexBJetTags+
                akPuSoftDrop4PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop4PFJetBtaggingNegSV = cms.Sequence(akPuSoftDrop4PFImpactParameterTagInfos
            *
            akPuSoftDrop4PFSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop4PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop4PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop4PFNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop4PFPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop4PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop4PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop4PFJetBtaggingMu = cms.Sequence(akPuSoftDrop4PFSoftPFMuonsTagInfos * (akPuSoftDrop4PFSoftPFMuonBJetTags
                +
                akPuSoftDrop4PFSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop4PFSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop4PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop4PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop4PFJetBtagging = cms.Sequence(akPuSoftDrop4PFJetBtaggingIP
            *akPuSoftDrop4PFJetBtaggingSV
            *akPuSoftDrop4PFJetBtaggingNegSV
#            *akPuSoftDrop4PFJetBtaggingMu
            )

akPuSoftDrop4PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop4PFJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop4PFmatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop4PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop4PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop4PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop4PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop4PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop4PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop4PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop4PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop4PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop4PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop4PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop4PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop4PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop4PFJetID"),
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

akPuSoftDrop4PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop4PFJets"),
           	    R0  = cms.double( 0.4)
)
akPuSoftDrop4PFpatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop4PFNjettiness:tau1','akPuSoftDrop4PFNjettiness:tau2','akPuSoftDrop4PFNjettiness:tau3']

akPuSoftDrop4PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop4PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak4HiGenJets',
                                                             rParam = 0.4,
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop4PF"),
                                                             jetName = cms.untracked.string("akPuSoftDrop4PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop4GenJets"),
                                                             doGenTaus = False
                                                             )

akPuSoftDrop4PFJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop4PFclean
                                                  #*
                                                  akPuSoftDrop4PFmatch
                                                  #*
                                                  #akPuSoftDrop4PFmatchGroomed
                                                  *
                                                  akPuSoftDrop4PFparton
                                                  *
                                                  akPuSoftDrop4PFcorr
                                                  *
                                                  #akPuSoftDrop4PFJetID
                                                  #*
                                                  akPuSoftDrop4PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop4PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop4PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop4PFJetBtagging
                                                  *
                                                  akPuSoftDrop4PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop4PFpatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop4PFJetAnalyzer
                                                  )

akPuSoftDrop4PFJetSequence_data = cms.Sequence(akPuSoftDrop4PFcorr
                                                    *
                                                    #akPuSoftDrop4PFJetID
                                                    #*
                                                    akPuSoftDrop4PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop4PFJetBtagging
                                                    *
                                                    akPuSoftDrop4PFNjettiness 
                                                    *
                                                    akPuSoftDrop4PFpatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop4PFJetAnalyzer
                                                    )

akPuSoftDrop4PFJetSequence_jec = cms.Sequence(akPuSoftDrop4PFJetSequence_mc)
akPuSoftDrop4PFJetSequence_mb = cms.Sequence(akPuSoftDrop4PFJetSequence_mc)

akPuSoftDrop4PFJetSequence = cms.Sequence(akPuSoftDrop4PFJetSequence_data)
