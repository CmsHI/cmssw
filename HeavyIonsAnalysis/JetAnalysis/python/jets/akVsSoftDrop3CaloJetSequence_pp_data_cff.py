

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop3Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop3CaloJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.3
    )

akVsSoftDrop3CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop3GenJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.3
    )

akVsSoftDrop3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop3CaloJets")
                                                        )

akVsSoftDrop3Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop3CaloJets"),
    payload = "AK3Calo_offline"
    )

akVsSoftDrop3CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop3CaloJets'))

#akVsSoftDrop3Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3GenJets'))

akVsSoftDrop3CalobTagger = bTaggers("akVsSoftDrop3Calo",0.3)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop3Calomatch = akVsSoftDrop3CalobTagger.match
akVsSoftDrop3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop3CaloJets"), matched = cms.InputTag("genParticles"))
akVsSoftDrop3CaloPatJetFlavourAssociationLegacy = akVsSoftDrop3CalobTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop3CaloPatJetPartons = akVsSoftDrop3CalobTagger.PatJetPartons
akVsSoftDrop3CaloJetTracksAssociatorAtVertex = akVsSoftDrop3CalobTagger.JetTracksAssociatorAtVertex
akVsSoftDrop3CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop3CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop3CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop3CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop3CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop3CaloJetBProbabilityBJetTags = akVsSoftDrop3CalobTagger.JetBProbabilityBJetTags
akVsSoftDrop3CaloSoftPFMuonByPtBJetTags = akVsSoftDrop3CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop3CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop3CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop3CaloTrackCountingHighEffBJetTags = akVsSoftDrop3CalobTagger.TrackCountingHighEffBJetTags
akVsSoftDrop3CaloTrackCountingHighPurBJetTags = akVsSoftDrop3CalobTagger.TrackCountingHighPurBJetTags
akVsSoftDrop3CaloPatJetPartonAssociationLegacy = akVsSoftDrop3CalobTagger.PatJetPartonAssociationLegacy

akVsSoftDrop3CaloImpactParameterTagInfos = akVsSoftDrop3CalobTagger.ImpactParameterTagInfos
akVsSoftDrop3CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop3CaloJetProbabilityBJetTags = akVsSoftDrop3CalobTagger.JetProbabilityBJetTags

akVsSoftDrop3CaloSecondaryVertexTagInfos = akVsSoftDrop3CalobTagger.SecondaryVertexTagInfos
akVsSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop3CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop3CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop3CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop3CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop3CaloSecondaryVertexNegativeTagInfos = akVsSoftDrop3CalobTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop3CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop3CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop3CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop3CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop3CaloNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop3CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop3CaloPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop3CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop3CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop3CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop3CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop3CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop3CaloSoftPFMuonsTagInfos = akVsSoftDrop3CalobTagger.SoftPFMuonsTagInfos
akVsSoftDrop3CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop3CaloSoftPFMuonBJetTags = akVsSoftDrop3CalobTagger.SoftPFMuonBJetTags
akVsSoftDrop3CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop3CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop3CaloSoftPFMuonByPtBJetTags = akVsSoftDrop3CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop3CaloNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop3CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop3CaloPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop3CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop3CaloPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop3CaloPatJetPartonAssociationLegacy*akVsSoftDrop3CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop3CaloPatJetFlavourAssociation = akVsSoftDrop3CalobTagger.PatJetFlavourAssociation
#akVsSoftDrop3CaloPatJetFlavourId = cms.Sequence(akVsSoftDrop3CaloPatJetPartons*akVsSoftDrop3CaloPatJetFlavourAssociation)

akVsSoftDrop3CaloJetBtaggingIP       = cms.Sequence(akVsSoftDrop3CaloImpactParameterTagInfos *
            (akVsSoftDrop3CaloTrackCountingHighEffBJetTags +
             akVsSoftDrop3CaloTrackCountingHighPurBJetTags +
             akVsSoftDrop3CaloJetProbabilityBJetTags +
             akVsSoftDrop3CaloJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop3CaloJetBtaggingSV = cms.Sequence(akVsSoftDrop3CaloImpactParameterTagInfos
            *
            akVsSoftDrop3CaloSecondaryVertexTagInfos
            * (akVsSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop3CaloCombinedSecondaryVertexBJetTags+
                akVsSoftDrop3CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop3CaloJetBtaggingNegSV = cms.Sequence(akVsSoftDrop3CaloImpactParameterTagInfos
            *
            akVsSoftDrop3CaloSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop3CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop3CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop3CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop3CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop3CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop3CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop3CaloJetBtaggingMu = cms.Sequence(akVsSoftDrop3CaloSoftPFMuonsTagInfos * (akVsSoftDrop3CaloSoftPFMuonBJetTags
                +
                akVsSoftDrop3CaloSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop3CaloSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop3CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop3CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop3CaloJetBtagging = cms.Sequence(akVsSoftDrop3CaloJetBtaggingIP
            *akVsSoftDrop3CaloJetBtaggingSV
            *akVsSoftDrop3CaloJetBtaggingNegSV
#            *akVsSoftDrop3CaloJetBtaggingMu
            )

akVsSoftDrop3CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop3CaloJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop3Calomatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop3Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop3Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop3CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop3CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop3CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop3CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop3CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop3CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop3CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop3CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop3CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop3CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop3CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop3CaloJetID"),
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

akVsSoftDrop3CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop3CaloJets"),
           	    R0  = cms.double( 0.3)
)
akVsSoftDrop3CalopatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop3CaloNjettiness:tau1','akVsSoftDrop3CaloNjettiness:tau2','akVsSoftDrop3CaloNjettiness:tau3']

akVsSoftDrop3CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop3CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak3GenJets',
                                                             rParam = 0.3,
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop3Calo"),
                                                             jetName = cms.untracked.string("akVsSoftDrop3Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop3GenJets"),
                                                             doGenTaus = False
                                                             )

akVsSoftDrop3CaloJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop3Caloclean
                                                  #*
                                                  akVsSoftDrop3Calomatch
                                                  #*
                                                  #akVsSoftDrop3CalomatchGroomed
                                                  *
                                                  akVsSoftDrop3Caloparton
                                                  *
                                                  akVsSoftDrop3Calocorr
                                                  *
                                                  #akVsSoftDrop3CaloJetID
                                                  #*
                                                  akVsSoftDrop3CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop3CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop3CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop3CaloJetBtagging
                                                  *
                                                  akVsSoftDrop3CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop3CalopatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop3CaloJetAnalyzer
                                                  )

akVsSoftDrop3CaloJetSequence_data = cms.Sequence(akVsSoftDrop3Calocorr
                                                    *
                                                    #akVsSoftDrop3CaloJetID
                                                    #*
                                                    akVsSoftDrop3CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop3CaloJetBtagging
                                                    *
                                                    akVsSoftDrop3CaloNjettiness 
                                                    *
                                                    akVsSoftDrop3CalopatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop3CaloJetAnalyzer
                                                    )

akVsSoftDrop3CaloJetSequence_jec = cms.Sequence(akVsSoftDrop3CaloJetSequence_mc)
akVsSoftDrop3CaloJetSequence_mb = cms.Sequence(akVsSoftDrop3CaloJetSequence_mc)

akVsSoftDrop3CaloJetSequence = cms.Sequence(akVsSoftDrop3CaloJetSequence_data)
