

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter3Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter3CaloJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.3
    )

akVsFilter3CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter3GenJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.3
    )

akVsFilter3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter3CaloJets")
                                                        )

akVsFilter3Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter3CaloJets"),
    payload = "AK3Calo_offline"
    )

akVsFilter3CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter3CaloJets'))

#akVsFilter3Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3GenJets'))

akVsFilter3CalobTagger = bTaggers("akVsFilter3Calo",0.3)

#create objects locally since they dont load properly otherwise
#akVsFilter3Calomatch = akVsFilter3CalobTagger.match
akVsFilter3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter3CaloJets"), matched = cms.InputTag("genParticles"))
akVsFilter3CaloPatJetFlavourAssociationLegacy = akVsFilter3CalobTagger.PatJetFlavourAssociationLegacy
akVsFilter3CaloPatJetPartons = akVsFilter3CalobTagger.PatJetPartons
akVsFilter3CaloJetTracksAssociatorAtVertex = akVsFilter3CalobTagger.JetTracksAssociatorAtVertex
akVsFilter3CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter3CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter3CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter3CaloCombinedSecondaryVertexBJetTags = akVsFilter3CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter3CaloCombinedSecondaryVertexV2BJetTags = akVsFilter3CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter3CaloJetBProbabilityBJetTags = akVsFilter3CalobTagger.JetBProbabilityBJetTags
akVsFilter3CaloSoftPFMuonByPtBJetTags = akVsFilter3CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter3CaloSoftPFMuonByIP3dBJetTags = akVsFilter3CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter3CaloTrackCountingHighEffBJetTags = akVsFilter3CalobTagger.TrackCountingHighEffBJetTags
akVsFilter3CaloTrackCountingHighPurBJetTags = akVsFilter3CalobTagger.TrackCountingHighPurBJetTags
akVsFilter3CaloPatJetPartonAssociationLegacy = akVsFilter3CalobTagger.PatJetPartonAssociationLegacy

akVsFilter3CaloImpactParameterTagInfos = akVsFilter3CalobTagger.ImpactParameterTagInfos
akVsFilter3CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter3CaloJetProbabilityBJetTags = akVsFilter3CalobTagger.JetProbabilityBJetTags

akVsFilter3CaloSecondaryVertexTagInfos = akVsFilter3CalobTagger.SecondaryVertexTagInfos
akVsFilter3CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter3CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter3CaloCombinedSecondaryVertexBJetTags = akVsFilter3CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter3CaloCombinedSecondaryVertexV2BJetTags = akVsFilter3CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter3CaloSecondaryVertexNegativeTagInfos = akVsFilter3CalobTagger.SecondaryVertexNegativeTagInfos
akVsFilter3CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter3CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter3CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter3CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter3CaloNegativeCombinedSecondaryVertexBJetTags = akVsFilter3CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter3CaloPositiveCombinedSecondaryVertexBJetTags = akVsFilter3CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter3CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter3CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter3CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter3CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter3CaloSoftPFMuonsTagInfos = akVsFilter3CalobTagger.SoftPFMuonsTagInfos
akVsFilter3CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter3CaloSoftPFMuonBJetTags = akVsFilter3CalobTagger.SoftPFMuonBJetTags
akVsFilter3CaloSoftPFMuonByIP3dBJetTags = akVsFilter3CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter3CaloSoftPFMuonByPtBJetTags = akVsFilter3CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter3CaloNegativeSoftPFMuonByPtBJetTags = akVsFilter3CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter3CaloPositiveSoftPFMuonByPtBJetTags = akVsFilter3CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter3CaloPatJetFlavourIdLegacy = cms.Sequence(akVsFilter3CaloPatJetPartonAssociationLegacy*akVsFilter3CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter3CaloPatJetFlavourAssociation = akVsFilter3CalobTagger.PatJetFlavourAssociation
#akVsFilter3CaloPatJetFlavourId = cms.Sequence(akVsFilter3CaloPatJetPartons*akVsFilter3CaloPatJetFlavourAssociation)

akVsFilter3CaloJetBtaggingIP       = cms.Sequence(akVsFilter3CaloImpactParameterTagInfos *
            (akVsFilter3CaloTrackCountingHighEffBJetTags +
             akVsFilter3CaloTrackCountingHighPurBJetTags +
             akVsFilter3CaloJetProbabilityBJetTags +
             akVsFilter3CaloJetBProbabilityBJetTags 
            )
            )

akVsFilter3CaloJetBtaggingSV = cms.Sequence(akVsFilter3CaloImpactParameterTagInfos
            *
            akVsFilter3CaloSecondaryVertexTagInfos
            * (akVsFilter3CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter3CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter3CaloCombinedSecondaryVertexBJetTags+
                akVsFilter3CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter3CaloJetBtaggingNegSV = cms.Sequence(akVsFilter3CaloImpactParameterTagInfos
            *
            akVsFilter3CaloSecondaryVertexNegativeTagInfos
            * (akVsFilter3CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter3CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter3CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter3CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter3CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter3CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter3CaloJetBtaggingMu = cms.Sequence(akVsFilter3CaloSoftPFMuonsTagInfos * (akVsFilter3CaloSoftPFMuonBJetTags
                +
                akVsFilter3CaloSoftPFMuonByIP3dBJetTags
                +
                akVsFilter3CaloSoftPFMuonByPtBJetTags
                +
                akVsFilter3CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter3CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter3CaloJetBtagging = cms.Sequence(akVsFilter3CaloJetBtaggingIP
            *akVsFilter3CaloJetBtaggingSV
            *akVsFilter3CaloJetBtaggingNegSV
#            *akVsFilter3CaloJetBtaggingMu
            )

akVsFilter3CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter3CaloJets"),
        genJetMatch          = cms.InputTag("akVsFilter3Calomatch"),
        genPartonMatch       = cms.InputTag("akVsFilter3Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter3Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter3CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter3CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter3CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter3CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter3CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter3CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter3CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter3CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter3CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter3CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter3CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter3CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter3CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter3CaloJetID"),
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

akVsFilter3CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter3CaloJets"),
           	    R0  = cms.double( 0.3)
)
akVsFilter3CalopatJetsWithBtagging.userData.userFloats.src += ['akVsFilter3CaloNjettiness:tau1','akVsFilter3CaloNjettiness:tau2','akVsFilter3CaloNjettiness:tau3']

akVsFilter3CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter3CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akVsFilter3Calo"),
                                                             jetName = cms.untracked.string("akVsFilter3Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter3GenJets"),
                                                             doGenTaus = False
                                                             )

akVsFilter3CaloJetSequence_mc = cms.Sequence(
                                                  #akVsFilter3Caloclean
                                                  #*
                                                  akVsFilter3Calomatch
                                                  #*
                                                  #akVsFilter3CalomatchGroomed
                                                  *
                                                  akVsFilter3Caloparton
                                                  *
                                                  akVsFilter3Calocorr
                                                  *
                                                  #akVsFilter3CaloJetID
                                                  #*
                                                  akVsFilter3CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter3CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter3CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter3CaloJetBtagging
                                                  *
                                                  akVsFilter3CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter3CalopatJetsWithBtagging
                                                  *
                                                  akVsFilter3CaloJetAnalyzer
                                                  )

akVsFilter3CaloJetSequence_data = cms.Sequence(akVsFilter3Calocorr
                                                    *
                                                    #akVsFilter3CaloJetID
                                                    #*
                                                    akVsFilter3CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter3CaloJetBtagging
                                                    *
                                                    akVsFilter3CaloNjettiness 
                                                    *
                                                    akVsFilter3CalopatJetsWithBtagging
                                                    *
                                                    akVsFilter3CaloJetAnalyzer
                                                    )

akVsFilter3CaloJetSequence_jec = cms.Sequence(akVsFilter3CaloJetSequence_mc)
akVsFilter3CaloJetSequence_mb = cms.Sequence(akVsFilter3CaloJetSequence_mc)

akVsFilter3CaloJetSequence = cms.Sequence(akVsFilter3CaloJetSequence_data)
