

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop3Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop3CaloJets"),
    matched = cms.InputTag("ak3HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akPuSoftDrop3CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop3HiGenJets"),
    matched = cms.InputTag("ak3HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akPuSoftDrop3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop3CaloJets")
                                                        )

akPuSoftDrop3Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop3CaloJets"),
    payload = "AKPu3Calo_offline"
    )

akPuSoftDrop3CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop3CaloJets'))

#akPuSoftDrop3Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiSignalGenJets'))

akPuSoftDrop3CalobTagger = bTaggers("akPuSoftDrop3Calo",0.3)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop3Calomatch = akPuSoftDrop3CalobTagger.match
akPuSoftDrop3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop3CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuSoftDrop3CaloPatJetFlavourAssociationLegacy = akPuSoftDrop3CalobTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop3CaloPatJetPartons = akPuSoftDrop3CalobTagger.PatJetPartons
akPuSoftDrop3CaloJetTracksAssociatorAtVertex = akPuSoftDrop3CalobTagger.JetTracksAssociatorAtVertex
akPuSoftDrop3CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop3CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop3CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop3CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop3CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop3CaloJetBProbabilityBJetTags = akPuSoftDrop3CalobTagger.JetBProbabilityBJetTags
akPuSoftDrop3CaloSoftPFMuonByPtBJetTags = akPuSoftDrop3CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop3CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop3CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop3CaloTrackCountingHighEffBJetTags = akPuSoftDrop3CalobTagger.TrackCountingHighEffBJetTags
akPuSoftDrop3CaloTrackCountingHighPurBJetTags = akPuSoftDrop3CalobTagger.TrackCountingHighPurBJetTags
akPuSoftDrop3CaloPatJetPartonAssociationLegacy = akPuSoftDrop3CalobTagger.PatJetPartonAssociationLegacy

akPuSoftDrop3CaloImpactParameterTagInfos = akPuSoftDrop3CalobTagger.ImpactParameterTagInfos
akPuSoftDrop3CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop3CaloJetProbabilityBJetTags = akPuSoftDrop3CalobTagger.JetProbabilityBJetTags

akPuSoftDrop3CaloSecondaryVertexTagInfos = akPuSoftDrop3CalobTagger.SecondaryVertexTagInfos
akPuSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop3CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop3CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop3CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop3CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop3CaloSecondaryVertexNegativeTagInfos = akPuSoftDrop3CalobTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop3CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop3CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop3CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop3CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop3CaloNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop3CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop3CaloPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop3CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop3CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop3CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop3CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop3CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop3CaloSoftPFMuonsTagInfos = akPuSoftDrop3CalobTagger.SoftPFMuonsTagInfos
akPuSoftDrop3CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop3CaloSoftPFMuonBJetTags = akPuSoftDrop3CalobTagger.SoftPFMuonBJetTags
akPuSoftDrop3CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop3CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop3CaloSoftPFMuonByPtBJetTags = akPuSoftDrop3CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop3CaloNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop3CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop3CaloPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop3CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop3CaloPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop3CaloPatJetPartonAssociationLegacy*akPuSoftDrop3CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop3CaloPatJetFlavourAssociation = akPuSoftDrop3CalobTagger.PatJetFlavourAssociation
#akPuSoftDrop3CaloPatJetFlavourId = cms.Sequence(akPuSoftDrop3CaloPatJetPartons*akPuSoftDrop3CaloPatJetFlavourAssociation)

akPuSoftDrop3CaloJetBtaggingIP       = cms.Sequence(akPuSoftDrop3CaloImpactParameterTagInfos *
            (akPuSoftDrop3CaloTrackCountingHighEffBJetTags +
             akPuSoftDrop3CaloTrackCountingHighPurBJetTags +
             akPuSoftDrop3CaloJetProbabilityBJetTags +
             akPuSoftDrop3CaloJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop3CaloJetBtaggingSV = cms.Sequence(akPuSoftDrop3CaloImpactParameterTagInfos
            *
            akPuSoftDrop3CaloSecondaryVertexTagInfos
            * (akPuSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop3CaloCombinedSecondaryVertexBJetTags+
                akPuSoftDrop3CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop3CaloJetBtaggingNegSV = cms.Sequence(akPuSoftDrop3CaloImpactParameterTagInfos
            *
            akPuSoftDrop3CaloSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop3CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop3CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop3CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop3CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop3CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop3CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop3CaloJetBtaggingMu = cms.Sequence(akPuSoftDrop3CaloSoftPFMuonsTagInfos * (akPuSoftDrop3CaloSoftPFMuonBJetTags
                +
                akPuSoftDrop3CaloSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop3CaloSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop3CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop3CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop3CaloJetBtagging = cms.Sequence(akPuSoftDrop3CaloJetBtaggingIP
            *akPuSoftDrop3CaloJetBtaggingSV
            *akPuSoftDrop3CaloJetBtaggingNegSV
#            *akPuSoftDrop3CaloJetBtaggingMu
            )

akPuSoftDrop3CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop3CaloJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop3Calomatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop3Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop3Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop3CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop3CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop3CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop3CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop3CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop3CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop3CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop3CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop3CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop3CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop3CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop3CaloJetID"),
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

akPuSoftDrop3CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop3CaloJets"),
           	    R0  = cms.double( 0.3)
)
akPuSoftDrop3CalopatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop3CaloNjettiness:tau1','akPuSoftDrop3CaloNjettiness:tau2','akPuSoftDrop3CaloNjettiness:tau3']

akPuSoftDrop3CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop3CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak3HiGenJets',
                                                             rParam = 0.3,
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop3Calo"),
                                                             jetName = cms.untracked.string("akPuSoftDrop3Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop3GenJets"),
                                                             doGenTaus = False
                                                             )

akPuSoftDrop3CaloJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop3Caloclean
                                                  #*
                                                  akPuSoftDrop3Calomatch
                                                  #*
                                                  #akPuSoftDrop3CalomatchGroomed
                                                  *
                                                  akPuSoftDrop3Caloparton
                                                  *
                                                  akPuSoftDrop3Calocorr
                                                  *
                                                  #akPuSoftDrop3CaloJetID
                                                  #*
                                                  akPuSoftDrop3CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop3CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop3CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop3CaloJetBtagging
                                                  *
                                                  akPuSoftDrop3CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop3CalopatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop3CaloJetAnalyzer
                                                  )

akPuSoftDrop3CaloJetSequence_data = cms.Sequence(akPuSoftDrop3Calocorr
                                                    *
                                                    #akPuSoftDrop3CaloJetID
                                                    #*
                                                    akPuSoftDrop3CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop3CaloJetBtagging
                                                    *
                                                    akPuSoftDrop3CaloNjettiness 
                                                    *
                                                    akPuSoftDrop3CalopatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop3CaloJetAnalyzer
                                                    )

akPuSoftDrop3CaloJetSequence_jec = cms.Sequence(akPuSoftDrop3CaloJetSequence_mc)
akPuSoftDrop3CaloJetSequence_mb = cms.Sequence(akPuSoftDrop3CaloJetSequence_mc)

akPuSoftDrop3CaloJetSequence = cms.Sequence(akPuSoftDrop3CaloJetSequence_data)
