

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter5Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter5CaloJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.5
    )

akVsFilter5CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter5HiGenJets"),
    matched = cms.InputTag("ak5HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.5
    )

akVsFilter5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter5CaloJets")
                                                        )

akVsFilter5Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter5CaloJets"),
    payload = "AK5Calo_offline"
    )

akVsFilter5CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter5CaloJets'))

#akVsFilter5Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak5HiSignalGenJets'))

akVsFilter5CalobTagger = bTaggers("akVsFilter5Calo",0.5)

#create objects locally since they dont load properly otherwise
#akVsFilter5Calomatch = akVsFilter5CalobTagger.match
akVsFilter5Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter5CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akVsFilter5CaloPatJetFlavourAssociationLegacy = akVsFilter5CalobTagger.PatJetFlavourAssociationLegacy
akVsFilter5CaloPatJetPartons = akVsFilter5CalobTagger.PatJetPartons
akVsFilter5CaloJetTracksAssociatorAtVertex = akVsFilter5CalobTagger.JetTracksAssociatorAtVertex
akVsFilter5CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter5CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter5CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter5CaloCombinedSecondaryVertexBJetTags = akVsFilter5CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter5CaloCombinedSecondaryVertexV2BJetTags = akVsFilter5CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter5CaloJetBProbabilityBJetTags = akVsFilter5CalobTagger.JetBProbabilityBJetTags
akVsFilter5CaloSoftPFMuonByPtBJetTags = akVsFilter5CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter5CaloSoftPFMuonByIP3dBJetTags = akVsFilter5CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter5CaloTrackCountingHighEffBJetTags = akVsFilter5CalobTagger.TrackCountingHighEffBJetTags
akVsFilter5CaloTrackCountingHighPurBJetTags = akVsFilter5CalobTagger.TrackCountingHighPurBJetTags
akVsFilter5CaloPatJetPartonAssociationLegacy = akVsFilter5CalobTagger.PatJetPartonAssociationLegacy

akVsFilter5CaloImpactParameterTagInfos = akVsFilter5CalobTagger.ImpactParameterTagInfos
akVsFilter5CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter5CaloJetProbabilityBJetTags = akVsFilter5CalobTagger.JetProbabilityBJetTags

akVsFilter5CaloSecondaryVertexTagInfos = akVsFilter5CalobTagger.SecondaryVertexTagInfos
akVsFilter5CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter5CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter5CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter5CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter5CaloCombinedSecondaryVertexBJetTags = akVsFilter5CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter5CaloCombinedSecondaryVertexV2BJetTags = akVsFilter5CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter5CaloSecondaryVertexNegativeTagInfos = akVsFilter5CalobTagger.SecondaryVertexNegativeTagInfos
akVsFilter5CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter5CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter5CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter5CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter5CaloNegativeCombinedSecondaryVertexBJetTags = akVsFilter5CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter5CaloPositiveCombinedSecondaryVertexBJetTags = akVsFilter5CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter5CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter5CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter5CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter5CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter5CaloSoftPFMuonsTagInfos = akVsFilter5CalobTagger.SoftPFMuonsTagInfos
akVsFilter5CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter5CaloSoftPFMuonBJetTags = akVsFilter5CalobTagger.SoftPFMuonBJetTags
akVsFilter5CaloSoftPFMuonByIP3dBJetTags = akVsFilter5CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter5CaloSoftPFMuonByPtBJetTags = akVsFilter5CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter5CaloNegativeSoftPFMuonByPtBJetTags = akVsFilter5CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter5CaloPositiveSoftPFMuonByPtBJetTags = akVsFilter5CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter5CaloPatJetFlavourIdLegacy = cms.Sequence(akVsFilter5CaloPatJetPartonAssociationLegacy*akVsFilter5CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter5CaloPatJetFlavourAssociation = akVsFilter5CalobTagger.PatJetFlavourAssociation
#akVsFilter5CaloPatJetFlavourId = cms.Sequence(akVsFilter5CaloPatJetPartons*akVsFilter5CaloPatJetFlavourAssociation)

akVsFilter5CaloJetBtaggingIP       = cms.Sequence(akVsFilter5CaloImpactParameterTagInfos *
            (akVsFilter5CaloTrackCountingHighEffBJetTags +
             akVsFilter5CaloTrackCountingHighPurBJetTags +
             akVsFilter5CaloJetProbabilityBJetTags +
             akVsFilter5CaloJetBProbabilityBJetTags 
            )
            )

akVsFilter5CaloJetBtaggingSV = cms.Sequence(akVsFilter5CaloImpactParameterTagInfos
            *
            akVsFilter5CaloSecondaryVertexTagInfos
            * (akVsFilter5CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter5CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter5CaloCombinedSecondaryVertexBJetTags+
                akVsFilter5CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter5CaloJetBtaggingNegSV = cms.Sequence(akVsFilter5CaloImpactParameterTagInfos
            *
            akVsFilter5CaloSecondaryVertexNegativeTagInfos
            * (akVsFilter5CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter5CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter5CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter5CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter5CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter5CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter5CaloJetBtaggingMu = cms.Sequence(akVsFilter5CaloSoftPFMuonsTagInfos * (akVsFilter5CaloSoftPFMuonBJetTags
                +
                akVsFilter5CaloSoftPFMuonByIP3dBJetTags
                +
                akVsFilter5CaloSoftPFMuonByPtBJetTags
                +
                akVsFilter5CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter5CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter5CaloJetBtagging = cms.Sequence(akVsFilter5CaloJetBtaggingIP
            *akVsFilter5CaloJetBtaggingSV
            *akVsFilter5CaloJetBtaggingNegSV
#            *akVsFilter5CaloJetBtaggingMu
            )

akVsFilter5CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter5CaloJets"),
        genJetMatch          = cms.InputTag("akVsFilter5Calomatch"),
        genPartonMatch       = cms.InputTag("akVsFilter5Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter5Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter5CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter5CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter5CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter5CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter5CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter5CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter5CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter5CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter5CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter5CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter5CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter5CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter5CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter5CaloJetID"),
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

akVsFilter5CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter5CaloJets"),
           	    R0  = cms.double( 0.5)
)
akVsFilter5CalopatJetsWithBtagging.userData.userFloats.src += ['akVsFilter5CaloNjettiness:tau1','akVsFilter5CaloNjettiness:tau2','akVsFilter5CaloNjettiness:tau3']

akVsFilter5CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter5CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak5HiGenJets',
                                                             rParam = 0.5,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJetsWithBtagging',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlowTmp'),
                                                             trackTag = cms.InputTag("hiGeneralTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
							     doSubEvent = False,
                                                             useHepMC = cms.untracked.bool(False),
							     genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator"),
                                                             doLifeTimeTagging = cms.untracked.bool(True),
                                                             doLifeTimeTaggingExtras = cms.untracked.bool(False),
                                                             bTagJetName = cms.untracked.string("akVsFilter5Calo"),
                                                             jetName = cms.untracked.string("akVsFilter5Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter5GenJets"),
                                                             doGenTaus = False
                                                             )

akVsFilter5CaloJetSequence_mc = cms.Sequence(
                                                  #akVsFilter5Caloclean
                                                  #*
                                                  akVsFilter5Calomatch
                                                  #*
                                                  #akVsFilter5CalomatchGroomed
                                                  *
                                                  akVsFilter5Caloparton
                                                  *
                                                  akVsFilter5Calocorr
                                                  *
                                                  #akVsFilter5CaloJetID
                                                  #*
                                                  akVsFilter5CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter5CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter5CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter5CaloJetBtagging
                                                  *
                                                  akVsFilter5CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter5CalopatJetsWithBtagging
                                                  *
                                                  akVsFilter5CaloJetAnalyzer
                                                  )

akVsFilter5CaloJetSequence_data = cms.Sequence(akVsFilter5Calocorr
                                                    *
                                                    #akVsFilter5CaloJetID
                                                    #*
                                                    akVsFilter5CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter5CaloJetBtagging
                                                    *
                                                    akVsFilter5CaloNjettiness 
                                                    *
                                                    akVsFilter5CalopatJetsWithBtagging
                                                    *
                                                    akVsFilter5CaloJetAnalyzer
                                                    )

akVsFilter5CaloJetSequence_jec = cms.Sequence(akVsFilter5CaloJetSequence_mc)
akVsFilter5CaloJetSequence_mb = cms.Sequence(akVsFilter5CaloJetSequence_mc)

akVsFilter5CaloJetSequence = cms.Sequence(akVsFilter5CaloJetSequence_data)
