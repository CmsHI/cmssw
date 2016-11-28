

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop1Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop1CaloJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.1
    )

akVsSoftDrop1CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop1HiGenJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.1
    )

akVsSoftDrop1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop1CaloJets")
                                                        )

akVsSoftDrop1Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop1CaloJets"),
    payload = "AK1Calo_offline"
    )

akVsSoftDrop1CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop1CaloJets'))

#akVsSoftDrop1Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1HiSignalGenJets'))

akVsSoftDrop1CalobTagger = bTaggers("akVsSoftDrop1Calo",0.1)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop1Calomatch = akVsSoftDrop1CalobTagger.match
akVsSoftDrop1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop1CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akVsSoftDrop1CaloPatJetFlavourAssociationLegacy = akVsSoftDrop1CalobTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop1CaloPatJetPartons = akVsSoftDrop1CalobTagger.PatJetPartons
akVsSoftDrop1CaloJetTracksAssociatorAtVertex = akVsSoftDrop1CalobTagger.JetTracksAssociatorAtVertex
akVsSoftDrop1CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop1CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop1CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop1CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop1CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop1CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop1CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop1CaloJetBProbabilityBJetTags = akVsSoftDrop1CalobTagger.JetBProbabilityBJetTags
akVsSoftDrop1CaloSoftPFMuonByPtBJetTags = akVsSoftDrop1CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop1CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop1CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop1CaloTrackCountingHighEffBJetTags = akVsSoftDrop1CalobTagger.TrackCountingHighEffBJetTags
akVsSoftDrop1CaloTrackCountingHighPurBJetTags = akVsSoftDrop1CalobTagger.TrackCountingHighPurBJetTags
akVsSoftDrop1CaloPatJetPartonAssociationLegacy = akVsSoftDrop1CalobTagger.PatJetPartonAssociationLegacy

akVsSoftDrop1CaloImpactParameterTagInfos = akVsSoftDrop1CalobTagger.ImpactParameterTagInfos
akVsSoftDrop1CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop1CaloJetProbabilityBJetTags = akVsSoftDrop1CalobTagger.JetProbabilityBJetTags

akVsSoftDrop1CaloSecondaryVertexTagInfos = akVsSoftDrop1CalobTagger.SecondaryVertexTagInfos
akVsSoftDrop1CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop1CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop1CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop1CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop1CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop1CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop1CaloSecondaryVertexNegativeTagInfos = akVsSoftDrop1CalobTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop1CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop1CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop1CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop1CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop1CaloNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop1CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop1CaloPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop1CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop1CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop1CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop1CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop1CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop1CaloSoftPFMuonsTagInfos = akVsSoftDrop1CalobTagger.SoftPFMuonsTagInfos
akVsSoftDrop1CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop1CaloSoftPFMuonBJetTags = akVsSoftDrop1CalobTagger.SoftPFMuonBJetTags
akVsSoftDrop1CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop1CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop1CaloSoftPFMuonByPtBJetTags = akVsSoftDrop1CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop1CaloNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop1CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop1CaloPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop1CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop1CaloPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop1CaloPatJetPartonAssociationLegacy*akVsSoftDrop1CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop1CaloPatJetFlavourAssociation = akVsSoftDrop1CalobTagger.PatJetFlavourAssociation
#akVsSoftDrop1CaloPatJetFlavourId = cms.Sequence(akVsSoftDrop1CaloPatJetPartons*akVsSoftDrop1CaloPatJetFlavourAssociation)

akVsSoftDrop1CaloJetBtaggingIP       = cms.Sequence(akVsSoftDrop1CaloImpactParameterTagInfos *
            (akVsSoftDrop1CaloTrackCountingHighEffBJetTags +
             akVsSoftDrop1CaloTrackCountingHighPurBJetTags +
             akVsSoftDrop1CaloJetProbabilityBJetTags +
             akVsSoftDrop1CaloJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop1CaloJetBtaggingSV = cms.Sequence(akVsSoftDrop1CaloImpactParameterTagInfos
            *
            akVsSoftDrop1CaloSecondaryVertexTagInfos
            * (akVsSoftDrop1CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop1CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop1CaloCombinedSecondaryVertexBJetTags+
                akVsSoftDrop1CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop1CaloJetBtaggingNegSV = cms.Sequence(akVsSoftDrop1CaloImpactParameterTagInfos
            *
            akVsSoftDrop1CaloSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop1CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop1CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop1CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop1CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop1CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop1CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop1CaloJetBtaggingMu = cms.Sequence(akVsSoftDrop1CaloSoftPFMuonsTagInfos * (akVsSoftDrop1CaloSoftPFMuonBJetTags
                +
                akVsSoftDrop1CaloSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop1CaloSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop1CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop1CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop1CaloJetBtagging = cms.Sequence(akVsSoftDrop1CaloJetBtaggingIP
            *akVsSoftDrop1CaloJetBtaggingSV
            *akVsSoftDrop1CaloJetBtaggingNegSV
#            *akVsSoftDrop1CaloJetBtaggingMu
            )

akVsSoftDrop1CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop1CaloJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop1Calomatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop1Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop1Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop1CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop1CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop1CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop1CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop1CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop1CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop1CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop1CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop1CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop1CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop1CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop1CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop1CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop1CaloJetID"),
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

akVsSoftDrop1CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop1CaloJets"),
           	    R0  = cms.double( 0.1)
)
akVsSoftDrop1CalopatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop1CaloNjettiness:tau1','akVsSoftDrop1CaloNjettiness:tau2','akVsSoftDrop1CaloNjettiness:tau3']

akVsSoftDrop1CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop1CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop1Calo"),
                                                             jetName = cms.untracked.string("akVsSoftDrop1Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop1GenJets"),
                                                             doGenTaus = False
                                                             )

akVsSoftDrop1CaloJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop1Caloclean
                                                  #*
                                                  akVsSoftDrop1Calomatch
                                                  #*
                                                  #akVsSoftDrop1CalomatchGroomed
                                                  *
                                                  akVsSoftDrop1Caloparton
                                                  *
                                                  akVsSoftDrop1Calocorr
                                                  *
                                                  #akVsSoftDrop1CaloJetID
                                                  #*
                                                  akVsSoftDrop1CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop1CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop1CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop1CaloJetBtagging
                                                  *
                                                  akVsSoftDrop1CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop1CalopatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop1CaloJetAnalyzer
                                                  )

akVsSoftDrop1CaloJetSequence_data = cms.Sequence(akVsSoftDrop1Calocorr
                                                    *
                                                    #akVsSoftDrop1CaloJetID
                                                    #*
                                                    akVsSoftDrop1CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop1CaloJetBtagging
                                                    *
                                                    akVsSoftDrop1CaloNjettiness 
                                                    *
                                                    akVsSoftDrop1CalopatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop1CaloJetAnalyzer
                                                    )

akVsSoftDrop1CaloJetSequence_jec = cms.Sequence(akVsSoftDrop1CaloJetSequence_mc)
akVsSoftDrop1CaloJetSequence_mb = cms.Sequence(akVsSoftDrop1CaloJetSequence_mc)

akVsSoftDrop1CaloJetSequence = cms.Sequence(akVsSoftDrop1CaloJetSequence_data)
