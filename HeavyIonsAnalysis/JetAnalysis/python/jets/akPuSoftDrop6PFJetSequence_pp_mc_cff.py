

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop6PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop6PFJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akPuSoftDrop6PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop6GenJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akPuSoftDrop6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop6PFJets")
                                                        )

akPuSoftDrop6PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop6PFJets"),
    payload = "AKPu6PF_offline"
    )

akPuSoftDrop6PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop6CaloJets'))

#akPuSoftDrop6PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6GenJets'))

akPuSoftDrop6PFbTagger = bTaggers("akPuSoftDrop6PF",0.6)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop6PFmatch = akPuSoftDrop6PFbTagger.match
akPuSoftDrop6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop6PFJets"), matched = cms.InputTag("genParticles"))
akPuSoftDrop6PFPatJetFlavourAssociationLegacy = akPuSoftDrop6PFbTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop6PFPatJetPartons = akPuSoftDrop6PFbTagger.PatJetPartons
akPuSoftDrop6PFJetTracksAssociatorAtVertex = akPuSoftDrop6PFbTagger.JetTracksAssociatorAtVertex
akPuSoftDrop6PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop6PFCombinedSecondaryVertexBJetTags = akPuSoftDrop6PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop6PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop6PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop6PFJetBProbabilityBJetTags = akPuSoftDrop6PFbTagger.JetBProbabilityBJetTags
akPuSoftDrop6PFSoftPFMuonByPtBJetTags = akPuSoftDrop6PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop6PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop6PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop6PFTrackCountingHighEffBJetTags = akPuSoftDrop6PFbTagger.TrackCountingHighEffBJetTags
akPuSoftDrop6PFTrackCountingHighPurBJetTags = akPuSoftDrop6PFbTagger.TrackCountingHighPurBJetTags
akPuSoftDrop6PFPatJetPartonAssociationLegacy = akPuSoftDrop6PFbTagger.PatJetPartonAssociationLegacy

akPuSoftDrop6PFImpactParameterTagInfos = akPuSoftDrop6PFbTagger.ImpactParameterTagInfos
akPuSoftDrop6PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop6PFJetProbabilityBJetTags = akPuSoftDrop6PFbTagger.JetProbabilityBJetTags

akPuSoftDrop6PFSecondaryVertexTagInfos = akPuSoftDrop6PFbTagger.SecondaryVertexTagInfos
akPuSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop6PFCombinedSecondaryVertexBJetTags = akPuSoftDrop6PFbTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop6PFCombinedSecondaryVertexV2BJetTags = akPuSoftDrop6PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop6PFSecondaryVertexNegativeTagInfos = akPuSoftDrop6PFbTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop6PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop6PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop6PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop6PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop6PFNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop6PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop6PFPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop6PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop6PFNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop6PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop6PFPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop6PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop6PFSoftPFMuonsTagInfos = akPuSoftDrop6PFbTagger.SoftPFMuonsTagInfos
akPuSoftDrop6PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop6PFSoftPFMuonBJetTags = akPuSoftDrop6PFbTagger.SoftPFMuonBJetTags
akPuSoftDrop6PFSoftPFMuonByIP3dBJetTags = akPuSoftDrop6PFbTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop6PFSoftPFMuonByPtBJetTags = akPuSoftDrop6PFbTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop6PFNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop6PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop6PFPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop6PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop6PFPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop6PFPatJetPartonAssociationLegacy*akPuSoftDrop6PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop6PFPatJetFlavourAssociation = akPuSoftDrop6PFbTagger.PatJetFlavourAssociation
#akPuSoftDrop6PFPatJetFlavourId = cms.Sequence(akPuSoftDrop6PFPatJetPartons*akPuSoftDrop6PFPatJetFlavourAssociation)

akPuSoftDrop6PFJetBtaggingIP       = cms.Sequence(akPuSoftDrop6PFImpactParameterTagInfos *
            (akPuSoftDrop6PFTrackCountingHighEffBJetTags +
             akPuSoftDrop6PFTrackCountingHighPurBJetTags +
             akPuSoftDrop6PFJetProbabilityBJetTags +
             akPuSoftDrop6PFJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop6PFJetBtaggingSV = cms.Sequence(akPuSoftDrop6PFImpactParameterTagInfos
            *
            akPuSoftDrop6PFSecondaryVertexTagInfos
            * (akPuSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop6PFCombinedSecondaryVertexBJetTags+
                akPuSoftDrop6PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop6PFJetBtaggingNegSV = cms.Sequence(akPuSoftDrop6PFImpactParameterTagInfos
            *
            akPuSoftDrop6PFSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop6PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop6PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop6PFNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop6PFPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop6PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop6PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop6PFJetBtaggingMu = cms.Sequence(akPuSoftDrop6PFSoftPFMuonsTagInfos * (akPuSoftDrop6PFSoftPFMuonBJetTags
                +
                akPuSoftDrop6PFSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop6PFSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop6PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop6PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop6PFJetBtagging = cms.Sequence(akPuSoftDrop6PFJetBtaggingIP
            *akPuSoftDrop6PFJetBtaggingSV
            *akPuSoftDrop6PFJetBtaggingNegSV
#            *akPuSoftDrop6PFJetBtaggingMu
            )

akPuSoftDrop6PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop6PFJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop6PFmatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop6PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop6PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop6PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop6PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop6PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop6PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop6PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop6PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop6PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop6PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop6PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop6PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop6PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop6PFJetID"),
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

akPuSoftDrop6PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop6PFJets"),
           	    R0  = cms.double( 0.6)
)
akPuSoftDrop6PFpatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop6PFNjettiness:tau1','akPuSoftDrop6PFNjettiness:tau2','akPuSoftDrop6PFNjettiness:tau3']

akPuSoftDrop6PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop6PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak6GenJets',
                                                             rParam = 0.6,
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop6PF"),
                                                             jetName = cms.untracked.string("akPuSoftDrop6PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(True),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop6GenJets"),
                                                             doGenTaus = True
                                                             )

akPuSoftDrop6PFJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop6PFclean
                                                  #*
                                                  akPuSoftDrop6PFmatch
                                                  #*
                                                  #akPuSoftDrop6PFmatchGroomed
                                                  *
                                                  akPuSoftDrop6PFparton
                                                  *
                                                  akPuSoftDrop6PFcorr
                                                  *
                                                  #akPuSoftDrop6PFJetID
                                                  #*
                                                  akPuSoftDrop6PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop6PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop6PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop6PFJetBtagging
                                                  *
                                                  akPuSoftDrop6PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop6PFpatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop6PFJetAnalyzer
                                                  )

akPuSoftDrop6PFJetSequence_data = cms.Sequence(akPuSoftDrop6PFcorr
                                                    *
                                                    #akPuSoftDrop6PFJetID
                                                    #*
                                                    akPuSoftDrop6PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop6PFJetBtagging
                                                    *
                                                    akPuSoftDrop6PFNjettiness 
                                                    *
                                                    akPuSoftDrop6PFpatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop6PFJetAnalyzer
                                                    )

akPuSoftDrop6PFJetSequence_jec = cms.Sequence(akPuSoftDrop6PFJetSequence_mc)
akPuSoftDrop6PFJetSequence_mb = cms.Sequence(akPuSoftDrop6PFJetSequence_mc)

akPuSoftDrop6PFJetSequence = cms.Sequence(akPuSoftDrop6PFJetSequence_mc)
