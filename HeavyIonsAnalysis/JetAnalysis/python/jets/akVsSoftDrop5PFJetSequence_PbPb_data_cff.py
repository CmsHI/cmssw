

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop5PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop5PFJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.5
    )

akVsSoftDrop5PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop5HiGenJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.5
    )

akVsSoftDrop5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop5PFJets")
                                                        )

akVsSoftDrop5PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop5PFJets"),
    payload = "AK5PF_offline"
    )

akVsSoftDrop5PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop5CaloJets'))

#akVsSoftDrop5PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5HiSignalGenJets'))

akVsSoftDrop5PFbTagger = bTaggers("akVsSoftDrop5PF",0.5)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop5PFmatch = akVsSoftDrop5PFbTagger.match
akVsSoftDrop5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop5PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akVsSoftDrop5PFPatJetFlavourAssociationLegacy = akVsSoftDrop5PFbTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop5PFPatJetPartons = akVsSoftDrop5PFbTagger.PatJetPartons
akVsSoftDrop5PFJetTracksAssociatorAtVertex = akVsSoftDrop5PFbTagger.JetTracksAssociatorAtVertex
akVsSoftDrop5PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop5PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop5PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop5PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop5PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop5PFCombinedSecondaryVertexBJetTags = akVsSoftDrop5PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop5PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop5PFbTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop5PFJetBProbabilityBJetTags = akVsSoftDrop5PFbTagger.JetBProbabilityBJetTags
akVsSoftDrop5PFSoftPFMuonByPtBJetTags = akVsSoftDrop5PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop5PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop5PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop5PFTrackCountingHighEffBJetTags = akVsSoftDrop5PFbTagger.TrackCountingHighEffBJetTags
akVsSoftDrop5PFTrackCountingHighPurBJetTags = akVsSoftDrop5PFbTagger.TrackCountingHighPurBJetTags
akVsSoftDrop5PFPatJetPartonAssociationLegacy = akVsSoftDrop5PFbTagger.PatJetPartonAssociationLegacy

akVsSoftDrop5PFImpactParameterTagInfos = akVsSoftDrop5PFbTagger.ImpactParameterTagInfos
akVsSoftDrop5PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop5PFJetProbabilityBJetTags = akVsSoftDrop5PFbTagger.JetProbabilityBJetTags

akVsSoftDrop5PFSecondaryVertexTagInfos = akVsSoftDrop5PFbTagger.SecondaryVertexTagInfos
akVsSoftDrop5PFSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop5PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop5PFSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop5PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop5PFCombinedSecondaryVertexBJetTags = akVsSoftDrop5PFbTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop5PFCombinedSecondaryVertexV2BJetTags = akVsSoftDrop5PFbTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop5PFSecondaryVertexNegativeTagInfos = akVsSoftDrop5PFbTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop5PFNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop5PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop5PFNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop5PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop5PFNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop5PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop5PFPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop5PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop5PFNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop5PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop5PFPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop5PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop5PFSoftPFMuonsTagInfos = akVsSoftDrop5PFbTagger.SoftPFMuonsTagInfos
akVsSoftDrop5PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop5PFSoftPFMuonBJetTags = akVsSoftDrop5PFbTagger.SoftPFMuonBJetTags
akVsSoftDrop5PFSoftPFMuonByIP3dBJetTags = akVsSoftDrop5PFbTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop5PFSoftPFMuonByPtBJetTags = akVsSoftDrop5PFbTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop5PFNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop5PFbTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop5PFPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop5PFbTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop5PFPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop5PFPatJetPartonAssociationLegacy*akVsSoftDrop5PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop5PFPatJetFlavourAssociation = akVsSoftDrop5PFbTagger.PatJetFlavourAssociation
#akVsSoftDrop5PFPatJetFlavourId = cms.Sequence(akVsSoftDrop5PFPatJetPartons*akVsSoftDrop5PFPatJetFlavourAssociation)

akVsSoftDrop5PFJetBtaggingIP       = cms.Sequence(akVsSoftDrop5PFImpactParameterTagInfos *
            (akVsSoftDrop5PFTrackCountingHighEffBJetTags +
             akVsSoftDrop5PFTrackCountingHighPurBJetTags +
             akVsSoftDrop5PFJetProbabilityBJetTags +
             akVsSoftDrop5PFJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop5PFJetBtaggingSV = cms.Sequence(akVsSoftDrop5PFImpactParameterTagInfos
            *
            akVsSoftDrop5PFSecondaryVertexTagInfos
            * (akVsSoftDrop5PFSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop5PFSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop5PFCombinedSecondaryVertexBJetTags+
                akVsSoftDrop5PFCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop5PFJetBtaggingNegSV = cms.Sequence(akVsSoftDrop5PFImpactParameterTagInfos
            *
            akVsSoftDrop5PFSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop5PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop5PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop5PFNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop5PFPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop5PFNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop5PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop5PFJetBtaggingMu = cms.Sequence(akVsSoftDrop5PFSoftPFMuonsTagInfos * (akVsSoftDrop5PFSoftPFMuonBJetTags
                +
                akVsSoftDrop5PFSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop5PFSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop5PFNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop5PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop5PFJetBtagging = cms.Sequence(akVsSoftDrop5PFJetBtaggingIP
            *akVsSoftDrop5PFJetBtaggingSV
            *akVsSoftDrop5PFJetBtaggingNegSV
#            *akVsSoftDrop5PFJetBtaggingMu
            )

akVsSoftDrop5PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop5PFJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop5PFmatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop5PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop5PFcorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop5PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop5PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop5PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop5PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop5PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop5PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop5PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop5PFJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop5PFJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop5PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop5PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop5PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop5PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop5PFJetID"),
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

akVsSoftDrop5PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop5PFJets"),
           	    R0  = cms.double( 0.5)
)
akVsSoftDrop5PFpatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop5PFNjettiness:tau1','akVsSoftDrop5PFNjettiness:tau2','akVsSoftDrop5PFNjettiness:tau3']

akVsSoftDrop5PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop5PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak5HiGenJets',
                                                             rParam = 0.5,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlowTmp'),
                                                             trackTag = cms.InputTag("hiGeneralTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
							     doSubEvent = False,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop5PF"),
                                                             jetName = cms.untracked.string("akVsSoftDrop5PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop5GenJets"),
                                                             doGenTaus = False
                                                             )

akVsSoftDrop5PFJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop5PFclean
                                                  #*
                                                  akVsSoftDrop5PFmatch
                                                  #*
                                                  #akVsSoftDrop5PFmatchGroomed
                                                  *
                                                  akVsSoftDrop5PFparton
                                                  *
                                                  akVsSoftDrop5PFcorr
                                                  *
                                                  #akVsSoftDrop5PFJetID
                                                  #*
                                                  akVsSoftDrop5PFPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop5PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop5PFJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop5PFJetBtagging
                                                  *
                                                  akVsSoftDrop5PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop5PFpatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop5PFJetAnalyzer
                                                  )

akVsSoftDrop5PFJetSequence_data = cms.Sequence(akVsSoftDrop5PFcorr
                                                    *
                                                    #akVsSoftDrop5PFJetID
                                                    #*
                                                    akVsSoftDrop5PFJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop5PFJetBtagging
                                                    *
                                                    akVsSoftDrop5PFNjettiness 
                                                    *
                                                    akVsSoftDrop5PFpatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop5PFJetAnalyzer
                                                    )

akVsSoftDrop5PFJetSequence_jec = cms.Sequence(akVsSoftDrop5PFJetSequence_mc)
akVsSoftDrop5PFJetSequence_mb = cms.Sequence(akVsSoftDrop5PFJetSequence_mc)

akVsSoftDrop5PFJetSequence = cms.Sequence(akVsSoftDrop5PFJetSequence_data)
