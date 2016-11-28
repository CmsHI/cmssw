

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter3Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter3CaloJets"),
    matched = cms.InputTag("ak3HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akPuFilter3CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter3HiGenJets"),
    matched = cms.InputTag("ak3HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akPuFilter3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter3CaloJets")
                                                        )

akPuFilter3Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter3CaloJets"),
    payload = "AKPu3Calo_offline"
    )

akPuFilter3CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter3CaloJets'))

#akPuFilter3Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiSignalGenJets'))

akPuFilter3CalobTagger = bTaggers("akPuFilter3Calo",0.3)

#create objects locally since they dont load properly otherwise
#akPuFilter3Calomatch = akPuFilter3CalobTagger.match
akPuFilter3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter3CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuFilter3CaloPatJetFlavourAssociationLegacy = akPuFilter3CalobTagger.PatJetFlavourAssociationLegacy
akPuFilter3CaloPatJetPartons = akPuFilter3CalobTagger.PatJetPartons
akPuFilter3CaloJetTracksAssociatorAtVertex = akPuFilter3CalobTagger.JetTracksAssociatorAtVertex
akPuFilter3CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter3CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter3CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter3CaloCombinedSecondaryVertexBJetTags = akPuFilter3CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter3CaloCombinedSecondaryVertexV2BJetTags = akPuFilter3CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter3CaloJetBProbabilityBJetTags = akPuFilter3CalobTagger.JetBProbabilityBJetTags
akPuFilter3CaloSoftPFMuonByPtBJetTags = akPuFilter3CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter3CaloSoftPFMuonByIP3dBJetTags = akPuFilter3CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter3CaloTrackCountingHighEffBJetTags = akPuFilter3CalobTagger.TrackCountingHighEffBJetTags
akPuFilter3CaloTrackCountingHighPurBJetTags = akPuFilter3CalobTagger.TrackCountingHighPurBJetTags
akPuFilter3CaloPatJetPartonAssociationLegacy = akPuFilter3CalobTagger.PatJetPartonAssociationLegacy

akPuFilter3CaloImpactParameterTagInfos = akPuFilter3CalobTagger.ImpactParameterTagInfos
akPuFilter3CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter3CaloJetProbabilityBJetTags = akPuFilter3CalobTagger.JetProbabilityBJetTags

akPuFilter3CaloSecondaryVertexTagInfos = akPuFilter3CalobTagger.SecondaryVertexTagInfos
akPuFilter3CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter3CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter3CaloCombinedSecondaryVertexBJetTags = akPuFilter3CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter3CaloCombinedSecondaryVertexV2BJetTags = akPuFilter3CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter3CaloSecondaryVertexNegativeTagInfos = akPuFilter3CalobTagger.SecondaryVertexNegativeTagInfos
akPuFilter3CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter3CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter3CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter3CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter3CaloNegativeCombinedSecondaryVertexBJetTags = akPuFilter3CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter3CaloPositiveCombinedSecondaryVertexBJetTags = akPuFilter3CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter3CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter3CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter3CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter3CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter3CaloSoftPFMuonsTagInfos = akPuFilter3CalobTagger.SoftPFMuonsTagInfos
akPuFilter3CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter3CaloSoftPFMuonBJetTags = akPuFilter3CalobTagger.SoftPFMuonBJetTags
akPuFilter3CaloSoftPFMuonByIP3dBJetTags = akPuFilter3CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter3CaloSoftPFMuonByPtBJetTags = akPuFilter3CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter3CaloNegativeSoftPFMuonByPtBJetTags = akPuFilter3CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter3CaloPositiveSoftPFMuonByPtBJetTags = akPuFilter3CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter3CaloPatJetFlavourIdLegacy = cms.Sequence(akPuFilter3CaloPatJetPartonAssociationLegacy*akPuFilter3CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter3CaloPatJetFlavourAssociation = akPuFilter3CalobTagger.PatJetFlavourAssociation
#akPuFilter3CaloPatJetFlavourId = cms.Sequence(akPuFilter3CaloPatJetPartons*akPuFilter3CaloPatJetFlavourAssociation)

akPuFilter3CaloJetBtaggingIP       = cms.Sequence(akPuFilter3CaloImpactParameterTagInfos *
            (akPuFilter3CaloTrackCountingHighEffBJetTags +
             akPuFilter3CaloTrackCountingHighPurBJetTags +
             akPuFilter3CaloJetProbabilityBJetTags +
             akPuFilter3CaloJetBProbabilityBJetTags 
            )
            )

akPuFilter3CaloJetBtaggingSV = cms.Sequence(akPuFilter3CaloImpactParameterTagInfos
            *
            akPuFilter3CaloSecondaryVertexTagInfos
            * (akPuFilter3CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter3CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter3CaloCombinedSecondaryVertexBJetTags+
                akPuFilter3CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter3CaloJetBtaggingNegSV = cms.Sequence(akPuFilter3CaloImpactParameterTagInfos
            *
            akPuFilter3CaloSecondaryVertexNegativeTagInfos
            * (akPuFilter3CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter3CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter3CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter3CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter3CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter3CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter3CaloJetBtaggingMu = cms.Sequence(akPuFilter3CaloSoftPFMuonsTagInfos * (akPuFilter3CaloSoftPFMuonBJetTags
                +
                akPuFilter3CaloSoftPFMuonByIP3dBJetTags
                +
                akPuFilter3CaloSoftPFMuonByPtBJetTags
                +
                akPuFilter3CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter3CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter3CaloJetBtagging = cms.Sequence(akPuFilter3CaloJetBtaggingIP
            *akPuFilter3CaloJetBtaggingSV
            *akPuFilter3CaloJetBtaggingNegSV
#            *akPuFilter3CaloJetBtaggingMu
            )

akPuFilter3CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter3CaloJets"),
        genJetMatch          = cms.InputTag("akPuFilter3Calomatch"),
        genPartonMatch       = cms.InputTag("akPuFilter3Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter3Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter3CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter3CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter3CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter3CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter3CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter3CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter3CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter3CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter3CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter3CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter3CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter3CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter3CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter3CaloJetID"),
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

akPuFilter3CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter3CaloJets"),
           	    R0  = cms.double( 0.3)
)
akPuFilter3CalopatJetsWithBtagging.userData.userFloats.src += ['akPuFilter3CaloNjettiness:tau1','akPuFilter3CaloNjettiness:tau2','akPuFilter3CaloNjettiness:tau3']

akPuFilter3CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter3CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuFilter3Calo"),
                                                             jetName = cms.untracked.string("akPuFilter3Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter3GenJets"),
                                                             doGenTaus = False
                                                             )

akPuFilter3CaloJetSequence_mc = cms.Sequence(
                                                  #akPuFilter3Caloclean
                                                  #*
                                                  akPuFilter3Calomatch
                                                  #*
                                                  #akPuFilter3CalomatchGroomed
                                                  *
                                                  akPuFilter3Caloparton
                                                  *
                                                  akPuFilter3Calocorr
                                                  *
                                                  #akPuFilter3CaloJetID
                                                  #*
                                                  akPuFilter3CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter3CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter3CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter3CaloJetBtagging
                                                  *
                                                  akPuFilter3CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter3CalopatJetsWithBtagging
                                                  *
                                                  akPuFilter3CaloJetAnalyzer
                                                  )

akPuFilter3CaloJetSequence_data = cms.Sequence(akPuFilter3Calocorr
                                                    *
                                                    #akPuFilter3CaloJetID
                                                    #*
                                                    akPuFilter3CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter3CaloJetBtagging
                                                    *
                                                    akPuFilter3CaloNjettiness 
                                                    *
                                                    akPuFilter3CalopatJetsWithBtagging
                                                    *
                                                    akPuFilter3CaloJetAnalyzer
                                                    )

akPuFilter3CaloJetSequence_jec = cms.Sequence(akPuFilter3CaloJetSequence_mc)
akPuFilter3CaloJetSequence_mb = cms.Sequence(akPuFilter3CaloJetSequence_mc)

akPuFilter3CaloJetSequence = cms.Sequence(akPuFilter3CaloJetSequence_data)
