

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akSoftDrop2Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop2CaloJets"),
    matched = cms.InputTag("ak2HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akSoftDrop2CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop2HiGenJets"),
    matched = cms.InputTag("ak2HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akSoftDrop2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop2CaloJets")
                                                        )

akSoftDrop2Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akSoftDrop2CaloJets"),
    payload = "AK2Calo_offline"
    )

akSoftDrop2CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akSoftDrop2CaloJets'))

#akSoftDrop2Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2HiCleanedGenJets'))

akSoftDrop2CalobTagger = bTaggers("akSoftDrop2Calo",0.2)

#create objects locally since they dont load properly otherwise
#akSoftDrop2Calomatch = akSoftDrop2CalobTagger.match
akSoftDrop2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop2CaloJets"), matched = cms.InputTag("selectedPartons"))
akSoftDrop2CaloPatJetFlavourAssociationLegacy = akSoftDrop2CalobTagger.PatJetFlavourAssociationLegacy
akSoftDrop2CaloPatJetPartons = akSoftDrop2CalobTagger.PatJetPartons
akSoftDrop2CaloJetTracksAssociatorAtVertex = akSoftDrop2CalobTagger.JetTracksAssociatorAtVertex
akSoftDrop2CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop2CaloCombinedSecondaryVertexBJetTags = akSoftDrop2CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop2CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop2CalobTagger.CombinedSecondaryVertexV2BJetTags
akSoftDrop2CaloJetBProbabilityBJetTags = akSoftDrop2CalobTagger.JetBProbabilityBJetTags
akSoftDrop2CaloSoftPFMuonByPtBJetTags = akSoftDrop2CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop2CaloSoftPFMuonByIP3dBJetTags = akSoftDrop2CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop2CaloTrackCountingHighEffBJetTags = akSoftDrop2CalobTagger.TrackCountingHighEffBJetTags
akSoftDrop2CaloTrackCountingHighPurBJetTags = akSoftDrop2CalobTagger.TrackCountingHighPurBJetTags
akSoftDrop2CaloPatJetPartonAssociationLegacy = akSoftDrop2CalobTagger.PatJetPartonAssociationLegacy

akSoftDrop2CaloImpactParameterTagInfos = akSoftDrop2CalobTagger.ImpactParameterTagInfos
akSoftDrop2CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop2CaloJetProbabilityBJetTags = akSoftDrop2CalobTagger.JetProbabilityBJetTags

akSoftDrop2CaloSecondaryVertexTagInfos = akSoftDrop2CalobTagger.SecondaryVertexTagInfos
akSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop2CaloCombinedSecondaryVertexBJetTags = akSoftDrop2CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop2CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop2CalobTagger.CombinedSecondaryVertexV2BJetTags

akSoftDrop2CaloSecondaryVertexNegativeTagInfos = akSoftDrop2CalobTagger.SecondaryVertexNegativeTagInfos
akSoftDrop2CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akSoftDrop2CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akSoftDrop2CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akSoftDrop2CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akSoftDrop2CaloNegativeCombinedSecondaryVertexBJetTags = akSoftDrop2CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akSoftDrop2CaloPositiveCombinedSecondaryVertexBJetTags = akSoftDrop2CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akSoftDrop2CaloNegativeCombinedSecondaryVertexV2BJetTags = akSoftDrop2CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akSoftDrop2CaloPositiveCombinedSecondaryVertexV2BJetTags = akSoftDrop2CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akSoftDrop2CaloSoftPFMuonsTagInfos = akSoftDrop2CalobTagger.SoftPFMuonsTagInfos
akSoftDrop2CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop2CaloSoftPFMuonBJetTags = akSoftDrop2CalobTagger.SoftPFMuonBJetTags
akSoftDrop2CaloSoftPFMuonByIP3dBJetTags = akSoftDrop2CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop2CaloSoftPFMuonByPtBJetTags = akSoftDrop2CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop2CaloNegativeSoftPFMuonByPtBJetTags = akSoftDrop2CalobTagger.NegativeSoftPFMuonByPtBJetTags
akSoftDrop2CaloPositiveSoftPFMuonByPtBJetTags = akSoftDrop2CalobTagger.PositiveSoftPFMuonByPtBJetTags
akSoftDrop2CaloPatJetFlavourIdLegacy = cms.Sequence(akSoftDrop2CaloPatJetPartonAssociationLegacy*akSoftDrop2CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akSoftDrop2CaloPatJetFlavourAssociation = akSoftDrop2CalobTagger.PatJetFlavourAssociation
#akSoftDrop2CaloPatJetFlavourId = cms.Sequence(akSoftDrop2CaloPatJetPartons*akSoftDrop2CaloPatJetFlavourAssociation)

akSoftDrop2CaloJetBtaggingIP       = cms.Sequence(akSoftDrop2CaloImpactParameterTagInfos *
            (akSoftDrop2CaloTrackCountingHighEffBJetTags +
             akSoftDrop2CaloTrackCountingHighPurBJetTags +
             akSoftDrop2CaloJetProbabilityBJetTags +
             akSoftDrop2CaloJetBProbabilityBJetTags 
            )
            )

akSoftDrop2CaloJetBtaggingSV = cms.Sequence(akSoftDrop2CaloImpactParameterTagInfos
            *
            akSoftDrop2CaloSecondaryVertexTagInfos
            * (akSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop2CaloCombinedSecondaryVertexBJetTags+
                akSoftDrop2CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop2CaloJetBtaggingNegSV = cms.Sequence(akSoftDrop2CaloImpactParameterTagInfos
            *
            akSoftDrop2CaloSecondaryVertexNegativeTagInfos
            * (akSoftDrop2CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop2CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop2CaloNegativeCombinedSecondaryVertexBJetTags+
                akSoftDrop2CaloPositiveCombinedSecondaryVertexBJetTags+
                akSoftDrop2CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akSoftDrop2CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop2CaloJetBtaggingMu = cms.Sequence(akSoftDrop2CaloSoftPFMuonsTagInfos * (akSoftDrop2CaloSoftPFMuonBJetTags
                +
                akSoftDrop2CaloSoftPFMuonByIP3dBJetTags
                +
                akSoftDrop2CaloSoftPFMuonByPtBJetTags
                +
                akSoftDrop2CaloNegativeSoftPFMuonByPtBJetTags
                +
                akSoftDrop2CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akSoftDrop2CaloJetBtagging = cms.Sequence(akSoftDrop2CaloJetBtaggingIP
            *akSoftDrop2CaloJetBtaggingSV
            *akSoftDrop2CaloJetBtaggingNegSV
#            *akSoftDrop2CaloJetBtaggingMu
            )

akSoftDrop2CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akSoftDrop2CaloJets"),
        genJetMatch          = cms.InputTag("akSoftDrop2Calomatch"),
        genPartonMatch       = cms.InputTag("akSoftDrop2Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akSoftDrop2Calocorr")),
        JetPartonMapSource   = cms.InputTag("akSoftDrop2CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akSoftDrop2CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akSoftDrop2CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akSoftDrop2CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akSoftDrop2CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akSoftDrop2CaloJetBProbabilityBJetTags"),
            cms.InputTag("akSoftDrop2CaloJetProbabilityBJetTags"),
            #cms.InputTag("akSoftDrop2CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akSoftDrop2CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akSoftDrop2CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akSoftDrop2CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akSoftDrop2CaloJetID"),
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

akSoftDrop2CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akSoftDrop2CaloJets"),
           	    R0  = cms.double( 0.2)
)
akSoftDrop2CalopatJetsWithBtagging.userData.userFloats.src += ['akSoftDrop2CaloNjettiness:tau1','akSoftDrop2CaloNjettiness:tau2','akSoftDrop2CaloNjettiness:tau3']

akSoftDrop2CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akSoftDrop2CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak2HiGenJets',
                                                             rParam = 0.2,
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
                                                             bTagJetName = cms.untracked.string("akSoftDrop2Calo"),
                                                             jetName = cms.untracked.string("akSoftDrop2Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop2GenJets"),
                                                             doGenTaus = True
                                                             )

akSoftDrop2CaloJetSequence_mc = cms.Sequence(
                                                  #akSoftDrop2Caloclean
                                                  #*
                                                  akSoftDrop2Calomatch
                                                  #*
                                                  #akSoftDrop2CalomatchGroomed
                                                  *
                                                  akSoftDrop2Caloparton
                                                  *
                                                  akSoftDrop2Calocorr
                                                  *
                                                  #akSoftDrop2CaloJetID
                                                  #*
                                                  akSoftDrop2CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akSoftDrop2CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akSoftDrop2CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akSoftDrop2CaloJetBtagging
                                                  *
                                                  akSoftDrop2CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akSoftDrop2CalopatJetsWithBtagging
                                                  *
                                                  akSoftDrop2CaloJetAnalyzer
                                                  )

akSoftDrop2CaloJetSequence_data = cms.Sequence(akSoftDrop2Calocorr
                                                    *
                                                    #akSoftDrop2CaloJetID
                                                    #*
                                                    akSoftDrop2CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akSoftDrop2CaloJetBtagging
                                                    *
                                                    akSoftDrop2CaloNjettiness 
                                                    *
                                                    akSoftDrop2CalopatJetsWithBtagging
                                                    *
                                                    akSoftDrop2CaloJetAnalyzer
                                                    )

akSoftDrop2CaloJetSequence_jec = cms.Sequence(akSoftDrop2CaloJetSequence_mc)
akSoftDrop2CaloJetSequence_mb = cms.Sequence(akSoftDrop2CaloJetSequence_mc)

akSoftDrop2CaloJetSequence = cms.Sequence(akSoftDrop2CaloJetSequence_mb)
