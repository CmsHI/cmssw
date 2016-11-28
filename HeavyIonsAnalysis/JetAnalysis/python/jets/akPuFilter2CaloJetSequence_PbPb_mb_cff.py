

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter2Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter2CaloJets"),
    matched = cms.InputTag("ak2HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akPuFilter2CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter2HiGenJets"),
    matched = cms.InputTag("ak2HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akPuFilter2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter2CaloJets")
                                                        )

akPuFilter2Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter2CaloJets"),
    payload = "AKPu2Calo_offline"
    )

akPuFilter2CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter2CaloJets'))

#akPuFilter2Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2HiCleanedGenJets'))

akPuFilter2CalobTagger = bTaggers("akPuFilter2Calo",0.2)

#create objects locally since they dont load properly otherwise
#akPuFilter2Calomatch = akPuFilter2CalobTagger.match
akPuFilter2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter2CaloJets"), matched = cms.InputTag("selectedPartons"))
akPuFilter2CaloPatJetFlavourAssociationLegacy = akPuFilter2CalobTagger.PatJetFlavourAssociationLegacy
akPuFilter2CaloPatJetPartons = akPuFilter2CalobTagger.PatJetPartons
akPuFilter2CaloJetTracksAssociatorAtVertex = akPuFilter2CalobTagger.JetTracksAssociatorAtVertex
akPuFilter2CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter2CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter2CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter2CaloCombinedSecondaryVertexBJetTags = akPuFilter2CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter2CaloCombinedSecondaryVertexV2BJetTags = akPuFilter2CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter2CaloJetBProbabilityBJetTags = akPuFilter2CalobTagger.JetBProbabilityBJetTags
akPuFilter2CaloSoftPFMuonByPtBJetTags = akPuFilter2CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter2CaloSoftPFMuonByIP3dBJetTags = akPuFilter2CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter2CaloTrackCountingHighEffBJetTags = akPuFilter2CalobTagger.TrackCountingHighEffBJetTags
akPuFilter2CaloTrackCountingHighPurBJetTags = akPuFilter2CalobTagger.TrackCountingHighPurBJetTags
akPuFilter2CaloPatJetPartonAssociationLegacy = akPuFilter2CalobTagger.PatJetPartonAssociationLegacy

akPuFilter2CaloImpactParameterTagInfos = akPuFilter2CalobTagger.ImpactParameterTagInfos
akPuFilter2CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter2CaloJetProbabilityBJetTags = akPuFilter2CalobTagger.JetProbabilityBJetTags

akPuFilter2CaloSecondaryVertexTagInfos = akPuFilter2CalobTagger.SecondaryVertexTagInfos
akPuFilter2CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter2CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter2CaloCombinedSecondaryVertexBJetTags = akPuFilter2CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter2CaloCombinedSecondaryVertexV2BJetTags = akPuFilter2CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter2CaloSecondaryVertexNegativeTagInfos = akPuFilter2CalobTagger.SecondaryVertexNegativeTagInfos
akPuFilter2CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter2CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter2CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter2CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter2CaloNegativeCombinedSecondaryVertexBJetTags = akPuFilter2CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter2CaloPositiveCombinedSecondaryVertexBJetTags = akPuFilter2CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter2CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter2CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter2CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter2CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter2CaloSoftPFMuonsTagInfos = akPuFilter2CalobTagger.SoftPFMuonsTagInfos
akPuFilter2CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter2CaloSoftPFMuonBJetTags = akPuFilter2CalobTagger.SoftPFMuonBJetTags
akPuFilter2CaloSoftPFMuonByIP3dBJetTags = akPuFilter2CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter2CaloSoftPFMuonByPtBJetTags = akPuFilter2CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter2CaloNegativeSoftPFMuonByPtBJetTags = akPuFilter2CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter2CaloPositiveSoftPFMuonByPtBJetTags = akPuFilter2CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter2CaloPatJetFlavourIdLegacy = cms.Sequence(akPuFilter2CaloPatJetPartonAssociationLegacy*akPuFilter2CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter2CaloPatJetFlavourAssociation = akPuFilter2CalobTagger.PatJetFlavourAssociation
#akPuFilter2CaloPatJetFlavourId = cms.Sequence(akPuFilter2CaloPatJetPartons*akPuFilter2CaloPatJetFlavourAssociation)

akPuFilter2CaloJetBtaggingIP       = cms.Sequence(akPuFilter2CaloImpactParameterTagInfos *
            (akPuFilter2CaloTrackCountingHighEffBJetTags +
             akPuFilter2CaloTrackCountingHighPurBJetTags +
             akPuFilter2CaloJetProbabilityBJetTags +
             akPuFilter2CaloJetBProbabilityBJetTags 
            )
            )

akPuFilter2CaloJetBtaggingSV = cms.Sequence(akPuFilter2CaloImpactParameterTagInfos
            *
            akPuFilter2CaloSecondaryVertexTagInfos
            * (akPuFilter2CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter2CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter2CaloCombinedSecondaryVertexBJetTags+
                akPuFilter2CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter2CaloJetBtaggingNegSV = cms.Sequence(akPuFilter2CaloImpactParameterTagInfos
            *
            akPuFilter2CaloSecondaryVertexNegativeTagInfos
            * (akPuFilter2CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter2CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter2CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter2CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter2CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter2CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter2CaloJetBtaggingMu = cms.Sequence(akPuFilter2CaloSoftPFMuonsTagInfos * (akPuFilter2CaloSoftPFMuonBJetTags
                +
                akPuFilter2CaloSoftPFMuonByIP3dBJetTags
                +
                akPuFilter2CaloSoftPFMuonByPtBJetTags
                +
                akPuFilter2CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter2CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter2CaloJetBtagging = cms.Sequence(akPuFilter2CaloJetBtaggingIP
            *akPuFilter2CaloJetBtaggingSV
            *akPuFilter2CaloJetBtaggingNegSV
#            *akPuFilter2CaloJetBtaggingMu
            )

akPuFilter2CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter2CaloJets"),
        genJetMatch          = cms.InputTag("akPuFilter2Calomatch"),
        genPartonMatch       = cms.InputTag("akPuFilter2Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter2Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter2CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter2CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter2CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter2CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter2CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter2CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter2CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter2CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter2CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter2CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter2CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter2CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter2CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter2CaloJetID"),
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

akPuFilter2CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter2CaloJets"),
           	    R0  = cms.double( 0.2)
)
akPuFilter2CalopatJetsWithBtagging.userData.userFloats.src += ['akPuFilter2CaloNjettiness:tau1','akPuFilter2CaloNjettiness:tau2','akPuFilter2CaloNjettiness:tau3']

akPuFilter2CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter2CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuFilter2Calo"),
                                                             jetName = cms.untracked.string("akPuFilter2Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter2GenJets"),
                                                             doGenTaus = True
                                                             )

akPuFilter2CaloJetSequence_mc = cms.Sequence(
                                                  #akPuFilter2Caloclean
                                                  #*
                                                  akPuFilter2Calomatch
                                                  #*
                                                  #akPuFilter2CalomatchGroomed
                                                  *
                                                  akPuFilter2Caloparton
                                                  *
                                                  akPuFilter2Calocorr
                                                  *
                                                  #akPuFilter2CaloJetID
                                                  #*
                                                  akPuFilter2CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter2CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter2CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter2CaloJetBtagging
                                                  *
                                                  akPuFilter2CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter2CalopatJetsWithBtagging
                                                  *
                                                  akPuFilter2CaloJetAnalyzer
                                                  )

akPuFilter2CaloJetSequence_data = cms.Sequence(akPuFilter2Calocorr
                                                    *
                                                    #akPuFilter2CaloJetID
                                                    #*
                                                    akPuFilter2CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter2CaloJetBtagging
                                                    *
                                                    akPuFilter2CaloNjettiness 
                                                    *
                                                    akPuFilter2CalopatJetsWithBtagging
                                                    *
                                                    akPuFilter2CaloJetAnalyzer
                                                    )

akPuFilter2CaloJetSequence_jec = cms.Sequence(akPuFilter2CaloJetSequence_mc)
akPuFilter2CaloJetSequence_mb = cms.Sequence(akPuFilter2CaloJetSequence_mc)

akPuFilter2CaloJetSequence = cms.Sequence(akPuFilter2CaloJetSequence_mb)
