

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akSoftDrop6Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop6CaloJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akSoftDrop6CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop6GenJets"),
    matched = cms.InputTag("ak6GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akSoftDrop6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop6CaloJets")
                                                        )

akSoftDrop6Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akSoftDrop6CaloJets"),
    payload = "AK6Calo_offline"
    )

akSoftDrop6CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akSoftDrop6CaloJets'))

#akSoftDrop6Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6GenJets'))

akSoftDrop6CalobTagger = bTaggers("akSoftDrop6Calo",0.6)

#create objects locally since they dont load properly otherwise
#akSoftDrop6Calomatch = akSoftDrop6CalobTagger.match
akSoftDrop6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akSoftDrop6CaloJets"), matched = cms.InputTag("genParticles"))
akSoftDrop6CaloPatJetFlavourAssociationLegacy = akSoftDrop6CalobTagger.PatJetFlavourAssociationLegacy
akSoftDrop6CaloPatJetPartons = akSoftDrop6CalobTagger.PatJetPartons
akSoftDrop6CaloJetTracksAssociatorAtVertex = akSoftDrop6CalobTagger.JetTracksAssociatorAtVertex
akSoftDrop6CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop6CaloCombinedSecondaryVertexBJetTags = akSoftDrop6CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop6CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop6CalobTagger.CombinedSecondaryVertexV2BJetTags
akSoftDrop6CaloJetBProbabilityBJetTags = akSoftDrop6CalobTagger.JetBProbabilityBJetTags
akSoftDrop6CaloSoftPFMuonByPtBJetTags = akSoftDrop6CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop6CaloSoftPFMuonByIP3dBJetTags = akSoftDrop6CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop6CaloTrackCountingHighEffBJetTags = akSoftDrop6CalobTagger.TrackCountingHighEffBJetTags
akSoftDrop6CaloTrackCountingHighPurBJetTags = akSoftDrop6CalobTagger.TrackCountingHighPurBJetTags
akSoftDrop6CaloPatJetPartonAssociationLegacy = akSoftDrop6CalobTagger.PatJetPartonAssociationLegacy

akSoftDrop6CaloImpactParameterTagInfos = akSoftDrop6CalobTagger.ImpactParameterTagInfos
akSoftDrop6CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop6CaloJetProbabilityBJetTags = akSoftDrop6CalobTagger.JetProbabilityBJetTags

akSoftDrop6CaloSecondaryVertexTagInfos = akSoftDrop6CalobTagger.SecondaryVertexTagInfos
akSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags = akSoftDrop6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags = akSoftDrop6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akSoftDrop6CaloCombinedSecondaryVertexBJetTags = akSoftDrop6CalobTagger.CombinedSecondaryVertexBJetTags
akSoftDrop6CaloCombinedSecondaryVertexV2BJetTags = akSoftDrop6CalobTagger.CombinedSecondaryVertexV2BJetTags

akSoftDrop6CaloSecondaryVertexNegativeTagInfos = akSoftDrop6CalobTagger.SecondaryVertexNegativeTagInfos
akSoftDrop6CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akSoftDrop6CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akSoftDrop6CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akSoftDrop6CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akSoftDrop6CaloNegativeCombinedSecondaryVertexBJetTags = akSoftDrop6CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akSoftDrop6CaloPositiveCombinedSecondaryVertexBJetTags = akSoftDrop6CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akSoftDrop6CaloNegativeCombinedSecondaryVertexV2BJetTags = akSoftDrop6CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akSoftDrop6CaloPositiveCombinedSecondaryVertexV2BJetTags = akSoftDrop6CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akSoftDrop6CaloSoftPFMuonsTagInfos = akSoftDrop6CalobTagger.SoftPFMuonsTagInfos
akSoftDrop6CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akSoftDrop6CaloSoftPFMuonBJetTags = akSoftDrop6CalobTagger.SoftPFMuonBJetTags
akSoftDrop6CaloSoftPFMuonByIP3dBJetTags = akSoftDrop6CalobTagger.SoftPFMuonByIP3dBJetTags
akSoftDrop6CaloSoftPFMuonByPtBJetTags = akSoftDrop6CalobTagger.SoftPFMuonByPtBJetTags
akSoftDrop6CaloNegativeSoftPFMuonByPtBJetTags = akSoftDrop6CalobTagger.NegativeSoftPFMuonByPtBJetTags
akSoftDrop6CaloPositiveSoftPFMuonByPtBJetTags = akSoftDrop6CalobTagger.PositiveSoftPFMuonByPtBJetTags
akSoftDrop6CaloPatJetFlavourIdLegacy = cms.Sequence(akSoftDrop6CaloPatJetPartonAssociationLegacy*akSoftDrop6CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akSoftDrop6CaloPatJetFlavourAssociation = akSoftDrop6CalobTagger.PatJetFlavourAssociation
#akSoftDrop6CaloPatJetFlavourId = cms.Sequence(akSoftDrop6CaloPatJetPartons*akSoftDrop6CaloPatJetFlavourAssociation)

akSoftDrop6CaloJetBtaggingIP       = cms.Sequence(akSoftDrop6CaloImpactParameterTagInfos *
            (akSoftDrop6CaloTrackCountingHighEffBJetTags +
             akSoftDrop6CaloTrackCountingHighPurBJetTags +
             akSoftDrop6CaloJetProbabilityBJetTags +
             akSoftDrop6CaloJetBProbabilityBJetTags 
            )
            )

akSoftDrop6CaloJetBtaggingSV = cms.Sequence(akSoftDrop6CaloImpactParameterTagInfos
            *
            akSoftDrop6CaloSecondaryVertexTagInfos
            * (akSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop6CaloCombinedSecondaryVertexBJetTags+
                akSoftDrop6CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop6CaloJetBtaggingNegSV = cms.Sequence(akSoftDrop6CaloImpactParameterTagInfos
            *
            akSoftDrop6CaloSecondaryVertexNegativeTagInfos
            * (akSoftDrop6CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akSoftDrop6CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akSoftDrop6CaloNegativeCombinedSecondaryVertexBJetTags+
                akSoftDrop6CaloPositiveCombinedSecondaryVertexBJetTags+
                akSoftDrop6CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akSoftDrop6CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akSoftDrop6CaloJetBtaggingMu = cms.Sequence(akSoftDrop6CaloSoftPFMuonsTagInfos * (akSoftDrop6CaloSoftPFMuonBJetTags
                +
                akSoftDrop6CaloSoftPFMuonByIP3dBJetTags
                +
                akSoftDrop6CaloSoftPFMuonByPtBJetTags
                +
                akSoftDrop6CaloNegativeSoftPFMuonByPtBJetTags
                +
                akSoftDrop6CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akSoftDrop6CaloJetBtagging = cms.Sequence(akSoftDrop6CaloJetBtaggingIP
            *akSoftDrop6CaloJetBtaggingSV
            *akSoftDrop6CaloJetBtaggingNegSV
#            *akSoftDrop6CaloJetBtaggingMu
            )

akSoftDrop6CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akSoftDrop6CaloJets"),
        genJetMatch          = cms.InputTag("akSoftDrop6Calomatch"),
        genPartonMatch       = cms.InputTag("akSoftDrop6Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akSoftDrop6Calocorr")),
        JetPartonMapSource   = cms.InputTag("akSoftDrop6CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akSoftDrop6CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akSoftDrop6CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akSoftDrop6CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akSoftDrop6CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akSoftDrop6CaloJetBProbabilityBJetTags"),
            cms.InputTag("akSoftDrop6CaloJetProbabilityBJetTags"),
            #cms.InputTag("akSoftDrop6CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akSoftDrop6CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akSoftDrop6CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akSoftDrop6CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akSoftDrop6CaloJetID"),
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

akSoftDrop6CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akSoftDrop6CaloJets"),
           	    R0  = cms.double( 0.6)
)
akSoftDrop6CalopatJetsWithBtagging.userData.userFloats.src += ['akSoftDrop6CaloNjettiness:tau1','akSoftDrop6CaloNjettiness:tau2','akSoftDrop6CaloNjettiness:tau3']

akSoftDrop6CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akSoftDrop6CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak6GenJets',
                                                             rParam = 0.6,
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
                                                             bTagJetName = cms.untracked.string("akSoftDrop6Calo"),
                                                             jetName = cms.untracked.string("akSoftDrop6Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop6GenJets"),
                                                             doGenTaus = False
                                                             )

akSoftDrop6CaloJetSequence_mc = cms.Sequence(
                                                  #akSoftDrop6Caloclean
                                                  #*
                                                  akSoftDrop6Calomatch
                                                  #*
                                                  #akSoftDrop6CalomatchGroomed
                                                  *
                                                  akSoftDrop6Caloparton
                                                  *
                                                  akSoftDrop6Calocorr
                                                  *
                                                  #akSoftDrop6CaloJetID
                                                  #*
                                                  akSoftDrop6CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akSoftDrop6CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akSoftDrop6CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akSoftDrop6CaloJetBtagging
                                                  *
                                                  akSoftDrop6CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akSoftDrop6CalopatJetsWithBtagging
                                                  *
                                                  akSoftDrop6CaloJetAnalyzer
                                                  )

akSoftDrop6CaloJetSequence_data = cms.Sequence(akSoftDrop6Calocorr
                                                    *
                                                    #akSoftDrop6CaloJetID
                                                    #*
                                                    akSoftDrop6CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akSoftDrop6CaloJetBtagging
                                                    *
                                                    akSoftDrop6CaloNjettiness 
                                                    *
                                                    akSoftDrop6CalopatJetsWithBtagging
                                                    *
                                                    akSoftDrop6CaloJetAnalyzer
                                                    )

akSoftDrop6CaloJetSequence_jec = cms.Sequence(akSoftDrop6CaloJetSequence_mc)
akSoftDrop6CaloJetSequence_mb = cms.Sequence(akSoftDrop6CaloJetSequence_mc)

akSoftDrop6CaloJetSequence = cms.Sequence(akSoftDrop6CaloJetSequence_data)
