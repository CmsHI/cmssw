

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter3PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter3PFJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akFilter3PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter3GenJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akFilter3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter3PFJets")
                                                        )

akFilter3PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter3PFJets"),
    payload = "AK3PF_offline"
    )

akFilter3PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter3CaloJets'))

#akFilter3PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3GenJets'))

akFilter3PFbTagger = bTaggers("akFilter3PF",0.3)

#create objects locally since they dont load properly otherwise
#akFilter3PFmatch = akFilter3PFbTagger.match
akFilter3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter3PFJets"), matched = cms.InputTag("genParticles"))
akFilter3PFPatJetFlavourAssociationLegacy = akFilter3PFbTagger.PatJetFlavourAssociationLegacy
akFilter3PFPatJetPartons = akFilter3PFbTagger.PatJetPartons
akFilter3PFJetTracksAssociatorAtVertex = akFilter3PFbTagger.JetTracksAssociatorAtVertex
akFilter3PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter3PFSimpleSecondaryVertexHighEffBJetTags = akFilter3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter3PFSimpleSecondaryVertexHighPurBJetTags = akFilter3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter3PFCombinedSecondaryVertexBJetTags = akFilter3PFbTagger.CombinedSecondaryVertexBJetTags
akFilter3PFCombinedSecondaryVertexV2BJetTags = akFilter3PFbTagger.CombinedSecondaryVertexV2BJetTags
akFilter3PFJetBProbabilityBJetTags = akFilter3PFbTagger.JetBProbabilityBJetTags
akFilter3PFSoftPFMuonByPtBJetTags = akFilter3PFbTagger.SoftPFMuonByPtBJetTags
akFilter3PFSoftPFMuonByIP3dBJetTags = akFilter3PFbTagger.SoftPFMuonByIP3dBJetTags
akFilter3PFTrackCountingHighEffBJetTags = akFilter3PFbTagger.TrackCountingHighEffBJetTags
akFilter3PFTrackCountingHighPurBJetTags = akFilter3PFbTagger.TrackCountingHighPurBJetTags
akFilter3PFPatJetPartonAssociationLegacy = akFilter3PFbTagger.PatJetPartonAssociationLegacy

akFilter3PFImpactParameterTagInfos = akFilter3PFbTagger.ImpactParameterTagInfos
akFilter3PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter3PFJetProbabilityBJetTags = akFilter3PFbTagger.JetProbabilityBJetTags

akFilter3PFSecondaryVertexTagInfos = akFilter3PFbTagger.SecondaryVertexTagInfos
akFilter3PFSimpleSecondaryVertexHighEffBJetTags = akFilter3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter3PFSimpleSecondaryVertexHighPurBJetTags = akFilter3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter3PFCombinedSecondaryVertexBJetTags = akFilter3PFbTagger.CombinedSecondaryVertexBJetTags
akFilter3PFCombinedSecondaryVertexV2BJetTags = akFilter3PFbTagger.CombinedSecondaryVertexV2BJetTags

akFilter3PFSecondaryVertexNegativeTagInfos = akFilter3PFbTagger.SecondaryVertexNegativeTagInfos
akFilter3PFNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter3PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter3PFNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter3PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter3PFNegativeCombinedSecondaryVertexBJetTags = akFilter3PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter3PFPositiveCombinedSecondaryVertexBJetTags = akFilter3PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter3PFNegativeCombinedSecondaryVertexV2BJetTags = akFilter3PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter3PFPositiveCombinedSecondaryVertexV2BJetTags = akFilter3PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter3PFSoftPFMuonsTagInfos = akFilter3PFbTagger.SoftPFMuonsTagInfos
akFilter3PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter3PFSoftPFMuonBJetTags = akFilter3PFbTagger.SoftPFMuonBJetTags
akFilter3PFSoftPFMuonByIP3dBJetTags = akFilter3PFbTagger.SoftPFMuonByIP3dBJetTags
akFilter3PFSoftPFMuonByPtBJetTags = akFilter3PFbTagger.SoftPFMuonByPtBJetTags
akFilter3PFNegativeSoftPFMuonByPtBJetTags = akFilter3PFbTagger.NegativeSoftPFMuonByPtBJetTags
akFilter3PFPositiveSoftPFMuonByPtBJetTags = akFilter3PFbTagger.PositiveSoftPFMuonByPtBJetTags
akFilter3PFPatJetFlavourIdLegacy = cms.Sequence(akFilter3PFPatJetPartonAssociationLegacy*akFilter3PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter3PFPatJetFlavourAssociation = akFilter3PFbTagger.PatJetFlavourAssociation
#akFilter3PFPatJetFlavourId = cms.Sequence(akFilter3PFPatJetPartons*akFilter3PFPatJetFlavourAssociation)

akFilter3PFJetBtaggingIP       = cms.Sequence(akFilter3PFImpactParameterTagInfos *
            (akFilter3PFTrackCountingHighEffBJetTags +
             akFilter3PFTrackCountingHighPurBJetTags +
             akFilter3PFJetProbabilityBJetTags +
             akFilter3PFJetBProbabilityBJetTags 
            )
            )

akFilter3PFJetBtaggingSV = cms.Sequence(akFilter3PFImpactParameterTagInfos
            *
            akFilter3PFSecondaryVertexTagInfos
            * (akFilter3PFSimpleSecondaryVertexHighEffBJetTags+
                akFilter3PFSimpleSecondaryVertexHighPurBJetTags+
                akFilter3PFCombinedSecondaryVertexBJetTags+
                akFilter3PFCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter3PFJetBtaggingNegSV = cms.Sequence(akFilter3PFImpactParameterTagInfos
            *
            akFilter3PFSecondaryVertexNegativeTagInfos
            * (akFilter3PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter3PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter3PFNegativeCombinedSecondaryVertexBJetTags+
                akFilter3PFPositiveCombinedSecondaryVertexBJetTags+
                akFilter3PFNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter3PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter3PFJetBtaggingMu = cms.Sequence(akFilter3PFSoftPFMuonsTagInfos * (akFilter3PFSoftPFMuonBJetTags
                +
                akFilter3PFSoftPFMuonByIP3dBJetTags
                +
                akFilter3PFSoftPFMuonByPtBJetTags
                +
                akFilter3PFNegativeSoftPFMuonByPtBJetTags
                +
                akFilter3PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter3PFJetBtagging = cms.Sequence(akFilter3PFJetBtaggingIP
            *akFilter3PFJetBtaggingSV
            *akFilter3PFJetBtaggingNegSV
#            *akFilter3PFJetBtaggingMu
            )

akFilter3PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter3PFJets"),
        genJetMatch          = cms.InputTag("akFilter3PFmatch"),
        genPartonMatch       = cms.InputTag("akFilter3PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter3PFcorr")),
        JetPartonMapSource   = cms.InputTag("akFilter3PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter3PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter3PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter3PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter3PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter3PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter3PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter3PFJetBProbabilityBJetTags"),
            cms.InputTag("akFilter3PFJetProbabilityBJetTags"),
            #cms.InputTag("akFilter3PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter3PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter3PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter3PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter3PFJetID"),
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

akFilter3PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter3PFJets"),
           	    R0  = cms.double( 0.3)
)
akFilter3PFpatJetsWithBtagging.userData.userFloats.src += ['akFilter3PFNjettiness:tau1','akFilter3PFNjettiness:tau2','akFilter3PFNjettiness:tau3']

akFilter3PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter3PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak3GenJets',
                                                             rParam = 0.3,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlow'),
                                                             trackTag = cms.InputTag("generalTracks"),
                                                             fillGenJets = True,
                                                             isMC = True,
							     doSubEvent = True,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akFilter3PF"),
                                                             jetName = cms.untracked.string("akFilter3PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter3GenJets"),
                                                             doGenTaus = True
                                                             )

akFilter3PFJetSequence_mc = cms.Sequence(
                                                  #akFilter3PFclean
                                                  #*
                                                  akFilter3PFmatch
                                                  #*
                                                  #akFilter3PFmatchGroomed
                                                  *
                                                  akFilter3PFparton
                                                  *
                                                  akFilter3PFcorr
                                                  *
                                                  #akFilter3PFJetID
                                                  #*
                                                  akFilter3PFPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter3PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter3PFJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter3PFJetBtagging
                                                  *
                                                  akFilter3PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter3PFpatJetsWithBtagging
                                                  *
                                                  akFilter3PFJetAnalyzer
                                                  )

akFilter3PFJetSequence_data = cms.Sequence(akFilter3PFcorr
                                                    *
                                                    #akFilter3PFJetID
                                                    #*
                                                    akFilter3PFJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter3PFJetBtagging
                                                    *
                                                    akFilter3PFNjettiness 
                                                    *
                                                    akFilter3PFpatJetsWithBtagging
                                                    *
                                                    akFilter3PFJetAnalyzer
                                                    )

akFilter3PFJetSequence_jec = cms.Sequence(akFilter3PFJetSequence_mc)
akFilter3PFJetSequence_mb = cms.Sequence(akFilter3PFJetSequence_mc)

akFilter3PFJetSequence = cms.Sequence(akFilter3PFJetSequence_mc)
