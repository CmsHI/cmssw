

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter2Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter2CaloJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.2
    )

akVsFilter2CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter2GenJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.2
    )

akVsFilter2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter2CaloJets")
                                                        )

akVsFilter2Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter2CaloJets"),
    payload = "AK2Calo_offline"
    )

akVsFilter2CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter2CaloJets'))

#akVsFilter2Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2GenJets'))

akVsFilter2CalobTagger = bTaggers("akVsFilter2Calo",0.2)

#create objects locally since they dont load properly otherwise
#akVsFilter2Calomatch = akVsFilter2CalobTagger.match
akVsFilter2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter2CaloJets"), matched = cms.InputTag("genParticles"))
akVsFilter2CaloPatJetFlavourAssociationLegacy = akVsFilter2CalobTagger.PatJetFlavourAssociationLegacy
akVsFilter2CaloPatJetPartons = akVsFilter2CalobTagger.PatJetPartons
akVsFilter2CaloJetTracksAssociatorAtVertex = akVsFilter2CalobTagger.JetTracksAssociatorAtVertex
akVsFilter2CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter2CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter2CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter2CaloCombinedSecondaryVertexBJetTags = akVsFilter2CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter2CaloCombinedSecondaryVertexV2BJetTags = akVsFilter2CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter2CaloJetBProbabilityBJetTags = akVsFilter2CalobTagger.JetBProbabilityBJetTags
akVsFilter2CaloSoftPFMuonByPtBJetTags = akVsFilter2CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter2CaloSoftPFMuonByIP3dBJetTags = akVsFilter2CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter2CaloTrackCountingHighEffBJetTags = akVsFilter2CalobTagger.TrackCountingHighEffBJetTags
akVsFilter2CaloTrackCountingHighPurBJetTags = akVsFilter2CalobTagger.TrackCountingHighPurBJetTags
akVsFilter2CaloPatJetPartonAssociationLegacy = akVsFilter2CalobTagger.PatJetPartonAssociationLegacy

akVsFilter2CaloImpactParameterTagInfos = akVsFilter2CalobTagger.ImpactParameterTagInfos
akVsFilter2CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter2CaloJetProbabilityBJetTags = akVsFilter2CalobTagger.JetProbabilityBJetTags

akVsFilter2CaloSecondaryVertexTagInfos = akVsFilter2CalobTagger.SecondaryVertexTagInfos
akVsFilter2CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter2CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter2CaloCombinedSecondaryVertexBJetTags = akVsFilter2CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter2CaloCombinedSecondaryVertexV2BJetTags = akVsFilter2CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter2CaloSecondaryVertexNegativeTagInfos = akVsFilter2CalobTagger.SecondaryVertexNegativeTagInfos
akVsFilter2CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter2CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter2CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter2CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter2CaloNegativeCombinedSecondaryVertexBJetTags = akVsFilter2CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter2CaloPositiveCombinedSecondaryVertexBJetTags = akVsFilter2CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter2CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter2CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter2CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter2CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter2CaloSoftPFMuonsTagInfos = akVsFilter2CalobTagger.SoftPFMuonsTagInfos
akVsFilter2CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter2CaloSoftPFMuonBJetTags = akVsFilter2CalobTagger.SoftPFMuonBJetTags
akVsFilter2CaloSoftPFMuonByIP3dBJetTags = akVsFilter2CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter2CaloSoftPFMuonByPtBJetTags = akVsFilter2CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter2CaloNegativeSoftPFMuonByPtBJetTags = akVsFilter2CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter2CaloPositiveSoftPFMuonByPtBJetTags = akVsFilter2CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter2CaloPatJetFlavourIdLegacy = cms.Sequence(akVsFilter2CaloPatJetPartonAssociationLegacy*akVsFilter2CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter2CaloPatJetFlavourAssociation = akVsFilter2CalobTagger.PatJetFlavourAssociation
#akVsFilter2CaloPatJetFlavourId = cms.Sequence(akVsFilter2CaloPatJetPartons*akVsFilter2CaloPatJetFlavourAssociation)

akVsFilter2CaloJetBtaggingIP       = cms.Sequence(akVsFilter2CaloImpactParameterTagInfos *
            (akVsFilter2CaloTrackCountingHighEffBJetTags +
             akVsFilter2CaloTrackCountingHighPurBJetTags +
             akVsFilter2CaloJetProbabilityBJetTags +
             akVsFilter2CaloJetBProbabilityBJetTags 
            )
            )

akVsFilter2CaloJetBtaggingSV = cms.Sequence(akVsFilter2CaloImpactParameterTagInfos
            *
            akVsFilter2CaloSecondaryVertexTagInfos
            * (akVsFilter2CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter2CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter2CaloCombinedSecondaryVertexBJetTags+
                akVsFilter2CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter2CaloJetBtaggingNegSV = cms.Sequence(akVsFilter2CaloImpactParameterTagInfos
            *
            akVsFilter2CaloSecondaryVertexNegativeTagInfos
            * (akVsFilter2CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter2CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter2CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter2CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter2CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter2CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter2CaloJetBtaggingMu = cms.Sequence(akVsFilter2CaloSoftPFMuonsTagInfos * (akVsFilter2CaloSoftPFMuonBJetTags
                +
                akVsFilter2CaloSoftPFMuonByIP3dBJetTags
                +
                akVsFilter2CaloSoftPFMuonByPtBJetTags
                +
                akVsFilter2CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter2CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter2CaloJetBtagging = cms.Sequence(akVsFilter2CaloJetBtaggingIP
            *akVsFilter2CaloJetBtaggingSV
            *akVsFilter2CaloJetBtaggingNegSV
#            *akVsFilter2CaloJetBtaggingMu
            )

akVsFilter2CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter2CaloJets"),
        genJetMatch          = cms.InputTag("akVsFilter2Calomatch"),
        genPartonMatch       = cms.InputTag("akVsFilter2Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter2Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter2CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter2CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter2CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter2CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter2CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter2CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter2CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter2CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter2CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter2CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter2CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter2CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter2CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter2CaloJetID"),
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

akVsFilter2CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter2CaloJets"),
           	    R0  = cms.double( 0.2)
)
akVsFilter2CalopatJetsWithBtagging.userData.userFloats.src += ['akVsFilter2CaloNjettiness:tau1','akVsFilter2CaloNjettiness:tau2','akVsFilter2CaloNjettiness:tau3']

akVsFilter2CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter2CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak2GenJets',
                                                             rParam = 0.2,
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
                                                             bTagJetName = cms.untracked.string("akVsFilter2Calo"),
                                                             jetName = cms.untracked.string("akVsFilter2Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter2GenJets"),
                                                             doGenTaus = True
                                                             )

akVsFilter2CaloJetSequence_mc = cms.Sequence(
                                                  #akVsFilter2Caloclean
                                                  #*
                                                  akVsFilter2Calomatch
                                                  #*
                                                  #akVsFilter2CalomatchGroomed
                                                  *
                                                  akVsFilter2Caloparton
                                                  *
                                                  akVsFilter2Calocorr
                                                  *
                                                  #akVsFilter2CaloJetID
                                                  #*
                                                  akVsFilter2CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter2CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter2CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter2CaloJetBtagging
                                                  *
                                                  akVsFilter2CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter2CalopatJetsWithBtagging
                                                  *
                                                  akVsFilter2CaloJetAnalyzer
                                                  )

akVsFilter2CaloJetSequence_data = cms.Sequence(akVsFilter2Calocorr
                                                    *
                                                    #akVsFilter2CaloJetID
                                                    #*
                                                    akVsFilter2CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter2CaloJetBtagging
                                                    *
                                                    akVsFilter2CaloNjettiness 
                                                    *
                                                    akVsFilter2CalopatJetsWithBtagging
                                                    *
                                                    akVsFilter2CaloJetAnalyzer
                                                    )

akVsFilter2CaloJetSequence_jec = cms.Sequence(akVsFilter2CaloJetSequence_mc)
akVsFilter2CaloJetSequence_mb = cms.Sequence(akVsFilter2CaloJetSequence_mc)

akVsFilter2CaloJetSequence = cms.Sequence(akVsFilter2CaloJetSequence_jec)
akVsFilter2CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akVsFilter2CaloJetAnalyzer.jetPtMin = cms.double(1)
