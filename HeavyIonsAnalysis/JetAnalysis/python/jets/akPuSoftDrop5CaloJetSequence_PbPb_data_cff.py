

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop5Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop5CaloJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akPuSoftDrop5CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop5HiGenJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akPuSoftDrop5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop5CaloJets")
                                                        )

akPuSoftDrop5Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop5CaloJets"),
    payload = "AKPu5Calo_offline"
    )

akPuSoftDrop5CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop5CaloJets'))

#akPuSoftDrop5Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5HiSignalGenJets'))

akPuSoftDrop5CalobTagger = bTaggers("akPuSoftDrop5Calo",0.5)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop5Calomatch = akPuSoftDrop5CalobTagger.match
akPuSoftDrop5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop5CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuSoftDrop5CaloPatJetFlavourAssociationLegacy = akPuSoftDrop5CalobTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop5CaloPatJetPartons = akPuSoftDrop5CalobTagger.PatJetPartons
akPuSoftDrop5CaloJetTracksAssociatorAtVertex = akPuSoftDrop5CalobTagger.JetTracksAssociatorAtVertex
akPuSoftDrop5CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop5CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop5CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop5CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop5CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop5CaloJetBProbabilityBJetTags = akPuSoftDrop5CalobTagger.JetBProbabilityBJetTags
akPuSoftDrop5CaloSoftPFMuonByPtBJetTags = akPuSoftDrop5CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop5CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop5CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop5CaloTrackCountingHighEffBJetTags = akPuSoftDrop5CalobTagger.TrackCountingHighEffBJetTags
akPuSoftDrop5CaloTrackCountingHighPurBJetTags = akPuSoftDrop5CalobTagger.TrackCountingHighPurBJetTags
akPuSoftDrop5CaloPatJetPartonAssociationLegacy = akPuSoftDrop5CalobTagger.PatJetPartonAssociationLegacy

akPuSoftDrop5CaloImpactParameterTagInfos = akPuSoftDrop5CalobTagger.ImpactParameterTagInfos
akPuSoftDrop5CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop5CaloJetProbabilityBJetTags = akPuSoftDrop5CalobTagger.JetProbabilityBJetTags

akPuSoftDrop5CaloSecondaryVertexTagInfos = akPuSoftDrop5CalobTagger.SecondaryVertexTagInfos
akPuSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop5CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop5CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop5CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop5CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop5CaloSecondaryVertexNegativeTagInfos = akPuSoftDrop5CalobTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop5CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop5CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop5CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop5CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop5CaloNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop5CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop5CaloPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop5CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop5CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop5CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop5CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop5CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop5CaloSoftPFMuonsTagInfos = akPuSoftDrop5CalobTagger.SoftPFMuonsTagInfos
akPuSoftDrop5CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop5CaloSoftPFMuonBJetTags = akPuSoftDrop5CalobTagger.SoftPFMuonBJetTags
akPuSoftDrop5CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop5CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop5CaloSoftPFMuonByPtBJetTags = akPuSoftDrop5CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop5CaloNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop5CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop5CaloPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop5CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop5CaloPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop5CaloPatJetPartonAssociationLegacy*akPuSoftDrop5CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop5CaloPatJetFlavourAssociation = akPuSoftDrop5CalobTagger.PatJetFlavourAssociation
#akPuSoftDrop5CaloPatJetFlavourId = cms.Sequence(akPuSoftDrop5CaloPatJetPartons*akPuSoftDrop5CaloPatJetFlavourAssociation)

akPuSoftDrop5CaloJetBtaggingIP       = cms.Sequence(akPuSoftDrop5CaloImpactParameterTagInfos *
            (akPuSoftDrop5CaloTrackCountingHighEffBJetTags +
             akPuSoftDrop5CaloTrackCountingHighPurBJetTags +
             akPuSoftDrop5CaloJetProbabilityBJetTags +
             akPuSoftDrop5CaloJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop5CaloJetBtaggingSV = cms.Sequence(akPuSoftDrop5CaloImpactParameterTagInfos
            *
            akPuSoftDrop5CaloSecondaryVertexTagInfos
            * (akPuSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop5CaloCombinedSecondaryVertexBJetTags+
                akPuSoftDrop5CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop5CaloJetBtaggingNegSV = cms.Sequence(akPuSoftDrop5CaloImpactParameterTagInfos
            *
            akPuSoftDrop5CaloSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop5CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop5CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop5CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop5CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop5CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop5CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop5CaloJetBtaggingMu = cms.Sequence(akPuSoftDrop5CaloSoftPFMuonsTagInfos * (akPuSoftDrop5CaloSoftPFMuonBJetTags
                +
                akPuSoftDrop5CaloSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop5CaloSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop5CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop5CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop5CaloJetBtagging = cms.Sequence(akPuSoftDrop5CaloJetBtaggingIP
            *akPuSoftDrop5CaloJetBtaggingSV
            *akPuSoftDrop5CaloJetBtaggingNegSV
#            *akPuSoftDrop5CaloJetBtaggingMu
            )

akPuSoftDrop5CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop5CaloJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop5Calomatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop5Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop5Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop5CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop5CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop5CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop5CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop5CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop5CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop5CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop5CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop5CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop5CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop5CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop5CaloJetID"),
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

akPuSoftDrop5CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop5CaloJets"),
           	    R0  = cms.double( 0.5)
)
akPuSoftDrop5CalopatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop5CaloNjettiness:tau1','akPuSoftDrop5CaloNjettiness:tau2','akPuSoftDrop5CaloNjettiness:tau3']

akPuSoftDrop5CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop5CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak5HiGenJets',
                                                             rParam = 0.5,
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop5Calo"),
                                                             jetName = cms.untracked.string("akPuSoftDrop5Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop5GenJets"),
                                                             doGenTaus = False
                                                             )

akPuSoftDrop5CaloJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop5Caloclean
                                                  #*
                                                  akPuSoftDrop5Calomatch
                                                  #*
                                                  #akPuSoftDrop5CalomatchGroomed
                                                  *
                                                  akPuSoftDrop5Caloparton
                                                  *
                                                  akPuSoftDrop5Calocorr
                                                  *
                                                  #akPuSoftDrop5CaloJetID
                                                  #*
                                                  akPuSoftDrop5CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop5CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop5CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop5CaloJetBtagging
                                                  *
                                                  akPuSoftDrop5CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop5CalopatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop5CaloJetAnalyzer
                                                  )

akPuSoftDrop5CaloJetSequence_data = cms.Sequence(akPuSoftDrop5Calocorr
                                                    *
                                                    #akPuSoftDrop5CaloJetID
                                                    #*
                                                    akPuSoftDrop5CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop5CaloJetBtagging
                                                    *
                                                    akPuSoftDrop5CaloNjettiness 
                                                    *
                                                    akPuSoftDrop5CalopatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop5CaloJetAnalyzer
                                                    )

akPuSoftDrop5CaloJetSequence_jec = cms.Sequence(akPuSoftDrop5CaloJetSequence_mc)
akPuSoftDrop5CaloJetSequence_mb = cms.Sequence(akPuSoftDrop5CaloJetSequence_mc)

akPuSoftDrop5CaloJetSequence = cms.Sequence(akPuSoftDrop5CaloJetSequence_data)
