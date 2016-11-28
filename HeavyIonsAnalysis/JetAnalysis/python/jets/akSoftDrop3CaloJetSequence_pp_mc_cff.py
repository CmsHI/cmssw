

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akSoftDrop3Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop3CaloJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akSoftDrop3CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop3GenJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akSoftDrop3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop3CaloJets")
                                                        )

akSoftDrop3Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akSoftDrop3CaloJets"),
    payload = "AK3Calo_offline"
    )

akSoftDrop3CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akSoftDrop3CaloJets'))

#akSoftDrop3Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3GenJets'))

akSoftDrop3CalobTagger = bTaggers("akSoftDrop3Calo",0.3)

#create objects locally since they dont load properly otherwise
#akSoftDrop3Calomatch = akSoftDrop3CalobTagger.match
akSoftDrop3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop3CaloJets"), matched = cms.InputTag("genParticles"))
akSoftDrop3CaloPatJetFlavourAssociationLegacy = akSoftDrop3CalobTagger.PatJetFlavourAssociationLegacy
akSoftDrop3CaloPatJetPartons = akSoftDrop3CalobTagger.PatJetPartons
akSoftDrop3CaloJetTracksAssociatorAtVertex = akSoftDrop3CalobTagger.JetTracksAssociatorAtVertex
akSoftDrop3CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop3CaloCombinedSecondaryVertexBJetTags = akSoftDrop3CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop3CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop3CalobTagger.CombinedSecondaryVertexV2BJetTags
akSoftDrop3CaloJetBProbabilityBJetTags = akSoftDrop3CalobTagger.JetBProbabilityBJetTags
akSoftDrop3CaloSoftPFMuonByPtBJetTags = akSoftDrop3CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop3CaloSoftPFMuonByIP3dBJetTags = akSoftDrop3CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop3CaloTrackCountingHighEffBJetTags = akSoftDrop3CalobTagger.TrackCountingHighEffBJetTags
akSoftDrop3CaloTrackCountingHighPurBJetTags = akSoftDrop3CalobTagger.TrackCountingHighPurBJetTags
akSoftDrop3CaloPatJetPartonAssociationLegacy = akSoftDrop3CalobTagger.PatJetPartonAssociationLegacy

akSoftDrop3CaloImpactParameterTagInfos = akSoftDrop3CalobTagger.ImpactParameterTagInfos
akSoftDrop3CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop3CaloJetProbabilityBJetTags = akSoftDrop3CalobTagger.JetProbabilityBJetTags

akSoftDrop3CaloSecondaryVertexTagInfos = akSoftDrop3CalobTagger.SecondaryVertexTagInfos
akSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop3CaloCombinedSecondaryVertexBJetTags = akSoftDrop3CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop3CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop3CalobTagger.CombinedSecondaryVertexV2BJetTags

akSoftDrop3CaloSecondaryVertexNegativeTagInfos = akSoftDrop3CalobTagger.SecondaryVertexNegativeTagInfos
akSoftDrop3CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akSoftDrop3CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akSoftDrop3CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akSoftDrop3CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akSoftDrop3CaloNegativeCombinedSecondaryVertexBJetTags = akSoftDrop3CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akSoftDrop3CaloPositiveCombinedSecondaryVertexBJetTags = akSoftDrop3CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akSoftDrop3CaloNegativeCombinedSecondaryVertexV2BJetTags = akSoftDrop3CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akSoftDrop3CaloPositiveCombinedSecondaryVertexV2BJetTags = akSoftDrop3CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akSoftDrop3CaloSoftPFMuonsTagInfos = akSoftDrop3CalobTagger.SoftPFMuonsTagInfos
akSoftDrop3CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop3CaloSoftPFMuonBJetTags = akSoftDrop3CalobTagger.SoftPFMuonBJetTags
akSoftDrop3CaloSoftPFMuonByIP3dBJetTags = akSoftDrop3CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop3CaloSoftPFMuonByPtBJetTags = akSoftDrop3CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop3CaloNegativeSoftPFMuonByPtBJetTags = akSoftDrop3CalobTagger.NegativeSoftPFMuonByPtBJetTags
akSoftDrop3CaloPositiveSoftPFMuonByPtBJetTags = akSoftDrop3CalobTagger.PositiveSoftPFMuonByPtBJetTags
akSoftDrop3CaloPatJetFlavourIdLegacy = cms.Sequence(akSoftDrop3CaloPatJetPartonAssociationLegacy*akSoftDrop3CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akSoftDrop3CaloPatJetFlavourAssociation = akSoftDrop3CalobTagger.PatJetFlavourAssociation
#akSoftDrop3CaloPatJetFlavourId = cms.Sequence(akSoftDrop3CaloPatJetPartons*akSoftDrop3CaloPatJetFlavourAssociation)

akSoftDrop3CaloJetBtaggingIP       = cms.Sequence(akSoftDrop3CaloImpactParameterTagInfos *
            (akSoftDrop3CaloTrackCountingHighEffBJetTags +
             akSoftDrop3CaloTrackCountingHighPurBJetTags +
             akSoftDrop3CaloJetProbabilityBJetTags +
             akSoftDrop3CaloJetBProbabilityBJetTags 
            )
            )

akSoftDrop3CaloJetBtaggingSV = cms.Sequence(akSoftDrop3CaloImpactParameterTagInfos
            *
            akSoftDrop3CaloSecondaryVertexTagInfos
            * (akSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop3CaloCombinedSecondaryVertexBJetTags+
                akSoftDrop3CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop3CaloJetBtaggingNegSV = cms.Sequence(akSoftDrop3CaloImpactParameterTagInfos
            *
            akSoftDrop3CaloSecondaryVertexNegativeTagInfos
            * (akSoftDrop3CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop3CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop3CaloNegativeCombinedSecondaryVertexBJetTags+
                akSoftDrop3CaloPositiveCombinedSecondaryVertexBJetTags+
                akSoftDrop3CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akSoftDrop3CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop3CaloJetBtaggingMu = cms.Sequence(akSoftDrop3CaloSoftPFMuonsTagInfos * (akSoftDrop3CaloSoftPFMuonBJetTags
                +
                akSoftDrop3CaloSoftPFMuonByIP3dBJetTags
                +
                akSoftDrop3CaloSoftPFMuonByPtBJetTags
                +
                akSoftDrop3CaloNegativeSoftPFMuonByPtBJetTags
                +
                akSoftDrop3CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akSoftDrop3CaloJetBtagging = cms.Sequence(akSoftDrop3CaloJetBtaggingIP
            *akSoftDrop3CaloJetBtaggingSV
            *akSoftDrop3CaloJetBtaggingNegSV
#            *akSoftDrop3CaloJetBtaggingMu
            )

akSoftDrop3CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akSoftDrop3CaloJets"),
        genJetMatch          = cms.InputTag("akSoftDrop3Calomatch"),
        genPartonMatch       = cms.InputTag("akSoftDrop3Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akSoftDrop3Calocorr")),
        JetPartonMapSource   = cms.InputTag("akSoftDrop3CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akSoftDrop3CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akSoftDrop3CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akSoftDrop3CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akSoftDrop3CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akSoftDrop3CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akSoftDrop3CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akSoftDrop3CaloJetBProbabilityBJetTags"),
            cms.InputTag("akSoftDrop3CaloJetProbabilityBJetTags"),
            #cms.InputTag("akSoftDrop3CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akSoftDrop3CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akSoftDrop3CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akSoftDrop3CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akSoftDrop3CaloJetID"),
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

akSoftDrop3CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akSoftDrop3CaloJets"),
           	    R0  = cms.double( 0.3)
)
akSoftDrop3CalopatJetsWithBtagging.userData.userFloats.src += ['akSoftDrop3CaloNjettiness:tau1','akSoftDrop3CaloNjettiness:tau2','akSoftDrop3CaloNjettiness:tau3']

akSoftDrop3CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akSoftDrop3CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak3GenJets',
                                                             rParam = 0.3,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlow'),
                                                             trackTag = cms.InputTag("generalTracks"),
                                                             fillGenJets = True,
                                                             isMC = True,
							     doSubEvent = True,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akSoftDrop3Calo"),
                                                             jetName = cms.untracked.string("akSoftDrop3Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(True),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop3GenJets"),
                                                             doGenTaus = True
                                                             )

akSoftDrop3CaloJetSequence_mc = cms.Sequence(
                                                  #akSoftDrop3Caloclean
                                                  #*
                                                  akSoftDrop3Calomatch
                                                  #*
                                                  #akSoftDrop3CalomatchGroomed
                                                  *
                                                  akSoftDrop3Caloparton
                                                  *
                                                  akSoftDrop3Calocorr
                                                  *
                                                  #akSoftDrop3CaloJetID
                                                  #*
                                                  akSoftDrop3CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akSoftDrop3CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akSoftDrop3CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akSoftDrop3CaloJetBtagging
                                                  *
                                                  akSoftDrop3CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akSoftDrop3CalopatJetsWithBtagging
                                                  *
                                                  akSoftDrop3CaloJetAnalyzer
                                                  )

akSoftDrop3CaloJetSequence_data = cms.Sequence(akSoftDrop3Calocorr
                                                    *
                                                    #akSoftDrop3CaloJetID
                                                    #*
                                                    akSoftDrop3CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akSoftDrop3CaloJetBtagging
                                                    *
                                                    akSoftDrop3CaloNjettiness 
                                                    *
                                                    akSoftDrop3CalopatJetsWithBtagging
                                                    *
                                                    akSoftDrop3CaloJetAnalyzer
                                                    )

akSoftDrop3CaloJetSequence_jec = cms.Sequence(akSoftDrop3CaloJetSequence_mc)
akSoftDrop3CaloJetSequence_mb = cms.Sequence(akSoftDrop3CaloJetSequence_mc)

akSoftDrop3CaloJetSequence = cms.Sequence(akSoftDrop3CaloJetSequence_mc)
