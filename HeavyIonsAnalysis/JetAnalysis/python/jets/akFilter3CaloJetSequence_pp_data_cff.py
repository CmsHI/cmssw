

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter3Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter3CaloJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akFilter3CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter3GenJets"),
    matched = cms.InputTag("ak3GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.3
    )

akFilter3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter3CaloJets")
                                                        )

akFilter3Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter3CaloJets"),
    payload = "AK3Calo_offline"
    )

akFilter3CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter3CaloJets'))

#akFilter3Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3GenJets'))

akFilter3CalobTagger = bTaggers("akFilter3Calo",0.3)

#create objects locally since they dont load properly otherwise
#akFilter3Calomatch = akFilter3CalobTagger.match
akFilter3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter3CaloJets"), matched = cms.InputTag("genParticles"))
akFilter3CaloPatJetFlavourAssociationLegacy = akFilter3CalobTagger.PatJetFlavourAssociationLegacy
akFilter3CaloPatJetPartons = akFilter3CalobTagger.PatJetPartons
akFilter3CaloJetTracksAssociatorAtVertex = akFilter3CalobTagger.JetTracksAssociatorAtVertex
akFilter3CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter3CaloSimpleSecondaryVertexHighEffBJetTags = akFilter3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter3CaloSimpleSecondaryVertexHighPurBJetTags = akFilter3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter3CaloCombinedSecondaryVertexBJetTags = akFilter3CalobTagger.CombinedSecondaryVertexBJetTags
akFilter3CaloCombinedSecondaryVertexV2BJetTags = akFilter3CalobTagger.CombinedSecondaryVertexV2BJetTags
akFilter3CaloJetBProbabilityBJetTags = akFilter3CalobTagger.JetBProbabilityBJetTags
akFilter3CaloSoftPFMuonByPtBJetTags = akFilter3CalobTagger.SoftPFMuonByPtBJetTags
akFilter3CaloSoftPFMuonByIP3dBJetTags = akFilter3CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter3CaloTrackCountingHighEffBJetTags = akFilter3CalobTagger.TrackCountingHighEffBJetTags
akFilter3CaloTrackCountingHighPurBJetTags = akFilter3CalobTagger.TrackCountingHighPurBJetTags
akFilter3CaloPatJetPartonAssociationLegacy = akFilter3CalobTagger.PatJetPartonAssociationLegacy

akFilter3CaloImpactParameterTagInfos = akFilter3CalobTagger.ImpactParameterTagInfos
akFilter3CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter3CaloJetProbabilityBJetTags = akFilter3CalobTagger.JetProbabilityBJetTags

akFilter3CaloSecondaryVertexTagInfos = akFilter3CalobTagger.SecondaryVertexTagInfos
akFilter3CaloSimpleSecondaryVertexHighEffBJetTags = akFilter3CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter3CaloSimpleSecondaryVertexHighPurBJetTags = akFilter3CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter3CaloCombinedSecondaryVertexBJetTags = akFilter3CalobTagger.CombinedSecondaryVertexBJetTags
akFilter3CaloCombinedSecondaryVertexV2BJetTags = akFilter3CalobTagger.CombinedSecondaryVertexV2BJetTags

akFilter3CaloSecondaryVertexNegativeTagInfos = akFilter3CalobTagger.SecondaryVertexNegativeTagInfos
akFilter3CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter3CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter3CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter3CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter3CaloNegativeCombinedSecondaryVertexBJetTags = akFilter3CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter3CaloPositiveCombinedSecondaryVertexBJetTags = akFilter3CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter3CaloNegativeCombinedSecondaryVertexV2BJetTags = akFilter3CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter3CaloPositiveCombinedSecondaryVertexV2BJetTags = akFilter3CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter3CaloSoftPFMuonsTagInfos = akFilter3CalobTagger.SoftPFMuonsTagInfos
akFilter3CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter3CaloSoftPFMuonBJetTags = akFilter3CalobTagger.SoftPFMuonBJetTags
akFilter3CaloSoftPFMuonByIP3dBJetTags = akFilter3CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter3CaloSoftPFMuonByPtBJetTags = akFilter3CalobTagger.SoftPFMuonByPtBJetTags
akFilter3CaloNegativeSoftPFMuonByPtBJetTags = akFilter3CalobTagger.NegativeSoftPFMuonByPtBJetTags
akFilter3CaloPositiveSoftPFMuonByPtBJetTags = akFilter3CalobTagger.PositiveSoftPFMuonByPtBJetTags
akFilter3CaloPatJetFlavourIdLegacy = cms.Sequence(akFilter3CaloPatJetPartonAssociationLegacy*akFilter3CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter3CaloPatJetFlavourAssociation = akFilter3CalobTagger.PatJetFlavourAssociation
#akFilter3CaloPatJetFlavourId = cms.Sequence(akFilter3CaloPatJetPartons*akFilter3CaloPatJetFlavourAssociation)

akFilter3CaloJetBtaggingIP       = cms.Sequence(akFilter3CaloImpactParameterTagInfos *
            (akFilter3CaloTrackCountingHighEffBJetTags +
             akFilter3CaloTrackCountingHighPurBJetTags +
             akFilter3CaloJetProbabilityBJetTags +
             akFilter3CaloJetBProbabilityBJetTags 
            )
            )

akFilter3CaloJetBtaggingSV = cms.Sequence(akFilter3CaloImpactParameterTagInfos
            *
            akFilter3CaloSecondaryVertexTagInfos
            * (akFilter3CaloSimpleSecondaryVertexHighEffBJetTags+
                akFilter3CaloSimpleSecondaryVertexHighPurBJetTags+
                akFilter3CaloCombinedSecondaryVertexBJetTags+
                akFilter3CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter3CaloJetBtaggingNegSV = cms.Sequence(akFilter3CaloImpactParameterTagInfos
            *
            akFilter3CaloSecondaryVertexNegativeTagInfos
            * (akFilter3CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter3CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter3CaloNegativeCombinedSecondaryVertexBJetTags+
                akFilter3CaloPositiveCombinedSecondaryVertexBJetTags+
                akFilter3CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter3CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter3CaloJetBtaggingMu = cms.Sequence(akFilter3CaloSoftPFMuonsTagInfos * (akFilter3CaloSoftPFMuonBJetTags
                +
                akFilter3CaloSoftPFMuonByIP3dBJetTags
                +
                akFilter3CaloSoftPFMuonByPtBJetTags
                +
                akFilter3CaloNegativeSoftPFMuonByPtBJetTags
                +
                akFilter3CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter3CaloJetBtagging = cms.Sequence(akFilter3CaloJetBtaggingIP
            *akFilter3CaloJetBtaggingSV
            *akFilter3CaloJetBtaggingNegSV
#            *akFilter3CaloJetBtaggingMu
            )

akFilter3CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter3CaloJets"),
        genJetMatch          = cms.InputTag("akFilter3Calomatch"),
        genPartonMatch       = cms.InputTag("akFilter3Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter3Calocorr")),
        JetPartonMapSource   = cms.InputTag("akFilter3CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter3CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter3CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter3CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter3CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter3CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter3CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter3CaloJetBProbabilityBJetTags"),
            cms.InputTag("akFilter3CaloJetProbabilityBJetTags"),
            #cms.InputTag("akFilter3CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter3CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter3CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter3CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter3CaloJetID"),
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

akFilter3CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter3CaloJets"),
           	    R0  = cms.double( 0.3)
)
akFilter3CalopatJetsWithBtagging.userData.userFloats.src += ['akFilter3CaloNjettiness:tau1','akFilter3CaloNjettiness:tau2','akFilter3CaloNjettiness:tau3']

akFilter3CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter3CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akFilter3Calo"),
                                                             jetName = cms.untracked.string("akFilter3Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter3GenJets"),
                                                             doGenTaus = False
                                                             )

akFilter3CaloJetSequence_mc = cms.Sequence(
                                                  #akFilter3Caloclean
                                                  #*
                                                  akFilter3Calomatch
                                                  #*
                                                  #akFilter3CalomatchGroomed
                                                  *
                                                  akFilter3Caloparton
                                                  *
                                                  akFilter3Calocorr
                                                  *
                                                  #akFilter3CaloJetID
                                                  #*
                                                  akFilter3CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter3CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter3CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter3CaloJetBtagging
                                                  *
                                                  akFilter3CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter3CalopatJetsWithBtagging
                                                  *
                                                  akFilter3CaloJetAnalyzer
                                                  )

akFilter3CaloJetSequence_data = cms.Sequence(akFilter3Calocorr
                                                    *
                                                    #akFilter3CaloJetID
                                                    #*
                                                    akFilter3CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter3CaloJetBtagging
                                                    *
                                                    akFilter3CaloNjettiness 
                                                    *
                                                    akFilter3CalopatJetsWithBtagging
                                                    *
                                                    akFilter3CaloJetAnalyzer
                                                    )

akFilter3CaloJetSequence_jec = cms.Sequence(akFilter3CaloJetSequence_mc)
akFilter3CaloJetSequence_mb = cms.Sequence(akFilter3CaloJetSequence_mc)

akFilter3CaloJetSequence = cms.Sequence(akFilter3CaloJetSequence_data)
