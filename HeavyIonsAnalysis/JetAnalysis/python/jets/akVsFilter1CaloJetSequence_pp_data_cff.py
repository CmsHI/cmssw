

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter1Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter1CaloJets"),
    matched = cms.InputTag("ak1GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.1
    )

akVsFilter1CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter1GenJets"),
    matched = cms.InputTag("ak1GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.1
    )

akVsFilter1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter1CaloJets")
                                                        )

akVsFilter1Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter1CaloJets"),
    payload = "AK1Calo_offline"
    )

akVsFilter1CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter1CaloJets'))

#akVsFilter1Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1GenJets'))

akVsFilter1CalobTagger = bTaggers("akVsFilter1Calo",0.1)

#create objects locally since they dont load properly otherwise
#akVsFilter1Calomatch = akVsFilter1CalobTagger.match
akVsFilter1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter1CaloJets"), matched = cms.InputTag("genParticles"))
akVsFilter1CaloPatJetFlavourAssociationLegacy = akVsFilter1CalobTagger.PatJetFlavourAssociationLegacy
akVsFilter1CaloPatJetPartons = akVsFilter1CalobTagger.PatJetPartons
akVsFilter1CaloJetTracksAssociatorAtVertex = akVsFilter1CalobTagger.JetTracksAssociatorAtVertex
akVsFilter1CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter1CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter1CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter1CaloCombinedSecondaryVertexBJetTags = akVsFilter1CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter1CaloCombinedSecondaryVertexV2BJetTags = akVsFilter1CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter1CaloJetBProbabilityBJetTags = akVsFilter1CalobTagger.JetBProbabilityBJetTags
akVsFilter1CaloSoftPFMuonByPtBJetTags = akVsFilter1CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter1CaloSoftPFMuonByIP3dBJetTags = akVsFilter1CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter1CaloTrackCountingHighEffBJetTags = akVsFilter1CalobTagger.TrackCountingHighEffBJetTags
akVsFilter1CaloTrackCountingHighPurBJetTags = akVsFilter1CalobTagger.TrackCountingHighPurBJetTags
akVsFilter1CaloPatJetPartonAssociationLegacy = akVsFilter1CalobTagger.PatJetPartonAssociationLegacy

akVsFilter1CaloImpactParameterTagInfos = akVsFilter1CalobTagger.ImpactParameterTagInfos
akVsFilter1CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter1CaloJetProbabilityBJetTags = akVsFilter1CalobTagger.JetProbabilityBJetTags

akVsFilter1CaloSecondaryVertexTagInfos = akVsFilter1CalobTagger.SecondaryVertexTagInfos
akVsFilter1CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter1CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter1CaloCombinedSecondaryVertexBJetTags = akVsFilter1CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter1CaloCombinedSecondaryVertexV2BJetTags = akVsFilter1CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter1CaloSecondaryVertexNegativeTagInfos = akVsFilter1CalobTagger.SecondaryVertexNegativeTagInfos
akVsFilter1CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter1CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter1CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter1CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter1CaloNegativeCombinedSecondaryVertexBJetTags = akVsFilter1CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter1CaloPositiveCombinedSecondaryVertexBJetTags = akVsFilter1CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter1CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter1CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter1CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter1CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter1CaloSoftPFMuonsTagInfos = akVsFilter1CalobTagger.SoftPFMuonsTagInfos
akVsFilter1CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter1CaloSoftPFMuonBJetTags = akVsFilter1CalobTagger.SoftPFMuonBJetTags
akVsFilter1CaloSoftPFMuonByIP3dBJetTags = akVsFilter1CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter1CaloSoftPFMuonByPtBJetTags = akVsFilter1CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter1CaloNegativeSoftPFMuonByPtBJetTags = akVsFilter1CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter1CaloPositiveSoftPFMuonByPtBJetTags = akVsFilter1CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter1CaloPatJetFlavourIdLegacy = cms.Sequence(akVsFilter1CaloPatJetPartonAssociationLegacy*akVsFilter1CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter1CaloPatJetFlavourAssociation = akVsFilter1CalobTagger.PatJetFlavourAssociation
#akVsFilter1CaloPatJetFlavourId = cms.Sequence(akVsFilter1CaloPatJetPartons*akVsFilter1CaloPatJetFlavourAssociation)

akVsFilter1CaloJetBtaggingIP       = cms.Sequence(akVsFilter1CaloImpactParameterTagInfos *
            (akVsFilter1CaloTrackCountingHighEffBJetTags +
             akVsFilter1CaloTrackCountingHighPurBJetTags +
             akVsFilter1CaloJetProbabilityBJetTags +
             akVsFilter1CaloJetBProbabilityBJetTags 
            )
            )

akVsFilter1CaloJetBtaggingSV = cms.Sequence(akVsFilter1CaloImpactParameterTagInfos
            *
            akVsFilter1CaloSecondaryVertexTagInfos
            * (akVsFilter1CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter1CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter1CaloCombinedSecondaryVertexBJetTags+
                akVsFilter1CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter1CaloJetBtaggingNegSV = cms.Sequence(akVsFilter1CaloImpactParameterTagInfos
            *
            akVsFilter1CaloSecondaryVertexNegativeTagInfos
            * (akVsFilter1CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter1CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter1CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter1CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter1CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter1CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter1CaloJetBtaggingMu = cms.Sequence(akVsFilter1CaloSoftPFMuonsTagInfos * (akVsFilter1CaloSoftPFMuonBJetTags
                +
                akVsFilter1CaloSoftPFMuonByIP3dBJetTags
                +
                akVsFilter1CaloSoftPFMuonByPtBJetTags
                +
                akVsFilter1CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter1CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter1CaloJetBtagging = cms.Sequence(akVsFilter1CaloJetBtaggingIP
            *akVsFilter1CaloJetBtaggingSV
            *akVsFilter1CaloJetBtaggingNegSV
#            *akVsFilter1CaloJetBtaggingMu
            )

akVsFilter1CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter1CaloJets"),
        genJetMatch          = cms.InputTag("akVsFilter1Calomatch"),
        genPartonMatch       = cms.InputTag("akVsFilter1Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter1Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter1CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter1CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter1CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter1CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter1CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter1CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter1CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter1CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter1CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter1CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter1CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter1CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter1CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter1CaloJetID"),
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

akVsFilter1CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter1CaloJets"),
           	    R0  = cms.double( 0.1)
)
akVsFilter1CalopatJetsWithBtagging.userData.userFloats.src += ['akVsFilter1CaloNjettiness:tau1','akVsFilter1CaloNjettiness:tau2','akVsFilter1CaloNjettiness:tau3']

akVsFilter1CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter1CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak1GenJets',
                                                             rParam = 0.1,
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
                                                             bTagJetName = cms.untracked.string("akVsFilter1Calo"),
                                                             jetName = cms.untracked.string("akVsFilter1Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter1GenJets"),
                                                             doGenTaus = False
                                                             )

akVsFilter1CaloJetSequence_mc = cms.Sequence(
                                                  #akVsFilter1Caloclean
                                                  #*
                                                  akVsFilter1Calomatch
                                                  #*
                                                  #akVsFilter1CalomatchGroomed
                                                  *
                                                  akVsFilter1Caloparton
                                                  *
                                                  akVsFilter1Calocorr
                                                  *
                                                  #akVsFilter1CaloJetID
                                                  #*
                                                  akVsFilter1CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter1CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter1CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter1CaloJetBtagging
                                                  *
                                                  akVsFilter1CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter1CalopatJetsWithBtagging
                                                  *
                                                  akVsFilter1CaloJetAnalyzer
                                                  )

akVsFilter1CaloJetSequence_data = cms.Sequence(akVsFilter1Calocorr
                                                    *
                                                    #akVsFilter1CaloJetID
                                                    #*
                                                    akVsFilter1CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter1CaloJetBtagging
                                                    *
                                                    akVsFilter1CaloNjettiness 
                                                    *
                                                    akVsFilter1CalopatJetsWithBtagging
                                                    *
                                                    akVsFilter1CaloJetAnalyzer
                                                    )

akVsFilter1CaloJetSequence_jec = cms.Sequence(akVsFilter1CaloJetSequence_mc)
akVsFilter1CaloJetSequence_mb = cms.Sequence(akVsFilter1CaloJetSequence_mc)

akVsFilter1CaloJetSequence = cms.Sequence(akVsFilter1CaloJetSequence_data)
