

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akSoftDrop4Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop4CaloJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akSoftDrop4CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop4GenJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akSoftDrop4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop4CaloJets")
                                                        )

akSoftDrop4Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akSoftDrop4CaloJets"),
    payload = "AK4Calo_offline"
    )

akSoftDrop4CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akSoftDrop4CaloJets'))

#akSoftDrop4Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4GenJets'))

akSoftDrop4CalobTagger = bTaggers("akSoftDrop4Calo",0.4)

#create objects locally since they dont load properly otherwise
#akSoftDrop4Calomatch = akSoftDrop4CalobTagger.match
akSoftDrop4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop4CaloJets"), matched = cms.InputTag("genParticles"))
akSoftDrop4CaloPatJetFlavourAssociationLegacy = akSoftDrop4CalobTagger.PatJetFlavourAssociationLegacy
akSoftDrop4CaloPatJetPartons = akSoftDrop4CalobTagger.PatJetPartons
akSoftDrop4CaloJetTracksAssociatorAtVertex = akSoftDrop4CalobTagger.JetTracksAssociatorAtVertex
akSoftDrop4CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop4CaloCombinedSecondaryVertexBJetTags = akSoftDrop4CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop4CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop4CalobTagger.CombinedSecondaryVertexV2BJetTags
akSoftDrop4CaloJetBProbabilityBJetTags = akSoftDrop4CalobTagger.JetBProbabilityBJetTags
akSoftDrop4CaloSoftPFMuonByPtBJetTags = akSoftDrop4CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop4CaloSoftPFMuonByIP3dBJetTags = akSoftDrop4CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop4CaloTrackCountingHighEffBJetTags = akSoftDrop4CalobTagger.TrackCountingHighEffBJetTags
akSoftDrop4CaloTrackCountingHighPurBJetTags = akSoftDrop4CalobTagger.TrackCountingHighPurBJetTags
akSoftDrop4CaloPatJetPartonAssociationLegacy = akSoftDrop4CalobTagger.PatJetPartonAssociationLegacy

akSoftDrop4CaloImpactParameterTagInfos = akSoftDrop4CalobTagger.ImpactParameterTagInfos
akSoftDrop4CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop4CaloJetProbabilityBJetTags = akSoftDrop4CalobTagger.JetProbabilityBJetTags

akSoftDrop4CaloSecondaryVertexTagInfos = akSoftDrop4CalobTagger.SecondaryVertexTagInfos
akSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop4CaloCombinedSecondaryVertexBJetTags = akSoftDrop4CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop4CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop4CalobTagger.CombinedSecondaryVertexV2BJetTags

akSoftDrop4CaloSecondaryVertexNegativeTagInfos = akSoftDrop4CalobTagger.SecondaryVertexNegativeTagInfos
akSoftDrop4CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akSoftDrop4CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akSoftDrop4CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akSoftDrop4CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akSoftDrop4CaloNegativeCombinedSecondaryVertexBJetTags = akSoftDrop4CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akSoftDrop4CaloPositiveCombinedSecondaryVertexBJetTags = akSoftDrop4CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akSoftDrop4CaloNegativeCombinedSecondaryVertexV2BJetTags = akSoftDrop4CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akSoftDrop4CaloPositiveCombinedSecondaryVertexV2BJetTags = akSoftDrop4CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akSoftDrop4CaloSoftPFMuonsTagInfos = akSoftDrop4CalobTagger.SoftPFMuonsTagInfos
akSoftDrop4CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop4CaloSoftPFMuonBJetTags = akSoftDrop4CalobTagger.SoftPFMuonBJetTags
akSoftDrop4CaloSoftPFMuonByIP3dBJetTags = akSoftDrop4CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop4CaloSoftPFMuonByPtBJetTags = akSoftDrop4CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop4CaloNegativeSoftPFMuonByPtBJetTags = akSoftDrop4CalobTagger.NegativeSoftPFMuonByPtBJetTags
akSoftDrop4CaloPositiveSoftPFMuonByPtBJetTags = akSoftDrop4CalobTagger.PositiveSoftPFMuonByPtBJetTags
akSoftDrop4CaloPatJetFlavourIdLegacy = cms.Sequence(akSoftDrop4CaloPatJetPartonAssociationLegacy*akSoftDrop4CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akSoftDrop4CaloPatJetFlavourAssociation = akSoftDrop4CalobTagger.PatJetFlavourAssociation
#akSoftDrop4CaloPatJetFlavourId = cms.Sequence(akSoftDrop4CaloPatJetPartons*akSoftDrop4CaloPatJetFlavourAssociation)

akSoftDrop4CaloJetBtaggingIP       = cms.Sequence(akSoftDrop4CaloImpactParameterTagInfos *
            (akSoftDrop4CaloTrackCountingHighEffBJetTags +
             akSoftDrop4CaloTrackCountingHighPurBJetTags +
             akSoftDrop4CaloJetProbabilityBJetTags +
             akSoftDrop4CaloJetBProbabilityBJetTags 
            )
            )

akSoftDrop4CaloJetBtaggingSV = cms.Sequence(akSoftDrop4CaloImpactParameterTagInfos
            *
            akSoftDrop4CaloSecondaryVertexTagInfos
            * (akSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop4CaloCombinedSecondaryVertexBJetTags+
                akSoftDrop4CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop4CaloJetBtaggingNegSV = cms.Sequence(akSoftDrop4CaloImpactParameterTagInfos
            *
            akSoftDrop4CaloSecondaryVertexNegativeTagInfos
            * (akSoftDrop4CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop4CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop4CaloNegativeCombinedSecondaryVertexBJetTags+
                akSoftDrop4CaloPositiveCombinedSecondaryVertexBJetTags+
                akSoftDrop4CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akSoftDrop4CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop4CaloJetBtaggingMu = cms.Sequence(akSoftDrop4CaloSoftPFMuonsTagInfos * (akSoftDrop4CaloSoftPFMuonBJetTags
                +
                akSoftDrop4CaloSoftPFMuonByIP3dBJetTags
                +
                akSoftDrop4CaloSoftPFMuonByPtBJetTags
                +
                akSoftDrop4CaloNegativeSoftPFMuonByPtBJetTags
                +
                akSoftDrop4CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akSoftDrop4CaloJetBtagging = cms.Sequence(akSoftDrop4CaloJetBtaggingIP
            *akSoftDrop4CaloJetBtaggingSV
            *akSoftDrop4CaloJetBtaggingNegSV
#            *akSoftDrop4CaloJetBtaggingMu
            )

akSoftDrop4CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akSoftDrop4CaloJets"),
        genJetMatch          = cms.InputTag("akSoftDrop4Calomatch"),
        genPartonMatch       = cms.InputTag("akSoftDrop4Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akSoftDrop4Calocorr")),
        JetPartonMapSource   = cms.InputTag("akSoftDrop4CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akSoftDrop4CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akSoftDrop4CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akSoftDrop4CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akSoftDrop4CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akSoftDrop4CaloJetBProbabilityBJetTags"),
            cms.InputTag("akSoftDrop4CaloJetProbabilityBJetTags"),
            #cms.InputTag("akSoftDrop4CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akSoftDrop4CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akSoftDrop4CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akSoftDrop4CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akSoftDrop4CaloJetID"),
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

akSoftDrop4CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akSoftDrop4CaloJets"),
           	    R0  = cms.double( 0.4)
)
akSoftDrop4CalopatJetsWithBtagging.userData.userFloats.src += ['akSoftDrop4CaloNjettiness:tau1','akSoftDrop4CaloNjettiness:tau2','akSoftDrop4CaloNjettiness:tau3']

akSoftDrop4CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akSoftDrop4CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak4GenJets',
                                                             rParam = 0.4,
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
                                                             bTagJetName = cms.untracked.string("akSoftDrop4Calo"),
                                                             jetName = cms.untracked.string("akSoftDrop4Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(True),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop4GenJets"),
                                                             doGenTaus = True
                                                             )

akSoftDrop4CaloJetSequence_mc = cms.Sequence(
                                                  #akSoftDrop4Caloclean
                                                  #*
                                                  akSoftDrop4Calomatch
                                                  #*
                                                  #akSoftDrop4CalomatchGroomed
                                                  *
                                                  akSoftDrop4Caloparton
                                                  *
                                                  akSoftDrop4Calocorr
                                                  *
                                                  #akSoftDrop4CaloJetID
                                                  #*
                                                  akSoftDrop4CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akSoftDrop4CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akSoftDrop4CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akSoftDrop4CaloJetBtagging
                                                  *
                                                  akSoftDrop4CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akSoftDrop4CalopatJetsWithBtagging
                                                  *
                                                  akSoftDrop4CaloJetAnalyzer
                                                  )

akSoftDrop4CaloJetSequence_data = cms.Sequence(akSoftDrop4Calocorr
                                                    *
                                                    #akSoftDrop4CaloJetID
                                                    #*
                                                    akSoftDrop4CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akSoftDrop4CaloJetBtagging
                                                    *
                                                    akSoftDrop4CaloNjettiness 
                                                    *
                                                    akSoftDrop4CalopatJetsWithBtagging
                                                    *
                                                    akSoftDrop4CaloJetAnalyzer
                                                    )

akSoftDrop4CaloJetSequence_jec = cms.Sequence(akSoftDrop4CaloJetSequence_mc)
akSoftDrop4CaloJetSequence_mb = cms.Sequence(akSoftDrop4CaloJetSequence_mc)

akSoftDrop4CaloJetSequence = cms.Sequence(akSoftDrop4CaloJetSequence_mc)
