

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akSoftDrop1PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop1PFJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akSoftDrop1PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop1HiGenJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akSoftDrop1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop1PFJets")
                                                        )

akSoftDrop1PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akSoftDrop1PFJets"),
    payload = "AK1PF_offline"
    )

akSoftDrop1PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akSoftDrop1CaloJets'))

#akSoftDrop1PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1HiSignalGenJets'))

akSoftDrop1PFbTagger = bTaggers("akSoftDrop1PF",0.1)

#create objects locally since they dont load properly otherwise
#akSoftDrop1PFmatch = akSoftDrop1PFbTagger.match
akSoftDrop1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop1PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akSoftDrop1PFPatJetFlavourAssociationLegacy = akSoftDrop1PFbTagger.PatJetFlavourAssociationLegacy
akSoftDrop1PFPatJetPartons = akSoftDrop1PFbTagger.PatJetPartons
akSoftDrop1PFJetTracksAssociatorAtVertex = akSoftDrop1PFbTagger.JetTracksAssociatorAtVertex
akSoftDrop1PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akSoftDrop1PFSimpleSecondaryVertexHighEffBJetTags = akSoftDrop1PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop1PFSimpleSecondaryVertexHighPurBJetTags = akSoftDrop1PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop1PFCombinedSecondaryVertexBJetTags = akSoftDrop1PFbTagger.CombinedSecondaryVertexBJetTags
akSoftDrop1PFCombinedSecondaryVertexV2BJetTags = akSoftDrop1PFbTagger.CombinedSecondaryVertexV2BJetTags
akSoftDrop1PFJetBProbabilityBJetTags = akSoftDrop1PFbTagger.JetBProbabilityBJetTags
akSoftDrop1PFSoftPFMuonByPtBJetTags = akSoftDrop1PFbTagger.SoftPFMuonByPtBJetTags
akSoftDrop1PFSoftPFMuonByIP3dBJetTags = akSoftDrop1PFbTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop1PFTrackCountingHighEffBJetTags = akSoftDrop1PFbTagger.TrackCountingHighEffBJetTags
akSoftDrop1PFTrackCountingHighPurBJetTags = akSoftDrop1PFbTagger.TrackCountingHighPurBJetTags
akSoftDrop1PFPatJetPartonAssociationLegacy = akSoftDrop1PFbTagger.PatJetPartonAssociationLegacy

akSoftDrop1PFImpactParameterTagInfos = akSoftDrop1PFbTagger.ImpactParameterTagInfos
akSoftDrop1PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop1PFJetProbabilityBJetTags = akSoftDrop1PFbTagger.JetProbabilityBJetTags

akSoftDrop1PFSecondaryVertexTagInfos = akSoftDrop1PFbTagger.SecondaryVertexTagInfos
akSoftDrop1PFSimpleSecondaryVertexHighEffBJetTags = akSoftDrop1PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop1PFSimpleSecondaryVertexHighPurBJetTags = akSoftDrop1PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop1PFCombinedSecondaryVertexBJetTags = akSoftDrop1PFbTagger.CombinedSecondaryVertexBJetTags
akSoftDrop1PFCombinedSecondaryVertexV2BJetTags = akSoftDrop1PFbTagger.CombinedSecondaryVertexV2BJetTags

akSoftDrop1PFSecondaryVertexNegativeTagInfos = akSoftDrop1PFbTagger.SecondaryVertexNegativeTagInfos
akSoftDrop1PFNegativeSimpleSecondaryVertexHighEffBJetTags = akSoftDrop1PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akSoftDrop1PFNegativeSimpleSecondaryVertexHighPurBJetTags = akSoftDrop1PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akSoftDrop1PFNegativeCombinedSecondaryVertexBJetTags = akSoftDrop1PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akSoftDrop1PFPositiveCombinedSecondaryVertexBJetTags = akSoftDrop1PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akSoftDrop1PFNegativeCombinedSecondaryVertexV2BJetTags = akSoftDrop1PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akSoftDrop1PFPositiveCombinedSecondaryVertexV2BJetTags = akSoftDrop1PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akSoftDrop1PFSoftPFMuonsTagInfos = akSoftDrop1PFbTagger.SoftPFMuonsTagInfos
akSoftDrop1PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop1PFSoftPFMuonBJetTags = akSoftDrop1PFbTagger.SoftPFMuonBJetTags
akSoftDrop1PFSoftPFMuonByIP3dBJetTags = akSoftDrop1PFbTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop1PFSoftPFMuonByPtBJetTags = akSoftDrop1PFbTagger.SoftPFMuonByPtBJetTags
akSoftDrop1PFNegativeSoftPFMuonByPtBJetTags = akSoftDrop1PFbTagger.NegativeSoftPFMuonByPtBJetTags
akSoftDrop1PFPositiveSoftPFMuonByPtBJetTags = akSoftDrop1PFbTagger.PositiveSoftPFMuonByPtBJetTags
akSoftDrop1PFPatJetFlavourIdLegacy = cms.Sequence(akSoftDrop1PFPatJetPartonAssociationLegacy*akSoftDrop1PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akSoftDrop1PFPatJetFlavourAssociation = akSoftDrop1PFbTagger.PatJetFlavourAssociation
#akSoftDrop1PFPatJetFlavourId = cms.Sequence(akSoftDrop1PFPatJetPartons*akSoftDrop1PFPatJetFlavourAssociation)

akSoftDrop1PFJetBtaggingIP       = cms.Sequence(akSoftDrop1PFImpactParameterTagInfos *
            (akSoftDrop1PFTrackCountingHighEffBJetTags +
             akSoftDrop1PFTrackCountingHighPurBJetTags +
             akSoftDrop1PFJetProbabilityBJetTags +
             akSoftDrop1PFJetBProbabilityBJetTags 
            )
            )

akSoftDrop1PFJetBtaggingSV = cms.Sequence(akSoftDrop1PFImpactParameterTagInfos
            *
            akSoftDrop1PFSecondaryVertexTagInfos
            * (akSoftDrop1PFSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop1PFSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop1PFCombinedSecondaryVertexBJetTags+
                akSoftDrop1PFCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop1PFJetBtaggingNegSV = cms.Sequence(akSoftDrop1PFImpactParameterTagInfos
            *
            akSoftDrop1PFSecondaryVertexNegativeTagInfos
            * (akSoftDrop1PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop1PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop1PFNegativeCombinedSecondaryVertexBJetTags+
                akSoftDrop1PFPositiveCombinedSecondaryVertexBJetTags+
                akSoftDrop1PFNegativeCombinedSecondaryVertexV2BJetTags+
                akSoftDrop1PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop1PFJetBtaggingMu = cms.Sequence(akSoftDrop1PFSoftPFMuonsTagInfos * (akSoftDrop1PFSoftPFMuonBJetTags
                +
                akSoftDrop1PFSoftPFMuonByIP3dBJetTags
                +
                akSoftDrop1PFSoftPFMuonByPtBJetTags
                +
                akSoftDrop1PFNegativeSoftPFMuonByPtBJetTags
                +
                akSoftDrop1PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akSoftDrop1PFJetBtagging = cms.Sequence(akSoftDrop1PFJetBtaggingIP
            *akSoftDrop1PFJetBtaggingSV
            *akSoftDrop1PFJetBtaggingNegSV
#            *akSoftDrop1PFJetBtaggingMu
            )

akSoftDrop1PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akSoftDrop1PFJets"),
        genJetMatch          = cms.InputTag("akSoftDrop1PFmatch"),
        genPartonMatch       = cms.InputTag("akSoftDrop1PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akSoftDrop1PFcorr")),
        JetPartonMapSource   = cms.InputTag("akSoftDrop1PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akSoftDrop1PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akSoftDrop1PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akSoftDrop1PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akSoftDrop1PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akSoftDrop1PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akSoftDrop1PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akSoftDrop1PFJetBProbabilityBJetTags"),
            cms.InputTag("akSoftDrop1PFJetProbabilityBJetTags"),
            #cms.InputTag("akSoftDrop1PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akSoftDrop1PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akSoftDrop1PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akSoftDrop1PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akSoftDrop1PFJetID"),
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

akSoftDrop1PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akSoftDrop1PFJets"),
           	    R0  = cms.double( 0.1)
)
akSoftDrop1PFpatJetsWithBtagging.userData.userFloats.src += ['akSoftDrop1PFNjettiness:tau1','akSoftDrop1PFNjettiness:tau2','akSoftDrop1PFNjettiness:tau3']

akSoftDrop1PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akSoftDrop1PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akSoftDrop1PF"),
                                                             jetName = cms.untracked.string("akSoftDrop1PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop1GenJets"),
                                                             doGenTaus = True
                                                             )

akSoftDrop1PFJetSequence_mc = cms.Sequence(
                                                  #akSoftDrop1PFclean
                                                  #*
                                                  akSoftDrop1PFmatch
                                                  #*
                                                  #akSoftDrop1PFmatchGroomed
                                                  *
                                                  akSoftDrop1PFparton
                                                  *
                                                  akSoftDrop1PFcorr
                                                  *
                                                  #akSoftDrop1PFJetID
                                                  #*
                                                  akSoftDrop1PFPatJetFlavourIdLegacy
                                                  #*
			                          #akSoftDrop1PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akSoftDrop1PFJetTracksAssociatorAtVertex
                                                  *
                                                  akSoftDrop1PFJetBtagging
                                                  *
                                                  akSoftDrop1PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akSoftDrop1PFpatJetsWithBtagging
                                                  *
                                                  akSoftDrop1PFJetAnalyzer
                                                  )

akSoftDrop1PFJetSequence_data = cms.Sequence(akSoftDrop1PFcorr
                                                    *
                                                    #akSoftDrop1PFJetID
                                                    #*
                                                    akSoftDrop1PFJetTracksAssociatorAtVertex
                                                    *
                                                    akSoftDrop1PFJetBtagging
                                                    *
                                                    akSoftDrop1PFNjettiness 
                                                    *
                                                    akSoftDrop1PFpatJetsWithBtagging
                                                    *
                                                    akSoftDrop1PFJetAnalyzer
                                                    )

akSoftDrop1PFJetSequence_jec = cms.Sequence(akSoftDrop1PFJetSequence_mc)
akSoftDrop1PFJetSequence_mb = cms.Sequence(akSoftDrop1PFJetSequence_mc)

akSoftDrop1PFJetSequence = cms.Sequence(akSoftDrop1PFJetSequence_jec)
akSoftDrop1PFJetAnalyzer.genPtMin = cms.untracked.double(1)
akSoftDrop1PFJetAnalyzer.jetPtMin = cms.double(1)
