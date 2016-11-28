

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter5PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter5PFJets"),
    matched = cms.InputTag("ak5GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.5
    )

akVsFilter5PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter5GenJets"),
    matched = cms.InputTag("ak5GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.5
    )

akVsFilter5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter5PFJets")
                                                        )

akVsFilter5PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter5PFJets"),
    payload = "AK5PF_offline"
    )

akVsFilter5PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter5CaloJets'))

#akVsFilter5PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5GenJets'))

akVsFilter5PFbTagger = bTaggers("akVsFilter5PF",0.5)

#create objects locally since they dont load properly otherwise
#akVsFilter5PFmatch = akVsFilter5PFbTagger.match
akVsFilter5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter5PFJets"), matched = cms.InputTag("genParticles"))
akVsFilter5PFPatJetFlavourAssociationLegacy = akVsFilter5PFbTagger.PatJetFlavourAssociationLegacy
akVsFilter5PFPatJetPartons = akVsFilter5PFbTagger.PatJetPartons
akVsFilter5PFJetTracksAssociatorAtVertex = akVsFilter5PFbTagger.JetTracksAssociatorAtVertex
akVsFilter5PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter5PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter5PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter5PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter5PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter5PFCombinedSecondaryVertexBJetTags = akVsFilter5PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter5PFCombinedSecondaryVertexV2BJetTags = akVsFilter5PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter5PFJetBProbabilityBJetTags = akVsFilter5PFbTagger.JetBProbabilityBJetTags
akVsFilter5PFSoftPFMuonByPtBJetTags = akVsFilter5PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter5PFSoftPFMuonByIP3dBJetTags = akVsFilter5PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter5PFTrackCountingHighEffBJetTags = akVsFilter5PFbTagger.TrackCountingHighEffBJetTags
akVsFilter5PFTrackCountingHighPurBJetTags = akVsFilter5PFbTagger.TrackCountingHighPurBJetTags
akVsFilter5PFPatJetPartonAssociationLegacy = akVsFilter5PFbTagger.PatJetPartonAssociationLegacy

akVsFilter5PFImpactParameterTagInfos = akVsFilter5PFbTagger.ImpactParameterTagInfos
akVsFilter5PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter5PFJetProbabilityBJetTags = akVsFilter5PFbTagger.JetProbabilityBJetTags

akVsFilter5PFSecondaryVertexTagInfos = akVsFilter5PFbTagger.SecondaryVertexTagInfos
akVsFilter5PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter5PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter5PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter5PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter5PFCombinedSecondaryVertexBJetTags = akVsFilter5PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter5PFCombinedSecondaryVertexV2BJetTags = akVsFilter5PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter5PFSecondaryVertexNegativeTagInfos = akVsFilter5PFbTagger.SecondaryVertexNegativeTagInfos
akVsFilter5PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter5PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter5PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter5PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter5PFNegativeCombinedSecondaryVertexBJetTags = akVsFilter5PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter5PFPositiveCombinedSecondaryVertexBJetTags = akVsFilter5PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter5PFNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter5PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter5PFPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter5PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter5PFSoftPFMuonsTagInfos = akVsFilter5PFbTagger.SoftPFMuonsTagInfos
akVsFilter5PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter5PFSoftPFMuonBJetTags = akVsFilter5PFbTagger.SoftPFMuonBJetTags
akVsFilter5PFSoftPFMuonByIP3dBJetTags = akVsFilter5PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter5PFSoftPFMuonByPtBJetTags = akVsFilter5PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter5PFNegativeSoftPFMuonByPtBJetTags = akVsFilter5PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter5PFPositiveSoftPFMuonByPtBJetTags = akVsFilter5PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter5PFPatJetFlavourIdLegacy = cms.Sequence(akVsFilter5PFPatJetPartonAssociationLegacy*akVsFilter5PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter5PFPatJetFlavourAssociation = akVsFilter5PFbTagger.PatJetFlavourAssociation
#akVsFilter5PFPatJetFlavourId = cms.Sequence(akVsFilter5PFPatJetPartons*akVsFilter5PFPatJetFlavourAssociation)

akVsFilter5PFJetBtaggingIP       = cms.Sequence(akVsFilter5PFImpactParameterTagInfos *
            (akVsFilter5PFTrackCountingHighEffBJetTags +
             akVsFilter5PFTrackCountingHighPurBJetTags +
             akVsFilter5PFJetProbabilityBJetTags +
             akVsFilter5PFJetBProbabilityBJetTags 
            )
            )

akVsFilter5PFJetBtaggingSV = cms.Sequence(akVsFilter5PFImpactParameterTagInfos
            *
            akVsFilter5PFSecondaryVertexTagInfos
            * (akVsFilter5PFSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter5PFSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter5PFCombinedSecondaryVertexBJetTags+
                akVsFilter5PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter5PFJetBtaggingNegSV = cms.Sequence(akVsFilter5PFImpactParameterTagInfos
            *
            akVsFilter5PFSecondaryVertexNegativeTagInfos
            * (akVsFilter5PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter5PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter5PFNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter5PFPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter5PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter5PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter5PFJetBtaggingMu = cms.Sequence(akVsFilter5PFSoftPFMuonsTagInfos * (akVsFilter5PFSoftPFMuonBJetTags
                +
                akVsFilter5PFSoftPFMuonByIP3dBJetTags
                +
                akVsFilter5PFSoftPFMuonByPtBJetTags
                +
                akVsFilter5PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter5PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter5PFJetBtagging = cms.Sequence(akVsFilter5PFJetBtaggingIP
            *akVsFilter5PFJetBtaggingSV
            *akVsFilter5PFJetBtaggingNegSV
#            *akVsFilter5PFJetBtaggingMu
            )

akVsFilter5PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter5PFJets"),
        genJetMatch          = cms.InputTag("akVsFilter5PFmatch"),
        genPartonMatch       = cms.InputTag("akVsFilter5PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter5PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter5PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter5PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter5PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter5PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter5PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter5PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter5PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter5PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter5PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter5PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter5PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter5PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter5PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter5PFJetID"),
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

akVsFilter5PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter5PFJets"),
           	    R0  = cms.double( 0.5)
)
akVsFilter5PFpatJetsWithBtagging.userData.userFloats.src += ['akVsFilter5PFNjettiness:tau1','akVsFilter5PFNjettiness:tau2','akVsFilter5PFNjettiness:tau3']

akVsFilter5PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter5PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akVsFilter5PF"),
                                                             jetName = cms.untracked.string("akVsFilter5PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter5GenJets"),
                                                             doGenTaus = False
                                                             )

akVsFilter5PFJetSequence_mc = cms.Sequence(
                                                  #akVsFilter5PFclean
                                                  #*
                                                  akVsFilter5PFmatch
                                                  #*
                                                  #akVsFilter5PFmatchGroomed
                                                  *
                                                  akVsFilter5PFparton
                                                  *
                                                  akVsFilter5PFcorr
                                                  *
                                                  #akVsFilter5PFJetID
                                                  #*
                                                  akVsFilter5PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter5PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter5PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter5PFJetBtagging
                                                  *
                                                  akVsFilter5PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter5PFpatJetsWithBtagging
                                                  *
                                                  akVsFilter5PFJetAnalyzer
                                                  )

akVsFilter5PFJetSequence_data = cms.Sequence(akVsFilter5PFcorr
                                                    *
                                                    #akVsFilter5PFJetID
                                                    #*
                                                    akVsFilter5PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter5PFJetBtagging
                                                    *
                                                    akVsFilter5PFNjettiness 
                                                    *
                                                    akVsFilter5PFpatJetsWithBtagging
                                                    *
                                                    akVsFilter5PFJetAnalyzer
                                                    )

akVsFilter5PFJetSequence_jec = cms.Sequence(akVsFilter5PFJetSequence_mc)
akVsFilter5PFJetSequence_mb = cms.Sequence(akVsFilter5PFJetSequence_mc)

akVsFilter5PFJetSequence = cms.Sequence(akVsFilter5PFJetSequence_data)
