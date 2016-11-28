

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter1Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter1CaloJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akFilter1CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter1HiGenJets"),
    matched = cms.InputTag("ak1HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.1
    )

akFilter1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter1CaloJets")
                                                        )

akFilter1Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter1CaloJets"),
    payload = "AK1Calo_offline"
    )

akFilter1CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter1CaloJets'))

#akFilter1Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak1HiSignalGenJets'))

akFilter1CalobTagger = bTaggers("akFilter1Calo",0.1)

#create objects locally since they dont load properly otherwise
#akFilter1Calomatch = akFilter1CalobTagger.match
akFilter1Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter1CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akFilter1CaloPatJetFlavourAssociationLegacy = akFilter1CalobTagger.PatJetFlavourAssociationLegacy
akFilter1CaloPatJetPartons = akFilter1CalobTagger.PatJetPartons
akFilter1CaloJetTracksAssociatorAtVertex = akFilter1CalobTagger.JetTracksAssociatorAtVertex
akFilter1CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter1CaloSimpleSecondaryVertexHighEffBJetTags = akFilter1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter1CaloSimpleSecondaryVertexHighPurBJetTags = akFilter1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter1CaloCombinedSecondaryVertexBJetTags = akFilter1CalobTagger.CombinedSecondaryVertexBJetTags
akFilter1CaloCombinedSecondaryVertexV2BJetTags = akFilter1CalobTagger.CombinedSecondaryVertexV2BJetTags
akFilter1CaloJetBProbabilityBJetTags = akFilter1CalobTagger.JetBProbabilityBJetTags
akFilter1CaloSoftPFMuonByPtBJetTags = akFilter1CalobTagger.SoftPFMuonByPtBJetTags
akFilter1CaloSoftPFMuonByIP3dBJetTags = akFilter1CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter1CaloTrackCountingHighEffBJetTags = akFilter1CalobTagger.TrackCountingHighEffBJetTags
akFilter1CaloTrackCountingHighPurBJetTags = akFilter1CalobTagger.TrackCountingHighPurBJetTags
akFilter1CaloPatJetPartonAssociationLegacy = akFilter1CalobTagger.PatJetPartonAssociationLegacy

akFilter1CaloImpactParameterTagInfos = akFilter1CalobTagger.ImpactParameterTagInfos
akFilter1CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter1CaloJetProbabilityBJetTags = akFilter1CalobTagger.JetProbabilityBJetTags

akFilter1CaloSecondaryVertexTagInfos = akFilter1CalobTagger.SecondaryVertexTagInfos
akFilter1CaloSimpleSecondaryVertexHighEffBJetTags = akFilter1CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter1CaloSimpleSecondaryVertexHighPurBJetTags = akFilter1CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter1CaloCombinedSecondaryVertexBJetTags = akFilter1CalobTagger.CombinedSecondaryVertexBJetTags
akFilter1CaloCombinedSecondaryVertexV2BJetTags = akFilter1CalobTagger.CombinedSecondaryVertexV2BJetTags

akFilter1CaloSecondaryVertexNegativeTagInfos = akFilter1CalobTagger.SecondaryVertexNegativeTagInfos
akFilter1CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter1CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter1CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter1CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter1CaloNegativeCombinedSecondaryVertexBJetTags = akFilter1CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter1CaloPositiveCombinedSecondaryVertexBJetTags = akFilter1CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter1CaloNegativeCombinedSecondaryVertexV2BJetTags = akFilter1CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter1CaloPositiveCombinedSecondaryVertexV2BJetTags = akFilter1CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter1CaloSoftPFMuonsTagInfos = akFilter1CalobTagger.SoftPFMuonsTagInfos
akFilter1CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter1CaloSoftPFMuonBJetTags = akFilter1CalobTagger.SoftPFMuonBJetTags
akFilter1CaloSoftPFMuonByIP3dBJetTags = akFilter1CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter1CaloSoftPFMuonByPtBJetTags = akFilter1CalobTagger.SoftPFMuonByPtBJetTags
akFilter1CaloNegativeSoftPFMuonByPtBJetTags = akFilter1CalobTagger.NegativeSoftPFMuonByPtBJetTags
akFilter1CaloPositiveSoftPFMuonByPtBJetTags = akFilter1CalobTagger.PositiveSoftPFMuonByPtBJetTags
akFilter1CaloPatJetFlavourIdLegacy = cms.Sequence(akFilter1CaloPatJetPartonAssociationLegacy*akFilter1CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter1CaloPatJetFlavourAssociation = akFilter1CalobTagger.PatJetFlavourAssociation
#akFilter1CaloPatJetFlavourId = cms.Sequence(akFilter1CaloPatJetPartons*akFilter1CaloPatJetFlavourAssociation)

akFilter1CaloJetBtaggingIP       = cms.Sequence(akFilter1CaloImpactParameterTagInfos *
            (akFilter1CaloTrackCountingHighEffBJetTags +
             akFilter1CaloTrackCountingHighPurBJetTags +
             akFilter1CaloJetProbabilityBJetTags +
             akFilter1CaloJetBProbabilityBJetTags 
            )
            )

akFilter1CaloJetBtaggingSV = cms.Sequence(akFilter1CaloImpactParameterTagInfos
            *
            akFilter1CaloSecondaryVertexTagInfos
            * (akFilter1CaloSimpleSecondaryVertexHighEffBJetTags+
                akFilter1CaloSimpleSecondaryVertexHighPurBJetTags+
                akFilter1CaloCombinedSecondaryVertexBJetTags+
                akFilter1CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter1CaloJetBtaggingNegSV = cms.Sequence(akFilter1CaloImpactParameterTagInfos
            *
            akFilter1CaloSecondaryVertexNegativeTagInfos
            * (akFilter1CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter1CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter1CaloNegativeCombinedSecondaryVertexBJetTags+
                akFilter1CaloPositiveCombinedSecondaryVertexBJetTags+
                akFilter1CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter1CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter1CaloJetBtaggingMu = cms.Sequence(akFilter1CaloSoftPFMuonsTagInfos * (akFilter1CaloSoftPFMuonBJetTags
                +
                akFilter1CaloSoftPFMuonByIP3dBJetTags
                +
                akFilter1CaloSoftPFMuonByPtBJetTags
                +
                akFilter1CaloNegativeSoftPFMuonByPtBJetTags
                +
                akFilter1CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter1CaloJetBtagging = cms.Sequence(akFilter1CaloJetBtaggingIP
            *akFilter1CaloJetBtaggingSV
            *akFilter1CaloJetBtaggingNegSV
#            *akFilter1CaloJetBtaggingMu
            )

akFilter1CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter1CaloJets"),
        genJetMatch          = cms.InputTag("akFilter1Calomatch"),
        genPartonMatch       = cms.InputTag("akFilter1Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter1Calocorr")),
        JetPartonMapSource   = cms.InputTag("akFilter1CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter1CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter1CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter1CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter1CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter1CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter1CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter1CaloJetBProbabilityBJetTags"),
            cms.InputTag("akFilter1CaloJetProbabilityBJetTags"),
            #cms.InputTag("akFilter1CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter1CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter1CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter1CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter1CaloJetID"),
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

akFilter1CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter1CaloJets"),
           	    R0  = cms.double( 0.1)
)
akFilter1CalopatJetsWithBtagging.userData.userFloats.src += ['akFilter1CaloNjettiness:tau1','akFilter1CaloNjettiness:tau2','akFilter1CaloNjettiness:tau3']

akFilter1CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter1CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak1HiGenJets',
                                                             rParam = 0.1,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlowTmp'),
                                                             trackTag = cms.InputTag("hiGeneralTracks"),
                                                             fillGenJets = True,
                                                             isMC = True,
							     doSubEvent = True,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akFilter1Calo"),
                                                             jetName = cms.untracked.string("akFilter1Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter1GenJets"),
                                                             doGenTaus = True
                                                             )

akFilter1CaloJetSequence_mc = cms.Sequence(
                                                  #akFilter1Caloclean
                                                  #*
                                                  akFilter1Calomatch
                                                  #*
                                                  #akFilter1CalomatchGroomed
                                                  *
                                                  akFilter1Caloparton
                                                  *
                                                  akFilter1Calocorr
                                                  *
                                                  #akFilter1CaloJetID
                                                  #*
                                                  akFilter1CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter1CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter1CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter1CaloJetBtagging
                                                  *
                                                  akFilter1CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter1CalopatJetsWithBtagging
                                                  *
                                                  akFilter1CaloJetAnalyzer
                                                  )

akFilter1CaloJetSequence_data = cms.Sequence(akFilter1Calocorr
                                                    *
                                                    #akFilter1CaloJetID
                                                    #*
                                                    akFilter1CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter1CaloJetBtagging
                                                    *
                                                    akFilter1CaloNjettiness 
                                                    *
                                                    akFilter1CalopatJetsWithBtagging
                                                    *
                                                    akFilter1CaloJetAnalyzer
                                                    )

akFilter1CaloJetSequence_jec = cms.Sequence(akFilter1CaloJetSequence_mc)
akFilter1CaloJetSequence_mb = cms.Sequence(akFilter1CaloJetSequence_mc)

akFilter1CaloJetSequence = cms.Sequence(akFilter1CaloJetSequence_jec)
akFilter1CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akFilter1CaloJetAnalyzer.jetPtMin = cms.double(1)
