

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter6PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter6PFJets"),
    matched = cms.InputTag("ak6HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akFilter6PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter6HiGenJets"),
    matched = cms.InputTag("ak6HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akFilter6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter6PFJets")
                                                        )

akFilter6PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter6PFJets"),
    payload = "AK6PF_offline"
    )

akFilter6PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter6CaloJets'))

#akFilter6PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6HiCleanedGenJets'))

akFilter6PFbTagger = bTaggers("akFilter6PF",0.6)

#create objects locally since they dont load properly otherwise
#akFilter6PFmatch = akFilter6PFbTagger.match
akFilter6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter6PFJets"), matched = cms.InputTag("selectedPartons"))
akFilter6PFPatJetFlavourAssociationLegacy = akFilter6PFbTagger.PatJetFlavourAssociationLegacy
akFilter6PFPatJetPartons = akFilter6PFbTagger.PatJetPartons
akFilter6PFJetTracksAssociatorAtVertex = akFilter6PFbTagger.JetTracksAssociatorAtVertex
akFilter6PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter6PFSimpleSecondaryVertexHighEffBJetTags = akFilter6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter6PFSimpleSecondaryVertexHighPurBJetTags = akFilter6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter6PFCombinedSecondaryVertexBJetTags = akFilter6PFbTagger.CombinedSecondaryVertexBJetTags
akFilter6PFCombinedSecondaryVertexV2BJetTags = akFilter6PFbTagger.CombinedSecondaryVertexV2BJetTags
akFilter6PFJetBProbabilityBJetTags = akFilter6PFbTagger.JetBProbabilityBJetTags
akFilter6PFSoftPFMuonByPtBJetTags = akFilter6PFbTagger.SoftPFMuonByPtBJetTags
akFilter6PFSoftPFMuonByIP3dBJetTags = akFilter6PFbTagger.SoftPFMuonByIP3dBJetTags
akFilter6PFTrackCountingHighEffBJetTags = akFilter6PFbTagger.TrackCountingHighEffBJetTags
akFilter6PFTrackCountingHighPurBJetTags = akFilter6PFbTagger.TrackCountingHighPurBJetTags
akFilter6PFPatJetPartonAssociationLegacy = akFilter6PFbTagger.PatJetPartonAssociationLegacy

akFilter6PFImpactParameterTagInfos = akFilter6PFbTagger.ImpactParameterTagInfos
akFilter6PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter6PFJetProbabilityBJetTags = akFilter6PFbTagger.JetProbabilityBJetTags

akFilter6PFSecondaryVertexTagInfos = akFilter6PFbTagger.SecondaryVertexTagInfos
akFilter6PFSimpleSecondaryVertexHighEffBJetTags = akFilter6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter6PFSimpleSecondaryVertexHighPurBJetTags = akFilter6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter6PFCombinedSecondaryVertexBJetTags = akFilter6PFbTagger.CombinedSecondaryVertexBJetTags
akFilter6PFCombinedSecondaryVertexV2BJetTags = akFilter6PFbTagger.CombinedSecondaryVertexV2BJetTags

akFilter6PFSecondaryVertexNegativeTagInfos = akFilter6PFbTagger.SecondaryVertexNegativeTagInfos
akFilter6PFNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter6PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter6PFNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter6PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter6PFNegativeCombinedSecondaryVertexBJetTags = akFilter6PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter6PFPositiveCombinedSecondaryVertexBJetTags = akFilter6PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter6PFNegativeCombinedSecondaryVertexV2BJetTags = akFilter6PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter6PFPositiveCombinedSecondaryVertexV2BJetTags = akFilter6PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter6PFSoftPFMuonsTagInfos = akFilter6PFbTagger.SoftPFMuonsTagInfos
akFilter6PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter6PFSoftPFMuonBJetTags = akFilter6PFbTagger.SoftPFMuonBJetTags
akFilter6PFSoftPFMuonByIP3dBJetTags = akFilter6PFbTagger.SoftPFMuonByIP3dBJetTags
akFilter6PFSoftPFMuonByPtBJetTags = akFilter6PFbTagger.SoftPFMuonByPtBJetTags
akFilter6PFNegativeSoftPFMuonByPtBJetTags = akFilter6PFbTagger.NegativeSoftPFMuonByPtBJetTags
akFilter6PFPositiveSoftPFMuonByPtBJetTags = akFilter6PFbTagger.PositiveSoftPFMuonByPtBJetTags
akFilter6PFPatJetFlavourIdLegacy = cms.Sequence(akFilter6PFPatJetPartonAssociationLegacy*akFilter6PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter6PFPatJetFlavourAssociation = akFilter6PFbTagger.PatJetFlavourAssociation
#akFilter6PFPatJetFlavourId = cms.Sequence(akFilter6PFPatJetPartons*akFilter6PFPatJetFlavourAssociation)

akFilter6PFJetBtaggingIP       = cms.Sequence(akFilter6PFImpactParameterTagInfos *
            (akFilter6PFTrackCountingHighEffBJetTags +
             akFilter6PFTrackCountingHighPurBJetTags +
             akFilter6PFJetProbabilityBJetTags +
             akFilter6PFJetBProbabilityBJetTags 
            )
            )

akFilter6PFJetBtaggingSV = cms.Sequence(akFilter6PFImpactParameterTagInfos
            *
            akFilter6PFSecondaryVertexTagInfos
            * (akFilter6PFSimpleSecondaryVertexHighEffBJetTags+
                akFilter6PFSimpleSecondaryVertexHighPurBJetTags+
                akFilter6PFCombinedSecondaryVertexBJetTags+
                akFilter6PFCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter6PFJetBtaggingNegSV = cms.Sequence(akFilter6PFImpactParameterTagInfos
            *
            akFilter6PFSecondaryVertexNegativeTagInfos
            * (akFilter6PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter6PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter6PFNegativeCombinedSecondaryVertexBJetTags+
                akFilter6PFPositiveCombinedSecondaryVertexBJetTags+
                akFilter6PFNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter6PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter6PFJetBtaggingMu = cms.Sequence(akFilter6PFSoftPFMuonsTagInfos * (akFilter6PFSoftPFMuonBJetTags
                +
                akFilter6PFSoftPFMuonByIP3dBJetTags
                +
                akFilter6PFSoftPFMuonByPtBJetTags
                +
                akFilter6PFNegativeSoftPFMuonByPtBJetTags
                +
                akFilter6PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter6PFJetBtagging = cms.Sequence(akFilter6PFJetBtaggingIP
            *akFilter6PFJetBtaggingSV
            *akFilter6PFJetBtaggingNegSV
#            *akFilter6PFJetBtaggingMu
            )

akFilter6PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter6PFJets"),
        genJetMatch          = cms.InputTag("akFilter6PFmatch"),
        genPartonMatch       = cms.InputTag("akFilter6PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter6PFcorr")),
        JetPartonMapSource   = cms.InputTag("akFilter6PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter6PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter6PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter6PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter6PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter6PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter6PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter6PFJetBProbabilityBJetTags"),
            cms.InputTag("akFilter6PFJetProbabilityBJetTags"),
            #cms.InputTag("akFilter6PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter6PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter6PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter6PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter6PFJetID"),
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

akFilter6PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter6PFJets"),
           	    R0  = cms.double( 0.6)
)
akFilter6PFpatJetsWithBtagging.userData.userFloats.src += ['akFilter6PFNjettiness:tau1','akFilter6PFNjettiness:tau2','akFilter6PFNjettiness:tau3']

akFilter6PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter6PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak6HiGenJets',
                                                             rParam = 0.6,
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
                                                             bTagJetName = cms.untracked.string("akFilter6PF"),
                                                             jetName = cms.untracked.string("akFilter6PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter6GenJets"),
                                                             doGenTaus = True
                                                             )

akFilter6PFJetSequence_mc = cms.Sequence(
                                                  #akFilter6PFclean
                                                  #*
                                                  akFilter6PFmatch
                                                  #*
                                                  #akFilter6PFmatchGroomed
                                                  *
                                                  akFilter6PFparton
                                                  *
                                                  akFilter6PFcorr
                                                  *
                                                  #akFilter6PFJetID
                                                  #*
                                                  akFilter6PFPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter6PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter6PFJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter6PFJetBtagging
                                                  *
                                                  akFilter6PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter6PFpatJetsWithBtagging
                                                  *
                                                  akFilter6PFJetAnalyzer
                                                  )

akFilter6PFJetSequence_data = cms.Sequence(akFilter6PFcorr
                                                    *
                                                    #akFilter6PFJetID
                                                    #*
                                                    akFilter6PFJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter6PFJetBtagging
                                                    *
                                                    akFilter6PFNjettiness 
                                                    *
                                                    akFilter6PFpatJetsWithBtagging
                                                    *
                                                    akFilter6PFJetAnalyzer
                                                    )

akFilter6PFJetSequence_jec = cms.Sequence(akFilter6PFJetSequence_mc)
akFilter6PFJetSequence_mb = cms.Sequence(akFilter6PFJetSequence_mc)

akFilter6PFJetSequence = cms.Sequence(akFilter6PFJetSequence_mb)
