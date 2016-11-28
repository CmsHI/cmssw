

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop1Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop1CaloJets"),
    matched = cms.InputTag("ak1GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akPuSoftDrop1CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop1GenJets"),
    matched = cms.InputTag("ak1GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akPuSoftDrop1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop1CaloJets")
                                                        )

akPuSoftDrop1Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop1CaloJets"),
    payload = "AKPu1Calo_offline"
    )

akPuSoftDrop1CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop1CaloJets'))

#akPuSoftDrop1Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1GenJets'))

akPuSoftDrop1CalobTagger = bTaggers("akPuSoftDrop1Calo",0.1)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop1Calomatch = akPuSoftDrop1CalobTagger.match
akPuSoftDrop1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop1CaloJets"), matched = cms.InputTag("genParticles"))
akPuSoftDrop1CaloPatJetFlavourAssociationLegacy = akPuSoftDrop1CalobTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop1CaloPatJetPartons = akPuSoftDrop1CalobTagger.PatJetPartons
akPuSoftDrop1CaloJetTracksAssociatorAtVertex = akPuSoftDrop1CalobTagger.JetTracksAssociatorAtVertex
akPuSoftDrop1CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop1CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop1CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop1CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop1CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop1CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop1CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop1CaloJetBProbabilityBJetTags = akPuSoftDrop1CalobTagger.JetBProbabilityBJetTags
akPuSoftDrop1CaloSoftPFMuonByPtBJetTags = akPuSoftDrop1CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop1CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop1CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop1CaloTrackCountingHighEffBJetTags = akPuSoftDrop1CalobTagger.TrackCountingHighEffBJetTags
akPuSoftDrop1CaloTrackCountingHighPurBJetTags = akPuSoftDrop1CalobTagger.TrackCountingHighPurBJetTags
akPuSoftDrop1CaloPatJetPartonAssociationLegacy = akPuSoftDrop1CalobTagger.PatJetPartonAssociationLegacy

akPuSoftDrop1CaloImpactParameterTagInfos = akPuSoftDrop1CalobTagger.ImpactParameterTagInfos
akPuSoftDrop1CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop1CaloJetProbabilityBJetTags = akPuSoftDrop1CalobTagger.JetProbabilityBJetTags

akPuSoftDrop1CaloSecondaryVertexTagInfos = akPuSoftDrop1CalobTagger.SecondaryVertexTagInfos
akPuSoftDrop1CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop1CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop1CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop1CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop1CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop1CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop1CaloSecondaryVertexNegativeTagInfos = akPuSoftDrop1CalobTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop1CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop1CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop1CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop1CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop1CaloNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop1CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop1CaloPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop1CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop1CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop1CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop1CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop1CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop1CaloSoftPFMuonsTagInfos = akPuSoftDrop1CalobTagger.SoftPFMuonsTagInfos
akPuSoftDrop1CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop1CaloSoftPFMuonBJetTags = akPuSoftDrop1CalobTagger.SoftPFMuonBJetTags
akPuSoftDrop1CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop1CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop1CaloSoftPFMuonByPtBJetTags = akPuSoftDrop1CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop1CaloNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop1CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop1CaloPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop1CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop1CaloPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop1CaloPatJetPartonAssociationLegacy*akPuSoftDrop1CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop1CaloPatJetFlavourAssociation = akPuSoftDrop1CalobTagger.PatJetFlavourAssociation
#akPuSoftDrop1CaloPatJetFlavourId = cms.Sequence(akPuSoftDrop1CaloPatJetPartons*akPuSoftDrop1CaloPatJetFlavourAssociation)

akPuSoftDrop1CaloJetBtaggingIP       = cms.Sequence(akPuSoftDrop1CaloImpactParameterTagInfos *
            (akPuSoftDrop1CaloTrackCountingHighEffBJetTags +
             akPuSoftDrop1CaloTrackCountingHighPurBJetTags +
             akPuSoftDrop1CaloJetProbabilityBJetTags +
             akPuSoftDrop1CaloJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop1CaloJetBtaggingSV = cms.Sequence(akPuSoftDrop1CaloImpactParameterTagInfos
            *
            akPuSoftDrop1CaloSecondaryVertexTagInfos
            * (akPuSoftDrop1CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop1CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop1CaloCombinedSecondaryVertexBJetTags+
                akPuSoftDrop1CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop1CaloJetBtaggingNegSV = cms.Sequence(akPuSoftDrop1CaloImpactParameterTagInfos
            *
            akPuSoftDrop1CaloSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop1CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop1CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop1CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop1CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop1CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop1CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop1CaloJetBtaggingMu = cms.Sequence(akPuSoftDrop1CaloSoftPFMuonsTagInfos * (akPuSoftDrop1CaloSoftPFMuonBJetTags
                +
                akPuSoftDrop1CaloSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop1CaloSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop1CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop1CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop1CaloJetBtagging = cms.Sequence(akPuSoftDrop1CaloJetBtaggingIP
            *akPuSoftDrop1CaloJetBtaggingSV
            *akPuSoftDrop1CaloJetBtaggingNegSV
#            *akPuSoftDrop1CaloJetBtaggingMu
            )

akPuSoftDrop1CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop1CaloJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop1Calomatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop1Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop1Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop1CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop1CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop1CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop1CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop1CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop1CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop1CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop1CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop1CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop1CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop1CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop1CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop1CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop1CaloJetID"),
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

akPuSoftDrop1CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop1CaloJets"),
           	    R0  = cms.double( 0.1)
)
akPuSoftDrop1CalopatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop1CaloNjettiness:tau1','akPuSoftDrop1CaloNjettiness:tau2','akPuSoftDrop1CaloNjettiness:tau3']

akPuSoftDrop1CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop1CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak1GenJets',
                                                             rParam = 0.1,
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop1Calo"),
                                                             jetName = cms.untracked.string("akPuSoftDrop1Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop1GenJets"),
                                                             doGenTaus = True
                                                             )

akPuSoftDrop1CaloJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop1Caloclean
                                                  #*
                                                  akPuSoftDrop1Calomatch
                                                  #*
                                                  #akPuSoftDrop1CalomatchGroomed
                                                  *
                                                  akPuSoftDrop1Caloparton
                                                  *
                                                  akPuSoftDrop1Calocorr
                                                  *
                                                  #akPuSoftDrop1CaloJetID
                                                  #*
                                                  akPuSoftDrop1CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop1CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop1CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop1CaloJetBtagging
                                                  *
                                                  akPuSoftDrop1CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop1CalopatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop1CaloJetAnalyzer
                                                  )

akPuSoftDrop1CaloJetSequence_data = cms.Sequence(akPuSoftDrop1Calocorr
                                                    *
                                                    #akPuSoftDrop1CaloJetID
                                                    #*
                                                    akPuSoftDrop1CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop1CaloJetBtagging
                                                    *
                                                    akPuSoftDrop1CaloNjettiness 
                                                    *
                                                    akPuSoftDrop1CalopatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop1CaloJetAnalyzer
                                                    )

akPuSoftDrop1CaloJetSequence_jec = cms.Sequence(akPuSoftDrop1CaloJetSequence_mc)
akPuSoftDrop1CaloJetSequence_mb = cms.Sequence(akPuSoftDrop1CaloJetSequence_mc)

akPuSoftDrop1CaloJetSequence = cms.Sequence(akPuSoftDrop1CaloJetSequence_jec)
akPuSoftDrop1CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akPuSoftDrop1CaloJetAnalyzer.jetPtMin = cms.double(1)
