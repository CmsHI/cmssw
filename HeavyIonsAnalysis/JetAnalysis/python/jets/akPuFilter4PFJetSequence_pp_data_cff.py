

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter4PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter4PFJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akPuFilter4PFmatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter4GenJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akPuFilter4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter4PFJets")
                                                        )

akPuFilter4PFcorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter4PFJets"),
    payload = "AKPu4PF_offline"
    )

akPuFilter4PFJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter4CaloJets'))

#akPuFilter4PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4GenJets'))

akPuFilter4PFbTagger = bTaggers("akPuFilter4PF",0.4)

#create objects locally since they dont load properly otherwise
#akPuFilter4PFmatch = akPuFilter4PFbTagger.match
akPuFilter4PFparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter4PFJets"), matched = cms.InputTag("genParticles"))
akPuFilter4PFPatJetFlavourAssociationLegacy = akPuFilter4PFbTagger.PatJetFlavourAssociationLegacy
akPuFilter4PFPatJetPartons = akPuFilter4PFbTagger.PatJetPartons
akPuFilter4PFJetTracksAssociatorAtVertex = akPuFilter4PFbTagger.JetTracksAssociatorAtVertex
akPuFilter4PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter4PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter4PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter4PFCombinedSecondaryVertexBJetTags = akPuFilter4PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter4PFCombinedSecondaryVertexV2BJetTags = akPuFilter4PFbTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter4PFJetBProbabilityBJetTags = akPuFilter4PFbTagger.JetBProbabilityBJetTags
akPuFilter4PFSoftPFMuonByPtBJetTags = akPuFilter4PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter4PFSoftPFMuonByIP3dBJetTags = akPuFilter4PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter4PFTrackCountingHighEffBJetTags = akPuFilter4PFbTagger.TrackCountingHighEffBJetTags
akPuFilter4PFTrackCountingHighPurBJetTags = akPuFilter4PFbTagger.TrackCountingHighPurBJetTags
akPuFilter4PFPatJetPartonAssociationLegacy = akPuFilter4PFbTagger.PatJetPartonAssociationLegacy

akPuFilter4PFImpactParameterTagInfos = akPuFilter4PFbTagger.ImpactParameterTagInfos
akPuFilter4PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter4PFJetProbabilityBJetTags = akPuFilter4PFbTagger.JetProbabilityBJetTags

akPuFilter4PFSecondaryVertexTagInfos = akPuFilter4PFbTagger.SecondaryVertexTagInfos
akPuFilter4PFSimpleSecondaryVertexHighEffBJetTags = akPuFilter4PFbTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter4PFSimpleSecondaryVertexHighPurBJetTags = akPuFilter4PFbTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter4PFCombinedSecondaryVertexBJetTags = akPuFilter4PFbTagger.CombinedSecondaryVertexBJetTags
akPuFilter4PFCombinedSecondaryVertexV2BJetTags = akPuFilter4PFbTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter4PFSecondaryVertexNegativeTagInfos = akPuFilter4PFbTagger.SecondaryVertexNegativeTagInfos
akPuFilter4PFNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter4PFbTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter4PFNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter4PFbTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter4PFNegativeCombinedSecondaryVertexBJetTags = akPuFilter4PFbTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter4PFPositiveCombinedSecondaryVertexBJetTags = akPuFilter4PFbTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter4PFNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter4PFbTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter4PFPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter4PFbTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter4PFSoftPFMuonsTagInfos = akPuFilter4PFbTagger.SoftPFMuonsTagInfos
akPuFilter4PFSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter4PFSoftPFMuonBJetTags = akPuFilter4PFbTagger.SoftPFMuonBJetTags
akPuFilter4PFSoftPFMuonByIP3dBJetTags = akPuFilter4PFbTagger.SoftPFMuonByIP3dBJetTags
akPuFilter4PFSoftPFMuonByPtBJetTags = akPuFilter4PFbTagger.SoftPFMuonByPtBJetTags
akPuFilter4PFNegativeSoftPFMuonByPtBJetTags = akPuFilter4PFbTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter4PFPositiveSoftPFMuonByPtBJetTags = akPuFilter4PFbTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter4PFPatJetFlavourIdLegacy = cms.Sequence(akPuFilter4PFPatJetPartonAssociationLegacy*akPuFilter4PFPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter4PFPatJetFlavourAssociation = akPuFilter4PFbTagger.PatJetFlavourAssociation
#akPuFilter4PFPatJetFlavourId = cms.Sequence(akPuFilter4PFPatJetPartons*akPuFilter4PFPatJetFlavourAssociation)

akPuFilter4PFJetBtaggingIP       = cms.Sequence(akPuFilter4PFImpactParameterTagInfos *
            (akPuFilter4PFTrackCountingHighEffBJetTags +
             akPuFilter4PFTrackCountingHighPurBJetTags +
             akPuFilter4PFJetProbabilityBJetTags +
             akPuFilter4PFJetBProbabilityBJetTags 
            )
            )

akPuFilter4PFJetBtaggingSV = cms.Sequence(akPuFilter4PFImpactParameterTagInfos
            *
            akPuFilter4PFSecondaryVertexTagInfos
            * (akPuFilter4PFSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter4PFSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter4PFCombinedSecondaryVertexBJetTags+
                akPuFilter4PFCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter4PFJetBtaggingNegSV = cms.Sequence(akPuFilter4PFImpactParameterTagInfos
            *
            akPuFilter4PFSecondaryVertexNegativeTagInfos
            * (akPuFilter4PFNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter4PFNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter4PFNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter4PFPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter4PFNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter4PFPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter4PFJetBtaggingMu = cms.Sequence(akPuFilter4PFSoftPFMuonsTagInfos * (akPuFilter4PFSoftPFMuonBJetTags
                +
                akPuFilter4PFSoftPFMuonByIP3dBJetTags
                +
                akPuFilter4PFSoftPFMuonByPtBJetTags
                +
                akPuFilter4PFNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter4PFPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter4PFJetBtagging = cms.Sequence(akPuFilter4PFJetBtaggingIP
            *akPuFilter4PFJetBtaggingSV
            *akPuFilter4PFJetBtaggingNegSV
#            *akPuFilter4PFJetBtaggingMu
            )

akPuFilter4PFpatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter4PFJets"),
        genJetMatch          = cms.InputTag("akPuFilter4PFmatch"),
        genPartonMatch       = cms.InputTag("akPuFilter4PFparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter4PFcorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter4PFPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter4PFPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter4PFJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter4PFSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter4PFSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter4PFCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter4PFCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter4PFJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter4PFJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter4PFSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter4PFSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter4PFTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter4PFTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter4PFJetID"),
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

akPuFilter4PFNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter4PFJets"),
           	    R0  = cms.double( 0.4)
)
akPuFilter4PFpatJetsWithBtagging.userData.userFloats.src += ['akPuFilter4PFNjettiness:tau1','akPuFilter4PFNjettiness:tau2','akPuFilter4PFNjettiness:tau3']

akPuFilter4PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter4PFpatJetsWithBtagging"),
                                                             genjetTag = 'ak4GenJets',
                                                             rParam = 0.4,
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
                                                             bTagJetName = cms.untracked.string("akPuFilter4PF"),
                                                             jetName = cms.untracked.string("akPuFilter4PF"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter4GenJets"),
                                                             doGenTaus = False
                                                             )

akPuFilter4PFJetSequence_mc = cms.Sequence(
                                                  #akPuFilter4PFclean
                                                  #*
                                                  akPuFilter4PFmatch
                                                  #*
                                                  #akPuFilter4PFmatchGroomed
                                                  *
                                                  akPuFilter4PFparton
                                                  *
                                                  akPuFilter4PFcorr
                                                  *
                                                  #akPuFilter4PFJetID
                                                  #*
                                                  akPuFilter4PFPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter4PFPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter4PFJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter4PFJetBtagging
                                                  *
                                                  akPuFilter4PFNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter4PFpatJetsWithBtagging
                                                  *
                                                  akPuFilter4PFJetAnalyzer
                                                  )

akPuFilter4PFJetSequence_data = cms.Sequence(akPuFilter4PFcorr
                                                    *
                                                    #akPuFilter4PFJetID
                                                    #*
                                                    akPuFilter4PFJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter4PFJetBtagging
                                                    *
                                                    akPuFilter4PFNjettiness 
                                                    *
                                                    akPuFilter4PFpatJetsWithBtagging
                                                    *
                                                    akPuFilter4PFJetAnalyzer
                                                    )

akPuFilter4PFJetSequence_jec = cms.Sequence(akPuFilter4PFJetSequence_mc)
akPuFilter4PFJetSequence_mb = cms.Sequence(akPuFilter4PFJetSequence_mc)

akPuFilter4PFJetSequence = cms.Sequence(akPuFilter4PFJetSequence_data)
