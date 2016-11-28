

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter5PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter5PFJets"),
    matched = cms.InputTag("ak5GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akPuFilter5PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter5GenJets"),
    matched = cms.InputTag("ak5GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akPuFilter5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter5PFJets")
                                                        )

akPuFilter5PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter5PFJets"),
    payload = "AKPu5PF_offline"
    )

akPuFilter5PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter5CaloJets'))

#akPuFilter5PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5GenJets'))

akPuFilter5PFbTagger = bTaggers("akPuFilter5PF",0.5)

#create objects locally since they dont load properly otherwise
#akPuFilter5PFmatch = akPuFilter5PFbTagger.match
akPuFilter5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter5PFJets"), matched = cms.InputTag("genParticles"))
akPuFilter5PFPatJetFlavourAssociationLegacy = akPuFilter5PFbTagger.PatJetFlavourAssociationLegacy
akPuFilter5PFPatJetPartons = akPuFilter5PFbTagger.PatJetPartons
akPuFilter5PFJetTracksAssociatorAtVertex = akPuFilter5PFbTagger.JetTracksAssociatorAtVertex
akPuFilter5PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter5PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter5PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter5PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter5PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter5PFCombinedSecondaryVertexBJetTags = akPuFilter5PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter5PFCombinedSecondaryVertexV2BJetTags = akPuFilter5PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter5PFJetBProbabilityBJetTags = akPuFilter5PFbTagger.JetBProbabilityBJetTags
akPuFilter5PFSoftPFMuonByPtBJetTags = akPuFilter5PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter5PFSoftPFMuonByIP3dBJetTags = akPuFilter5PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter5PFTrackCountingHighEffBJetTags = akPuFilter5PFbTagger.TrackCountingHighEffBJetTags
akPuFilter5PFTrackCountingHighPurBJetTags = akPuFilter5PFbTagger.TrackCountingHighPurBJetTags
akPuFilter5PFPatJetPartonAssociationLegacy = akPuFilter5PFbTagger.PatJetPartonAssociationLegacy

akPuFilter5PFImpactParameterTagInfos = akPuFilter5PFbTagger.ImpactParameterTagInfos
akPuFilter5PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter5PFJetProbabilityBJetTags = akPuFilter5PFbTagger.JetProbabilityBJetTags

akPuFilter5PFSecondaryVertexTagInfos = akPuFilter5PFbTagger.SecondaryVertexTagInfos
akPuFilter5PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter5PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter5PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter5PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter5PFCombinedSecondaryVertexBJetTags = akPuFilter5PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter5PFCombinedSecondaryVertexV2BJetTags = akPuFilter5PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter5PFSecondaryVertexNegativeTagInfos = akPuFilter5PFbTagger.SecondaryVertexNegativeTagInfos
akPuFilter5PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter5PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter5PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter5PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter5PFNegativeCombinedSecondaryVertexBJetTags = akPuFilter5PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter5PFPositiveCombinedSecondaryVertexBJetTags = akPuFilter5PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter5PFNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter5PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter5PFPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter5PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter5PFSoftPFMuonsTagInfos = akPuFilter5PFbTagger.SoftPFMuonsTagInfos
akPuFilter5PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter5PFSoftPFMuonBJetTags = akPuFilter5PFbTagger.SoftPFMuonBJetTags
akPuFilter5PFSoftPFMuonByIP3dBJetTags = akPuFilter5PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter5PFSoftPFMuonByPtBJetTags = akPuFilter5PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter5PFNegativeSoftPFMuonByPtBJetTags = akPuFilter5PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter5PFPositiveSoftPFMuonByPtBJetTags = akPuFilter5PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter5PFPatJetFlavourIdLegacy = cms.Sequence(akPuFilter5PFPatJetPartonAssociationLegacy*akPuFilter5PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter5PFPatJetFlavourAssociation = akPuFilter5PFbTagger.PatJetFlavourAssociation
#akPuFilter5PFPatJetFlavourId = cms.Sequence(akPuFilter5PFPatJetPartons*akPuFilter5PFPatJetFlavourAssociation)

akPuFilter5PFJetBtaggingIP       = cms.Sequence(akPuFilter5PFImpactParameterTagInfos *
            (akPuFilter5PFTrackCountingHighEffBJetTags +
             akPuFilter5PFTrackCountingHighPurBJetTags +
             akPuFilter5PFJetProbabilityBJetTags +
             akPuFilter5PFJetBProbabilityBJetTags 
            )
            )

akPuFilter5PFJetBtaggingSV = cms.Sequence(akPuFilter5PFImpactParameterTagInfos
            *
            akPuFilter5PFSecondaryVertexTagInfos
            * (akPuFilter5PFSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter5PFSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter5PFCombinedSecondaryVertexBJetTags+
                akPuFilter5PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter5PFJetBtaggingNegSV = cms.Sequence(akPuFilter5PFImpactParameterTagInfos
            *
            akPuFilter5PFSecondaryVertexNegativeTagInfos
            * (akPuFilter5PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter5PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter5PFNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter5PFPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter5PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter5PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter5PFJetBtaggingMu = cms.Sequence(akPuFilter5PFSoftPFMuonsTagInfos * (akPuFilter5PFSoftPFMuonBJetTags
                +
                akPuFilter5PFSoftPFMuonByIP3dBJetTags
                +
                akPuFilter5PFSoftPFMuonByPtBJetTags
                +
                akPuFilter5PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter5PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter5PFJetBtagging = cms.Sequence(akPuFilter5PFJetBtaggingIP
            *akPuFilter5PFJetBtaggingSV
            *akPuFilter5PFJetBtaggingNegSV
#            *akPuFilter5PFJetBtaggingMu
            )

akPuFilter5PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter5PFJets"),
        genJetMatch          = cms.InputTag("akPuFilter5PFmatch"),
        genPartonMatch       = cms.InputTag("akPuFilter5PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter5PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter5PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter5PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter5PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter5PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter5PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter5PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter5PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter5PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter5PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter5PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter5PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter5PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter5PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter5PFJetID"),
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

akPuFilter5PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter5PFJets"),
           	    R0  = cms.double( 0.5)
)
akPuFilter5PFpatJetsWithBtagging.userData.userFloats.src += ['akPuFilter5PFNjettiness:tau1','akPuFilter5PFNjettiness:tau2','akPuFilter5PFNjettiness:tau3']

akPuFilter5PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter5PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak5GenJets',
                                                             rParam = 0.5,
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
                                                             bTagJetName = cms.untracked.string("akPuFilter5PF"),
                                                             jetName = cms.untracked.string("akPuFilter5PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter5GenJets"),
                                                             doGenTaus = False
                                                             )

akPuFilter5PFJetSequence_mc = cms.Sequence(
                                                  #akPuFilter5PFclean
                                                  #*
                                                  akPuFilter5PFmatch
                                                  #*
                                                  #akPuFilter5PFmatchGroomed
                                                  *
                                                  akPuFilter5PFparton
                                                  *
                                                  akPuFilter5PFcorr
                                                  *
                                                  #akPuFilter5PFJetID
                                                  #*
                                                  akPuFilter5PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter5PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter5PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter5PFJetBtagging
                                                  *
                                                  akPuFilter5PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter5PFpatJetsWithBtagging
                                                  *
                                                  akPuFilter5PFJetAnalyzer
                                                  )

akPuFilter5PFJetSequence_data = cms.Sequence(akPuFilter5PFcorr
                                                    *
                                                    #akPuFilter5PFJetID
                                                    #*
                                                    akPuFilter5PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter5PFJetBtagging
                                                    *
                                                    akPuFilter5PFNjettiness 
                                                    *
                                                    akPuFilter5PFpatJetsWithBtagging
                                                    *
                                                    akPuFilter5PFJetAnalyzer
                                                    )

akPuFilter5PFJetSequence_jec = cms.Sequence(akPuFilter5PFJetSequence_mc)
akPuFilter5PFJetSequence_mb = cms.Sequence(akPuFilter5PFJetSequence_mc)

akPuFilter5PFJetSequence = cms.Sequence(akPuFilter5PFJetSequence_data)
