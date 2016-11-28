

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter1PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter1PFJets"),
    matched = cms.InputTag("ak1GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.1
    )

akVsFilter1PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter1GenJets"),
    matched = cms.InputTag("ak1GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.1
    )

akVsFilter1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter1PFJets")
                                                        )

akVsFilter1PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter1PFJets"),
    payload = "AK1PF_offline"
    )

akVsFilter1PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter1CaloJets'))

#akVsFilter1PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1GenJets'))

akVsFilter1PFbTagger = bTaggers("akVsFilter1PF",0.1)

#create objects locally since they dont load properly otherwise
#akVsFilter1PFmatch = akVsFilter1PFbTagger.match
akVsFilter1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter1PFJets"), matched = cms.InputTag("genParticles"))
akVsFilter1PFPatJetFlavourAssociationLegacy = akVsFilter1PFbTagger.PatJetFlavourAssociationLegacy
akVsFilter1PFPatJetPartons = akVsFilter1PFbTagger.PatJetPartons
akVsFilter1PFJetTracksAssociatorAtVertex = akVsFilter1PFbTagger.JetTracksAssociatorAtVertex
akVsFilter1PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter1PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter1PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter1PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter1PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter1PFCombinedSecondaryVertexBJetTags = akVsFilter1PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter1PFCombinedSecondaryVertexV2BJetTags = akVsFilter1PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter1PFJetBProbabilityBJetTags = akVsFilter1PFbTagger.JetBProbabilityBJetTags
akVsFilter1PFSoftPFMuonByPtBJetTags = akVsFilter1PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter1PFSoftPFMuonByIP3dBJetTags = akVsFilter1PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter1PFTrackCountingHighEffBJetTags = akVsFilter1PFbTagger.TrackCountingHighEffBJetTags
akVsFilter1PFTrackCountingHighPurBJetTags = akVsFilter1PFbTagger.TrackCountingHighPurBJetTags
akVsFilter1PFPatJetPartonAssociationLegacy = akVsFilter1PFbTagger.PatJetPartonAssociationLegacy

akVsFilter1PFImpactParameterTagInfos = akVsFilter1PFbTagger.ImpactParameterTagInfos
akVsFilter1PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter1PFJetProbabilityBJetTags = akVsFilter1PFbTagger.JetProbabilityBJetTags

akVsFilter1PFSecondaryVertexTagInfos = akVsFilter1PFbTagger.SecondaryVertexTagInfos
akVsFilter1PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter1PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter1PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter1PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter1PFCombinedSecondaryVertexBJetTags = akVsFilter1PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter1PFCombinedSecondaryVertexV2BJetTags = akVsFilter1PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter1PFSecondaryVertexNegativeTagInfos = akVsFilter1PFbTagger.SecondaryVertexNegativeTagInfos
akVsFilter1PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter1PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter1PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter1PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter1PFNegativeCombinedSecondaryVertexBJetTags = akVsFilter1PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter1PFPositiveCombinedSecondaryVertexBJetTags = akVsFilter1PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter1PFNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter1PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter1PFPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter1PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter1PFSoftPFMuonsTagInfos = akVsFilter1PFbTagger.SoftPFMuonsTagInfos
akVsFilter1PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter1PFSoftPFMuonBJetTags = akVsFilter1PFbTagger.SoftPFMuonBJetTags
akVsFilter1PFSoftPFMuonByIP3dBJetTags = akVsFilter1PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter1PFSoftPFMuonByPtBJetTags = akVsFilter1PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter1PFNegativeSoftPFMuonByPtBJetTags = akVsFilter1PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter1PFPositiveSoftPFMuonByPtBJetTags = akVsFilter1PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter1PFPatJetFlavourIdLegacy = cms.Sequence(akVsFilter1PFPatJetPartonAssociationLegacy*akVsFilter1PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter1PFPatJetFlavourAssociation = akVsFilter1PFbTagger.PatJetFlavourAssociation
#akVsFilter1PFPatJetFlavourId = cms.Sequence(akVsFilter1PFPatJetPartons*akVsFilter1PFPatJetFlavourAssociation)

akVsFilter1PFJetBtaggingIP       = cms.Sequence(akVsFilter1PFImpactParameterTagInfos *
            (akVsFilter1PFTrackCountingHighEffBJetTags +
             akVsFilter1PFTrackCountingHighPurBJetTags +
             akVsFilter1PFJetProbabilityBJetTags +
             akVsFilter1PFJetBProbabilityBJetTags 
            )
            )

akVsFilter1PFJetBtaggingSV = cms.Sequence(akVsFilter1PFImpactParameterTagInfos
            *
            akVsFilter1PFSecondaryVertexTagInfos
            * (akVsFilter1PFSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter1PFSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter1PFCombinedSecondaryVertexBJetTags+
                akVsFilter1PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter1PFJetBtaggingNegSV = cms.Sequence(akVsFilter1PFImpactParameterTagInfos
            *
            akVsFilter1PFSecondaryVertexNegativeTagInfos
            * (akVsFilter1PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter1PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter1PFNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter1PFPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter1PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter1PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter1PFJetBtaggingMu = cms.Sequence(akVsFilter1PFSoftPFMuonsTagInfos * (akVsFilter1PFSoftPFMuonBJetTags
                +
                akVsFilter1PFSoftPFMuonByIP3dBJetTags
                +
                akVsFilter1PFSoftPFMuonByPtBJetTags
                +
                akVsFilter1PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter1PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter1PFJetBtagging = cms.Sequence(akVsFilter1PFJetBtaggingIP
            *akVsFilter1PFJetBtaggingSV
            *akVsFilter1PFJetBtaggingNegSV
#            *akVsFilter1PFJetBtaggingMu
            )

akVsFilter1PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter1PFJets"),
        genJetMatch          = cms.InputTag("akVsFilter1PFmatch"),
        genPartonMatch       = cms.InputTag("akVsFilter1PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter1PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter1PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter1PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter1PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter1PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter1PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter1PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter1PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter1PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter1PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter1PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter1PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter1PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter1PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter1PFJetID"),
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

akVsFilter1PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter1PFJets"),
           	    R0  = cms.double( 0.1)
)
akVsFilter1PFpatJetsWithBtagging.userData.userFloats.src += ['akVsFilter1PFNjettiness:tau1','akVsFilter1PFNjettiness:tau2','akVsFilter1PFNjettiness:tau3']

akVsFilter1PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter1PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak1GenJets',
                                                             rParam = 0.1,
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
                                                             bTagJetName = cms.untracked.string("akVsFilter1PF"),
                                                             jetName = cms.untracked.string("akVsFilter1PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter1GenJets"),
                                                             doGenTaus = True
                                                             )

akVsFilter1PFJetSequence_mc = cms.Sequence(
                                                  #akVsFilter1PFclean
                                                  #*
                                                  akVsFilter1PFmatch
                                                  #*
                                                  #akVsFilter1PFmatchGroomed
                                                  *
                                                  akVsFilter1PFparton
                                                  *
                                                  akVsFilter1PFcorr
                                                  *
                                                  #akVsFilter1PFJetID
                                                  #*
                                                  akVsFilter1PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter1PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter1PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter1PFJetBtagging
                                                  *
                                                  akVsFilter1PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter1PFpatJetsWithBtagging
                                                  *
                                                  akVsFilter1PFJetAnalyzer
                                                  )

akVsFilter1PFJetSequence_data = cms.Sequence(akVsFilter1PFcorr
                                                    *
                                                    #akVsFilter1PFJetID
                                                    #*
                                                    akVsFilter1PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter1PFJetBtagging
                                                    *
                                                    akVsFilter1PFNjettiness 
                                                    *
                                                    akVsFilter1PFpatJetsWithBtagging
                                                    *
                                                    akVsFilter1PFJetAnalyzer
                                                    )

akVsFilter1PFJetSequence_jec = cms.Sequence(akVsFilter1PFJetSequence_mc)
akVsFilter1PFJetSequence_mb = cms.Sequence(akVsFilter1PFJetSequence_mc)

akVsFilter1PFJetSequence = cms.Sequence(akVsFilter1PFJetSequence_jec)
akVsFilter1PFJetAnalyzer.genPtMin = cms.untracked.double(1)
akVsFilter1PFJetAnalyzer.jetPtMin = cms.double(1)
