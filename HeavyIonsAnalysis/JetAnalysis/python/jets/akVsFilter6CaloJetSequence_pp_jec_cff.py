

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter6Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter6CaloJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.6
    )

akVsFilter6CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter6GenJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.6
    )

akVsFilter6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter6CaloJets")
                                                        )

akVsFilter6Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter6CaloJets"),
    payload = "AK6Calo_offline"
    )

akVsFilter6CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter6CaloJets'))

#akVsFilter6Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6GenJets'))

akVsFilter6CalobTagger = bTaggers("akVsFilter6Calo",0.6)

#create objects locally since they dont load properly otherwise
#akVsFilter6Calomatch = akVsFilter6CalobTagger.match
akVsFilter6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter6CaloJets"), matched = cms.InputTag("genParticles"))
akVsFilter6CaloPatJetFlavourAssociationLegacy = akVsFilter6CalobTagger.PatJetFlavourAssociationLegacy
akVsFilter6CaloPatJetPartons = akVsFilter6CalobTagger.PatJetPartons
akVsFilter6CaloJetTracksAssociatorAtVertex = akVsFilter6CalobTagger.JetTracksAssociatorAtVertex
akVsFilter6CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter6CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter6CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter6CaloCombinedSecondaryVertexBJetTags = akVsFilter6CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter6CaloCombinedSecondaryVertexV2BJetTags = akVsFilter6CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter6CaloJetBProbabilityBJetTags = akVsFilter6CalobTagger.JetBProbabilityBJetTags
akVsFilter6CaloSoftPFMuonByPtBJetTags = akVsFilter6CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter6CaloSoftPFMuonByIP3dBJetTags = akVsFilter6CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter6CaloTrackCountingHighEffBJetTags = akVsFilter6CalobTagger.TrackCountingHighEffBJetTags
akVsFilter6CaloTrackCountingHighPurBJetTags = akVsFilter6CalobTagger.TrackCountingHighPurBJetTags
akVsFilter6CaloPatJetPartonAssociationLegacy = akVsFilter6CalobTagger.PatJetPartonAssociationLegacy

akVsFilter6CaloImpactParameterTagInfos = akVsFilter6CalobTagger.ImpactParameterTagInfos
akVsFilter6CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter6CaloJetProbabilityBJetTags = akVsFilter6CalobTagger.JetProbabilityBJetTags

akVsFilter6CaloSecondaryVertexTagInfos = akVsFilter6CalobTagger.SecondaryVertexTagInfos
akVsFilter6CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter6CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter6CaloCombinedSecondaryVertexBJetTags = akVsFilter6CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter6CaloCombinedSecondaryVertexV2BJetTags = akVsFilter6CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter6CaloSecondaryVertexNegativeTagInfos = akVsFilter6CalobTagger.SecondaryVertexNegativeTagInfos
akVsFilter6CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter6CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter6CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter6CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter6CaloNegativeCombinedSecondaryVertexBJetTags = akVsFilter6CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter6CaloPositiveCombinedSecondaryVertexBJetTags = akVsFilter6CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter6CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter6CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter6CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter6CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter6CaloSoftPFMuonsTagInfos = akVsFilter6CalobTagger.SoftPFMuonsTagInfos
akVsFilter6CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter6CaloSoftPFMuonBJetTags = akVsFilter6CalobTagger.SoftPFMuonBJetTags
akVsFilter6CaloSoftPFMuonByIP3dBJetTags = akVsFilter6CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter6CaloSoftPFMuonByPtBJetTags = akVsFilter6CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter6CaloNegativeSoftPFMuonByPtBJetTags = akVsFilter6CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter6CaloPositiveSoftPFMuonByPtBJetTags = akVsFilter6CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter6CaloPatJetFlavourIdLegacy = cms.Sequence(akVsFilter6CaloPatJetPartonAssociationLegacy*akVsFilter6CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter6CaloPatJetFlavourAssociation = akVsFilter6CalobTagger.PatJetFlavourAssociation
#akVsFilter6CaloPatJetFlavourId = cms.Sequence(akVsFilter6CaloPatJetPartons*akVsFilter6CaloPatJetFlavourAssociation)

akVsFilter6CaloJetBtaggingIP       = cms.Sequence(akVsFilter6CaloImpactParameterTagInfos *
            (akVsFilter6CaloTrackCountingHighEffBJetTags +
             akVsFilter6CaloTrackCountingHighPurBJetTags +
             akVsFilter6CaloJetProbabilityBJetTags +
             akVsFilter6CaloJetBProbabilityBJetTags 
            )
            )

akVsFilter6CaloJetBtaggingSV = cms.Sequence(akVsFilter6CaloImpactParameterTagInfos
            *
            akVsFilter6CaloSecondaryVertexTagInfos
            * (akVsFilter6CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter6CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter6CaloCombinedSecondaryVertexBJetTags+
                akVsFilter6CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter6CaloJetBtaggingNegSV = cms.Sequence(akVsFilter6CaloImpactParameterTagInfos
            *
            akVsFilter6CaloSecondaryVertexNegativeTagInfos
            * (akVsFilter6CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter6CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter6CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter6CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter6CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter6CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter6CaloJetBtaggingMu = cms.Sequence(akVsFilter6CaloSoftPFMuonsTagInfos * (akVsFilter6CaloSoftPFMuonBJetTags
                +
                akVsFilter6CaloSoftPFMuonByIP3dBJetTags
                +
                akVsFilter6CaloSoftPFMuonByPtBJetTags
                +
                akVsFilter6CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter6CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter6CaloJetBtagging = cms.Sequence(akVsFilter6CaloJetBtaggingIP
            *akVsFilter6CaloJetBtaggingSV
            *akVsFilter6CaloJetBtaggingNegSV
#            *akVsFilter6CaloJetBtaggingMu
            )

akVsFilter6CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter6CaloJets"),
        genJetMatch          = cms.InputTag("akVsFilter6Calomatch"),
        genPartonMatch       = cms.InputTag("akVsFilter6Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter6Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter6CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter6CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter6CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter6CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter6CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter6CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter6CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter6CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter6CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter6CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter6CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter6CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter6CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter6CaloJetID"),
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

akVsFilter6CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter6CaloJets"),
           	    R0  = cms.double( 0.6)
)
akVsFilter6CalopatJetsWithBtagging.userData.userFloats.src += ['akVsFilter6CaloNjettiness:tau1','akVsFilter6CaloNjettiness:tau2','akVsFilter6CaloNjettiness:tau3']

akVsFilter6CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter6CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak6GenJets',
                                                             rParam = 0.6,
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
                                                             bTagJetName = cms.untracked.string("akVsFilter6Calo"),
                                                             jetName = cms.untracked.string("akVsFilter6Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter6GenJets"),
                                                             doGenTaus = True
                                                             )

akVsFilter6CaloJetSequence_mc = cms.Sequence(
                                                  #akVsFilter6Caloclean
                                                  #*
                                                  akVsFilter6Calomatch
                                                  #*
                                                  #akVsFilter6CalomatchGroomed
                                                  *
                                                  akVsFilter6Caloparton
                                                  *
                                                  akVsFilter6Calocorr
                                                  *
                                                  #akVsFilter6CaloJetID
                                                  #*
                                                  akVsFilter6CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter6CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter6CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter6CaloJetBtagging
                                                  *
                                                  akVsFilter6CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter6CalopatJetsWithBtagging
                                                  *
                                                  akVsFilter6CaloJetAnalyzer
                                                  )

akVsFilter6CaloJetSequence_data = cms.Sequence(akVsFilter6Calocorr
                                                    *
                                                    #akVsFilter6CaloJetID
                                                    #*
                                                    akVsFilter6CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter6CaloJetBtagging
                                                    *
                                                    akVsFilter6CaloNjettiness 
                                                    *
                                                    akVsFilter6CalopatJetsWithBtagging
                                                    *
                                                    akVsFilter6CaloJetAnalyzer
                                                    )

akVsFilter6CaloJetSequence_jec = cms.Sequence(akVsFilter6CaloJetSequence_mc)
akVsFilter6CaloJetSequence_mb = cms.Sequence(akVsFilter6CaloJetSequence_mc)

akVsFilter6CaloJetSequence = cms.Sequence(akVsFilter6CaloJetSequence_jec)
akVsFilter6CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akVsFilter6CaloJetAnalyzer.jetPtMin = cms.double(1)
