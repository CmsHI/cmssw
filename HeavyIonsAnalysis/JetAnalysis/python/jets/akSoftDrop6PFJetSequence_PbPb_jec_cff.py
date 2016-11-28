

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akSoftDrop6PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop6PFJets"),
    matched = cms.InputTag("ak6HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akSoftDrop6PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop6HiGenJets"),
    matched = cms.InputTag("ak6HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akSoftDrop6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop6PFJets")
                                                        )

akSoftDrop6PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akSoftDrop6PFJets"),
    payload = "AK6PF_offline"
    )

akSoftDrop6PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akSoftDrop6CaloJets'))

#akSoftDrop6PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6HiSignalGenJets'))

akSoftDrop6PFbTagger = bTaggers("akSoftDrop6PF",0.6)

#create objects locally since they dont load properly otherwise
#akSoftDrop6PFmatch = akSoftDrop6PFbTagger.match
akSoftDrop6PFparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop6PFJets"), matched = cms.InputTag("hiSignalGenParticles"))
akSoftDrop6PFPatJetFlavourAssociationLegacy = akSoftDrop6PFbTagger.PatJetFlavourAssociationLegacy
akSoftDrop6PFPatJetPartons = akSoftDrop6PFbTagger.PatJetPartons
akSoftDrop6PFJetTracksAssociatorAtVertex = akSoftDrop6PFbTagger.JetTracksAssociatorAtVertex
akSoftDrop6PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags = akSoftDrop6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags = akSoftDrop6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop6PFCombinedSecondaryVertexBJetTags = akSoftDrop6PFbTagger.CombinedSecondaryVertexBJetTags
akSoftDrop6PFCombinedSecondaryVertexV2BJetTags = akSoftDrop6PFbTagger.CombinedSecondaryVertexV2BJetTags
akSoftDrop6PFJetBProbabilityBJetTags = akSoftDrop6PFbTagger.JetBProbabilityBJetTags
akSoftDrop6PFSoftPFMuonByPtBJetTags = akSoftDrop6PFbTagger.SoftPFMuonByPtBJetTags
akSoftDrop6PFSoftPFMuonByIP3dBJetTags = akSoftDrop6PFbTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop6PFTrackCountingHighEffBJetTags = akSoftDrop6PFbTagger.TrackCountingHighEffBJetTags
akSoftDrop6PFTrackCountingHighPurBJetTags = akSoftDrop6PFbTagger.TrackCountingHighPurBJetTags
akSoftDrop6PFPatJetPartonAssociationLegacy = akSoftDrop6PFbTagger.PatJetPartonAssociationLegacy

akSoftDrop6PFImpactParameterTagInfos = akSoftDrop6PFbTagger.ImpactParameterTagInfos
akSoftDrop6PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop6PFJetProbabilityBJetTags = akSoftDrop6PFbTagger.JetProbabilityBJetTags

akSoftDrop6PFSecondaryVertexTagInfos = akSoftDrop6PFbTagger.SecondaryVertexTagInfos
akSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags = akSoftDrop6PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags = akSoftDrop6PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop6PFCombinedSecondaryVertexBJetTags = akSoftDrop6PFbTagger.CombinedSecondaryVertexBJetTags
akSoftDrop6PFCombinedSecondaryVertexV2BJetTags = akSoftDrop6PFbTagger.CombinedSecondaryVertexV2BJetTags

akSoftDrop6PFSecondaryVertexNegativeTagInfos = akSoftDrop6PFbTagger.SecondaryVertexNegativeTagInfos
akSoftDrop6PFNegativeSimpleSecondaryVertexHighEffBJetTags = akSoftDrop6PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akSoftDrop6PFNegativeSimpleSecondaryVertexHighPurBJetTags = akSoftDrop6PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akSoftDrop6PFNegativeCombinedSecondaryVertexBJetTags = akSoftDrop6PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akSoftDrop6PFPositiveCombinedSecondaryVertexBJetTags = akSoftDrop6PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akSoftDrop6PFNegativeCombinedSecondaryVertexV2BJetTags = akSoftDrop6PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akSoftDrop6PFPositiveCombinedSecondaryVertexV2BJetTags = akSoftDrop6PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akSoftDrop6PFSoftPFMuonsTagInfos = akSoftDrop6PFbTagger.SoftPFMuonsTagInfos
akSoftDrop6PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop6PFSoftPFMuonBJetTags = akSoftDrop6PFbTagger.SoftPFMuonBJetTags
akSoftDrop6PFSoftPFMuonByIP3dBJetTags = akSoftDrop6PFbTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop6PFSoftPFMuonByPtBJetTags = akSoftDrop6PFbTagger.SoftPFMuonByPtBJetTags
akSoftDrop6PFNegativeSoftPFMuonByPtBJetTags = akSoftDrop6PFbTagger.NegativeSoftPFMuonByPtBJetTags
akSoftDrop6PFPositiveSoftPFMuonByPtBJetTags = akSoftDrop6PFbTagger.PositiveSoftPFMuonByPtBJetTags
akSoftDrop6PFPatJetFlavourIdLegacy = cms.Sequence(akSoftDrop6PFPatJetPartonAssociationLegacy*akSoftDrop6PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akSoftDrop6PFPatJetFlavourAssociation = akSoftDrop6PFbTagger.PatJetFlavourAssociation
#akSoftDrop6PFPatJetFlavourId = cms.Sequence(akSoftDrop6PFPatJetPartons*akSoftDrop6PFPatJetFlavourAssociation)

akSoftDrop6PFJetBtaggingIP       = cms.Sequence(akSoftDrop6PFImpactParameterTagInfos *
            (akSoftDrop6PFTrackCountingHighEffBJetTags +
             akSoftDrop6PFTrackCountingHighPurBJetTags +
             akSoftDrop6PFJetProbabilityBJetTags +
             akSoftDrop6PFJetBProbabilityBJetTags 
            )
            )

akSoftDrop6PFJetBtaggingSV = cms.Sequence(akSoftDrop6PFImpactParameterTagInfos
            *
            akSoftDrop6PFSecondaryVertexTagInfos
            * (akSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop6PFCombinedSecondaryVertexBJetTags+
                akSoftDrop6PFCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop6PFJetBtaggingNegSV = cms.Sequence(akSoftDrop6PFImpactParameterTagInfos
            *
            akSoftDrop6PFSecondaryVertexNegativeTagInfos
            * (akSoftDrop6PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop6PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop6PFNegativeCombinedSecondaryVertexBJetTags+
                akSoftDrop6PFPositiveCombinedSecondaryVertexBJetTags+
                akSoftDrop6PFNegativeCombinedSecondaryVertexV2BJetTags+
                akSoftDrop6PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop6PFJetBtaggingMu = cms.Sequence(akSoftDrop6PFSoftPFMuonsTagInfos * (akSoftDrop6PFSoftPFMuonBJetTags
                +
                akSoftDrop6PFSoftPFMuonByIP3dBJetTags
                +
                akSoftDrop6PFSoftPFMuonByPtBJetTags
                +
                akSoftDrop6PFNegativeSoftPFMuonByPtBJetTags
                +
                akSoftDrop6PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akSoftDrop6PFJetBtagging = cms.Sequence(akSoftDrop6PFJetBtaggingIP
            *akSoftDrop6PFJetBtaggingSV
            *akSoftDrop6PFJetBtaggingNegSV
#            *akSoftDrop6PFJetBtaggingMu
            )

akSoftDrop6PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akSoftDrop6PFJets"),
        genJetMatch          = cms.InputTag("akSoftDrop6PFmatch"),
        genPartonMatch       = cms.InputTag("akSoftDrop6PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akSoftDrop6PFcorr")),
        JetPartonMapSource   = cms.InputTag("akSoftDrop6PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akSoftDrop6PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akSoftDrop6PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akSoftDrop6PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akSoftDrop6PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akSoftDrop6PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akSoftDrop6PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akSoftDrop6PFJetBProbabilityBJetTags"),
            cms.InputTag("akSoftDrop6PFJetProbabilityBJetTags"),
            #cms.InputTag("akSoftDrop6PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akSoftDrop6PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akSoftDrop6PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akSoftDrop6PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akSoftDrop6PFJetID"),
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

akSoftDrop6PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akSoftDrop6PFJets"),
           	    R0  = cms.double( 0.6)
)
akSoftDrop6PFpatJetsWithBtagging.userData.userFloats.src += ['akSoftDrop6PFNjettiness:tau1','akSoftDrop6PFNjettiness:tau2','akSoftDrop6PFNjettiness:tau3']

akSoftDrop6PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akSoftDrop6PFpatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akSoftDrop6PF"),
                                                             jetName = cms.untracked.string("akSoftDrop6PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop6GenJets"),
                                                             doGenTaus = True
                                                             )

akSoftDrop6PFJetSequence_mc = cms.Sequence(
                                                  #akSoftDrop6PFclean
                                                  #*
                                                  akSoftDrop6PFmatch
                                                  #*
                                                  #akSoftDrop6PFmatchGroomed
                                                  *
                                                  akSoftDrop6PFparton
                                                  *
                                                  akSoftDrop6PFcorr
                                                  *
                                                  #akSoftDrop6PFJetID
                                                  #*
                                                  akSoftDrop6PFPatJetFlavourIdLegacy
                                                  #*
			                          #akSoftDrop6PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akSoftDrop6PFJetTracksAssociatorAtVertex
                                                  *
                                                  akSoftDrop6PFJetBtagging
                                                  *
                                                  akSoftDrop6PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akSoftDrop6PFpatJetsWithBtagging
                                                  *
                                                  akSoftDrop6PFJetAnalyzer
                                                  )

akSoftDrop6PFJetSequence_data = cms.Sequence(akSoftDrop6PFcorr
                                                    *
                                                    #akSoftDrop6PFJetID
                                                    #*
                                                    akSoftDrop6PFJetTracksAssociatorAtVertex
                                                    *
                                                    akSoftDrop6PFJetBtagging
                                                    *
                                                    akSoftDrop6PFNjettiness 
                                                    *
                                                    akSoftDrop6PFpatJetsWithBtagging
                                                    *
                                                    akSoftDrop6PFJetAnalyzer
                                                    )

akSoftDrop6PFJetSequence_jec = cms.Sequence(akSoftDrop6PFJetSequence_mc)
akSoftDrop6PFJetSequence_mb = cms.Sequence(akSoftDrop6PFJetSequence_mc)

akSoftDrop6PFJetSequence = cms.Sequence(akSoftDrop6PFJetSequence_jec)
akSoftDrop6PFJetAnalyzer.genPtMin = cms.untracked.double(1)
akSoftDrop6PFJetAnalyzer.jetPtMin = cms.double(1)
