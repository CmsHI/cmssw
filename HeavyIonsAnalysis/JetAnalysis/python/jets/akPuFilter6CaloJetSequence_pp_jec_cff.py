

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter6Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter6CaloJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akPuFilter6CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter6GenJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akPuFilter6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter6CaloJets")
                                                        )

akPuFilter6Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter6CaloJets"),
    payload = "AKPu6Calo_offline"
    )

akPuFilter6CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter6CaloJets'))

#akPuFilter6Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6GenJets'))

akPuFilter6CalobTagger = bTaggers("akPuFilter6Calo",0.6)

#create objects locally since they dont load properly otherwise
#akPuFilter6Calomatch = akPuFilter6CalobTagger.match
akPuFilter6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter6CaloJets"), matched = cms.InputTag("genParticles"))
akPuFilter6CaloPatJetFlavourAssociationLegacy = akPuFilter6CalobTagger.PatJetFlavourAssociationLegacy
akPuFilter6CaloPatJetPartons = akPuFilter6CalobTagger.PatJetPartons
akPuFilter6CaloJetTracksAssociatorAtVertex = akPuFilter6CalobTagger.JetTracksAssociatorAtVertex
akPuFilter6CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter6CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter6CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter6CaloCombinedSecondaryVertexBJetTags = akPuFilter6CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter6CaloCombinedSecondaryVertexV2BJetTags = akPuFilter6CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter6CaloJetBProbabilityBJetTags = akPuFilter6CalobTagger.JetBProbabilityBJetTags
akPuFilter6CaloSoftPFMuonByPtBJetTags = akPuFilter6CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter6CaloSoftPFMuonByIP3dBJetTags = akPuFilter6CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter6CaloTrackCountingHighEffBJetTags = akPuFilter6CalobTagger.TrackCountingHighEffBJetTags
akPuFilter6CaloTrackCountingHighPurBJetTags = akPuFilter6CalobTagger.TrackCountingHighPurBJetTags
akPuFilter6CaloPatJetPartonAssociationLegacy = akPuFilter6CalobTagger.PatJetPartonAssociationLegacy

akPuFilter6CaloImpactParameterTagInfos = akPuFilter6CalobTagger.ImpactParameterTagInfos
akPuFilter6CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter6CaloJetProbabilityBJetTags = akPuFilter6CalobTagger.JetProbabilityBJetTags

akPuFilter6CaloSecondaryVertexTagInfos = akPuFilter6CalobTagger.SecondaryVertexTagInfos
akPuFilter6CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter6CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter6CaloCombinedSecondaryVertexBJetTags = akPuFilter6CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter6CaloCombinedSecondaryVertexV2BJetTags = akPuFilter6CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter6CaloSecondaryVertexNegativeTagInfos = akPuFilter6CalobTagger.SecondaryVertexNegativeTagInfos
akPuFilter6CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter6CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter6CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter6CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter6CaloNegativeCombinedSecondaryVertexBJetTags = akPuFilter6CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter6CaloPositiveCombinedSecondaryVertexBJetTags = akPuFilter6CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter6CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter6CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter6CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter6CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter6CaloSoftPFMuonsTagInfos = akPuFilter6CalobTagger.SoftPFMuonsTagInfos
akPuFilter6CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter6CaloSoftPFMuonBJetTags = akPuFilter6CalobTagger.SoftPFMuonBJetTags
akPuFilter6CaloSoftPFMuonByIP3dBJetTags = akPuFilter6CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter6CaloSoftPFMuonByPtBJetTags = akPuFilter6CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter6CaloNegativeSoftPFMuonByPtBJetTags = akPuFilter6CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter6CaloPositiveSoftPFMuonByPtBJetTags = akPuFilter6CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter6CaloPatJetFlavourIdLegacy = cms.Sequence(akPuFilter6CaloPatJetPartonAssociationLegacy*akPuFilter6CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter6CaloPatJetFlavourAssociation = akPuFilter6CalobTagger.PatJetFlavourAssociation
#akPuFilter6CaloPatJetFlavourId = cms.Sequence(akPuFilter6CaloPatJetPartons*akPuFilter6CaloPatJetFlavourAssociation)

akPuFilter6CaloJetBtaggingIP       = cms.Sequence(akPuFilter6CaloImpactParameterTagInfos *
            (akPuFilter6CaloTrackCountingHighEffBJetTags +
             akPuFilter6CaloTrackCountingHighPurBJetTags +
             akPuFilter6CaloJetProbabilityBJetTags +
             akPuFilter6CaloJetBProbabilityBJetTags 
            )
            )

akPuFilter6CaloJetBtaggingSV = cms.Sequence(akPuFilter6CaloImpactParameterTagInfos
            *
            akPuFilter6CaloSecondaryVertexTagInfos
            * (akPuFilter6CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter6CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter6CaloCombinedSecondaryVertexBJetTags+
                akPuFilter6CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter6CaloJetBtaggingNegSV = cms.Sequence(akPuFilter6CaloImpactParameterTagInfos
            *
            akPuFilter6CaloSecondaryVertexNegativeTagInfos
            * (akPuFilter6CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter6CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter6CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter6CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter6CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter6CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter6CaloJetBtaggingMu = cms.Sequence(akPuFilter6CaloSoftPFMuonsTagInfos * (akPuFilter6CaloSoftPFMuonBJetTags
                +
                akPuFilter6CaloSoftPFMuonByIP3dBJetTags
                +
                akPuFilter6CaloSoftPFMuonByPtBJetTags
                +
                akPuFilter6CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter6CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter6CaloJetBtagging = cms.Sequence(akPuFilter6CaloJetBtaggingIP
            *akPuFilter6CaloJetBtaggingSV
            *akPuFilter6CaloJetBtaggingNegSV
#            *akPuFilter6CaloJetBtaggingMu
            )

akPuFilter6CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter6CaloJets"),
        genJetMatch          = cms.InputTag("akPuFilter6Calomatch"),
        genPartonMatch       = cms.InputTag("akPuFilter6Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter6Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter6CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter6CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter6CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter6CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter6CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter6CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter6CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter6CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter6CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter6CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter6CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter6CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter6CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter6CaloJetID"),
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

akPuFilter6CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter6CaloJets"),
           	    R0  = cms.double( 0.6)
)
akPuFilter6CalopatJetsWithBtagging.userData.userFloats.src += ['akPuFilter6CaloNjettiness:tau1','akPuFilter6CaloNjettiness:tau2','akPuFilter6CaloNjettiness:tau3']

akPuFilter6CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter6CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuFilter6Calo"),
                                                             jetName = cms.untracked.string("akPuFilter6Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter6GenJets"),
                                                             doGenTaus = True
                                                             )

akPuFilter6CaloJetSequence_mc = cms.Sequence(
                                                  #akPuFilter6Caloclean
                                                  #*
                                                  akPuFilter6Calomatch
                                                  #*
                                                  #akPuFilter6CalomatchGroomed
                                                  *
                                                  akPuFilter6Caloparton
                                                  *
                                                  akPuFilter6Calocorr
                                                  *
                                                  #akPuFilter6CaloJetID
                                                  #*
                                                  akPuFilter6CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter6CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter6CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter6CaloJetBtagging
                                                  *
                                                  akPuFilter6CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter6CalopatJetsWithBtagging
                                                  *
                                                  akPuFilter6CaloJetAnalyzer
                                                  )

akPuFilter6CaloJetSequence_data = cms.Sequence(akPuFilter6Calocorr
                                                    *
                                                    #akPuFilter6CaloJetID
                                                    #*
                                                    akPuFilter6CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter6CaloJetBtagging
                                                    *
                                                    akPuFilter6CaloNjettiness 
                                                    *
                                                    akPuFilter6CalopatJetsWithBtagging
                                                    *
                                                    akPuFilter6CaloJetAnalyzer
                                                    )

akPuFilter6CaloJetSequence_jec = cms.Sequence(akPuFilter6CaloJetSequence_mc)
akPuFilter6CaloJetSequence_mb = cms.Sequence(akPuFilter6CaloJetSequence_mc)

akPuFilter6CaloJetSequence = cms.Sequence(akPuFilter6CaloJetSequence_jec)
akPuFilter6CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akPuFilter6CaloJetAnalyzer.jetPtMin = cms.double(1)
