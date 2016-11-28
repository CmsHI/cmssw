

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter6PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter6PFJets"),
    matched = cms.InputTag("ak6HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.6
    )

akVsFilter6PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter6HiGenJets"),
    matched = cms.InputTag("ak6HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.6
    )

akVsFilter6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter6PFJets")
                                                        )

akVsFilter6PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter6PFJets"),
    payload = "AK6PF_offline"
    )

akVsFilter6PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter6CaloJets'))

#akVsFilter6PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6HiSignalGenJets'))

akVsFilter6PFbTagger = bTaggers("akVsFilter6PF",0.6)

#create objects locally since they dont load properly otherwise
#akVsFilter6PFmatch = akVsFilter6PFbTagger.match
akVsFilter6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter6PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akVsFilter6PFPatJetFlavourAssociationLegacy = akVsFilter6PFbTagger.PatJetFlavourAssociationLegacy
akVsFilter6PFPatJetPartons = akVsFilter6PFbTagger.PatJetPartons
akVsFilter6PFJetTracksAssociatorAtVertex = akVsFilter6PFbTagger.JetTracksAssociatorAtVertex
akVsFilter6PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter6PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter6PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter6PFCombinedSecondaryVertexBJetTags = akVsFilter6PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter6PFCombinedSecondaryVertexV2BJetTags = akVsFilter6PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter6PFJetBProbabilityBJetTags = akVsFilter6PFbTagger.JetBProbabilityBJetTags
akVsFilter6PFSoftPFMuonByPtBJetTags = akVsFilter6PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter6PFSoftPFMuonByIP3dBJetTags = akVsFilter6PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter6PFTrackCountingHighEffBJetTags = akVsFilter6PFbTagger.TrackCountingHighEffBJetTags
akVsFilter6PFTrackCountingHighPurBJetTags = akVsFilter6PFbTagger.TrackCountingHighPurBJetTags
akVsFilter6PFPatJetPartonAssociationLegacy = akVsFilter6PFbTagger.PatJetPartonAssociationLegacy

akVsFilter6PFImpactParameterTagInfos = akVsFilter6PFbTagger.ImpactParameterTagInfos
akVsFilter6PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter6PFJetProbabilityBJetTags = akVsFilter6PFbTagger.JetProbabilityBJetTags

akVsFilter6PFSecondaryVertexTagInfos = akVsFilter6PFbTagger.SecondaryVertexTagInfos
akVsFilter6PFSimpleSecondaryVertexHighEffBJetTags = akVsFilter6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter6PFSimpleSecondaryVertexHighPurBJetTags = akVsFilter6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter6PFCombinedSecondaryVertexBJetTags = akVsFilter6PFbTagger.CombinedSecondaryVertexBJetTags
akVsFilter6PFCombinedSecondaryVertexV2BJetTags = akVsFilter6PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter6PFSecondaryVertexNegativeTagInfos = akVsFilter6PFbTagger.SecondaryVertexNegativeTagInfos
akVsFilter6PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter6PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter6PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter6PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter6PFNegativeCombinedSecondaryVertexBJetTags = akVsFilter6PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter6PFPositiveCombinedSecondaryVertexBJetTags = akVsFilter6PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter6PFNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter6PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter6PFPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter6PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter6PFSoftPFMuonsTagInfos = akVsFilter6PFbTagger.SoftPFMuonsTagInfos
akVsFilter6PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter6PFSoftPFMuonBJetTags = akVsFilter6PFbTagger.SoftPFMuonBJetTags
akVsFilter6PFSoftPFMuonByIP3dBJetTags = akVsFilter6PFbTagger.SoftPFMuonByIP3dBJetTags
akVsFilter6PFSoftPFMuonByPtBJetTags = akVsFilter6PFbTagger.SoftPFMuonByPtBJetTags
akVsFilter6PFNegativeSoftPFMuonByPtBJetTags = akVsFilter6PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter6PFPositiveSoftPFMuonByPtBJetTags = akVsFilter6PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter6PFPatJetFlavourIdLegacy = cms.Sequence(akVsFilter6PFPatJetPartonAssociationLegacy*akVsFilter6PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter6PFPatJetFlavourAssociation = akVsFilter6PFbTagger.PatJetFlavourAssociation
#akVsFilter6PFPatJetFlavourId = cms.Sequence(akVsFilter6PFPatJetPartons*akVsFilter6PFPatJetFlavourAssociation)

akVsFilter6PFJetBtaggingIP       = cms.Sequence(akVsFilter6PFImpactParameterTagInfos *
            (akVsFilter6PFTrackCountingHighEffBJetTags +
             akVsFilter6PFTrackCountingHighPurBJetTags +
             akVsFilter6PFJetProbabilityBJetTags +
             akVsFilter6PFJetBProbabilityBJetTags 
            )
            )

akVsFilter6PFJetBtaggingSV = cms.Sequence(akVsFilter6PFImpactParameterTagInfos
            *
            akVsFilter6PFSecondaryVertexTagInfos
            * (akVsFilter6PFSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter6PFSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter6PFCombinedSecondaryVertexBJetTags+
                akVsFilter6PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter6PFJetBtaggingNegSV = cms.Sequence(akVsFilter6PFImpactParameterTagInfos
            *
            akVsFilter6PFSecondaryVertexNegativeTagInfos
            * (akVsFilter6PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter6PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter6PFNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter6PFPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter6PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter6PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter6PFJetBtaggingMu = cms.Sequence(akVsFilter6PFSoftPFMuonsTagInfos * (akVsFilter6PFSoftPFMuonBJetTags
                +
                akVsFilter6PFSoftPFMuonByIP3dBJetTags
                +
                akVsFilter6PFSoftPFMuonByPtBJetTags
                +
                akVsFilter6PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter6PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter6PFJetBtagging = cms.Sequence(akVsFilter6PFJetBtaggingIP
            *akVsFilter6PFJetBtaggingSV
            *akVsFilter6PFJetBtaggingNegSV
#            *akVsFilter6PFJetBtaggingMu
            )

akVsFilter6PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter6PFJets"),
        genJetMatch          = cms.InputTag("akVsFilter6PFmatch"),
        genPartonMatch       = cms.InputTag("akVsFilter6PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter6PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter6PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter6PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter6PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter6PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter6PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter6PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter6PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter6PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter6PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter6PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter6PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter6PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter6PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter6PFJetID"),
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

akVsFilter6PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter6PFJets"),
           	    R0  = cms.double( 0.6)
)
akVsFilter6PFpatJetsWithBtagging.userData.userFloats.src += ['akVsFilter6PFNjettiness:tau1','akVsFilter6PFNjettiness:tau2','akVsFilter6PFNjettiness:tau3']

akVsFilter6PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter6PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak6HiGenJets',
                                                             rParam = 0.6,
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
                                                             bTagJetName = cms.untracked.string("akVsFilter6PF"),
                                                             jetName = cms.untracked.string("akVsFilter6PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter6GenJets"),
                                                             doGenTaus = True
                                                             )

akVsFilter6PFJetSequence_mc = cms.Sequence(
                                                  #akVsFilter6PFclean
                                                  #*
                                                  akVsFilter6PFmatch
                                                  #*
                                                  #akVsFilter6PFmatchGroomed
                                                  *
                                                  akVsFilter6PFparton
                                                  *
                                                  akVsFilter6PFcorr
                                                  *
                                                  #akVsFilter6PFJetID
                                                  #*
                                                  akVsFilter6PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter6PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter6PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter6PFJetBtagging
                                                  *
                                                  akVsFilter6PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter6PFpatJetsWithBtagging
                                                  *
                                                  akVsFilter6PFJetAnalyzer
                                                  )

akVsFilter6PFJetSequence_data = cms.Sequence(akVsFilter6PFcorr
                                                    *
                                                    #akVsFilter6PFJetID
                                                    #*
                                                    akVsFilter6PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter6PFJetBtagging
                                                    *
                                                    akVsFilter6PFNjettiness 
                                                    *
                                                    akVsFilter6PFpatJetsWithBtagging
                                                    *
                                                    akVsFilter6PFJetAnalyzer
                                                    )

akVsFilter6PFJetSequence_jec = cms.Sequence(akVsFilter6PFJetSequence_mc)
akVsFilter6PFJetSequence_mb = cms.Sequence(akVsFilter6PFJetSequence_mc)

akVsFilter6PFJetSequence = cms.Sequence(akVsFilter6PFJetSequence_jec)
akVsFilter6PFJetAnalyzer.genPtMin = cms.untracked.double(1)
akVsFilter6PFJetAnalyzer.jetPtMin = cms.double(1)
