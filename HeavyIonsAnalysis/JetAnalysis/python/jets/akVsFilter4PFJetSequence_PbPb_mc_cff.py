

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter4PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter4PFJets"),
    matched = cms.InputTag("ak4HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.4
    )

akVsFilter4PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter4HiGenJets"),
    matched = cms.InputTag("ak4HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.4
    )

akVsFilter4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter4PFJets")
                                                        )

akVsFilter4PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter4PFJets"),
    payload = "AK4PF_offline"
    )

akVsFilter4PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter4CaloJets'))

#akVsFilter4PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4HiSignalGenJets'))

akVsFilter4PFbTagger = bTaggers("akVsFilter4PF",0.4)

#create objects locally since they dont load properly otherwise
#akVsFilter4PFmatch = akVsFilter4PFbTagger.match
akVsFilter4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter4PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akVsFilter4PFPatJetFlavourAssociationLegacy = akVsFilter4PFbTagger.PatJetFlavourAssociationLegacy
akVsFilter4PFPatJetPartons = akVsFilter4PFbTagger.PatJetPartons
akVsFilter4PFJetTracksAssociatorAtVertex = akVsFilter4PFbTagger.JetTracksAssociatorAtVertex
akVsFilter4PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter4PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter4PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter4PFCombinedSecondaryVertexBJetTags = akVsFilter4PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter4PFCombinedSecondaryVertexV2BJetTags = akVsFilter4PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter4PFJetBProbabilityBJetTags = akVsFilter4PFbTagger.JetBProbabilityBJetTags
akVsFilter4PFSoftPFMuonByPtBJetTags = akVsFilter4PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter4PFSoftPFMuonByIP3dBJetTags = akVsFilter4PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter4PFTrackCountingHighEffBJetTags = akVsFilter4PFbTagger.TrackCountingHighEffBJetTags
akVsFilter4PFTrackCountingHighPurBJetTags = akVsFilter4PFbTagger.TrackCountingHighPurBJetTags
akVsFilter4PFPatJetPartonAssociationLegacy = akVsFilter4PFbTagger.PatJetPartonAssociationLegacy

akVsFilter4PFImpactParameterTagInfos = akVsFilter4PFbTagger.ImpactParameterTagInfos
akVsFilter4PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter4PFJetProbabilityBJetTags = akVsFilter4PFbTagger.JetProbabilityBJetTags

akVsFilter4PFSecondaryVertexTagInfos = akVsFilter4PFbTagger.SecondaryVertexTagInfos
akVsFilter4PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter4PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter4PFCombinedSecondaryVertexBJetTags = akVsFilter4PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter4PFCombinedSecondaryVertexV2BJetTags = akVsFilter4PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter4PFSecondaryVertexNegativeTagInfos = akVsFilter4PFbTagger.SecondaryVertexNegativeTagInfos
akVsFilter4PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter4PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter4PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter4PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter4PFNegativeCombinedSecondaryVertexBJetTags = akVsFilter4PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter4PFPositiveCombinedSecondaryVertexBJetTags = akVsFilter4PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter4PFNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter4PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter4PFPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter4PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter4PFSoftPFMuonsTagInfos = akVsFilter4PFbTagger.SoftPFMuonsTagInfos
akVsFilter4PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter4PFSoftPFMuonBJetTags = akVsFilter4PFbTagger.SoftPFMuonBJetTags
akVsFilter4PFSoftPFMuonByIP3dBJetTags = akVsFilter4PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter4PFSoftPFMuonByPtBJetTags = akVsFilter4PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter4PFNegativeSoftPFMuonByPtBJetTags = akVsFilter4PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter4PFPositiveSoftPFMuonByPtBJetTags = akVsFilter4PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter4PFPatJetFlavourIdLegacy = cms.Sequence(akVsFilter4PFPatJetPartonAssociationLegacy*akVsFilter4PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter4PFPatJetFlavourAssociation = akVsFilter4PFbTagger.PatJetFlavourAssociation
#akVsFilter4PFPatJetFlavourId = cms.Sequence(akVsFilter4PFPatJetPartons*akVsFilter4PFPatJetFlavourAssociation)

akVsFilter4PFJetBtaggingIP       = cms.Sequence(akVsFilter4PFImpactParameterTagInfos *
            (akVsFilter4PFTrackCountingHighEffBJetTags +
             akVsFilter4PFTrackCountingHighPurBJetTags +
             akVsFilter4PFJetProbabilityBJetTags +
             akVsFilter4PFJetBProbabilityBJetTags 
            )
            )

akVsFilter4PFJetBtaggingSV = cms.Sequence(akVsFilter4PFImpactParameterTagInfos
            *
            akVsFilter4PFSecondaryVertexTagInfos
            * (akVsFilter4PFSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter4PFSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter4PFCombinedSecondaryVertexBJetTags+
                akVsFilter4PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter4PFJetBtaggingNegSV = cms.Sequence(akVsFilter4PFImpactParameterTagInfos
            *
            akVsFilter4PFSecondaryVertexNegativeTagInfos
            * (akVsFilter4PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter4PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter4PFNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter4PFPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter4PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter4PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter4PFJetBtaggingMu = cms.Sequence(akVsFilter4PFSoftPFMuonsTagInfos * (akVsFilter4PFSoftPFMuonBJetTags
                +
                akVsFilter4PFSoftPFMuonByIP3dBJetTags
                +
                akVsFilter4PFSoftPFMuonByPtBJetTags
                +
                akVsFilter4PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter4PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter4PFJetBtagging = cms.Sequence(akVsFilter4PFJetBtaggingIP
            *akVsFilter4PFJetBtaggingSV
            *akVsFilter4PFJetBtaggingNegSV
#            *akVsFilter4PFJetBtaggingMu
            )

akVsFilter4PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter4PFJets"),
        genJetMatch          = cms.InputTag("akVsFilter4PFmatch"),
        genPartonMatch       = cms.InputTag("akVsFilter4PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter4PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter4PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter4PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter4PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter4PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter4PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter4PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter4PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter4PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter4PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter4PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter4PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter4PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter4PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter4PFJetID"),
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

akVsFilter4PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter4PFJets"),
           	    R0  = cms.double( 0.4)
)
akVsFilter4PFpatJetsWithBtagging.userData.userFloats.src += ['akVsFilter4PFNjettiness:tau1','akVsFilter4PFNjettiness:tau2','akVsFilter4PFNjettiness:tau3']

akVsFilter4PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter4PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak4HiGenJets',
                                                             rParam = 0.4,
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
                                                             bTagJetName = cms.untracked.string("akVsFilter4PF"),
                                                             jetName = cms.untracked.string("akVsFilter4PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter4GenJets"),
                                                             doGenTaus = True
                                                             )

akVsFilter4PFJetSequence_mc = cms.Sequence(
                                                  #akVsFilter4PFclean
                                                  #*
                                                  akVsFilter4PFmatch
                                                  #*
                                                  #akVsFilter4PFmatchGroomed
                                                  *
                                                  akVsFilter4PFparton
                                                  *
                                                  akVsFilter4PFcorr
                                                  *
                                                  #akVsFilter4PFJetID
                                                  #*
                                                  akVsFilter4PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter4PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter4PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter4PFJetBtagging
                                                  *
                                                  akVsFilter4PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter4PFpatJetsWithBtagging
                                                  *
                                                  akVsFilter4PFJetAnalyzer
                                                  )

akVsFilter4PFJetSequence_data = cms.Sequence(akVsFilter4PFcorr
                                                    *
                                                    #akVsFilter4PFJetID
                                                    #*
                                                    akVsFilter4PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter4PFJetBtagging
                                                    *
                                                    akVsFilter4PFNjettiness 
                                                    *
                                                    akVsFilter4PFpatJetsWithBtagging
                                                    *
                                                    akVsFilter4PFJetAnalyzer
                                                    )

akVsFilter4PFJetSequence_jec = cms.Sequence(akVsFilter4PFJetSequence_mc)
akVsFilter4PFJetSequence_mb = cms.Sequence(akVsFilter4PFJetSequence_mc)

akVsFilter4PFJetSequence = cms.Sequence(akVsFilter4PFJetSequence_mc)
