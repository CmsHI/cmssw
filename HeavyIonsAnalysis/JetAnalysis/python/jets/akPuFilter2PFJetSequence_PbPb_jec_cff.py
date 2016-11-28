

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter2PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter2PFJets"),
    matched = cms.InputTag("ak2HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akPuFilter2PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter2HiGenJets"),
    matched = cms.InputTag("ak2HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akPuFilter2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter2PFJets")
                                                        )

akPuFilter2PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter2PFJets"),
    payload = "AKPu2PF_offline"
    )

akPuFilter2PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter2CaloJets'))

#akPuFilter2PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2HiSignalGenJets'))

akPuFilter2PFbTagger = bTaggers("akPuFilter2PF",0.2)

#create objects locally since they dont load properly otherwise
#akPuFilter2PFmatch = akPuFilter2PFbTagger.match
akPuFilter2PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter2PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuFilter2PFPatJetFlavourAssociationLegacy = akPuFilter2PFbTagger.PatJetFlavourAssociationLegacy
akPuFilter2PFPatJetPartons = akPuFilter2PFbTagger.PatJetPartons
akPuFilter2PFJetTracksAssociatorAtVertex = akPuFilter2PFbTagger.JetTracksAssociatorAtVertex
akPuFilter2PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter2PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter2PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter2PFCombinedSecondaryVertexBJetTags = akPuFilter2PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter2PFCombinedSecondaryVertexV2BJetTags = akPuFilter2PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter2PFJetBProbabilityBJetTags = akPuFilter2PFbTagger.JetBProbabilityBJetTags
akPuFilter2PFSoftPFMuonByPtBJetTags = akPuFilter2PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter2PFSoftPFMuonByIP3dBJetTags = akPuFilter2PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter2PFTrackCountingHighEffBJetTags = akPuFilter2PFbTagger.TrackCountingHighEffBJetTags
akPuFilter2PFTrackCountingHighPurBJetTags = akPuFilter2PFbTagger.TrackCountingHighPurBJetTags
akPuFilter2PFPatJetPartonAssociationLegacy = akPuFilter2PFbTagger.PatJetPartonAssociationLegacy

akPuFilter2PFImpactParameterTagInfos = akPuFilter2PFbTagger.ImpactParameterTagInfos
akPuFilter2PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter2PFJetProbabilityBJetTags = akPuFilter2PFbTagger.JetProbabilityBJetTags

akPuFilter2PFSecondaryVertexTagInfos = akPuFilter2PFbTagger.SecondaryVertexTagInfos
akPuFilter2PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter2PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter2PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter2PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter2PFCombinedSecondaryVertexBJetTags = akPuFilter2PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter2PFCombinedSecondaryVertexV2BJetTags = akPuFilter2PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter2PFSecondaryVertexNegativeTagInfos = akPuFilter2PFbTagger.SecondaryVertexNegativeTagInfos
akPuFilter2PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter2PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter2PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter2PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter2PFNegativeCombinedSecondaryVertexBJetTags = akPuFilter2PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter2PFPositiveCombinedSecondaryVertexBJetTags = akPuFilter2PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter2PFNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter2PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter2PFPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter2PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter2PFSoftPFMuonsTagInfos = akPuFilter2PFbTagger.SoftPFMuonsTagInfos
akPuFilter2PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter2PFSoftPFMuonBJetTags = akPuFilter2PFbTagger.SoftPFMuonBJetTags
akPuFilter2PFSoftPFMuonByIP3dBJetTags = akPuFilter2PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter2PFSoftPFMuonByPtBJetTags = akPuFilter2PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter2PFNegativeSoftPFMuonByPtBJetTags = akPuFilter2PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter2PFPositiveSoftPFMuonByPtBJetTags = akPuFilter2PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter2PFPatJetFlavourIdLegacy = cms.Sequence(akPuFilter2PFPatJetPartonAssociationLegacy*akPuFilter2PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter2PFPatJetFlavourAssociation = akPuFilter2PFbTagger.PatJetFlavourAssociation
#akPuFilter2PFPatJetFlavourId = cms.Sequence(akPuFilter2PFPatJetPartons*akPuFilter2PFPatJetFlavourAssociation)

akPuFilter2PFJetBtaggingIP       = cms.Sequence(akPuFilter2PFImpactParameterTagInfos *
            (akPuFilter2PFTrackCountingHighEffBJetTags +
             akPuFilter2PFTrackCountingHighPurBJetTags +
             akPuFilter2PFJetProbabilityBJetTags +
             akPuFilter2PFJetBProbabilityBJetTags 
            )
            )

akPuFilter2PFJetBtaggingSV = cms.Sequence(akPuFilter2PFImpactParameterTagInfos
            *
            akPuFilter2PFSecondaryVertexTagInfos
            * (akPuFilter2PFSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter2PFSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter2PFCombinedSecondaryVertexBJetTags+
                akPuFilter2PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter2PFJetBtaggingNegSV = cms.Sequence(akPuFilter2PFImpactParameterTagInfos
            *
            akPuFilter2PFSecondaryVertexNegativeTagInfos
            * (akPuFilter2PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter2PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter2PFNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter2PFPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter2PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter2PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter2PFJetBtaggingMu = cms.Sequence(akPuFilter2PFSoftPFMuonsTagInfos * (akPuFilter2PFSoftPFMuonBJetTags
                +
                akPuFilter2PFSoftPFMuonByIP3dBJetTags
                +
                akPuFilter2PFSoftPFMuonByPtBJetTags
                +
                akPuFilter2PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter2PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter2PFJetBtagging = cms.Sequence(akPuFilter2PFJetBtaggingIP
            *akPuFilter2PFJetBtaggingSV
            *akPuFilter2PFJetBtaggingNegSV
#            *akPuFilter2PFJetBtaggingMu
            )

akPuFilter2PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter2PFJets"),
        genJetMatch          = cms.InputTag("akPuFilter2PFmatch"),
        genPartonMatch       = cms.InputTag("akPuFilter2PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter2PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter2PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter2PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter2PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter2PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter2PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter2PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter2PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter2PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter2PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter2PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter2PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter2PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter2PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter2PFJetID"),
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

akPuFilter2PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter2PFJets"),
           	    R0  = cms.double( 0.2)
)
akPuFilter2PFpatJetsWithBtagging.userData.userFloats.src += ['akPuFilter2PFNjettiness:tau1','akPuFilter2PFNjettiness:tau2','akPuFilter2PFNjettiness:tau3']

akPuFilter2PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter2PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuFilter2PF"),
                                                             jetName = cms.untracked.string("akPuFilter2PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter2GenJets"),
                                                             doGenTaus = True
                                                             )

akPuFilter2PFJetSequence_mc = cms.Sequence(
                                                  #akPuFilter2PFclean
                                                  #*
                                                  akPuFilter2PFmatch
                                                  #*
                                                  #akPuFilter2PFmatchGroomed
                                                  *
                                                  akPuFilter2PFparton
                                                  *
                                                  akPuFilter2PFcorr
                                                  *
                                                  #akPuFilter2PFJetID
                                                  #*
                                                  akPuFilter2PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter2PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter2PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter2PFJetBtagging
                                                  *
                                                  akPuFilter2PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter2PFpatJetsWithBtagging
                                                  *
                                                  akPuFilter2PFJetAnalyzer
                                                  )

akPuFilter2PFJetSequence_data = cms.Sequence(akPuFilter2PFcorr
                                                    *
                                                    #akPuFilter2PFJetID
                                                    #*
                                                    akPuFilter2PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter2PFJetBtagging
                                                    *
                                                    akPuFilter2PFNjettiness 
                                                    *
                                                    akPuFilter2PFpatJetsWithBtagging
                                                    *
                                                    akPuFilter2PFJetAnalyzer
                                                    )

akPuFilter2PFJetSequence_jec = cms.Sequence(akPuFilter2PFJetSequence_mc)
akPuFilter2PFJetSequence_mb = cms.Sequence(akPuFilter2PFJetSequence_mc)

akPuFilter2PFJetSequence = cms.Sequence(akPuFilter2PFJetSequence_jec)
akPuFilter2PFJetAnalyzer.genPtMin = cms.untracked.double(1)
akPuFilter2PFJetAnalyzer.jetPtMin = cms.double(1)
