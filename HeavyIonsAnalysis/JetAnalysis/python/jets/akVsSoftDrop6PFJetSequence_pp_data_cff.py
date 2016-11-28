

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop6PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop6PFJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.6
    )

akVsSoftDrop6PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop6GenJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.6
    )

akVsSoftDrop6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop6PFJets")
                                                        )

akVsSoftDrop6PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop6PFJets"),
    payload = "AK6PF_offline"
    )

akVsSoftDrop6PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop6CaloJets'))

#akVsSoftDrop6PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6GenJets'))

akVsSoftDrop6PFbTagger = bTaggers("akVsSoftDrop6PF",0.6)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop6PFmatch = akVsSoftDrop6PFbTagger.match
akVsSoftDrop6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop6PFJets"), matched = cms.InputTag("genParticles"))
akVsSoftDrop6PFPatJetFlavourAssociationLegacy = akVsSoftDrop6PFbTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop6PFPatJetPartons = akVsSoftDrop6PFbTagger.PatJetPartons
akVsSoftDrop6PFJetTracksAssociatorAtVertex = akVsSoftDrop6PFbTagger.JetTracksAssociatorAtVertex
akVsSoftDrop6PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop6PFCombinedSecondaryVertexBJetTags = akVsSoftDrop6PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop6PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop6PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop6PFJetBProbabilityBJetTags = akVsSoftDrop6PFbTagger.JetBProbabilityBJetTags
akVsSoftDrop6PFSoftPFMuonByPtBJetTags = akVsSoftDrop6PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop6PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop6PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop6PFTrackCountingHighEffBJetTags = akVsSoftDrop6PFbTagger.TrackCountingHighEffBJetTags
akVsSoftDrop6PFTrackCountingHighPurBJetTags = akVsSoftDrop6PFbTagger.TrackCountingHighPurBJetTags
akVsSoftDrop6PFPatJetPartonAssociationLegacy = akVsSoftDrop6PFbTagger.PatJetPartonAssociationLegacy

akVsSoftDrop6PFImpactParameterTagInfos = akVsSoftDrop6PFbTagger.ImpactParameterTagInfos
akVsSoftDrop6PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop6PFJetProbabilityBJetTags = akVsSoftDrop6PFbTagger.JetProbabilityBJetTags

akVsSoftDrop6PFSecondaryVertexTagInfos = akVsSoftDrop6PFbTagger.SecondaryVertexTagInfos
akVsSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop6PFCombinedSecondaryVertexBJetTags = akVsSoftDrop6PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop6PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop6PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop6PFSecondaryVertexNegativeTagInfos = akVsSoftDrop6PFbTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop6PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop6PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop6PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop6PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop6PFNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop6PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop6PFPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop6PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop6PFNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop6PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop6PFPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop6PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop6PFSoftPFMuonsTagInfos = akVsSoftDrop6PFbTagger.SoftPFMuonsTagInfos
akVsSoftDrop6PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop6PFSoftPFMuonBJetTags = akVsSoftDrop6PFbTagger.SoftPFMuonBJetTags
akVsSoftDrop6PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop6PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop6PFSoftPFMuonByPtBJetTags = akVsSoftDrop6PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop6PFNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop6PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop6PFPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop6PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop6PFPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop6PFPatJetPartonAssociationLegacy*akVsSoftDrop6PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop6PFPatJetFlavourAssociation = akVsSoftDrop6PFbTagger.PatJetFlavourAssociation
#akVsSoftDrop6PFPatJetFlavourId = cms.Sequence(akVsSoftDrop6PFPatJetPartons*akVsSoftDrop6PFPatJetFlavourAssociation)

akVsSoftDrop6PFJetBtaggingIP       = cms.Sequence(akVsSoftDrop6PFImpactParameterTagInfos *
            (akVsSoftDrop6PFTrackCountingHighEffBJetTags +
             akVsSoftDrop6PFTrackCountingHighPurBJetTags +
             akVsSoftDrop6PFJetProbabilityBJetTags +
             akVsSoftDrop6PFJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop6PFJetBtaggingSV = cms.Sequence(akVsSoftDrop6PFImpactParameterTagInfos
            *
            akVsSoftDrop6PFSecondaryVertexTagInfos
            * (akVsSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop6PFCombinedSecondaryVertexBJetTags+
                akVsSoftDrop6PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop6PFJetBtaggingNegSV = cms.Sequence(akVsSoftDrop6PFImpactParameterTagInfos
            *
            akVsSoftDrop6PFSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop6PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop6PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop6PFNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop6PFPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop6PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop6PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop6PFJetBtaggingMu = cms.Sequence(akVsSoftDrop6PFSoftPFMuonsTagInfos * (akVsSoftDrop6PFSoftPFMuonBJetTags
                +
                akVsSoftDrop6PFSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop6PFSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop6PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop6PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop6PFJetBtagging = cms.Sequence(akVsSoftDrop6PFJetBtaggingIP
            *akVsSoftDrop6PFJetBtaggingSV
            *akVsSoftDrop6PFJetBtaggingNegSV
#            *akVsSoftDrop6PFJetBtaggingMu
            )

akVsSoftDrop6PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop6PFJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop6PFmatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop6PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop6PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop6PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop6PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop6PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop6PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop6PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop6PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop6PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop6PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop6PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop6PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop6PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop6PFJetID"),
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

akVsSoftDrop6PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop6PFJets"),
           	    R0  = cms.double( 0.6)
)
akVsSoftDrop6PFpatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop6PFNjettiness:tau1','akVsSoftDrop6PFNjettiness:tau2','akVsSoftDrop6PFNjettiness:tau3']

akVsSoftDrop6PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop6PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak6GenJets',
                                                             rParam = 0.6,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlow'),
                                                             trackTag = cms.InputTag("generalTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
							     doSubEvent = False,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop6PF"),
                                                             jetName = cms.untracked.string("akVsSoftDrop6PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop6GenJets"),
                                                             doGenTaus = False
                                                             )

akVsSoftDrop6PFJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop6PFclean
                                                  #*
                                                  akVsSoftDrop6PFmatch
                                                  #*
                                                  #akVsSoftDrop6PFmatchGroomed
                                                  *
                                                  akVsSoftDrop6PFparton
                                                  *
                                                  akVsSoftDrop6PFcorr
                                                  *
                                                  #akVsSoftDrop6PFJetID
                                                  #*
                                                  akVsSoftDrop6PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop6PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop6PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop6PFJetBtagging
                                                  *
                                                  akVsSoftDrop6PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop6PFpatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop6PFJetAnalyzer
                                                  )

akVsSoftDrop6PFJetSequence_data = cms.Sequence(akVsSoftDrop6PFcorr
                                                    *
                                                    #akVsSoftDrop6PFJetID
                                                    #*
                                                    akVsSoftDrop6PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop6PFJetBtagging
                                                    *
                                                    akVsSoftDrop6PFNjettiness 
                                                    *
                                                    akVsSoftDrop6PFpatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop6PFJetAnalyzer
                                                    )

akVsSoftDrop6PFJetSequence_jec = cms.Sequence(akVsSoftDrop6PFJetSequence_mc)
akVsSoftDrop6PFJetSequence_mb = cms.Sequence(akVsSoftDrop6PFJetSequence_mc)

akVsSoftDrop6PFJetSequence = cms.Sequence(akVsSoftDrop6PFJetSequence_data)
