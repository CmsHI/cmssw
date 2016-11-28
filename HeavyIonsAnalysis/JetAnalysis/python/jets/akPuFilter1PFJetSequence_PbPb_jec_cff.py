

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter1PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter1PFJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akPuFilter1PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter1HiGenJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akPuFilter1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter1PFJets")
                                                        )

akPuFilter1PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter1PFJets"),
    payload = "AKPu1PF_offline"
    )

akPuFilter1PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter1CaloJets'))

#akPuFilter1PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1HiSignalGenJets'))

akPuFilter1PFbTagger = bTaggers("akPuFilter1PF",0.1)

#create objects locally since they dont load properly otherwise
#akPuFilter1PFmatch = akPuFilter1PFbTagger.match
akPuFilter1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter1PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuFilter1PFPatJetFlavourAssociationLegacy = akPuFilter1PFbTagger.PatJetFlavourAssociationLegacy
akPuFilter1PFPatJetPartons = akPuFilter1PFbTagger.PatJetPartons
akPuFilter1PFJetTracksAssociatorAtVertex = akPuFilter1PFbTagger.JetTracksAssociatorAtVertex
akPuFilter1PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter1PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter1PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter1PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter1PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter1PFCombinedSecondaryVertexBJetTags = akPuFilter1PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter1PFCombinedSecondaryVertexV2BJetTags = akPuFilter1PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter1PFJetBProbabilityBJetTags = akPuFilter1PFbTagger.JetBProbabilityBJetTags
akPuFilter1PFSoftPFMuonByPtBJetTags = akPuFilter1PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter1PFSoftPFMuonByIP3dBJetTags = akPuFilter1PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter1PFTrackCountingHighEffBJetTags = akPuFilter1PFbTagger.TrackCountingHighEffBJetTags
akPuFilter1PFTrackCountingHighPurBJetTags = akPuFilter1PFbTagger.TrackCountingHighPurBJetTags
akPuFilter1PFPatJetPartonAssociationLegacy = akPuFilter1PFbTagger.PatJetPartonAssociationLegacy

akPuFilter1PFImpactParameterTagInfos = akPuFilter1PFbTagger.ImpactParameterTagInfos
akPuFilter1PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter1PFJetProbabilityBJetTags = akPuFilter1PFbTagger.JetProbabilityBJetTags

akPuFilter1PFSecondaryVertexTagInfos = akPuFilter1PFbTagger.SecondaryVertexTagInfos
akPuFilter1PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter1PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter1PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter1PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter1PFCombinedSecondaryVertexBJetTags = akPuFilter1PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter1PFCombinedSecondaryVertexV2BJetTags = akPuFilter1PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter1PFSecondaryVertexNegativeTagInfos = akPuFilter1PFbTagger.SecondaryVertexNegativeTagInfos
akPuFilter1PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter1PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter1PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter1PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter1PFNegativeCombinedSecondaryVertexBJetTags = akPuFilter1PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter1PFPositiveCombinedSecondaryVertexBJetTags = akPuFilter1PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter1PFNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter1PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter1PFPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter1PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter1PFSoftPFMuonsTagInfos = akPuFilter1PFbTagger.SoftPFMuonsTagInfos
akPuFilter1PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter1PFSoftPFMuonBJetTags = akPuFilter1PFbTagger.SoftPFMuonBJetTags
akPuFilter1PFSoftPFMuonByIP3dBJetTags = akPuFilter1PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter1PFSoftPFMuonByPtBJetTags = akPuFilter1PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter1PFNegativeSoftPFMuonByPtBJetTags = akPuFilter1PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter1PFPositiveSoftPFMuonByPtBJetTags = akPuFilter1PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter1PFPatJetFlavourIdLegacy = cms.Sequence(akPuFilter1PFPatJetPartonAssociationLegacy*akPuFilter1PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter1PFPatJetFlavourAssociation = akPuFilter1PFbTagger.PatJetFlavourAssociation
#akPuFilter1PFPatJetFlavourId = cms.Sequence(akPuFilter1PFPatJetPartons*akPuFilter1PFPatJetFlavourAssociation)

akPuFilter1PFJetBtaggingIP       = cms.Sequence(akPuFilter1PFImpactParameterTagInfos *
            (akPuFilter1PFTrackCountingHighEffBJetTags +
             akPuFilter1PFTrackCountingHighPurBJetTags +
             akPuFilter1PFJetProbabilityBJetTags +
             akPuFilter1PFJetBProbabilityBJetTags 
            )
            )

akPuFilter1PFJetBtaggingSV = cms.Sequence(akPuFilter1PFImpactParameterTagInfos
            *
            akPuFilter1PFSecondaryVertexTagInfos
            * (akPuFilter1PFSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter1PFSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter1PFCombinedSecondaryVertexBJetTags+
                akPuFilter1PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter1PFJetBtaggingNegSV = cms.Sequence(akPuFilter1PFImpactParameterTagInfos
            *
            akPuFilter1PFSecondaryVertexNegativeTagInfos
            * (akPuFilter1PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter1PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter1PFNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter1PFPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter1PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter1PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter1PFJetBtaggingMu = cms.Sequence(akPuFilter1PFSoftPFMuonsTagInfos * (akPuFilter1PFSoftPFMuonBJetTags
                +
                akPuFilter1PFSoftPFMuonByIP3dBJetTags
                +
                akPuFilter1PFSoftPFMuonByPtBJetTags
                +
                akPuFilter1PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter1PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter1PFJetBtagging = cms.Sequence(akPuFilter1PFJetBtaggingIP
            *akPuFilter1PFJetBtaggingSV
            *akPuFilter1PFJetBtaggingNegSV
#            *akPuFilter1PFJetBtaggingMu
            )

akPuFilter1PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter1PFJets"),
        genJetMatch          = cms.InputTag("akPuFilter1PFmatch"),
        genPartonMatch       = cms.InputTag("akPuFilter1PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter1PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter1PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter1PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter1PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter1PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter1PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter1PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter1PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter1PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter1PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter1PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter1PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter1PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter1PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter1PFJetID"),
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

akPuFilter1PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter1PFJets"),
           	    R0  = cms.double( 0.1)
)
akPuFilter1PFpatJetsWithBtagging.userData.userFloats.src += ['akPuFilter1PFNjettiness:tau1','akPuFilter1PFNjettiness:tau2','akPuFilter1PFNjettiness:tau3']

akPuFilter1PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter1PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuFilter1PF"),
                                                             jetName = cms.untracked.string("akPuFilter1PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter1GenJets"),
                                                             doGenTaus = True
                                                             )

akPuFilter1PFJetSequence_mc = cms.Sequence(
                                                  #akPuFilter1PFclean
                                                  #*
                                                  akPuFilter1PFmatch
                                                  #*
                                                  #akPuFilter1PFmatchGroomed
                                                  *
                                                  akPuFilter1PFparton
                                                  *
                                                  akPuFilter1PFcorr
                                                  *
                                                  #akPuFilter1PFJetID
                                                  #*
                                                  akPuFilter1PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter1PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter1PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter1PFJetBtagging
                                                  *
                                                  akPuFilter1PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter1PFpatJetsWithBtagging
                                                  *
                                                  akPuFilter1PFJetAnalyzer
                                                  )

akPuFilter1PFJetSequence_data = cms.Sequence(akPuFilter1PFcorr
                                                    *
                                                    #akPuFilter1PFJetID
                                                    #*
                                                    akPuFilter1PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter1PFJetBtagging
                                                    *
                                                    akPuFilter1PFNjettiness 
                                                    *
                                                    akPuFilter1PFpatJetsWithBtagging
                                                    *
                                                    akPuFilter1PFJetAnalyzer
                                                    )

akPuFilter1PFJetSequence_jec = cms.Sequence(akPuFilter1PFJetSequence_mc)
akPuFilter1PFJetSequence_mb = cms.Sequence(akPuFilter1PFJetSequence_mc)

akPuFilter1PFJetSequence = cms.Sequence(akPuFilter1PFJetSequence_jec)
akPuFilter1PFJetAnalyzer.genPtMin = cms.untracked.double(1)
akPuFilter1PFJetAnalyzer.jetPtMin = cms.double(1)
