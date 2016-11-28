

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter2Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter2CaloJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akFilter2CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter2GenJets"),
    matched = cms.InputTag("ak2GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.2
    )

akFilter2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter2CaloJets")
                                                        )

akFilter2Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter2CaloJets"),
    payload = "AK2Calo_offline"
    )

akFilter2CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter2CaloJets'))

#akFilter2Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak2GenJets'))

akFilter2CalobTagger = bTaggers("akFilter2Calo",0.2)

#create objects locally since they dont load properly otherwise
#akFilter2Calomatch = akFilter2CalobTagger.match
akFilter2Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter2CaloJets"), matched = cms.InputTag("genParticles"))
akFilter2CaloPatJetFlavourAssociationLegacy = akFilter2CalobTagger.PatJetFlavourAssociationLegacy
akFilter2CaloPatJetPartons = akFilter2CalobTagger.PatJetPartons
akFilter2CaloJetTracksAssociatorAtVertex = akFilter2CalobTagger.JetTracksAssociatorAtVertex
akFilter2CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter2CaloSimpleSecondaryVertexHighEffBJetTags = akFilter2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter2CaloSimpleSecondaryVertexHighPurBJetTags = akFilter2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter2CaloCombinedSecondaryVertexBJetTags = akFilter2CalobTagger.CombinedSecondaryVertexBJetTags
akFilter2CaloCombinedSecondaryVertexV2BJetTags = akFilter2CalobTagger.CombinedSecondaryVertexV2BJetTags
akFilter2CaloJetBProbabilityBJetTags = akFilter2CalobTagger.JetBProbabilityBJetTags
akFilter2CaloSoftPFMuonByPtBJetTags = akFilter2CalobTagger.SoftPFMuonByPtBJetTags
akFilter2CaloSoftPFMuonByIP3dBJetTags = akFilter2CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter2CaloTrackCountingHighEffBJetTags = akFilter2CalobTagger.TrackCountingHighEffBJetTags
akFilter2CaloTrackCountingHighPurBJetTags = akFilter2CalobTagger.TrackCountingHighPurBJetTags
akFilter2CaloPatJetPartonAssociationLegacy = akFilter2CalobTagger.PatJetPartonAssociationLegacy

akFilter2CaloImpactParameterTagInfos = akFilter2CalobTagger.ImpactParameterTagInfos
akFilter2CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter2CaloJetProbabilityBJetTags = akFilter2CalobTagger.JetProbabilityBJetTags

akFilter2CaloSecondaryVertexTagInfos = akFilter2CalobTagger.SecondaryVertexTagInfos
akFilter2CaloSimpleSecondaryVertexHighEffBJetTags = akFilter2CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter2CaloSimpleSecondaryVertexHighPurBJetTags = akFilter2CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter2CaloCombinedSecondaryVertexBJetTags = akFilter2CalobTagger.CombinedSecondaryVertexBJetTags
akFilter2CaloCombinedSecondaryVertexV2BJetTags = akFilter2CalobTagger.CombinedSecondaryVertexV2BJetTags

akFilter2CaloSecondaryVertexNegativeTagInfos = akFilter2CalobTagger.SecondaryVertexNegativeTagInfos
akFilter2CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter2CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter2CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter2CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter2CaloNegativeCombinedSecondaryVertexBJetTags = akFilter2CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter2CaloPositiveCombinedSecondaryVertexBJetTags = akFilter2CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter2CaloNegativeCombinedSecondaryVertexV2BJetTags = akFilter2CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter2CaloPositiveCombinedSecondaryVertexV2BJetTags = akFilter2CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter2CaloSoftPFMuonsTagInfos = akFilter2CalobTagger.SoftPFMuonsTagInfos
akFilter2CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter2CaloSoftPFMuonBJetTags = akFilter2CalobTagger.SoftPFMuonBJetTags
akFilter2CaloSoftPFMuonByIP3dBJetTags = akFilter2CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter2CaloSoftPFMuonByPtBJetTags = akFilter2CalobTagger.SoftPFMuonByPtBJetTags
akFilter2CaloNegativeSoftPFMuonByPtBJetTags = akFilter2CalobTagger.NegativeSoftPFMuonByPtBJetTags
akFilter2CaloPositiveSoftPFMuonByPtBJetTags = akFilter2CalobTagger.PositiveSoftPFMuonByPtBJetTags
akFilter2CaloPatJetFlavourIdLegacy = cms.Sequence(akFilter2CaloPatJetPartonAssociationLegacy*akFilter2CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter2CaloPatJetFlavourAssociation = akFilter2CalobTagger.PatJetFlavourAssociation
#akFilter2CaloPatJetFlavourId = cms.Sequence(akFilter2CaloPatJetPartons*akFilter2CaloPatJetFlavourAssociation)

akFilter2CaloJetBtaggingIP       = cms.Sequence(akFilter2CaloImpactParameterTagInfos *
            (akFilter2CaloTrackCountingHighEffBJetTags +
             akFilter2CaloTrackCountingHighPurBJetTags +
             akFilter2CaloJetProbabilityBJetTags +
             akFilter2CaloJetBProbabilityBJetTags 
            )
            )

akFilter2CaloJetBtaggingSV = cms.Sequence(akFilter2CaloImpactParameterTagInfos
            *
            akFilter2CaloSecondaryVertexTagInfos
            * (akFilter2CaloSimpleSecondaryVertexHighEffBJetTags+
                akFilter2CaloSimpleSecondaryVertexHighPurBJetTags+
                akFilter2CaloCombinedSecondaryVertexBJetTags+
                akFilter2CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter2CaloJetBtaggingNegSV = cms.Sequence(akFilter2CaloImpactParameterTagInfos
            *
            akFilter2CaloSecondaryVertexNegativeTagInfos
            * (akFilter2CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter2CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter2CaloNegativeCombinedSecondaryVertexBJetTags+
                akFilter2CaloPositiveCombinedSecondaryVertexBJetTags+
                akFilter2CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter2CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter2CaloJetBtaggingMu = cms.Sequence(akFilter2CaloSoftPFMuonsTagInfos * (akFilter2CaloSoftPFMuonBJetTags
                +
                akFilter2CaloSoftPFMuonByIP3dBJetTags
                +
                akFilter2CaloSoftPFMuonByPtBJetTags
                +
                akFilter2CaloNegativeSoftPFMuonByPtBJetTags
                +
                akFilter2CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter2CaloJetBtagging = cms.Sequence(akFilter2CaloJetBtaggingIP
            *akFilter2CaloJetBtaggingSV
            *akFilter2CaloJetBtaggingNegSV
#            *akFilter2CaloJetBtaggingMu
            )

akFilter2CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter2CaloJets"),
        genJetMatch          = cms.InputTag("akFilter2Calomatch"),
        genPartonMatch       = cms.InputTag("akFilter2Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter2Calocorr")),
        JetPartonMapSource   = cms.InputTag("akFilter2CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter2CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter2CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter2CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter2CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter2CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter2CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter2CaloJetBProbabilityBJetTags"),
            cms.InputTag("akFilter2CaloJetProbabilityBJetTags"),
            #cms.InputTag("akFilter2CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter2CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter2CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter2CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter2CaloJetID"),
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

akFilter2CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter2CaloJets"),
           	    R0  = cms.double( 0.2)
)
akFilter2CalopatJetsWithBtagging.userData.userFloats.src += ['akFilter2CaloNjettiness:tau1','akFilter2CaloNjettiness:tau2','akFilter2CaloNjettiness:tau3']

akFilter2CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter2CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akFilter2Calo"),
                                                             jetName = cms.untracked.string("akFilter2Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter2GenJets"),
                                                             doGenTaus = True
                                                             )

akFilter2CaloJetSequence_mc = cms.Sequence(
                                                  #akFilter2Caloclean
                                                  #*
                                                  akFilter2Calomatch
                                                  #*
                                                  #akFilter2CalomatchGroomed
                                                  *
                                                  akFilter2Caloparton
                                                  *
                                                  akFilter2Calocorr
                                                  *
                                                  #akFilter2CaloJetID
                                                  #*
                                                  akFilter2CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter2CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter2CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter2CaloJetBtagging
                                                  *
                                                  akFilter2CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter2CalopatJetsWithBtagging
                                                  *
                                                  akFilter2CaloJetAnalyzer
                                                  )

akFilter2CaloJetSequence_data = cms.Sequence(akFilter2Calocorr
                                                    *
                                                    #akFilter2CaloJetID
                                                    #*
                                                    akFilter2CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter2CaloJetBtagging
                                                    *
                                                    akFilter2CaloNjettiness 
                                                    *
                                                    akFilter2CalopatJetsWithBtagging
                                                    *
                                                    akFilter2CaloJetAnalyzer
                                                    )

akFilter2CaloJetSequence_jec = cms.Sequence(akFilter2CaloJetSequence_mc)
akFilter2CaloJetSequence_mb = cms.Sequence(akFilter2CaloJetSequence_mc)

akFilter2CaloJetSequence = cms.Sequence(akFilter2CaloJetSequence_jec)
akFilter2CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akFilter2CaloJetAnalyzer.jetPtMin = cms.double(1)
