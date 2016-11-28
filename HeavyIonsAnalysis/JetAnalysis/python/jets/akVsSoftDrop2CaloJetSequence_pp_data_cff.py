

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop2Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop2CaloJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.2
    )

akVsSoftDrop2CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop2GenJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.2
    )

akVsSoftDrop2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop2CaloJets")
                                                        )

akVsSoftDrop2Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop2CaloJets"),
    payload = "AK2Calo_offline"
    )

akVsSoftDrop2CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop2CaloJets'))

#akVsSoftDrop2Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2GenJets'))

akVsSoftDrop2CalobTagger = bTaggers("akVsSoftDrop2Calo",0.2)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop2Calomatch = akVsSoftDrop2CalobTagger.match
akVsSoftDrop2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop2CaloJets"), matched = cms.InputTag("genParticles"))
akVsSoftDrop2CaloPatJetFlavourAssociationLegacy = akVsSoftDrop2CalobTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop2CaloPatJetPartons = akVsSoftDrop2CalobTagger.PatJetPartons
akVsSoftDrop2CaloJetTracksAssociatorAtVertex = akVsSoftDrop2CalobTagger.JetTracksAssociatorAtVertex
akVsSoftDrop2CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop2CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop2CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop2CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop2CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop2CaloJetBProbabilityBJetTags = akVsSoftDrop2CalobTagger.JetBProbabilityBJetTags
akVsSoftDrop2CaloSoftPFMuonByPtBJetTags = akVsSoftDrop2CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop2CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop2CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop2CaloTrackCountingHighEffBJetTags = akVsSoftDrop2CalobTagger.TrackCountingHighEffBJetTags
akVsSoftDrop2CaloTrackCountingHighPurBJetTags = akVsSoftDrop2CalobTagger.TrackCountingHighPurBJetTags
akVsSoftDrop2CaloPatJetPartonAssociationLegacy = akVsSoftDrop2CalobTagger.PatJetPartonAssociationLegacy

akVsSoftDrop2CaloImpactParameterTagInfos = akVsSoftDrop2CalobTagger.ImpactParameterTagInfos
akVsSoftDrop2CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop2CaloJetProbabilityBJetTags = akVsSoftDrop2CalobTagger.JetProbabilityBJetTags

akVsSoftDrop2CaloSecondaryVertexTagInfos = akVsSoftDrop2CalobTagger.SecondaryVertexTagInfos
akVsSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop2CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop2CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop2CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop2CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop2CaloSecondaryVertexNegativeTagInfos = akVsSoftDrop2CalobTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop2CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop2CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop2CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop2CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop2CaloNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop2CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop2CaloPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop2CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop2CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop2CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop2CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop2CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop2CaloSoftPFMuonsTagInfos = akVsSoftDrop2CalobTagger.SoftPFMuonsTagInfos
akVsSoftDrop2CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop2CaloSoftPFMuonBJetTags = akVsSoftDrop2CalobTagger.SoftPFMuonBJetTags
akVsSoftDrop2CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop2CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop2CaloSoftPFMuonByPtBJetTags = akVsSoftDrop2CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop2CaloNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop2CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop2CaloPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop2CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop2CaloPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop2CaloPatJetPartonAssociationLegacy*akVsSoftDrop2CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop2CaloPatJetFlavourAssociation = akVsSoftDrop2CalobTagger.PatJetFlavourAssociation
#akVsSoftDrop2CaloPatJetFlavourId = cms.Sequence(akVsSoftDrop2CaloPatJetPartons*akVsSoftDrop2CaloPatJetFlavourAssociation)

akVsSoftDrop2CaloJetBtaggingIP       = cms.Sequence(akVsSoftDrop2CaloImpactParameterTagInfos *
            (akVsSoftDrop2CaloTrackCountingHighEffBJetTags +
             akVsSoftDrop2CaloTrackCountingHighPurBJetTags +
             akVsSoftDrop2CaloJetProbabilityBJetTags +
             akVsSoftDrop2CaloJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop2CaloJetBtaggingSV = cms.Sequence(akVsSoftDrop2CaloImpactParameterTagInfos
            *
            akVsSoftDrop2CaloSecondaryVertexTagInfos
            * (akVsSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop2CaloCombinedSecondaryVertexBJetTags+
                akVsSoftDrop2CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop2CaloJetBtaggingNegSV = cms.Sequence(akVsSoftDrop2CaloImpactParameterTagInfos
            *
            akVsSoftDrop2CaloSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop2CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop2CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop2CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop2CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop2CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop2CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop2CaloJetBtaggingMu = cms.Sequence(akVsSoftDrop2CaloSoftPFMuonsTagInfos * (akVsSoftDrop2CaloSoftPFMuonBJetTags
                +
                akVsSoftDrop2CaloSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop2CaloSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop2CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop2CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop2CaloJetBtagging = cms.Sequence(akVsSoftDrop2CaloJetBtaggingIP
            *akVsSoftDrop2CaloJetBtaggingSV
            *akVsSoftDrop2CaloJetBtaggingNegSV
#            *akVsSoftDrop2CaloJetBtaggingMu
            )

akVsSoftDrop2CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop2CaloJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop2Calomatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop2Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop2Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop2CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop2CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop2CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop2CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop2CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop2CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop2CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop2CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop2CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop2CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop2CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop2CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop2CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop2CaloJetID"),
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

akVsSoftDrop2CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop2CaloJets"),
           	    R0  = cms.double( 0.2)
)
akVsSoftDrop2CalopatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop2CaloNjettiness:tau1','akVsSoftDrop2CaloNjettiness:tau2','akVsSoftDrop2CaloNjettiness:tau3']

akVsSoftDrop2CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop2CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak2GenJets',
                                                             rParam = 0.2,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlow'),
                                                             trackTag = cms.InputTag("generalTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
							     doSubEvent = False,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop2Calo"),
                                                             jetName = cms.untracked.string("akVsSoftDrop2Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop2GenJets"),
                                                             doGenTaus = False
                                                             )

akVsSoftDrop2CaloJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop2Caloclean
                                                  #*
                                                  akVsSoftDrop2Calomatch
                                                  #*
                                                  #akVsSoftDrop2CalomatchGroomed
                                                  *
                                                  akVsSoftDrop2Caloparton
                                                  *
                                                  akVsSoftDrop2Calocorr
                                                  *
                                                  #akVsSoftDrop2CaloJetID
                                                  #*
                                                  akVsSoftDrop2CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop2CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop2CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop2CaloJetBtagging
                                                  *
                                                  akVsSoftDrop2CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop2CalopatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop2CaloJetAnalyzer
                                                  )

akVsSoftDrop2CaloJetSequence_data = cms.Sequence(akVsSoftDrop2Calocorr
                                                    *
                                                    #akVsSoftDrop2CaloJetID
                                                    #*
                                                    akVsSoftDrop2CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop2CaloJetBtagging
                                                    *
                                                    akVsSoftDrop2CaloNjettiness 
                                                    *
                                                    akVsSoftDrop2CalopatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop2CaloJetAnalyzer
                                                    )

akVsSoftDrop2CaloJetSequence_jec = cms.Sequence(akVsSoftDrop2CaloJetSequence_mc)
akVsSoftDrop2CaloJetSequence_mb = cms.Sequence(akVsSoftDrop2CaloJetSequence_mc)

akVsSoftDrop2CaloJetSequence = cms.Sequence(akVsSoftDrop2CaloJetSequence_data)
