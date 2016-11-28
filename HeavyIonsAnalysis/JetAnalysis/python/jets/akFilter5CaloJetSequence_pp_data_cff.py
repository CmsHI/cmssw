

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter5Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter5CaloJets"),
    matched = cms.InputTag("ak5GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akFilter5CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter5GenJets"),
    matched = cms.InputTag("ak5GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akFilter5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter5CaloJets")
                                                        )

akFilter5Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter5CaloJets"),
    payload = "AK5Calo_offline"
    )

akFilter5CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter5CaloJets'))

#akFilter5Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5GenJets'))

akFilter5CalobTagger = bTaggers("akFilter5Calo",0.5)

#create objects locally since they dont load properly otherwise
#akFilter5Calomatch = akFilter5CalobTagger.match
akFilter5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter5CaloJets"), matched = cms.InputTag("genParticles"))
akFilter5CaloPatJetFlavourAssociationLegacy = akFilter5CalobTagger.PatJetFlavourAssociationLegacy
akFilter5CaloPatJetPartons = akFilter5CalobTagger.PatJetPartons
akFilter5CaloJetTracksAssociatorAtVertex = akFilter5CalobTagger.JetTracksAssociatorAtVertex
akFilter5CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter5CaloSimpleSecondaryVertexHighEffBJetTags = akFilter5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter5CaloSimpleSecondaryVertexHighPurBJetTags = akFilter5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter5CaloCombinedSecondaryVertexBJetTags = akFilter5CalobTagger.CombinedSecondaryVertexBJetTags
akFilter5CaloCombinedSecondaryVertexV2BJetTags = akFilter5CalobTagger.CombinedSecondaryVertexV2BJetTags
akFilter5CaloJetBProbabilityBJetTags = akFilter5CalobTagger.JetBProbabilityBJetTags
akFilter5CaloSoftPFMuonByPtBJetTags = akFilter5CalobTagger.SoftPFMuonByPtBJetTags
akFilter5CaloSoftPFMuonByIP3dBJetTags = akFilter5CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter5CaloTrackCountingHighEffBJetTags = akFilter5CalobTagger.TrackCountingHighEffBJetTags
akFilter5CaloTrackCountingHighPurBJetTags = akFilter5CalobTagger.TrackCountingHighPurBJetTags
akFilter5CaloPatJetPartonAssociationLegacy = akFilter5CalobTagger.PatJetPartonAssociationLegacy

akFilter5CaloImpactParameterTagInfos = akFilter5CalobTagger.ImpactParameterTagInfos
akFilter5CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter5CaloJetProbabilityBJetTags = akFilter5CalobTagger.JetProbabilityBJetTags

akFilter5CaloSecondaryVertexTagInfos = akFilter5CalobTagger.SecondaryVertexTagInfos
akFilter5CaloSimpleSecondaryVertexHighEffBJetTags = akFilter5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter5CaloSimpleSecondaryVertexHighPurBJetTags = akFilter5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter5CaloCombinedSecondaryVertexBJetTags = akFilter5CalobTagger.CombinedSecondaryVertexBJetTags
akFilter5CaloCombinedSecondaryVertexV2BJetTags = akFilter5CalobTagger.CombinedSecondaryVertexV2BJetTags

akFilter5CaloSecondaryVertexNegativeTagInfos = akFilter5CalobTagger.SecondaryVertexNegativeTagInfos
akFilter5CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter5CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter5CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter5CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter5CaloNegativeCombinedSecondaryVertexBJetTags = akFilter5CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter5CaloPositiveCombinedSecondaryVertexBJetTags = akFilter5CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter5CaloNegativeCombinedSecondaryVertexV2BJetTags = akFilter5CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter5CaloPositiveCombinedSecondaryVertexV2BJetTags = akFilter5CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter5CaloSoftPFMuonsTagInfos = akFilter5CalobTagger.SoftPFMuonsTagInfos
akFilter5CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter5CaloSoftPFMuonBJetTags = akFilter5CalobTagger.SoftPFMuonBJetTags
akFilter5CaloSoftPFMuonByIP3dBJetTags = akFilter5CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter5CaloSoftPFMuonByPtBJetTags = akFilter5CalobTagger.SoftPFMuonByPtBJetTags
akFilter5CaloNegativeSoftPFMuonByPtBJetTags = akFilter5CalobTagger.NegativeSoftPFMuonByPtBJetTags
akFilter5CaloPositiveSoftPFMuonByPtBJetTags = akFilter5CalobTagger.PositiveSoftPFMuonByPtBJetTags
akFilter5CaloPatJetFlavourIdLegacy = cms.Sequence(akFilter5CaloPatJetPartonAssociationLegacy*akFilter5CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter5CaloPatJetFlavourAssociation = akFilter5CalobTagger.PatJetFlavourAssociation
#akFilter5CaloPatJetFlavourId = cms.Sequence(akFilter5CaloPatJetPartons*akFilter5CaloPatJetFlavourAssociation)

akFilter5CaloJetBtaggingIP       = cms.Sequence(akFilter5CaloImpactParameterTagInfos *
            (akFilter5CaloTrackCountingHighEffBJetTags +
             akFilter5CaloTrackCountingHighPurBJetTags +
             akFilter5CaloJetProbabilityBJetTags +
             akFilter5CaloJetBProbabilityBJetTags 
            )
            )

akFilter5CaloJetBtaggingSV = cms.Sequence(akFilter5CaloImpactParameterTagInfos
            *
            akFilter5CaloSecondaryVertexTagInfos
            * (akFilter5CaloSimpleSecondaryVertexHighEffBJetTags+
                akFilter5CaloSimpleSecondaryVertexHighPurBJetTags+
                akFilter5CaloCombinedSecondaryVertexBJetTags+
                akFilter5CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter5CaloJetBtaggingNegSV = cms.Sequence(akFilter5CaloImpactParameterTagInfos
            *
            akFilter5CaloSecondaryVertexNegativeTagInfos
            * (akFilter5CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter5CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter5CaloNegativeCombinedSecondaryVertexBJetTags+
                akFilter5CaloPositiveCombinedSecondaryVertexBJetTags+
                akFilter5CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter5CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter5CaloJetBtaggingMu = cms.Sequence(akFilter5CaloSoftPFMuonsTagInfos * (akFilter5CaloSoftPFMuonBJetTags
                +
                akFilter5CaloSoftPFMuonByIP3dBJetTags
                +
                akFilter5CaloSoftPFMuonByPtBJetTags
                +
                akFilter5CaloNegativeSoftPFMuonByPtBJetTags
                +
                akFilter5CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter5CaloJetBtagging = cms.Sequence(akFilter5CaloJetBtaggingIP
            *akFilter5CaloJetBtaggingSV
            *akFilter5CaloJetBtaggingNegSV
#            *akFilter5CaloJetBtaggingMu
            )

akFilter5CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter5CaloJets"),
        genJetMatch          = cms.InputTag("akFilter5Calomatch"),
        genPartonMatch       = cms.InputTag("akFilter5Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter5Calocorr")),
        JetPartonMapSource   = cms.InputTag("akFilter5CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter5CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter5CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter5CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter5CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter5CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter5CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter5CaloJetBProbabilityBJetTags"),
            cms.InputTag("akFilter5CaloJetProbabilityBJetTags"),
            #cms.InputTag("akFilter5CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter5CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter5CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter5CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter5CaloJetID"),
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

akFilter5CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter5CaloJets"),
           	    R0  = cms.double( 0.5)
)
akFilter5CalopatJetsWithBtagging.userData.userFloats.src += ['akFilter5CaloNjettiness:tau1','akFilter5CaloNjettiness:tau2','akFilter5CaloNjettiness:tau3']

akFilter5CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter5CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak5GenJets',
                                                             rParam = 0.5,
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
                                                             bTagJetName = cms.untracked.string("akFilter5Calo"),
                                                             jetName = cms.untracked.string("akFilter5Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter5GenJets"),
                                                             doGenTaus = False
                                                             )

akFilter5CaloJetSequence_mc = cms.Sequence(
                                                  #akFilter5Caloclean
                                                  #*
                                                  akFilter5Calomatch
                                                  #*
                                                  #akFilter5CalomatchGroomed
                                                  *
                                                  akFilter5Caloparton
                                                  *
                                                  akFilter5Calocorr
                                                  *
                                                  #akFilter5CaloJetID
                                                  #*
                                                  akFilter5CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter5CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter5CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter5CaloJetBtagging
                                                  *
                                                  akFilter5CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter5CalopatJetsWithBtagging
                                                  *
                                                  akFilter5CaloJetAnalyzer
                                                  )

akFilter5CaloJetSequence_data = cms.Sequence(akFilter5Calocorr
                                                    *
                                                    #akFilter5CaloJetID
                                                    #*
                                                    akFilter5CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter5CaloJetBtagging
                                                    *
                                                    akFilter5CaloNjettiness 
                                                    *
                                                    akFilter5CalopatJetsWithBtagging
                                                    *
                                                    akFilter5CaloJetAnalyzer
                                                    )

akFilter5CaloJetSequence_jec = cms.Sequence(akFilter5CaloJetSequence_mc)
akFilter5CaloJetSequence_mb = cms.Sequence(akFilter5CaloJetSequence_mc)

akFilter5CaloJetSequence = cms.Sequence(akFilter5CaloJetSequence_data)
