

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop6Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop6CaloJets"),
    matched = cms.InputTag("ak6HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akPuSoftDrop6CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop6HiGenJets"),
    matched = cms.InputTag("ak6HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akPuSoftDrop6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop6CaloJets")
                                                        )

akPuSoftDrop6Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop6CaloJets"),
    payload = "AKPu6Calo_offline"
    )

akPuSoftDrop6CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop6CaloJets'))

#akPuSoftDrop6Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6HiCleanedGenJets'))

akPuSoftDrop6CalobTagger = bTaggers("akPuSoftDrop6Calo",0.6)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop6Calomatch = akPuSoftDrop6CalobTagger.match
akPuSoftDrop6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop6CaloJets"), matched = cms.InputTag("selectedPartons"))
akPuSoftDrop6CaloPatJetFlavourAssociationLegacy = akPuSoftDrop6CalobTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop6CaloPatJetPartons = akPuSoftDrop6CalobTagger.PatJetPartons
akPuSoftDrop6CaloJetTracksAssociatorAtVertex = akPuSoftDrop6CalobTagger.JetTracksAssociatorAtVertex
akPuSoftDrop6CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop6CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop6CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop6CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop6CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop6CaloJetBProbabilityBJetTags = akPuSoftDrop6CalobTagger.JetBProbabilityBJetTags
akPuSoftDrop6CaloSoftPFMuonByPtBJetTags = akPuSoftDrop6CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop6CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop6CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop6CaloTrackCountingHighEffBJetTags = akPuSoftDrop6CalobTagger.TrackCountingHighEffBJetTags
akPuSoftDrop6CaloTrackCountingHighPurBJetTags = akPuSoftDrop6CalobTagger.TrackCountingHighPurBJetTags
akPuSoftDrop6CaloPatJetPartonAssociationLegacy = akPuSoftDrop6CalobTagger.PatJetPartonAssociationLegacy

akPuSoftDrop6CaloImpactParameterTagInfos = akPuSoftDrop6CalobTagger.ImpactParameterTagInfos
akPuSoftDrop6CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop6CaloJetProbabilityBJetTags = akPuSoftDrop6CalobTagger.JetProbabilityBJetTags

akPuSoftDrop6CaloSecondaryVertexTagInfos = akPuSoftDrop6CalobTagger.SecondaryVertexTagInfos
akPuSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop6CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop6CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop6CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop6CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop6CaloSecondaryVertexNegativeTagInfos = akPuSoftDrop6CalobTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop6CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop6CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop6CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop6CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop6CaloNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop6CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop6CaloPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop6CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop6CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop6CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop6CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop6CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop6CaloSoftPFMuonsTagInfos = akPuSoftDrop6CalobTagger.SoftPFMuonsTagInfos
akPuSoftDrop6CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop6CaloSoftPFMuonBJetTags = akPuSoftDrop6CalobTagger.SoftPFMuonBJetTags
akPuSoftDrop6CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop6CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop6CaloSoftPFMuonByPtBJetTags = akPuSoftDrop6CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop6CaloNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop6CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop6CaloPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop6CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop6CaloPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop6CaloPatJetPartonAssociationLegacy*akPuSoftDrop6CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop6CaloPatJetFlavourAssociation = akPuSoftDrop6CalobTagger.PatJetFlavourAssociation
#akPuSoftDrop6CaloPatJetFlavourId = cms.Sequence(akPuSoftDrop6CaloPatJetPartons*akPuSoftDrop6CaloPatJetFlavourAssociation)

akPuSoftDrop6CaloJetBtaggingIP       = cms.Sequence(akPuSoftDrop6CaloImpactParameterTagInfos *
            (akPuSoftDrop6CaloTrackCountingHighEffBJetTags +
             akPuSoftDrop6CaloTrackCountingHighPurBJetTags +
             akPuSoftDrop6CaloJetProbabilityBJetTags +
             akPuSoftDrop6CaloJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop6CaloJetBtaggingSV = cms.Sequence(akPuSoftDrop6CaloImpactParameterTagInfos
            *
            akPuSoftDrop6CaloSecondaryVertexTagInfos
            * (akPuSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop6CaloCombinedSecondaryVertexBJetTags+
                akPuSoftDrop6CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop6CaloJetBtaggingNegSV = cms.Sequence(akPuSoftDrop6CaloImpactParameterTagInfos
            *
            akPuSoftDrop6CaloSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop6CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop6CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop6CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop6CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop6CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop6CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop6CaloJetBtaggingMu = cms.Sequence(akPuSoftDrop6CaloSoftPFMuonsTagInfos * (akPuSoftDrop6CaloSoftPFMuonBJetTags
                +
                akPuSoftDrop6CaloSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop6CaloSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop6CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop6CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop6CaloJetBtagging = cms.Sequence(akPuSoftDrop6CaloJetBtaggingIP
            *akPuSoftDrop6CaloJetBtaggingSV
            *akPuSoftDrop6CaloJetBtaggingNegSV
#            *akPuSoftDrop6CaloJetBtaggingMu
            )

akPuSoftDrop6CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop6CaloJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop6Calomatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop6Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop6Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop6CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop6CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop6CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop6CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop6CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop6CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop6CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop6CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop6CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop6CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop6CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop6CaloJetID"),
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

akPuSoftDrop6CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop6CaloJets"),
           	    R0  = cms.double( 0.6)
)
akPuSoftDrop6CalopatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop6CaloNjettiness:tau1','akPuSoftDrop6CaloNjettiness:tau2','akPuSoftDrop6CaloNjettiness:tau3']

akPuSoftDrop6CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop6CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop6Calo"),
                                                             jetName = cms.untracked.string("akPuSoftDrop6Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop6GenJets"),
                                                             doGenTaus = True
                                                             )

akPuSoftDrop6CaloJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop6Caloclean
                                                  #*
                                                  akPuSoftDrop6Calomatch
                                                  #*
                                                  #akPuSoftDrop6CalomatchGroomed
                                                  *
                                                  akPuSoftDrop6Caloparton
                                                  *
                                                  akPuSoftDrop6Calocorr
                                                  *
                                                  #akPuSoftDrop6CaloJetID
                                                  #*
                                                  akPuSoftDrop6CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop6CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop6CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop6CaloJetBtagging
                                                  *
                                                  akPuSoftDrop6CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop6CalopatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop6CaloJetAnalyzer
                                                  )

akPuSoftDrop6CaloJetSequence_data = cms.Sequence(akPuSoftDrop6Calocorr
                                                    *
                                                    #akPuSoftDrop6CaloJetID
                                                    #*
                                                    akPuSoftDrop6CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop6CaloJetBtagging
                                                    *
                                                    akPuSoftDrop6CaloNjettiness 
                                                    *
                                                    akPuSoftDrop6CalopatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop6CaloJetAnalyzer
                                                    )

akPuSoftDrop6CaloJetSequence_jec = cms.Sequence(akPuSoftDrop6CaloJetSequence_mc)
akPuSoftDrop6CaloJetSequence_mb = cms.Sequence(akPuSoftDrop6CaloJetSequence_mc)

akPuSoftDrop6CaloJetSequence = cms.Sequence(akPuSoftDrop6CaloJetSequence_mb)
