

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop5Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop5CaloJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.5
    )

akVsSoftDrop5CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop5HiGenJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.5
    )

akVsSoftDrop5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop5CaloJets")
                                                        )

akVsSoftDrop5Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop5CaloJets"),
    payload = "AK5Calo_offline"
    )

akVsSoftDrop5CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop5CaloJets'))

#akVsSoftDrop5Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5HiSignalGenJets'))

akVsSoftDrop5CalobTagger = bTaggers("akVsSoftDrop5Calo",0.5)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop5Calomatch = akVsSoftDrop5CalobTagger.match
akVsSoftDrop5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop5CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akVsSoftDrop5CaloPatJetFlavourAssociationLegacy = akVsSoftDrop5CalobTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop5CaloPatJetPartons = akVsSoftDrop5CalobTagger.PatJetPartons
akVsSoftDrop5CaloJetTracksAssociatorAtVertex = akVsSoftDrop5CalobTagger.JetTracksAssociatorAtVertex
akVsSoftDrop5CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop5CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop5CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop5CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop5CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop5CaloJetBProbabilityBJetTags = akVsSoftDrop5CalobTagger.JetBProbabilityBJetTags
akVsSoftDrop5CaloSoftPFMuonByPtBJetTags = akVsSoftDrop5CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop5CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop5CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop5CaloTrackCountingHighEffBJetTags = akVsSoftDrop5CalobTagger.TrackCountingHighEffBJetTags
akVsSoftDrop5CaloTrackCountingHighPurBJetTags = akVsSoftDrop5CalobTagger.TrackCountingHighPurBJetTags
akVsSoftDrop5CaloPatJetPartonAssociationLegacy = akVsSoftDrop5CalobTagger.PatJetPartonAssociationLegacy

akVsSoftDrop5CaloImpactParameterTagInfos = akVsSoftDrop5CalobTagger.ImpactParameterTagInfos
akVsSoftDrop5CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop5CaloJetProbabilityBJetTags = akVsSoftDrop5CalobTagger.JetProbabilityBJetTags

akVsSoftDrop5CaloSecondaryVertexTagInfos = akVsSoftDrop5CalobTagger.SecondaryVertexTagInfos
akVsSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop5CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop5CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop5CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop5CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop5CaloSecondaryVertexNegativeTagInfos = akVsSoftDrop5CalobTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop5CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop5CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop5CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop5CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop5CaloNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop5CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop5CaloPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop5CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop5CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop5CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop5CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop5CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop5CaloSoftPFMuonsTagInfos = akVsSoftDrop5CalobTagger.SoftPFMuonsTagInfos
akVsSoftDrop5CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop5CaloSoftPFMuonBJetTags = akVsSoftDrop5CalobTagger.SoftPFMuonBJetTags
akVsSoftDrop5CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop5CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop5CaloSoftPFMuonByPtBJetTags = akVsSoftDrop5CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop5CaloNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop5CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop5CaloPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop5CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop5CaloPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop5CaloPatJetPartonAssociationLegacy*akVsSoftDrop5CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop5CaloPatJetFlavourAssociation = akVsSoftDrop5CalobTagger.PatJetFlavourAssociation
#akVsSoftDrop5CaloPatJetFlavourId = cms.Sequence(akVsSoftDrop5CaloPatJetPartons*akVsSoftDrop5CaloPatJetFlavourAssociation)

akVsSoftDrop5CaloJetBtaggingIP       = cms.Sequence(akVsSoftDrop5CaloImpactParameterTagInfos *
            (akVsSoftDrop5CaloTrackCountingHighEffBJetTags +
             akVsSoftDrop5CaloTrackCountingHighPurBJetTags +
             akVsSoftDrop5CaloJetProbabilityBJetTags +
             akVsSoftDrop5CaloJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop5CaloJetBtaggingSV = cms.Sequence(akVsSoftDrop5CaloImpactParameterTagInfos
            *
            akVsSoftDrop5CaloSecondaryVertexTagInfos
            * (akVsSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop5CaloCombinedSecondaryVertexBJetTags+
                akVsSoftDrop5CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop5CaloJetBtaggingNegSV = cms.Sequence(akVsSoftDrop5CaloImpactParameterTagInfos
            *
            akVsSoftDrop5CaloSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop5CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop5CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop5CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop5CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop5CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop5CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop5CaloJetBtaggingMu = cms.Sequence(akVsSoftDrop5CaloSoftPFMuonsTagInfos * (akVsSoftDrop5CaloSoftPFMuonBJetTags
                +
                akVsSoftDrop5CaloSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop5CaloSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop5CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop5CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop5CaloJetBtagging = cms.Sequence(akVsSoftDrop5CaloJetBtaggingIP
            *akVsSoftDrop5CaloJetBtaggingSV
            *akVsSoftDrop5CaloJetBtaggingNegSV
#            *akVsSoftDrop5CaloJetBtaggingMu
            )

akVsSoftDrop5CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop5CaloJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop5Calomatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop5Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop5Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop5CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop5CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop5CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop5CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop5CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop5CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop5CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop5CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop5CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop5CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop5CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop5CaloJetID"),
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

akVsSoftDrop5CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop5CaloJets"),
           	    R0  = cms.double( 0.5)
)
akVsSoftDrop5CalopatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop5CaloNjettiness:tau1','akVsSoftDrop5CaloNjettiness:tau2','akVsSoftDrop5CaloNjettiness:tau3']

akVsSoftDrop5CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop5CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak5HiGenJets',
                                                             rParam = 0.5,
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop5Calo"),
                                                             jetName = cms.untracked.string("akVsSoftDrop5Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop5GenJets"),
                                                             doGenTaus = True
                                                             )

akVsSoftDrop5CaloJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop5Caloclean
                                                  #*
                                                  akVsSoftDrop5Calomatch
                                                  #*
                                                  #akVsSoftDrop5CalomatchGroomed
                                                  *
                                                  akVsSoftDrop5Caloparton
                                                  *
                                                  akVsSoftDrop5Calocorr
                                                  *
                                                  #akVsSoftDrop5CaloJetID
                                                  #*
                                                  akVsSoftDrop5CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop5CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop5CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop5CaloJetBtagging
                                                  *
                                                  akVsSoftDrop5CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop5CalopatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop5CaloJetAnalyzer
                                                  )

akVsSoftDrop5CaloJetSequence_data = cms.Sequence(akVsSoftDrop5Calocorr
                                                    *
                                                    #akVsSoftDrop5CaloJetID
                                                    #*
                                                    akVsSoftDrop5CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop5CaloJetBtagging
                                                    *
                                                    akVsSoftDrop5CaloNjettiness 
                                                    *
                                                    akVsSoftDrop5CalopatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop5CaloJetAnalyzer
                                                    )

akVsSoftDrop5CaloJetSequence_jec = cms.Sequence(akVsSoftDrop5CaloJetSequence_mc)
akVsSoftDrop5CaloJetSequence_mb = cms.Sequence(akVsSoftDrop5CaloJetSequence_mc)

akVsSoftDrop5CaloJetSequence = cms.Sequence(akVsSoftDrop5CaloJetSequence_jec)
akVsSoftDrop5CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akVsSoftDrop5CaloJetAnalyzer.jetPtMin = cms.double(1)
