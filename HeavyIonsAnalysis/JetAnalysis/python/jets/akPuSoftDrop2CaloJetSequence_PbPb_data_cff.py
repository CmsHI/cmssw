

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop2Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop2CaloJets"),
    matched = cms.InputTag("ak2HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akPuSoftDrop2CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop2HiGenJets"),
    matched = cms.InputTag("ak2HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akPuSoftDrop2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop2CaloJets")
                                                        )

akPuSoftDrop2Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop2CaloJets"),
    payload = "AKPu2Calo_offline"
    )

akPuSoftDrop2CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop2CaloJets'))

#akPuSoftDrop2Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2HiSignalGenJets'))

akPuSoftDrop2CalobTagger = bTaggers("akPuSoftDrop2Calo",0.2)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop2Calomatch = akPuSoftDrop2CalobTagger.match
akPuSoftDrop2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop2CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuSoftDrop2CaloPatJetFlavourAssociationLegacy = akPuSoftDrop2CalobTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop2CaloPatJetPartons = akPuSoftDrop2CalobTagger.PatJetPartons
akPuSoftDrop2CaloJetTracksAssociatorAtVertex = akPuSoftDrop2CalobTagger.JetTracksAssociatorAtVertex
akPuSoftDrop2CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop2CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop2CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop2CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop2CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop2CaloJetBProbabilityBJetTags = akPuSoftDrop2CalobTagger.JetBProbabilityBJetTags
akPuSoftDrop2CaloSoftPFMuonByPtBJetTags = akPuSoftDrop2CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop2CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop2CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop2CaloTrackCountingHighEffBJetTags = akPuSoftDrop2CalobTagger.TrackCountingHighEffBJetTags
akPuSoftDrop2CaloTrackCountingHighPurBJetTags = akPuSoftDrop2CalobTagger.TrackCountingHighPurBJetTags
akPuSoftDrop2CaloPatJetPartonAssociationLegacy = akPuSoftDrop2CalobTagger.PatJetPartonAssociationLegacy

akPuSoftDrop2CaloImpactParameterTagInfos = akPuSoftDrop2CalobTagger.ImpactParameterTagInfos
akPuSoftDrop2CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop2CaloJetProbabilityBJetTags = akPuSoftDrop2CalobTagger.JetProbabilityBJetTags

akPuSoftDrop2CaloSecondaryVertexTagInfos = akPuSoftDrop2CalobTagger.SecondaryVertexTagInfos
akPuSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop2CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop2CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop2CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop2CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop2CaloSecondaryVertexNegativeTagInfos = akPuSoftDrop2CalobTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop2CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop2CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop2CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop2CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop2CaloNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop2CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop2CaloPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop2CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop2CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop2CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop2CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop2CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop2CaloSoftPFMuonsTagInfos = akPuSoftDrop2CalobTagger.SoftPFMuonsTagInfos
akPuSoftDrop2CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop2CaloSoftPFMuonBJetTags = akPuSoftDrop2CalobTagger.SoftPFMuonBJetTags
akPuSoftDrop2CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop2CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop2CaloSoftPFMuonByPtBJetTags = akPuSoftDrop2CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop2CaloNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop2CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop2CaloPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop2CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop2CaloPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop2CaloPatJetPartonAssociationLegacy*akPuSoftDrop2CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop2CaloPatJetFlavourAssociation = akPuSoftDrop2CalobTagger.PatJetFlavourAssociation
#akPuSoftDrop2CaloPatJetFlavourId = cms.Sequence(akPuSoftDrop2CaloPatJetPartons*akPuSoftDrop2CaloPatJetFlavourAssociation)

akPuSoftDrop2CaloJetBtaggingIP       = cms.Sequence(akPuSoftDrop2CaloImpactParameterTagInfos *
            (akPuSoftDrop2CaloTrackCountingHighEffBJetTags +
             akPuSoftDrop2CaloTrackCountingHighPurBJetTags +
             akPuSoftDrop2CaloJetProbabilityBJetTags +
             akPuSoftDrop2CaloJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop2CaloJetBtaggingSV = cms.Sequence(akPuSoftDrop2CaloImpactParameterTagInfos
            *
            akPuSoftDrop2CaloSecondaryVertexTagInfos
            * (akPuSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop2CaloCombinedSecondaryVertexBJetTags+
                akPuSoftDrop2CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop2CaloJetBtaggingNegSV = cms.Sequence(akPuSoftDrop2CaloImpactParameterTagInfos
            *
            akPuSoftDrop2CaloSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop2CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop2CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop2CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop2CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop2CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop2CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop2CaloJetBtaggingMu = cms.Sequence(akPuSoftDrop2CaloSoftPFMuonsTagInfos * (akPuSoftDrop2CaloSoftPFMuonBJetTags
                +
                akPuSoftDrop2CaloSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop2CaloSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop2CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop2CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop2CaloJetBtagging = cms.Sequence(akPuSoftDrop2CaloJetBtaggingIP
            *akPuSoftDrop2CaloJetBtaggingSV
            *akPuSoftDrop2CaloJetBtaggingNegSV
#            *akPuSoftDrop2CaloJetBtaggingMu
            )

akPuSoftDrop2CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop2CaloJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop2Calomatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop2Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop2Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop2CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop2CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop2CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop2CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop2CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop2CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop2CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop2CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop2CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop2CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop2CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop2CaloJetID"),
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

akPuSoftDrop2CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop2CaloJets"),
           	    R0  = cms.double( 0.2)
)
akPuSoftDrop2CalopatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop2CaloNjettiness:tau1','akPuSoftDrop2CaloNjettiness:tau2','akPuSoftDrop2CaloNjettiness:tau3']

akPuSoftDrop2CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop2CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak2HiGenJets',
                                                             rParam = 0.2,
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop2Calo"),
                                                             jetName = cms.untracked.string("akPuSoftDrop2Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop2GenJets"),
                                                             doGenTaus = False
                                                             )

akPuSoftDrop2CaloJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop2Caloclean
                                                  #*
                                                  akPuSoftDrop2Calomatch
                                                  #*
                                                  #akPuSoftDrop2CalomatchGroomed
                                                  *
                                                  akPuSoftDrop2Caloparton
                                                  *
                                                  akPuSoftDrop2Calocorr
                                                  *
                                                  #akPuSoftDrop2CaloJetID
                                                  #*
                                                  akPuSoftDrop2CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop2CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop2CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop2CaloJetBtagging
                                                  *
                                                  akPuSoftDrop2CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop2CalopatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop2CaloJetAnalyzer
                                                  )

akPuSoftDrop2CaloJetSequence_data = cms.Sequence(akPuSoftDrop2Calocorr
                                                    *
                                                    #akPuSoftDrop2CaloJetID
                                                    #*
                                                    akPuSoftDrop2CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop2CaloJetBtagging
                                                    *
                                                    akPuSoftDrop2CaloNjettiness 
                                                    *
                                                    akPuSoftDrop2CalopatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop2CaloJetAnalyzer
                                                    )

akPuSoftDrop2CaloJetSequence_jec = cms.Sequence(akPuSoftDrop2CaloJetSequence_mc)
akPuSoftDrop2CaloJetSequence_mb = cms.Sequence(akPuSoftDrop2CaloJetSequence_mc)

akPuSoftDrop2CaloJetSequence = cms.Sequence(akPuSoftDrop2CaloJetSequence_data)
