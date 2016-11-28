

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsFilter4Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsFilter4CaloJets"),
    matched = cms.InputTag("ak4HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.4
    )

akVsFilter4CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter4HiGenJets"),
    matched = cms.InputTag("ak4HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.4
    )

akVsFilter4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter4CaloJets")
                                                        )

akVsFilter4Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsFilter4CaloJets"),
    payload = "AK4Calo_offline"
    )

akVsFilter4CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsFilter4CaloJets'))

#akVsFilter4Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4HiCleanedGenJets'))

akVsFilter4CalobTagger = bTaggers("akVsFilter4Calo",0.4)

#create objects locally since they dont load properly otherwise
#akVsFilter4Calomatch = akVsFilter4CalobTagger.match
akVsFilter4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsFilter4CaloJets"), matched = cms.InputTag("selectedPartons"))
akVsFilter4CaloPatJetFlavourAssociationLegacy = akVsFilter4CalobTagger.PatJetFlavourAssociationLegacy
akVsFilter4CaloPatJetPartons = akVsFilter4CalobTagger.PatJetPartons
akVsFilter4CaloJetTracksAssociatorAtVertex = akVsFilter4CalobTagger.JetTracksAssociatorAtVertex
akVsFilter4CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsFilter4CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter4CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter4CaloCombinedSecondaryVertexBJetTags = akVsFilter4CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter4CaloCombinedSecondaryVertexV2BJetTags = akVsFilter4CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsFilter4CaloJetBProbabilityBJetTags = akVsFilter4CalobTagger.JetBProbabilityBJetTags
akVsFilter4CaloSoftPFMuonByPtBJetTags = akVsFilter4CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter4CaloSoftPFMuonByIP3dBJetTags = akVsFilter4CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter4CaloTrackCountingHighEffBJetTags = akVsFilter4CalobTagger.TrackCountingHighEffBJetTags
akVsFilter4CaloTrackCountingHighPurBJetTags = akVsFilter4CalobTagger.TrackCountingHighPurBJetTags
akVsFilter4CaloPatJetPartonAssociationLegacy = akVsFilter4CalobTagger.PatJetPartonAssociationLegacy

akVsFilter4CaloImpactParameterTagInfos = akVsFilter4CalobTagger.ImpactParameterTagInfos
akVsFilter4CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter4CaloJetProbabilityBJetTags = akVsFilter4CalobTagger.JetProbabilityBJetTags

akVsFilter4CaloSecondaryVertexTagInfos = akVsFilter4CalobTagger.SecondaryVertexTagInfos
akVsFilter4CaloSimpleSecondaryVertexHighEffBJetTags = akVsFilter4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsFilter4CaloSimpleSecondaryVertexHighPurBJetTags = akVsFilter4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsFilter4CaloCombinedSecondaryVertexBJetTags = akVsFilter4CalobTagger.CombinedSecondaryVertexBJetTags
akVsFilter4CaloCombinedSecondaryVertexV2BJetTags = akVsFilter4CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsFilter4CaloSecondaryVertexNegativeTagInfos = akVsFilter4CalobTagger.SecondaryVertexNegativeTagInfos
akVsFilter4CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsFilter4CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsFilter4CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsFilter4CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsFilter4CaloNegativeCombinedSecondaryVertexBJetTags = akVsFilter4CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsFilter4CaloPositiveCombinedSecondaryVertexBJetTags = akVsFilter4CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsFilter4CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsFilter4CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsFilter4CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsFilter4CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsFilter4CaloSoftPFMuonsTagInfos = akVsFilter4CalobTagger.SoftPFMuonsTagInfos
akVsFilter4CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsFilter4CaloSoftPFMuonBJetTags = akVsFilter4CalobTagger.SoftPFMuonBJetTags
akVsFilter4CaloSoftPFMuonByIP3dBJetTags = akVsFilter4CalobTagger.SoftPFMuonByIP3dBJetTags
akVsFilter4CaloSoftPFMuonByPtBJetTags = akVsFilter4CalobTagger.SoftPFMuonByPtBJetTags
akVsFilter4CaloNegativeSoftPFMuonByPtBJetTags = akVsFilter4CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsFilter4CaloPositiveSoftPFMuonByPtBJetTags = akVsFilter4CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsFilter4CaloPatJetFlavourIdLegacy = cms.Sequence(akVsFilter4CaloPatJetPartonAssociationLegacy*akVsFilter4CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsFilter4CaloPatJetFlavourAssociation = akVsFilter4CalobTagger.PatJetFlavourAssociation
#akVsFilter4CaloPatJetFlavourId = cms.Sequence(akVsFilter4CaloPatJetPartons*akVsFilter4CaloPatJetFlavourAssociation)

akVsFilter4CaloJetBtaggingIP       = cms.Sequence(akVsFilter4CaloImpactParameterTagInfos *
            (akVsFilter4CaloTrackCountingHighEffBJetTags +
             akVsFilter4CaloTrackCountingHighPurBJetTags +
             akVsFilter4CaloJetProbabilityBJetTags +
             akVsFilter4CaloJetBProbabilityBJetTags 
            )
            )

akVsFilter4CaloJetBtaggingSV = cms.Sequence(akVsFilter4CaloImpactParameterTagInfos
            *
            akVsFilter4CaloSecondaryVertexTagInfos
            * (akVsFilter4CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter4CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter4CaloCombinedSecondaryVertexBJetTags+
                akVsFilter4CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter4CaloJetBtaggingNegSV = cms.Sequence(akVsFilter4CaloImpactParameterTagInfos
            *
            akVsFilter4CaloSecondaryVertexNegativeTagInfos
            * (akVsFilter4CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsFilter4CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsFilter4CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsFilter4CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsFilter4CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsFilter4CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsFilter4CaloJetBtaggingMu = cms.Sequence(akVsFilter4CaloSoftPFMuonsTagInfos * (akVsFilter4CaloSoftPFMuonBJetTags
                +
                akVsFilter4CaloSoftPFMuonByIP3dBJetTags
                +
                akVsFilter4CaloSoftPFMuonByPtBJetTags
                +
                akVsFilter4CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsFilter4CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsFilter4CaloJetBtagging = cms.Sequence(akVsFilter4CaloJetBtaggingIP
            *akVsFilter4CaloJetBtaggingSV
            *akVsFilter4CaloJetBtaggingNegSV
#            *akVsFilter4CaloJetBtaggingMu
            )

akVsFilter4CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsFilter4CaloJets"),
        genJetMatch          = cms.InputTag("akVsFilter4Calomatch"),
        genPartonMatch       = cms.InputTag("akVsFilter4Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsFilter4Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsFilter4CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsFilter4CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsFilter4CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsFilter4CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsFilter4CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsFilter4CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsFilter4CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsFilter4CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsFilter4CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsFilter4CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsFilter4CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsFilter4CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsFilter4CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsFilter4CaloJetID"),
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

akVsFilter4CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsFilter4CaloJets"),
           	    R0  = cms.double( 0.4)
)
akVsFilter4CalopatJetsWithBtagging.userData.userFloats.src += ['akVsFilter4CaloNjettiness:tau1','akVsFilter4CaloNjettiness:tau2','akVsFilter4CaloNjettiness:tau3']

akVsFilter4CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsFilter4CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak4HiGenJets',
                                                             rParam = 0.4,
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
                                                             bTagJetName = cms.untracked.string("akVsFilter4Calo"),
                                                             jetName = cms.untracked.string("akVsFilter4Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter4GenJets"),
                                                             doGenTaus = True
                                                             )

akVsFilter4CaloJetSequence_mc = cms.Sequence(
                                                  #akVsFilter4Caloclean
                                                  #*
                                                  akVsFilter4Calomatch
                                                  #*
                                                  #akVsFilter4CalomatchGroomed
                                                  *
                                                  akVsFilter4Caloparton
                                                  *
                                                  akVsFilter4Calocorr
                                                  *
                                                  #akVsFilter4CaloJetID
                                                  #*
                                                  akVsFilter4CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsFilter4CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsFilter4CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsFilter4CaloJetBtagging
                                                  *
                                                  akVsFilter4CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsFilter4CalopatJetsWithBtagging
                                                  *
                                                  akVsFilter4CaloJetAnalyzer
                                                  )

akVsFilter4CaloJetSequence_data = cms.Sequence(akVsFilter4Calocorr
                                                    *
                                                    #akVsFilter4CaloJetID
                                                    #*
                                                    akVsFilter4CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsFilter4CaloJetBtagging
                                                    *
                                                    akVsFilter4CaloNjettiness 
                                                    *
                                                    akVsFilter4CalopatJetsWithBtagging
                                                    *
                                                    akVsFilter4CaloJetAnalyzer
                                                    )

akVsFilter4CaloJetSequence_jec = cms.Sequence(akVsFilter4CaloJetSequence_mc)
akVsFilter4CaloJetSequence_mb = cms.Sequence(akVsFilter4CaloJetSequence_mc)

akVsFilter4CaloJetSequence = cms.Sequence(akVsFilter4CaloJetSequence_mb)
