

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter5Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter5CaloJets"),
    matched = cms.InputTag("ak5GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akPuFilter5CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter5GenJets"),
    matched = cms.InputTag("ak5GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.5
    )

akPuFilter5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter5CaloJets")
                                                        )

akPuFilter5Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter5CaloJets"),
    payload = "AKPu5Calo_offline"
    )

akPuFilter5CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter5CaloJets'))

#akPuFilter5Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5GenJets'))

akPuFilter5CalobTagger = bTaggers("akPuFilter5Calo",0.5)

#create objects locally since they dont load properly otherwise
#akPuFilter5Calomatch = akPuFilter5CalobTagger.match
akPuFilter5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter5CaloJets"), matched = cms.InputTag("genParticles"))
akPuFilter5CaloPatJetFlavourAssociationLegacy = akPuFilter5CalobTagger.PatJetFlavourAssociationLegacy
akPuFilter5CaloPatJetPartons = akPuFilter5CalobTagger.PatJetPartons
akPuFilter5CaloJetTracksAssociatorAtVertex = akPuFilter5CalobTagger.JetTracksAssociatorAtVertex
akPuFilter5CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter5CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter5CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter5CaloCombinedSecondaryVertexBJetTags = akPuFilter5CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter5CaloCombinedSecondaryVertexV2BJetTags = akPuFilter5CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter5CaloJetBProbabilityBJetTags = akPuFilter5CalobTagger.JetBProbabilityBJetTags
akPuFilter5CaloSoftPFMuonByPtBJetTags = akPuFilter5CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter5CaloSoftPFMuonByIP3dBJetTags = akPuFilter5CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter5CaloTrackCountingHighEffBJetTags = akPuFilter5CalobTagger.TrackCountingHighEffBJetTags
akPuFilter5CaloTrackCountingHighPurBJetTags = akPuFilter5CalobTagger.TrackCountingHighPurBJetTags
akPuFilter5CaloPatJetPartonAssociationLegacy = akPuFilter5CalobTagger.PatJetPartonAssociationLegacy

akPuFilter5CaloImpactParameterTagInfos = akPuFilter5CalobTagger.ImpactParameterTagInfos
akPuFilter5CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter5CaloJetProbabilityBJetTags = akPuFilter5CalobTagger.JetProbabilityBJetTags

akPuFilter5CaloSecondaryVertexTagInfos = akPuFilter5CalobTagger.SecondaryVertexTagInfos
akPuFilter5CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter5CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter5CaloCombinedSecondaryVertexBJetTags = akPuFilter5CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter5CaloCombinedSecondaryVertexV2BJetTags = akPuFilter5CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter5CaloSecondaryVertexNegativeTagInfos = akPuFilter5CalobTagger.SecondaryVertexNegativeTagInfos
akPuFilter5CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter5CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter5CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter5CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter5CaloNegativeCombinedSecondaryVertexBJetTags = akPuFilter5CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter5CaloPositiveCombinedSecondaryVertexBJetTags = akPuFilter5CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter5CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter5CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter5CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter5CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter5CaloSoftPFMuonsTagInfos = akPuFilter5CalobTagger.SoftPFMuonsTagInfos
akPuFilter5CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter5CaloSoftPFMuonBJetTags = akPuFilter5CalobTagger.SoftPFMuonBJetTags
akPuFilter5CaloSoftPFMuonByIP3dBJetTags = akPuFilter5CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter5CaloSoftPFMuonByPtBJetTags = akPuFilter5CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter5CaloNegativeSoftPFMuonByPtBJetTags = akPuFilter5CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter5CaloPositiveSoftPFMuonByPtBJetTags = akPuFilter5CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter5CaloPatJetFlavourIdLegacy = cms.Sequence(akPuFilter5CaloPatJetPartonAssociationLegacy*akPuFilter5CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter5CaloPatJetFlavourAssociation = akPuFilter5CalobTagger.PatJetFlavourAssociation
#akPuFilter5CaloPatJetFlavourId = cms.Sequence(akPuFilter5CaloPatJetPartons*akPuFilter5CaloPatJetFlavourAssociation)

akPuFilter5CaloJetBtaggingIP       = cms.Sequence(akPuFilter5CaloImpactParameterTagInfos *
            (akPuFilter5CaloTrackCountingHighEffBJetTags +
             akPuFilter5CaloTrackCountingHighPurBJetTags +
             akPuFilter5CaloJetProbabilityBJetTags +
             akPuFilter5CaloJetBProbabilityBJetTags 
            )
            )

akPuFilter5CaloJetBtaggingSV = cms.Sequence(akPuFilter5CaloImpactParameterTagInfos
            *
            akPuFilter5CaloSecondaryVertexTagInfos
            * (akPuFilter5CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter5CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter5CaloCombinedSecondaryVertexBJetTags+
                akPuFilter5CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter5CaloJetBtaggingNegSV = cms.Sequence(akPuFilter5CaloImpactParameterTagInfos
            *
            akPuFilter5CaloSecondaryVertexNegativeTagInfos
            * (akPuFilter5CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter5CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter5CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter5CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter5CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter5CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter5CaloJetBtaggingMu = cms.Sequence(akPuFilter5CaloSoftPFMuonsTagInfos * (akPuFilter5CaloSoftPFMuonBJetTags
                +
                akPuFilter5CaloSoftPFMuonByIP3dBJetTags
                +
                akPuFilter5CaloSoftPFMuonByPtBJetTags
                +
                akPuFilter5CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter5CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter5CaloJetBtagging = cms.Sequence(akPuFilter5CaloJetBtaggingIP
            *akPuFilter5CaloJetBtaggingSV
            *akPuFilter5CaloJetBtaggingNegSV
#            *akPuFilter5CaloJetBtaggingMu
            )

akPuFilter5CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter5CaloJets"),
        genJetMatch          = cms.InputTag("akPuFilter5Calomatch"),
        genPartonMatch       = cms.InputTag("akPuFilter5Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter5Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter5CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter5CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter5CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter5CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter5CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter5CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter5CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter5CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter5CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter5CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter5CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter5CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter5CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter5CaloJetID"),
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

akPuFilter5CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter5CaloJets"),
           	    R0  = cms.double( 0.5)
)
akPuFilter5CalopatJetsWithBtagging.userData.userFloats.src += ['akPuFilter5CaloNjettiness:tau1','akPuFilter5CaloNjettiness:tau2','akPuFilter5CaloNjettiness:tau3']

akPuFilter5CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter5CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak5GenJets',
                                                             rParam = 0.5,
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
                                                             bTagJetName = cms.untracked.string("akPuFilter5Calo"),
                                                             jetName = cms.untracked.string("akPuFilter5Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter5GenJets"),
                                                             doGenTaus = True
                                                             )

akPuFilter5CaloJetSequence_mc = cms.Sequence(
                                                  #akPuFilter5Caloclean
                                                  #*
                                                  akPuFilter5Calomatch
                                                  #*
                                                  #akPuFilter5CalomatchGroomed
                                                  *
                                                  akPuFilter5Caloparton
                                                  *
                                                  akPuFilter5Calocorr
                                                  *
                                                  #akPuFilter5CaloJetID
                                                  #*
                                                  akPuFilter5CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter5CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter5CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter5CaloJetBtagging
                                                  *
                                                  akPuFilter5CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter5CalopatJetsWithBtagging
                                                  *
                                                  akPuFilter5CaloJetAnalyzer
                                                  )

akPuFilter5CaloJetSequence_data = cms.Sequence(akPuFilter5Calocorr
                                                    *
                                                    #akPuFilter5CaloJetID
                                                    #*
                                                    akPuFilter5CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter5CaloJetBtagging
                                                    *
                                                    akPuFilter5CaloNjettiness 
                                                    *
                                                    akPuFilter5CalopatJetsWithBtagging
                                                    *
                                                    akPuFilter5CaloJetAnalyzer
                                                    )

akPuFilter5CaloJetSequence_jec = cms.Sequence(akPuFilter5CaloJetSequence_mc)
akPuFilter5CaloJetSequence_mb = cms.Sequence(akPuFilter5CaloJetSequence_mc)

akPuFilter5CaloJetSequence = cms.Sequence(akPuFilter5CaloJetSequence_jec)
akPuFilter5CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akPuFilter5CaloJetAnalyzer.jetPtMin = cms.double(1)
