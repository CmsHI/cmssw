

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter3PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter3PFJets"),
    matched = cms.InputTag("ak3HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akPuFilter3PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter3HiGenJets"),
    matched = cms.InputTag("ak3HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akPuFilter3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter3PFJets")
                                                        )

akPuFilter3PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter3PFJets"),
    payload = "AKPu3PF_offline"
    )

akPuFilter3PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter3CaloJets'))

#akPuFilter3PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiSignalGenJets'))

akPuFilter3PFbTagger = bTaggers("akPuFilter3PF",0.3)

#create objects locally since they dont load properly otherwise
#akPuFilter3PFmatch = akPuFilter3PFbTagger.match
akPuFilter3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter3PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuFilter3PFPatJetFlavourAssociationLegacy = akPuFilter3PFbTagger.PatJetFlavourAssociationLegacy
akPuFilter3PFPatJetPartons = akPuFilter3PFbTagger.PatJetPartons
akPuFilter3PFJetTracksAssociatorAtVertex = akPuFilter3PFbTagger.JetTracksAssociatorAtVertex
akPuFilter3PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter3PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter3PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter3PFCombinedSecondaryVertexBJetTags = akPuFilter3PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter3PFCombinedSecondaryVertexV2BJetTags = akPuFilter3PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter3PFJetBProbabilityBJetTags = akPuFilter3PFbTagger.JetBProbabilityBJetTags
akPuFilter3PFSoftPFMuonByPtBJetTags = akPuFilter3PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter3PFSoftPFMuonByIP3dBJetTags = akPuFilter3PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter3PFTrackCountingHighEffBJetTags = akPuFilter3PFbTagger.TrackCountingHighEffBJetTags
akPuFilter3PFTrackCountingHighPurBJetTags = akPuFilter3PFbTagger.TrackCountingHighPurBJetTags
akPuFilter3PFPatJetPartonAssociationLegacy = akPuFilter3PFbTagger.PatJetPartonAssociationLegacy

akPuFilter3PFImpactParameterTagInfos = akPuFilter3PFbTagger.ImpactParameterTagInfos
akPuFilter3PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter3PFJetProbabilityBJetTags = akPuFilter3PFbTagger.JetProbabilityBJetTags

akPuFilter3PFSecondaryVertexTagInfos = akPuFilter3PFbTagger.SecondaryVertexTagInfos
akPuFilter3PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter3PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter3PFCombinedSecondaryVertexBJetTags = akPuFilter3PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter3PFCombinedSecondaryVertexV2BJetTags = akPuFilter3PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter3PFSecondaryVertexNegativeTagInfos = akPuFilter3PFbTagger.SecondaryVertexNegativeTagInfos
akPuFilter3PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter3PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter3PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter3PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter3PFNegativeCombinedSecondaryVertexBJetTags = akPuFilter3PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter3PFPositiveCombinedSecondaryVertexBJetTags = akPuFilter3PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter3PFNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter3PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter3PFPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter3PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter3PFSoftPFMuonsTagInfos = akPuFilter3PFbTagger.SoftPFMuonsTagInfos
akPuFilter3PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter3PFSoftPFMuonBJetTags = akPuFilter3PFbTagger.SoftPFMuonBJetTags
akPuFilter3PFSoftPFMuonByIP3dBJetTags = akPuFilter3PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter3PFSoftPFMuonByPtBJetTags = akPuFilter3PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter3PFNegativeSoftPFMuonByPtBJetTags = akPuFilter3PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter3PFPositiveSoftPFMuonByPtBJetTags = akPuFilter3PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter3PFPatJetFlavourIdLegacy = cms.Sequence(akPuFilter3PFPatJetPartonAssociationLegacy*akPuFilter3PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter3PFPatJetFlavourAssociation = akPuFilter3PFbTagger.PatJetFlavourAssociation
#akPuFilter3PFPatJetFlavourId = cms.Sequence(akPuFilter3PFPatJetPartons*akPuFilter3PFPatJetFlavourAssociation)

akPuFilter3PFJetBtaggingIP       = cms.Sequence(akPuFilter3PFImpactParameterTagInfos *
            (akPuFilter3PFTrackCountingHighEffBJetTags +
             akPuFilter3PFTrackCountingHighPurBJetTags +
             akPuFilter3PFJetProbabilityBJetTags +
             akPuFilter3PFJetBProbabilityBJetTags 
            )
            )

akPuFilter3PFJetBtaggingSV = cms.Sequence(akPuFilter3PFImpactParameterTagInfos
            *
            akPuFilter3PFSecondaryVertexTagInfos
            * (akPuFilter3PFSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter3PFSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter3PFCombinedSecondaryVertexBJetTags+
                akPuFilter3PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter3PFJetBtaggingNegSV = cms.Sequence(akPuFilter3PFImpactParameterTagInfos
            *
            akPuFilter3PFSecondaryVertexNegativeTagInfos
            * (akPuFilter3PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter3PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter3PFNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter3PFPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter3PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter3PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter3PFJetBtaggingMu = cms.Sequence(akPuFilter3PFSoftPFMuonsTagInfos * (akPuFilter3PFSoftPFMuonBJetTags
                +
                akPuFilter3PFSoftPFMuonByIP3dBJetTags
                +
                akPuFilter3PFSoftPFMuonByPtBJetTags
                +
                akPuFilter3PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter3PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter3PFJetBtagging = cms.Sequence(akPuFilter3PFJetBtaggingIP
            *akPuFilter3PFJetBtaggingSV
            *akPuFilter3PFJetBtaggingNegSV
#            *akPuFilter3PFJetBtaggingMu
            )

akPuFilter3PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter3PFJets"),
        genJetMatch          = cms.InputTag("akPuFilter3PFmatch"),
        genPartonMatch       = cms.InputTag("akPuFilter3PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter3PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter3PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter3PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter3PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter3PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter3PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter3PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter3PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter3PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter3PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter3PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter3PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter3PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter3PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter3PFJetID"),
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

akPuFilter3PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter3PFJets"),
           	    R0  = cms.double( 0.3)
)
akPuFilter3PFpatJetsWithBtagging.userData.userFloats.src += ['akPuFilter3PFNjettiness:tau1','akPuFilter3PFNjettiness:tau2','akPuFilter3PFNjettiness:tau3']

akPuFilter3PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter3PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak3HiGenJets',
                                                             rParam = 0.3,
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
                                                             bTagJetName = cms.untracked.string("akPuFilter3PF"),
                                                             jetName = cms.untracked.string("akPuFilter3PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter3GenJets"),
                                                             doGenTaus = False
                                                             )

akPuFilter3PFJetSequence_mc = cms.Sequence(
                                                  #akPuFilter3PFclean
                                                  #*
                                                  akPuFilter3PFmatch
                                                  #*
                                                  #akPuFilter3PFmatchGroomed
                                                  *
                                                  akPuFilter3PFparton
                                                  *
                                                  akPuFilter3PFcorr
                                                  *
                                                  #akPuFilter3PFJetID
                                                  #*
                                                  akPuFilter3PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter3PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter3PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter3PFJetBtagging
                                                  *
                                                  akPuFilter3PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter3PFpatJetsWithBtagging
                                                  *
                                                  akPuFilter3PFJetAnalyzer
                                                  )

akPuFilter3PFJetSequence_data = cms.Sequence(akPuFilter3PFcorr
                                                    *
                                                    #akPuFilter3PFJetID
                                                    #*
                                                    akPuFilter3PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter3PFJetBtagging
                                                    *
                                                    akPuFilter3PFNjettiness 
                                                    *
                                                    akPuFilter3PFpatJetsWithBtagging
                                                    *
                                                    akPuFilter3PFJetAnalyzer
                                                    )

akPuFilter3PFJetSequence_jec = cms.Sequence(akPuFilter3PFJetSequence_mc)
akPuFilter3PFJetSequence_mb = cms.Sequence(akPuFilter3PFJetSequence_mc)

akPuFilter3PFJetSequence = cms.Sequence(akPuFilter3PFJetSequence_data)
