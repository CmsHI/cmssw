

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuSoftDrop4Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuSoftDrop4CaloJets"),
    matched = cms.InputTag("ak4HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akPuSoftDrop4CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop4HiGenJets"),
    matched = cms.InputTag("ak4HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akPuSoftDrop4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop4CaloJets")
                                                        )

akPuSoftDrop4Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuSoftDrop4CaloJets"),
    payload = "AKPu4Calo_offline"
    )

akPuSoftDrop4CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuSoftDrop4CaloJets'))

#akPuSoftDrop4Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4HiSignalGenJets'))

akPuSoftDrop4CalobTagger = bTaggers("akPuSoftDrop4Calo",0.4)

#create objects locally since they dont load properly otherwise
#akPuSoftDrop4Calomatch = akPuSoftDrop4CalobTagger.match
akPuSoftDrop4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuSoftDrop4CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akPuSoftDrop4CaloPatJetFlavourAssociationLegacy = akPuSoftDrop4CalobTagger.PatJetFlavourAssociationLegacy
akPuSoftDrop4CaloPatJetPartons = akPuSoftDrop4CalobTagger.PatJetPartons
akPuSoftDrop4CaloJetTracksAssociatorAtVertex = akPuSoftDrop4CalobTagger.JetTracksAssociatorAtVertex
akPuSoftDrop4CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop4CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop4CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop4CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop4CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuSoftDrop4CaloJetBProbabilityBJetTags = akPuSoftDrop4CalobTagger.JetBProbabilityBJetTags
akPuSoftDrop4CaloSoftPFMuonByPtBJetTags = akPuSoftDrop4CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop4CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop4CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop4CaloTrackCountingHighEffBJetTags = akPuSoftDrop4CalobTagger.TrackCountingHighEffBJetTags
akPuSoftDrop4CaloTrackCountingHighPurBJetTags = akPuSoftDrop4CalobTagger.TrackCountingHighPurBJetTags
akPuSoftDrop4CaloPatJetPartonAssociationLegacy = akPuSoftDrop4CalobTagger.PatJetPartonAssociationLegacy

akPuSoftDrop4CaloImpactParameterTagInfos = akPuSoftDrop4CalobTagger.ImpactParameterTagInfos
akPuSoftDrop4CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop4CaloJetProbabilityBJetTags = akPuSoftDrop4CalobTagger.JetProbabilityBJetTags

akPuSoftDrop4CaloSecondaryVertexTagInfos = akPuSoftDrop4CalobTagger.SecondaryVertexTagInfos
akPuSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop4CaloCombinedSecondaryVertexBJetTags = akPuSoftDrop4CalobTagger.CombinedSecondaryVertexBJetTags
akPuSoftDrop4CaloCombinedSecondaryVertexV2BJetTags = akPuSoftDrop4CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuSoftDrop4CaloSecondaryVertexNegativeTagInfos = akPuSoftDrop4CalobTagger.SecondaryVertexNegativeTagInfos
akPuSoftDrop4CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuSoftDrop4CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuSoftDrop4CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuSoftDrop4CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuSoftDrop4CaloNegativeCombinedSecondaryVertexBJetTags = akPuSoftDrop4CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuSoftDrop4CaloPositiveCombinedSecondaryVertexBJetTags = akPuSoftDrop4CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuSoftDrop4CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuSoftDrop4CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuSoftDrop4CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuSoftDrop4CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuSoftDrop4CaloSoftPFMuonsTagInfos = akPuSoftDrop4CalobTagger.SoftPFMuonsTagInfos
akPuSoftDrop4CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuSoftDrop4CaloSoftPFMuonBJetTags = akPuSoftDrop4CalobTagger.SoftPFMuonBJetTags
akPuSoftDrop4CaloSoftPFMuonByIP3dBJetTags = akPuSoftDrop4CalobTagger.SoftPFMuonByIP3dBJetTags
akPuSoftDrop4CaloSoftPFMuonByPtBJetTags = akPuSoftDrop4CalobTagger.SoftPFMuonByPtBJetTags
akPuSoftDrop4CaloNegativeSoftPFMuonByPtBJetTags = akPuSoftDrop4CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuSoftDrop4CaloPositiveSoftPFMuonByPtBJetTags = akPuSoftDrop4CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuSoftDrop4CaloPatJetFlavourIdLegacy = cms.Sequence(akPuSoftDrop4CaloPatJetPartonAssociationLegacy*akPuSoftDrop4CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuSoftDrop4CaloPatJetFlavourAssociation = akPuSoftDrop4CalobTagger.PatJetFlavourAssociation
#akPuSoftDrop4CaloPatJetFlavourId = cms.Sequence(akPuSoftDrop4CaloPatJetPartons*akPuSoftDrop4CaloPatJetFlavourAssociation)

akPuSoftDrop4CaloJetBtaggingIP       = cms.Sequence(akPuSoftDrop4CaloImpactParameterTagInfos *
            (akPuSoftDrop4CaloTrackCountingHighEffBJetTags +
             akPuSoftDrop4CaloTrackCountingHighPurBJetTags +
             akPuSoftDrop4CaloJetProbabilityBJetTags +
             akPuSoftDrop4CaloJetBProbabilityBJetTags 
            )
            )

akPuSoftDrop4CaloJetBtaggingSV = cms.Sequence(akPuSoftDrop4CaloImpactParameterTagInfos
            *
            akPuSoftDrop4CaloSecondaryVertexTagInfos
            * (akPuSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop4CaloCombinedSecondaryVertexBJetTags+
                akPuSoftDrop4CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop4CaloJetBtaggingNegSV = cms.Sequence(akPuSoftDrop4CaloImpactParameterTagInfos
            *
            akPuSoftDrop4CaloSecondaryVertexNegativeTagInfos
            * (akPuSoftDrop4CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuSoftDrop4CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuSoftDrop4CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuSoftDrop4CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuSoftDrop4CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuSoftDrop4CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuSoftDrop4CaloJetBtaggingMu = cms.Sequence(akPuSoftDrop4CaloSoftPFMuonsTagInfos * (akPuSoftDrop4CaloSoftPFMuonBJetTags
                +
                akPuSoftDrop4CaloSoftPFMuonByIP3dBJetTags
                +
                akPuSoftDrop4CaloSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop4CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuSoftDrop4CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuSoftDrop4CaloJetBtagging = cms.Sequence(akPuSoftDrop4CaloJetBtaggingIP
            *akPuSoftDrop4CaloJetBtaggingSV
            *akPuSoftDrop4CaloJetBtaggingNegSV
#            *akPuSoftDrop4CaloJetBtaggingMu
            )

akPuSoftDrop4CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuSoftDrop4CaloJets"),
        genJetMatch          = cms.InputTag("akPuSoftDrop4Calomatch"),
        genPartonMatch       = cms.InputTag("akPuSoftDrop4Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuSoftDrop4Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuSoftDrop4CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuSoftDrop4CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuSoftDrop4CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuSoftDrop4CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuSoftDrop4CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuSoftDrop4CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuSoftDrop4CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuSoftDrop4CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuSoftDrop4CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuSoftDrop4CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuSoftDrop4CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuSoftDrop4CaloJetID"),
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

akPuSoftDrop4CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuSoftDrop4CaloJets"),
           	    R0  = cms.double( 0.4)
)
akPuSoftDrop4CalopatJetsWithBtagging.userData.userFloats.src += ['akPuSoftDrop4CaloNjettiness:tau1','akPuSoftDrop4CaloNjettiness:tau2','akPuSoftDrop4CaloNjettiness:tau3']

akPuSoftDrop4CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuSoftDrop4CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuSoftDrop4Calo"),
                                                             jetName = cms.untracked.string("akPuSoftDrop4Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop4GenJets"),
                                                             doGenTaus = True
                                                             )

akPuSoftDrop4CaloJetSequence_mc = cms.Sequence(
                                                  #akPuSoftDrop4Caloclean
                                                  #*
                                                  akPuSoftDrop4Calomatch
                                                  #*
                                                  #akPuSoftDrop4CalomatchGroomed
                                                  *
                                                  akPuSoftDrop4Caloparton
                                                  *
                                                  akPuSoftDrop4Calocorr
                                                  *
                                                  #akPuSoftDrop4CaloJetID
                                                  #*
                                                  akPuSoftDrop4CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuSoftDrop4CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuSoftDrop4CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuSoftDrop4CaloJetBtagging
                                                  *
                                                  akPuSoftDrop4CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuSoftDrop4CalopatJetsWithBtagging
                                                  *
                                                  akPuSoftDrop4CaloJetAnalyzer
                                                  )

akPuSoftDrop4CaloJetSequence_data = cms.Sequence(akPuSoftDrop4Calocorr
                                                    *
                                                    #akPuSoftDrop4CaloJetID
                                                    #*
                                                    akPuSoftDrop4CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuSoftDrop4CaloJetBtagging
                                                    *
                                                    akPuSoftDrop4CaloNjettiness 
                                                    *
                                                    akPuSoftDrop4CalopatJetsWithBtagging
                                                    *
                                                    akPuSoftDrop4CaloJetAnalyzer
                                                    )

akPuSoftDrop4CaloJetSequence_jec = cms.Sequence(akPuSoftDrop4CaloJetSequence_mc)
akPuSoftDrop4CaloJetSequence_mb = cms.Sequence(akPuSoftDrop4CaloJetSequence_mc)

akPuSoftDrop4CaloJetSequence = cms.Sequence(akPuSoftDrop4CaloJetSequence_jec)
akPuSoftDrop4CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akPuSoftDrop4CaloJetAnalyzer.jetPtMin = cms.double(1)
