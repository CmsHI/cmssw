

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akSoftDrop5Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop5CaloJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akSoftDrop5CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop5HiGenJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akSoftDrop5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop5CaloJets")
                                                        )

akSoftDrop5Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akSoftDrop5CaloJets"),
    payload = "AK5Calo_offline"
    )

akSoftDrop5CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akSoftDrop5CaloJets'))

#akSoftDrop5Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5HiSignalGenJets'))

akSoftDrop5CalobTagger = bTaggers("akSoftDrop5Calo",0.5)

#create objects locally since they dont load properly otherwise
#akSoftDrop5Calomatch = akSoftDrop5CalobTagger.match
akSoftDrop5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop5CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akSoftDrop5CaloPatJetFlavourAssociationLegacy = akSoftDrop5CalobTagger.PatJetFlavourAssociationLegacy
akSoftDrop5CaloPatJetPartons = akSoftDrop5CalobTagger.PatJetPartons
akSoftDrop5CaloJetTracksAssociatorAtVertex = akSoftDrop5CalobTagger.JetTracksAssociatorAtVertex
akSoftDrop5CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop5CaloCombinedSecondaryVertexBJetTags = akSoftDrop5CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop5CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop5CalobTagger.CombinedSecondaryVertexV2BJetTags
akSoftDrop5CaloJetBProbabilityBJetTags = akSoftDrop5CalobTagger.JetBProbabilityBJetTags
akSoftDrop5CaloSoftPFMuonByPtBJetTags = akSoftDrop5CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop5CaloSoftPFMuonByIP3dBJetTags = akSoftDrop5CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop5CaloTrackCountingHighEffBJetTags = akSoftDrop5CalobTagger.TrackCountingHighEffBJetTags
akSoftDrop5CaloTrackCountingHighPurBJetTags = akSoftDrop5CalobTagger.TrackCountingHighPurBJetTags
akSoftDrop5CaloPatJetPartonAssociationLegacy = akSoftDrop5CalobTagger.PatJetPartonAssociationLegacy

akSoftDrop5CaloImpactParameterTagInfos = akSoftDrop5CalobTagger.ImpactParameterTagInfos
akSoftDrop5CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop5CaloJetProbabilityBJetTags = akSoftDrop5CalobTagger.JetProbabilityBJetTags

akSoftDrop5CaloSecondaryVertexTagInfos = akSoftDrop5CalobTagger.SecondaryVertexTagInfos
akSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop5CaloCombinedSecondaryVertexBJetTags = akSoftDrop5CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop5CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop5CalobTagger.CombinedSecondaryVertexV2BJetTags

akSoftDrop5CaloSecondaryVertexNegativeTagInfos = akSoftDrop5CalobTagger.SecondaryVertexNegativeTagInfos
akSoftDrop5CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akSoftDrop5CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akSoftDrop5CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akSoftDrop5CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akSoftDrop5CaloNegativeCombinedSecondaryVertexBJetTags = akSoftDrop5CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akSoftDrop5CaloPositiveCombinedSecondaryVertexBJetTags = akSoftDrop5CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akSoftDrop5CaloNegativeCombinedSecondaryVertexV2BJetTags = akSoftDrop5CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akSoftDrop5CaloPositiveCombinedSecondaryVertexV2BJetTags = akSoftDrop5CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akSoftDrop5CaloSoftPFMuonsTagInfos = akSoftDrop5CalobTagger.SoftPFMuonsTagInfos
akSoftDrop5CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop5CaloSoftPFMuonBJetTags = akSoftDrop5CalobTagger.SoftPFMuonBJetTags
akSoftDrop5CaloSoftPFMuonByIP3dBJetTags = akSoftDrop5CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop5CaloSoftPFMuonByPtBJetTags = akSoftDrop5CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop5CaloNegativeSoftPFMuonByPtBJetTags = akSoftDrop5CalobTagger.NegativeSoftPFMuonByPtBJetTags
akSoftDrop5CaloPositiveSoftPFMuonByPtBJetTags = akSoftDrop5CalobTagger.PositiveSoftPFMuonByPtBJetTags
akSoftDrop5CaloPatJetFlavourIdLegacy = cms.Sequence(akSoftDrop5CaloPatJetPartonAssociationLegacy*akSoftDrop5CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akSoftDrop5CaloPatJetFlavourAssociation = akSoftDrop5CalobTagger.PatJetFlavourAssociation
#akSoftDrop5CaloPatJetFlavourId = cms.Sequence(akSoftDrop5CaloPatJetPartons*akSoftDrop5CaloPatJetFlavourAssociation)

akSoftDrop5CaloJetBtaggingIP       = cms.Sequence(akSoftDrop5CaloImpactParameterTagInfos *
            (akSoftDrop5CaloTrackCountingHighEffBJetTags +
             akSoftDrop5CaloTrackCountingHighPurBJetTags +
             akSoftDrop5CaloJetProbabilityBJetTags +
             akSoftDrop5CaloJetBProbabilityBJetTags 
            )
            )

akSoftDrop5CaloJetBtaggingSV = cms.Sequence(akSoftDrop5CaloImpactParameterTagInfos
            *
            akSoftDrop5CaloSecondaryVertexTagInfos
            * (akSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop5CaloCombinedSecondaryVertexBJetTags+
                akSoftDrop5CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop5CaloJetBtaggingNegSV = cms.Sequence(akSoftDrop5CaloImpactParameterTagInfos
            *
            akSoftDrop5CaloSecondaryVertexNegativeTagInfos
            * (akSoftDrop5CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop5CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop5CaloNegativeCombinedSecondaryVertexBJetTags+
                akSoftDrop5CaloPositiveCombinedSecondaryVertexBJetTags+
                akSoftDrop5CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akSoftDrop5CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop5CaloJetBtaggingMu = cms.Sequence(akSoftDrop5CaloSoftPFMuonsTagInfos * (akSoftDrop5CaloSoftPFMuonBJetTags
                +
                akSoftDrop5CaloSoftPFMuonByIP3dBJetTags
                +
                akSoftDrop5CaloSoftPFMuonByPtBJetTags
                +
                akSoftDrop5CaloNegativeSoftPFMuonByPtBJetTags
                +
                akSoftDrop5CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akSoftDrop5CaloJetBtagging = cms.Sequence(akSoftDrop5CaloJetBtaggingIP
            *akSoftDrop5CaloJetBtaggingSV
            *akSoftDrop5CaloJetBtaggingNegSV
#            *akSoftDrop5CaloJetBtaggingMu
            )

akSoftDrop5CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akSoftDrop5CaloJets"),
        genJetMatch          = cms.InputTag("akSoftDrop5Calomatch"),
        genPartonMatch       = cms.InputTag("akSoftDrop5Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akSoftDrop5Calocorr")),
        JetPartonMapSource   = cms.InputTag("akSoftDrop5CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akSoftDrop5CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akSoftDrop5CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akSoftDrop5CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akSoftDrop5CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akSoftDrop5CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akSoftDrop5CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akSoftDrop5CaloJetBProbabilityBJetTags"),
            cms.InputTag("akSoftDrop5CaloJetProbabilityBJetTags"),
            #cms.InputTag("akSoftDrop5CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akSoftDrop5CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akSoftDrop5CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akSoftDrop5CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akSoftDrop5CaloJetID"),
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

akSoftDrop5CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akSoftDrop5CaloJets"),
           	    R0  = cms.double( 0.5)
)
akSoftDrop5CalopatJetsWithBtagging.userData.userFloats.src += ['akSoftDrop5CaloNjettiness:tau1','akSoftDrop5CaloNjettiness:tau2','akSoftDrop5CaloNjettiness:tau3']

akSoftDrop5CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akSoftDrop5CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akSoftDrop5Calo"),
                                                             jetName = cms.untracked.string("akSoftDrop5Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(True),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop5GenJets"),
                                                             doGenTaus = True
                                                             )

akSoftDrop5CaloJetSequence_mc = cms.Sequence(
                                                  #akSoftDrop5Caloclean
                                                  #*
                                                  akSoftDrop5Calomatch
                                                  #*
                                                  #akSoftDrop5CalomatchGroomed
                                                  *
                                                  akSoftDrop5Caloparton
                                                  *
                                                  akSoftDrop5Calocorr
                                                  *
                                                  #akSoftDrop5CaloJetID
                                                  #*
                                                  akSoftDrop5CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akSoftDrop5CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akSoftDrop5CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akSoftDrop5CaloJetBtagging
                                                  *
                                                  akSoftDrop5CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akSoftDrop5CalopatJetsWithBtagging
                                                  *
                                                  akSoftDrop5CaloJetAnalyzer
                                                  )

akSoftDrop5CaloJetSequence_data = cms.Sequence(akSoftDrop5Calocorr
                                                    *
                                                    #akSoftDrop5CaloJetID
                                                    #*
                                                    akSoftDrop5CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akSoftDrop5CaloJetBtagging
                                                    *
                                                    akSoftDrop5CaloNjettiness 
                                                    *
                                                    akSoftDrop5CalopatJetsWithBtagging
                                                    *
                                                    akSoftDrop5CaloJetAnalyzer
                                                    )

akSoftDrop5CaloJetSequence_jec = cms.Sequence(akSoftDrop5CaloJetSequence_mc)
akSoftDrop5CaloJetSequence_mb = cms.Sequence(akSoftDrop5CaloJetSequence_mc)

akSoftDrop5CaloJetSequence = cms.Sequence(akSoftDrop5CaloJetSequence_mc)
