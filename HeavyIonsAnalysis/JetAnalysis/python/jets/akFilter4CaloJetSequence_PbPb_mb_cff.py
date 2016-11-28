

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter4Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter4CaloJets"),
    matched = cms.InputTag("ak4HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akFilter4CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter4HiGenJets"),
    matched = cms.InputTag("ak4HiCleanedGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akFilter4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter4CaloJets")
                                                        )

akFilter4Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter4CaloJets"),
    payload = "AK4Calo_offline"
    )

akFilter4CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter4CaloJets'))

#akFilter4Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4HiCleanedGenJets'))

akFilter4CalobTagger = bTaggers("akFilter4Calo",0.4)

#create objects locally since they dont load properly otherwise
#akFilter4Calomatch = akFilter4CalobTagger.match
akFilter4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter4CaloJets"), matched = cms.InputTag("selectedPartons"))
akFilter4CaloPatJetFlavourAssociationLegacy = akFilter4CalobTagger.PatJetFlavourAssociationLegacy
akFilter4CaloPatJetPartons = akFilter4CalobTagger.PatJetPartons
akFilter4CaloJetTracksAssociatorAtVertex = akFilter4CalobTagger.JetTracksAssociatorAtVertex
akFilter4CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter4CaloSimpleSecondaryVertexHighEffBJetTags = akFilter4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter4CaloSimpleSecondaryVertexHighPurBJetTags = akFilter4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter4CaloCombinedSecondaryVertexBJetTags = akFilter4CalobTagger.CombinedSecondaryVertexBJetTags
akFilter4CaloCombinedSecondaryVertexV2BJetTags = akFilter4CalobTagger.CombinedSecondaryVertexV2BJetTags
akFilter4CaloJetBProbabilityBJetTags = akFilter4CalobTagger.JetBProbabilityBJetTags
akFilter4CaloSoftPFMuonByPtBJetTags = akFilter4CalobTagger.SoftPFMuonByPtBJetTags
akFilter4CaloSoftPFMuonByIP3dBJetTags = akFilter4CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter4CaloTrackCountingHighEffBJetTags = akFilter4CalobTagger.TrackCountingHighEffBJetTags
akFilter4CaloTrackCountingHighPurBJetTags = akFilter4CalobTagger.TrackCountingHighPurBJetTags
akFilter4CaloPatJetPartonAssociationLegacy = akFilter4CalobTagger.PatJetPartonAssociationLegacy

akFilter4CaloImpactParameterTagInfos = akFilter4CalobTagger.ImpactParameterTagInfos
akFilter4CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter4CaloJetProbabilityBJetTags = akFilter4CalobTagger.JetProbabilityBJetTags

akFilter4CaloSecondaryVertexTagInfos = akFilter4CalobTagger.SecondaryVertexTagInfos
akFilter4CaloSimpleSecondaryVertexHighEffBJetTags = akFilter4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter4CaloSimpleSecondaryVertexHighPurBJetTags = akFilter4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter4CaloCombinedSecondaryVertexBJetTags = akFilter4CalobTagger.CombinedSecondaryVertexBJetTags
akFilter4CaloCombinedSecondaryVertexV2BJetTags = akFilter4CalobTagger.CombinedSecondaryVertexV2BJetTags

akFilter4CaloSecondaryVertexNegativeTagInfos = akFilter4CalobTagger.SecondaryVertexNegativeTagInfos
akFilter4CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter4CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter4CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter4CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter4CaloNegativeCombinedSecondaryVertexBJetTags = akFilter4CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter4CaloPositiveCombinedSecondaryVertexBJetTags = akFilter4CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter4CaloNegativeCombinedSecondaryVertexV2BJetTags = akFilter4CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter4CaloPositiveCombinedSecondaryVertexV2BJetTags = akFilter4CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter4CaloSoftPFMuonsTagInfos = akFilter4CalobTagger.SoftPFMuonsTagInfos
akFilter4CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter4CaloSoftPFMuonBJetTags = akFilter4CalobTagger.SoftPFMuonBJetTags
akFilter4CaloSoftPFMuonByIP3dBJetTags = akFilter4CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter4CaloSoftPFMuonByPtBJetTags = akFilter4CalobTagger.SoftPFMuonByPtBJetTags
akFilter4CaloNegativeSoftPFMuonByPtBJetTags = akFilter4CalobTagger.NegativeSoftPFMuonByPtBJetTags
akFilter4CaloPositiveSoftPFMuonByPtBJetTags = akFilter4CalobTagger.PositiveSoftPFMuonByPtBJetTags
akFilter4CaloPatJetFlavourIdLegacy = cms.Sequence(akFilter4CaloPatJetPartonAssociationLegacy*akFilter4CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter4CaloPatJetFlavourAssociation = akFilter4CalobTagger.PatJetFlavourAssociation
#akFilter4CaloPatJetFlavourId = cms.Sequence(akFilter4CaloPatJetPartons*akFilter4CaloPatJetFlavourAssociation)

akFilter4CaloJetBtaggingIP       = cms.Sequence(akFilter4CaloImpactParameterTagInfos *
            (akFilter4CaloTrackCountingHighEffBJetTags +
             akFilter4CaloTrackCountingHighPurBJetTags +
             akFilter4CaloJetProbabilityBJetTags +
             akFilter4CaloJetBProbabilityBJetTags 
            )
            )

akFilter4CaloJetBtaggingSV = cms.Sequence(akFilter4CaloImpactParameterTagInfos
            *
            akFilter4CaloSecondaryVertexTagInfos
            * (akFilter4CaloSimpleSecondaryVertexHighEffBJetTags+
                akFilter4CaloSimpleSecondaryVertexHighPurBJetTags+
                akFilter4CaloCombinedSecondaryVertexBJetTags+
                akFilter4CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter4CaloJetBtaggingNegSV = cms.Sequence(akFilter4CaloImpactParameterTagInfos
            *
            akFilter4CaloSecondaryVertexNegativeTagInfos
            * (akFilter4CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter4CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter4CaloNegativeCombinedSecondaryVertexBJetTags+
                akFilter4CaloPositiveCombinedSecondaryVertexBJetTags+
                akFilter4CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter4CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter4CaloJetBtaggingMu = cms.Sequence(akFilter4CaloSoftPFMuonsTagInfos * (akFilter4CaloSoftPFMuonBJetTags
                +
                akFilter4CaloSoftPFMuonByIP3dBJetTags
                +
                akFilter4CaloSoftPFMuonByPtBJetTags
                +
                akFilter4CaloNegativeSoftPFMuonByPtBJetTags
                +
                akFilter4CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter4CaloJetBtagging = cms.Sequence(akFilter4CaloJetBtaggingIP
            *akFilter4CaloJetBtaggingSV
            *akFilter4CaloJetBtaggingNegSV
#            *akFilter4CaloJetBtaggingMu
            )

akFilter4CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter4CaloJets"),
        genJetMatch          = cms.InputTag("akFilter4Calomatch"),
        genPartonMatch       = cms.InputTag("akFilter4Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter4Calocorr")),
        JetPartonMapSource   = cms.InputTag("akFilter4CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter4CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter4CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter4CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter4CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter4CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter4CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter4CaloJetBProbabilityBJetTags"),
            cms.InputTag("akFilter4CaloJetProbabilityBJetTags"),
            #cms.InputTag("akFilter4CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter4CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter4CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter4CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter4CaloJetID"),
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

akFilter4CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter4CaloJets"),
           	    R0  = cms.double( 0.4)
)
akFilter4CalopatJetsWithBtagging.userData.userFloats.src += ['akFilter4CaloNjettiness:tau1','akFilter4CaloNjettiness:tau2','akFilter4CaloNjettiness:tau3']

akFilter4CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter4CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akFilter4Calo"),
                                                             jetName = cms.untracked.string("akFilter4Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter4GenJets"),
                                                             doGenTaus = True
                                                             )

akFilter4CaloJetSequence_mc = cms.Sequence(
                                                  #akFilter4Caloclean
                                                  #*
                                                  akFilter4Calomatch
                                                  #*
                                                  #akFilter4CalomatchGroomed
                                                  *
                                                  akFilter4Caloparton
                                                  *
                                                  akFilter4Calocorr
                                                  *
                                                  #akFilter4CaloJetID
                                                  #*
                                                  akFilter4CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter4CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter4CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter4CaloJetBtagging
                                                  *
                                                  akFilter4CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter4CalopatJetsWithBtagging
                                                  *
                                                  akFilter4CaloJetAnalyzer
                                                  )

akFilter4CaloJetSequence_data = cms.Sequence(akFilter4Calocorr
                                                    *
                                                    #akFilter4CaloJetID
                                                    #*
                                                    akFilter4CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter4CaloJetBtagging
                                                    *
                                                    akFilter4CaloNjettiness 
                                                    *
                                                    akFilter4CalopatJetsWithBtagging
                                                    *
                                                    akFilter4CaloJetAnalyzer
                                                    )

akFilter4CaloJetSequence_jec = cms.Sequence(akFilter4CaloJetSequence_mc)
akFilter4CaloJetSequence_mb = cms.Sequence(akFilter4CaloJetSequence_mc)

akFilter4CaloJetSequence = cms.Sequence(akFilter4CaloJetSequence_mb)
