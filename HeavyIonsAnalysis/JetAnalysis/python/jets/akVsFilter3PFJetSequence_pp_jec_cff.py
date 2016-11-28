

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter3PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter3PFJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.3
    )

akVsFilter3PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter3GenJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.3
    )

akVsFilter3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter3PFJets")
                                                        )

akVsFilter3PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter3PFJets"),
    payload = "AK3PF_offline"
    )

akVsFilter3PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter3CaloJets'))

#akVsFilter3PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3GenJets'))

akVsFilter3PFbTagger = bTaggers("akVsFilter3PF",0.3)

#create objects locally since they dont load properly otherwise
#akVsFilter3PFmatch = akVsFilter3PFbTagger.match
akVsFilter3PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter3PFJets"), matched = cms.InputTag("genParticles"))
akVsFilter3PFPatJetFlavourAssociationLegacy = akVsFilter3PFbTagger.PatJetFlavourAssociationLegacy
akVsFilter3PFPatJetPartons = akVsFilter3PFbTagger.PatJetPartons
akVsFilter3PFJetTracksAssociatorAtVertex = akVsFilter3PFbTagger.JetTracksAssociatorAtVertex
akVsFilter3PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter3PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter3PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter3PFCombinedSecondaryVertexBJetTags = akVsFilter3PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter3PFCombinedSecondaryVertexV2BJetTags = akVsFilter3PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter3PFJetBProbabilityBJetTags = akVsFilter3PFbTagger.JetBProbabilityBJetTags
akVsFilter3PFSoftPFMuonByPtBJetTags = akVsFilter3PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter3PFSoftPFMuonByIP3dBJetTags = akVsFilter3PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter3PFTrackCountingHighEffBJetTags = akVsFilter3PFbTagger.TrackCountingHighEffBJetTags
akVsFilter3PFTrackCountingHighPurBJetTags = akVsFilter3PFbTagger.TrackCountingHighPurBJetTags
akVsFilter3PFPatJetPartonAssociationLegacy = akVsFilter3PFbTagger.PatJetPartonAssociationLegacy

akVsFilter3PFImpactParameterTagInfos = akVsFilter3PFbTagger.ImpactParameterTagInfos
akVsFilter3PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter3PFJetProbabilityBJetTags = akVsFilter3PFbTagger.JetProbabilityBJetTags

akVsFilter3PFSecondaryVertexTagInfos = akVsFilter3PFbTagger.SecondaryVertexTagInfos
akVsFilter3PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter3PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter3PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter3PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter3PFCombinedSecondaryVertexBJetTags = akVsFilter3PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter3PFCombinedSecondaryVertexV2BJetTags = akVsFilter3PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter3PFSecondaryVertexNegativeTagInfos = akVsFilter3PFbTagger.SecondaryVertexNegativeTagInfos
akVsFilter3PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter3PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter3PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter3PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter3PFNegativeCombinedSecondaryVertexBJetTags = akVsFilter3PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter3PFPositiveCombinedSecondaryVertexBJetTags = akVsFilter3PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter3PFNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter3PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter3PFPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter3PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter3PFSoftPFMuonsTagInfos = akVsFilter3PFbTagger.SoftPFMuonsTagInfos
akVsFilter3PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter3PFSoftPFMuonBJetTags = akVsFilter3PFbTagger.SoftPFMuonBJetTags
akVsFilter3PFSoftPFMuonByIP3dBJetTags = akVsFilter3PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter3PFSoftPFMuonByPtBJetTags = akVsFilter3PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter3PFNegativeSoftPFMuonByPtBJetTags = akVsFilter3PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter3PFPositiveSoftPFMuonByPtBJetTags = akVsFilter3PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter3PFPatJetFlavourIdLegacy = cms.Sequence(akVsFilter3PFPatJetPartonAssociationLegacy*akVsFilter3PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter3PFPatJetFlavourAssociation = akVsFilter3PFbTagger.PatJetFlavourAssociation
#akVsFilter3PFPatJetFlavourId = cms.Sequence(akVsFilter3PFPatJetPartons*akVsFilter3PFPatJetFlavourAssociation)

akVsFilter3PFJetBtaggingIP       = cms.Sequence(akVsFilter3PFImpactParameterTagInfos *
            (akVsFilter3PFTrackCountingHighEffBJetTags +
             akVsFilter3PFTrackCountingHighPurBJetTags +
             akVsFilter3PFJetProbabilityBJetTags +
             akVsFilter3PFJetBProbabilityBJetTags 
            )
            )

akVsFilter3PFJetBtaggingSV = cms.Sequence(akVsFilter3PFImpactParameterTagInfos
            *
            akVsFilter3PFSecondaryVertexTagInfos
            * (akVsFilter3PFSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter3PFSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter3PFCombinedSecondaryVertexBJetTags+
                akVsFilter3PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter3PFJetBtaggingNegSV = cms.Sequence(akVsFilter3PFImpactParameterTagInfos
            *
            akVsFilter3PFSecondaryVertexNegativeTagInfos
            * (akVsFilter3PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter3PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter3PFNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter3PFPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter3PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter3PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter3PFJetBtaggingMu = cms.Sequence(akVsFilter3PFSoftPFMuonsTagInfos * (akVsFilter3PFSoftPFMuonBJetTags
                +
                akVsFilter3PFSoftPFMuonByIP3dBJetTags
                +
                akVsFilter3PFSoftPFMuonByPtBJetTags
                +
                akVsFilter3PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter3PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter3PFJetBtagging = cms.Sequence(akVsFilter3PFJetBtaggingIP
            *akVsFilter3PFJetBtaggingSV
            *akVsFilter3PFJetBtaggingNegSV
#            *akVsFilter3PFJetBtaggingMu
            )

akVsFilter3PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter3PFJets"),
        genJetMatch          = cms.InputTag("akVsFilter3PFmatch"),
        genPartonMatch       = cms.InputTag("akVsFilter3PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter3PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter3PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter3PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter3PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter3PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter3PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter3PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter3PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter3PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter3PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter3PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter3PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter3PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter3PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter3PFJetID"),
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

akVsFilter3PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter3PFJets"),
           	    R0  = cms.double( 0.3)
)
akVsFilter3PFpatJetsWithBtagging.userData.userFloats.src += ['akVsFilter3PFNjettiness:tau1','akVsFilter3PFNjettiness:tau2','akVsFilter3PFNjettiness:tau3']

akVsFilter3PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter3PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akVsFilter3PF"),
                                                             jetName = cms.untracked.string("akVsFilter3PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter3GenJets"),
                                                             doGenTaus = True
                                                             )

akVsFilter3PFJetSequence_mc = cms.Sequence(
                                                  #akVsFilter3PFclean
                                                  #*
                                                  akVsFilter3PFmatch
                                                  #*
                                                  #akVsFilter3PFmatchGroomed
                                                  *
                                                  akVsFilter3PFparton
                                                  *
                                                  akVsFilter3PFcorr
                                                  *
                                                  #akVsFilter3PFJetID
                                                  #*
                                                  akVsFilter3PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter3PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter3PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter3PFJetBtagging
                                                  *
                                                  akVsFilter3PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter3PFpatJetsWithBtagging
                                                  *
                                                  akVsFilter3PFJetAnalyzer
                                                  )

akVsFilter3PFJetSequence_data = cms.Sequence(akVsFilter3PFcorr
                                                    *
                                                    #akVsFilter3PFJetID
                                                    #*
                                                    akVsFilter3PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter3PFJetBtagging
                                                    *
                                                    akVsFilter3PFNjettiness 
                                                    *
                                                    akVsFilter3PFpatJetsWithBtagging
                                                    *
                                                    akVsFilter3PFJetAnalyzer
                                                    )

akVsFilter3PFJetSequence_jec = cms.Sequence(akVsFilter3PFJetSequence_mc)
akVsFilter3PFJetSequence_mb = cms.Sequence(akVsFilter3PFJetSequence_mc)

akVsFilter3PFJetSequence = cms.Sequence(akVsFilter3PFJetSequence_jec)
akVsFilter3PFJetAnalyzer.genPtMin = cms.untracked.double(1)
akVsFilter3PFJetAnalyzer.jetPtMin = cms.double(1)
