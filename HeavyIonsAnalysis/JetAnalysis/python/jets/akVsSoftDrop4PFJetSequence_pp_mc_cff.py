

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop4PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop4PFJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.4
    )

akVsSoftDrop4PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop4GenJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.4
    )

akVsSoftDrop4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop4PFJets")
                                                        )

akVsSoftDrop4PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop4PFJets"),
    payload = "AK4PF_offline"
    )

akVsSoftDrop4PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop4CaloJets'))

#akVsSoftDrop4PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4GenJets'))

akVsSoftDrop4PFbTagger = bTaggers("akVsSoftDrop4PF",0.4)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop4PFmatch = akVsSoftDrop4PFbTagger.match
akVsSoftDrop4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop4PFJets"), matched = cms.InputTag("genParticles"))
akVsSoftDrop4PFPatJetFlavourAssociationLegacy = akVsSoftDrop4PFbTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop4PFPatJetPartons = akVsSoftDrop4PFbTagger.PatJetPartons
akVsSoftDrop4PFJetTracksAssociatorAtVertex = akVsSoftDrop4PFbTagger.JetTracksAssociatorAtVertex
akVsSoftDrop4PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop4PFCombinedSecondaryVertexBJetTags = akVsSoftDrop4PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop4PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop4PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop4PFJetBProbabilityBJetTags = akVsSoftDrop4PFbTagger.JetBProbabilityBJetTags
akVsSoftDrop4PFSoftPFMuonByPtBJetTags = akVsSoftDrop4PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop4PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop4PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop4PFTrackCountingHighEffBJetTags = akVsSoftDrop4PFbTagger.TrackCountingHighEffBJetTags
akVsSoftDrop4PFTrackCountingHighPurBJetTags = akVsSoftDrop4PFbTagger.TrackCountingHighPurBJetTags
akVsSoftDrop4PFPatJetPartonAssociationLegacy = akVsSoftDrop4PFbTagger.PatJetPartonAssociationLegacy

akVsSoftDrop4PFImpactParameterTagInfos = akVsSoftDrop4PFbTagger.ImpactParameterTagInfos
akVsSoftDrop4PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop4PFJetProbabilityBJetTags = akVsSoftDrop4PFbTagger.JetProbabilityBJetTags

akVsSoftDrop4PFSecondaryVertexTagInfos = akVsSoftDrop4PFbTagger.SecondaryVertexTagInfos
akVsSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop4PFCombinedSecondaryVertexBJetTags = akVsSoftDrop4PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop4PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop4PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop4PFSecondaryVertexNegativeTagInfos = akVsSoftDrop4PFbTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop4PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop4PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop4PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop4PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop4PFNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop4PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop4PFPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop4PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop4PFNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop4PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop4PFPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop4PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop4PFSoftPFMuonsTagInfos = akVsSoftDrop4PFbTagger.SoftPFMuonsTagInfos
akVsSoftDrop4PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop4PFSoftPFMuonBJetTags = akVsSoftDrop4PFbTagger.SoftPFMuonBJetTags
akVsSoftDrop4PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop4PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop4PFSoftPFMuonByPtBJetTags = akVsSoftDrop4PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop4PFNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop4PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop4PFPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop4PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop4PFPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop4PFPatJetPartonAssociationLegacy*akVsSoftDrop4PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop4PFPatJetFlavourAssociation = akVsSoftDrop4PFbTagger.PatJetFlavourAssociation
#akVsSoftDrop4PFPatJetFlavourId = cms.Sequence(akVsSoftDrop4PFPatJetPartons*akVsSoftDrop4PFPatJetFlavourAssociation)

akVsSoftDrop4PFJetBtaggingIP       = cms.Sequence(akVsSoftDrop4PFImpactParameterTagInfos *
            (akVsSoftDrop4PFTrackCountingHighEffBJetTags +
             akVsSoftDrop4PFTrackCountingHighPurBJetTags +
             akVsSoftDrop4PFJetProbabilityBJetTags +
             akVsSoftDrop4PFJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop4PFJetBtaggingSV = cms.Sequence(akVsSoftDrop4PFImpactParameterTagInfos
            *
            akVsSoftDrop4PFSecondaryVertexTagInfos
            * (akVsSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop4PFCombinedSecondaryVertexBJetTags+
                akVsSoftDrop4PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop4PFJetBtaggingNegSV = cms.Sequence(akVsSoftDrop4PFImpactParameterTagInfos
            *
            akVsSoftDrop4PFSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop4PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop4PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop4PFNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop4PFPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop4PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop4PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop4PFJetBtaggingMu = cms.Sequence(akVsSoftDrop4PFSoftPFMuonsTagInfos * (akVsSoftDrop4PFSoftPFMuonBJetTags
                +
                akVsSoftDrop4PFSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop4PFSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop4PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop4PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop4PFJetBtagging = cms.Sequence(akVsSoftDrop4PFJetBtaggingIP
            *akVsSoftDrop4PFJetBtaggingSV
            *akVsSoftDrop4PFJetBtaggingNegSV
#            *akVsSoftDrop4PFJetBtaggingMu
            )

akVsSoftDrop4PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop4PFJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop4PFmatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop4PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop4PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop4PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop4PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop4PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop4PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop4PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop4PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop4PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop4PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop4PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop4PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop4PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop4PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop4PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop4PFJetID"),
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

akVsSoftDrop4PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop4PFJets"),
           	    R0  = cms.double( 0.4)
)
akVsSoftDrop4PFpatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop4PFNjettiness:tau1','akVsSoftDrop4PFNjettiness:tau2','akVsSoftDrop4PFNjettiness:tau3']

akVsSoftDrop4PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop4PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak4GenJets',
                                                             rParam = 0.4,
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop4PF"),
                                                             jetName = cms.untracked.string("akVsSoftDrop4PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(True),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop4GenJets"),
                                                             doGenTaus = True
                                                             )

akVsSoftDrop4PFJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop4PFclean
                                                  #*
                                                  akVsSoftDrop4PFmatch
                                                  #*
                                                  #akVsSoftDrop4PFmatchGroomed
                                                  *
                                                  akVsSoftDrop4PFparton
                                                  *
                                                  akVsSoftDrop4PFcorr
                                                  *
                                                  #akVsSoftDrop4PFJetID
                                                  #*
                                                  akVsSoftDrop4PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop4PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop4PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop4PFJetBtagging
                                                  *
                                                  akVsSoftDrop4PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop4PFpatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop4PFJetAnalyzer
                                                  )

akVsSoftDrop4PFJetSequence_data = cms.Sequence(akVsSoftDrop4PFcorr
                                                    *
                                                    #akVsSoftDrop4PFJetID
                                                    #*
                                                    akVsSoftDrop4PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop4PFJetBtagging
                                                    *
                                                    akVsSoftDrop4PFNjettiness 
                                                    *
                                                    akVsSoftDrop4PFpatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop4PFJetAnalyzer
                                                    )

akVsSoftDrop4PFJetSequence_jec = cms.Sequence(akVsSoftDrop4PFJetSequence_mc)
akVsSoftDrop4PFJetSequence_mb = cms.Sequence(akVsSoftDrop4PFJetSequence_mc)

akVsSoftDrop4PFJetSequence = cms.Sequence(akVsSoftDrop4PFJetSequence_mc)
