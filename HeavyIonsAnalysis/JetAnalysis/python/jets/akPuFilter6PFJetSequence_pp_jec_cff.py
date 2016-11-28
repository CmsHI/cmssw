

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter6PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter6PFJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akPuFilter6PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter6GenJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akPuFilter6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter6PFJets")
                                                        )

akPuFilter6PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter6PFJets"),
    payload = "AKPu6PF_offline"
    )

akPuFilter6PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter6CaloJets'))

#akPuFilter6PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6GenJets'))

akPuFilter6PFbTagger = bTaggers("akPuFilter6PF",0.6)

#create objects locally since they dont load properly otherwise
#akPuFilter6PFmatch = akPuFilter6PFbTagger.match
akPuFilter6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter6PFJets"), matched = cms.InputTag("genParticles"))
akPuFilter6PFPatJetFlavourAssociationLegacy = akPuFilter6PFbTagger.PatJetFlavourAssociationLegacy
akPuFilter6PFPatJetPartons = akPuFilter6PFbTagger.PatJetPartons
akPuFilter6PFJetTracksAssociatorAtVertex = akPuFilter6PFbTagger.JetTracksAssociatorAtVertex
akPuFilter6PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter6PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter6PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter6PFCombinedSecondaryVertexBJetTags = akPuFilter6PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter6PFCombinedSecondaryVertexV2BJetTags = akPuFilter6PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter6PFJetBProbabilityBJetTags = akPuFilter6PFbTagger.JetBProbabilityBJetTags
akPuFilter6PFSoftPFMuonByPtBJetTags = akPuFilter6PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter6PFSoftPFMuonByIP3dBJetTags = akPuFilter6PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter6PFTrackCountingHighEffBJetTags = akPuFilter6PFbTagger.TrackCountingHighEffBJetTags
akPuFilter6PFTrackCountingHighPurBJetTags = akPuFilter6PFbTagger.TrackCountingHighPurBJetTags
akPuFilter6PFPatJetPartonAssociationLegacy = akPuFilter6PFbTagger.PatJetPartonAssociationLegacy

akPuFilter6PFImpactParameterTagInfos = akPuFilter6PFbTagger.ImpactParameterTagInfos
akPuFilter6PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter6PFJetProbabilityBJetTags = akPuFilter6PFbTagger.JetProbabilityBJetTags

akPuFilter6PFSecondaryVertexTagInfos = akPuFilter6PFbTagger.SecondaryVertexTagInfos
akPuFilter6PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter6PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter6PFCombinedSecondaryVertexBJetTags = akPuFilter6PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter6PFCombinedSecondaryVertexV2BJetTags = akPuFilter6PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter6PFSecondaryVertexNegativeTagInfos = akPuFilter6PFbTagger.SecondaryVertexNegativeTagInfos
akPuFilter6PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter6PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter6PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter6PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter6PFNegativeCombinedSecondaryVertexBJetTags = akPuFilter6PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter6PFPositiveCombinedSecondaryVertexBJetTags = akPuFilter6PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter6PFNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter6PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter6PFPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter6PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter6PFSoftPFMuonsTagInfos = akPuFilter6PFbTagger.SoftPFMuonsTagInfos
akPuFilter6PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter6PFSoftPFMuonBJetTags = akPuFilter6PFbTagger.SoftPFMuonBJetTags
akPuFilter6PFSoftPFMuonByIP3dBJetTags = akPuFilter6PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter6PFSoftPFMuonByPtBJetTags = akPuFilter6PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter6PFNegativeSoftPFMuonByPtBJetTags = akPuFilter6PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter6PFPositiveSoftPFMuonByPtBJetTags = akPuFilter6PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter6PFPatJetFlavourIdLegacy = cms.Sequence(akPuFilter6PFPatJetPartonAssociationLegacy*akPuFilter6PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter6PFPatJetFlavourAssociation = akPuFilter6PFbTagger.PatJetFlavourAssociation
#akPuFilter6PFPatJetFlavourId = cms.Sequence(akPuFilter6PFPatJetPartons*akPuFilter6PFPatJetFlavourAssociation)

akPuFilter6PFJetBtaggingIP       = cms.Sequence(akPuFilter6PFImpactParameterTagInfos *
            (akPuFilter6PFTrackCountingHighEffBJetTags +
             akPuFilter6PFTrackCountingHighPurBJetTags +
             akPuFilter6PFJetProbabilityBJetTags +
             akPuFilter6PFJetBProbabilityBJetTags 
            )
            )

akPuFilter6PFJetBtaggingSV = cms.Sequence(akPuFilter6PFImpactParameterTagInfos
            *
            akPuFilter6PFSecondaryVertexTagInfos
            * (akPuFilter6PFSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter6PFSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter6PFCombinedSecondaryVertexBJetTags+
                akPuFilter6PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter6PFJetBtaggingNegSV = cms.Sequence(akPuFilter6PFImpactParameterTagInfos
            *
            akPuFilter6PFSecondaryVertexNegativeTagInfos
            * (akPuFilter6PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter6PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter6PFNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter6PFPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter6PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter6PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter6PFJetBtaggingMu = cms.Sequence(akPuFilter6PFSoftPFMuonsTagInfos * (akPuFilter6PFSoftPFMuonBJetTags
                +
                akPuFilter6PFSoftPFMuonByIP3dBJetTags
                +
                akPuFilter6PFSoftPFMuonByPtBJetTags
                +
                akPuFilter6PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter6PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter6PFJetBtagging = cms.Sequence(akPuFilter6PFJetBtaggingIP
            *akPuFilter6PFJetBtaggingSV
            *akPuFilter6PFJetBtaggingNegSV
#            *akPuFilter6PFJetBtaggingMu
            )

akPuFilter6PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter6PFJets"),
        genJetMatch          = cms.InputTag("akPuFilter6PFmatch"),
        genPartonMatch       = cms.InputTag("akPuFilter6PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter6PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter6PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter6PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter6PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter6PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter6PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter6PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter6PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter6PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter6PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter6PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter6PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter6PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter6PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter6PFJetID"),
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

akPuFilter6PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter6PFJets"),
           	    R0  = cms.double( 0.6)
)
akPuFilter6PFpatJetsWithBtagging.userData.userFloats.src += ['akPuFilter6PFNjettiness:tau1','akPuFilter6PFNjettiness:tau2','akPuFilter6PFNjettiness:tau3']

akPuFilter6PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter6PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuFilter6PF"),
                                                             jetName = cms.untracked.string("akPuFilter6PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter6GenJets"),
                                                             doGenTaus = True
                                                             )

akPuFilter6PFJetSequence_mc = cms.Sequence(
                                                  #akPuFilter6PFclean
                                                  #*
                                                  akPuFilter6PFmatch
                                                  #*
                                                  #akPuFilter6PFmatchGroomed
                                                  *
                                                  akPuFilter6PFparton
                                                  *
                                                  akPuFilter6PFcorr
                                                  *
                                                  #akPuFilter6PFJetID
                                                  #*
                                                  akPuFilter6PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter6PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter6PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter6PFJetBtagging
                                                  *
                                                  akPuFilter6PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter6PFpatJetsWithBtagging
                                                  *
                                                  akPuFilter6PFJetAnalyzer
                                                  )

akPuFilter6PFJetSequence_data = cms.Sequence(akPuFilter6PFcorr
                                                    *
                                                    #akPuFilter6PFJetID
                                                    #*
                                                    akPuFilter6PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter6PFJetBtagging
                                                    *
                                                    akPuFilter6PFNjettiness 
                                                    *
                                                    akPuFilter6PFpatJetsWithBtagging
                                                    *
                                                    akPuFilter6PFJetAnalyzer
                                                    )

akPuFilter6PFJetSequence_jec = cms.Sequence(akPuFilter6PFJetSequence_mc)
akPuFilter6PFJetSequence_mb = cms.Sequence(akPuFilter6PFJetSequence_mc)

akPuFilter6PFJetSequence = cms.Sequence(akPuFilter6PFJetSequence_jec)
akPuFilter6PFJetAnalyzer.genPtMin = cms.untracked.double(1)
akPuFilter6PFJetAnalyzer.jetPtMin = cms.double(1)
