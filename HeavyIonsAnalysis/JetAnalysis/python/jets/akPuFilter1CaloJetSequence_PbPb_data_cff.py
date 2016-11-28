

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter1Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter1CaloJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akPuFilter1CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter1HiGenJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akPuFilter1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter1CaloJets")
                                                        )

akPuFilter1Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter1CaloJets"),
    payload = "AKPu1Calo_offline"
    )

akPuFilter1CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter1CaloJets'))

#akPuFilter1Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1HiSignalGenJets'))

akPuFilter1CalobTagger = bTaggers("akPuFilter1Calo",0.1)

#create objects locally since they dont load properly otherwise
#akPuFilter1Calomatch = akPuFilter1CalobTagger.match
akPuFilter1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter1CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuFilter1CaloPatJetFlavourAssociationLegacy = akPuFilter1CalobTagger.PatJetFlavourAssociationLegacy
akPuFilter1CaloPatJetPartons = akPuFilter1CalobTagger.PatJetPartons
akPuFilter1CaloJetTracksAssociatorAtVertex = akPuFilter1CalobTagger.JetTracksAssociatorAtVertex
akPuFilter1CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter1CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter1CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter1CaloCombinedSecondaryVertexBJetTags = akPuFilter1CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter1CaloCombinedSecondaryVertexV2BJetTags = akPuFilter1CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter1CaloJetBProbabilityBJetTags = akPuFilter1CalobTagger.JetBProbabilityBJetTags
akPuFilter1CaloSoftPFMuonByPtBJetTags = akPuFilter1CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter1CaloSoftPFMuonByIP3dBJetTags = akPuFilter1CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter1CaloTrackCountingHighEffBJetTags = akPuFilter1CalobTagger.TrackCountingHighEffBJetTags
akPuFilter1CaloTrackCountingHighPurBJetTags = akPuFilter1CalobTagger.TrackCountingHighPurBJetTags
akPuFilter1CaloPatJetPartonAssociationLegacy = akPuFilter1CalobTagger.PatJetPartonAssociationLegacy

akPuFilter1CaloImpactParameterTagInfos = akPuFilter1CalobTagger.ImpactParameterTagInfos
akPuFilter1CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter1CaloJetProbabilityBJetTags = akPuFilter1CalobTagger.JetProbabilityBJetTags

akPuFilter1CaloSecondaryVertexTagInfos = akPuFilter1CalobTagger.SecondaryVertexTagInfos
akPuFilter1CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter1CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter1CaloCombinedSecondaryVertexBJetTags = akPuFilter1CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter1CaloCombinedSecondaryVertexV2BJetTags = akPuFilter1CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter1CaloSecondaryVertexNegativeTagInfos = akPuFilter1CalobTagger.SecondaryVertexNegativeTagInfos
akPuFilter1CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter1CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter1CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter1CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter1CaloNegativeCombinedSecondaryVertexBJetTags = akPuFilter1CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter1CaloPositiveCombinedSecondaryVertexBJetTags = akPuFilter1CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter1CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter1CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter1CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter1CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter1CaloSoftPFMuonsTagInfos = akPuFilter1CalobTagger.SoftPFMuonsTagInfos
akPuFilter1CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter1CaloSoftPFMuonBJetTags = akPuFilter1CalobTagger.SoftPFMuonBJetTags
akPuFilter1CaloSoftPFMuonByIP3dBJetTags = akPuFilter1CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter1CaloSoftPFMuonByPtBJetTags = akPuFilter1CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter1CaloNegativeSoftPFMuonByPtBJetTags = akPuFilter1CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter1CaloPositiveSoftPFMuonByPtBJetTags = akPuFilter1CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter1CaloPatJetFlavourIdLegacy = cms.Sequence(akPuFilter1CaloPatJetPartonAssociationLegacy*akPuFilter1CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter1CaloPatJetFlavourAssociation = akPuFilter1CalobTagger.PatJetFlavourAssociation
#akPuFilter1CaloPatJetFlavourId = cms.Sequence(akPuFilter1CaloPatJetPartons*akPuFilter1CaloPatJetFlavourAssociation)

akPuFilter1CaloJetBtaggingIP       = cms.Sequence(akPuFilter1CaloImpactParameterTagInfos *
            (akPuFilter1CaloTrackCountingHighEffBJetTags +
             akPuFilter1CaloTrackCountingHighPurBJetTags +
             akPuFilter1CaloJetProbabilityBJetTags +
             akPuFilter1CaloJetBProbabilityBJetTags 
            )
            )

akPuFilter1CaloJetBtaggingSV = cms.Sequence(akPuFilter1CaloImpactParameterTagInfos
            *
            akPuFilter1CaloSecondaryVertexTagInfos
            * (akPuFilter1CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter1CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter1CaloCombinedSecondaryVertexBJetTags+
                akPuFilter1CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter1CaloJetBtaggingNegSV = cms.Sequence(akPuFilter1CaloImpactParameterTagInfos
            *
            akPuFilter1CaloSecondaryVertexNegativeTagInfos
            * (akPuFilter1CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter1CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter1CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter1CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter1CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter1CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter1CaloJetBtaggingMu = cms.Sequence(akPuFilter1CaloSoftPFMuonsTagInfos * (akPuFilter1CaloSoftPFMuonBJetTags
                +
                akPuFilter1CaloSoftPFMuonByIP3dBJetTags
                +
                akPuFilter1CaloSoftPFMuonByPtBJetTags
                +
                akPuFilter1CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter1CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter1CaloJetBtagging = cms.Sequence(akPuFilter1CaloJetBtaggingIP
            *akPuFilter1CaloJetBtaggingSV
            *akPuFilter1CaloJetBtaggingNegSV
#            *akPuFilter1CaloJetBtaggingMu
            )

akPuFilter1CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter1CaloJets"),
        genJetMatch          = cms.InputTag("akPuFilter1Calomatch"),
        genPartonMatch       = cms.InputTag("akPuFilter1Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter1Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter1CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter1CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter1CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter1CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter1CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter1CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter1CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter1CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter1CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter1CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter1CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter1CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter1CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter1CaloJetID"),
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

akPuFilter1CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter1CaloJets"),
           	    R0  = cms.double( 0.1)
)
akPuFilter1CalopatJetsWithBtagging.userData.userFloats.src += ['akPuFilter1CaloNjettiness:tau1','akPuFilter1CaloNjettiness:tau2','akPuFilter1CaloNjettiness:tau3']

akPuFilter1CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter1CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak1HiGenJets',
                                                             rParam = 0.1,
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
                                                             bTagJetName = cms.untracked.string("akPuFilter1Calo"),
                                                             jetName = cms.untracked.string("akPuFilter1Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter1GenJets"),
                                                             doGenTaus = False
                                                             )

akPuFilter1CaloJetSequence_mc = cms.Sequence(
                                                  #akPuFilter1Caloclean
                                                  #*
                                                  akPuFilter1Calomatch
                                                  #*
                                                  #akPuFilter1CalomatchGroomed
                                                  *
                                                  akPuFilter1Caloparton
                                                  *
                                                  akPuFilter1Calocorr
                                                  *
                                                  #akPuFilter1CaloJetID
                                                  #*
                                                  akPuFilter1CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter1CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter1CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter1CaloJetBtagging
                                                  *
                                                  akPuFilter1CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter1CalopatJetsWithBtagging
                                                  *
                                                  akPuFilter1CaloJetAnalyzer
                                                  )

akPuFilter1CaloJetSequence_data = cms.Sequence(akPuFilter1Calocorr
                                                    *
                                                    #akPuFilter1CaloJetID
                                                    #*
                                                    akPuFilter1CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter1CaloJetBtagging
                                                    *
                                                    akPuFilter1CaloNjettiness 
                                                    *
                                                    akPuFilter1CalopatJetsWithBtagging
                                                    *
                                                    akPuFilter1CaloJetAnalyzer
                                                    )

akPuFilter1CaloJetSequence_jec = cms.Sequence(akPuFilter1CaloJetSequence_mc)
akPuFilter1CaloJetSequence_mb = cms.Sequence(akPuFilter1CaloJetSequence_mc)

akPuFilter1CaloJetSequence = cms.Sequence(akPuFilter1CaloJetSequence_data)
