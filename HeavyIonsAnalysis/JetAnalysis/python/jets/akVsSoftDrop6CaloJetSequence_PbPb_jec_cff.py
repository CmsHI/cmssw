

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop6Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop6CaloJets"),
    matched = cms.InputTag("ak6HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.6
    )

akVsSoftDrop6CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop6HiGenJets"),
    matched = cms.InputTag("ak6HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.6
    )

akVsSoftDrop6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop6CaloJets")
                                                        )

akVsSoftDrop6Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop6CaloJets"),
    payload = "AK6Calo_offline"
    )

akVsSoftDrop6CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop6CaloJets'))

#akVsSoftDrop6Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6HiSignalGenJets'))

akVsSoftDrop6CalobTagger = bTaggers("akVsSoftDrop6Calo",0.6)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop6Calomatch = akVsSoftDrop6CalobTagger.match
akVsSoftDrop6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop6CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akVsSoftDrop6CaloPatJetFlavourAssociationLegacy = akVsSoftDrop6CalobTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop6CaloPatJetPartons = akVsSoftDrop6CalobTagger.PatJetPartons
akVsSoftDrop6CaloJetTracksAssociatorAtVertex = akVsSoftDrop6CalobTagger.JetTracksAssociatorAtVertex
akVsSoftDrop6CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop6CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop6CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop6CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop6CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop6CaloJetBProbabilityBJetTags = akVsSoftDrop6CalobTagger.JetBProbabilityBJetTags
akVsSoftDrop6CaloSoftPFMuonByPtBJetTags = akVsSoftDrop6CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop6CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop6CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop6CaloTrackCountingHighEffBJetTags = akVsSoftDrop6CalobTagger.TrackCountingHighEffBJetTags
akVsSoftDrop6CaloTrackCountingHighPurBJetTags = akVsSoftDrop6CalobTagger.TrackCountingHighPurBJetTags
akVsSoftDrop6CaloPatJetPartonAssociationLegacy = akVsSoftDrop6CalobTagger.PatJetPartonAssociationLegacy

akVsSoftDrop6CaloImpactParameterTagInfos = akVsSoftDrop6CalobTagger.ImpactParameterTagInfos
akVsSoftDrop6CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop6CaloJetProbabilityBJetTags = akVsSoftDrop6CalobTagger.JetProbabilityBJetTags

akVsSoftDrop6CaloSecondaryVertexTagInfos = akVsSoftDrop6CalobTagger.SecondaryVertexTagInfos
akVsSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop6CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop6CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop6CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop6CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop6CaloSecondaryVertexNegativeTagInfos = akVsSoftDrop6CalobTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop6CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop6CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop6CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop6CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop6CaloNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop6CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop6CaloPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop6CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop6CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop6CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop6CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop6CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop6CaloSoftPFMuonsTagInfos = akVsSoftDrop6CalobTagger.SoftPFMuonsTagInfos
akVsSoftDrop6CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop6CaloSoftPFMuonBJetTags = akVsSoftDrop6CalobTagger.SoftPFMuonBJetTags
akVsSoftDrop6CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop6CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop6CaloSoftPFMuonByPtBJetTags = akVsSoftDrop6CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop6CaloNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop6CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop6CaloPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop6CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop6CaloPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop6CaloPatJetPartonAssociationLegacy*akVsSoftDrop6CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop6CaloPatJetFlavourAssociation = akVsSoftDrop6CalobTagger.PatJetFlavourAssociation
#akVsSoftDrop6CaloPatJetFlavourId = cms.Sequence(akVsSoftDrop6CaloPatJetPartons*akVsSoftDrop6CaloPatJetFlavourAssociation)

akVsSoftDrop6CaloJetBtaggingIP       = cms.Sequence(akVsSoftDrop6CaloImpactParameterTagInfos *
            (akVsSoftDrop6CaloTrackCountingHighEffBJetTags +
             akVsSoftDrop6CaloTrackCountingHighPurBJetTags +
             akVsSoftDrop6CaloJetProbabilityBJetTags +
             akVsSoftDrop6CaloJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop6CaloJetBtaggingSV = cms.Sequence(akVsSoftDrop6CaloImpactParameterTagInfos
            *
            akVsSoftDrop6CaloSecondaryVertexTagInfos
            * (akVsSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop6CaloCombinedSecondaryVertexBJetTags+
                akVsSoftDrop6CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop6CaloJetBtaggingNegSV = cms.Sequence(akVsSoftDrop6CaloImpactParameterTagInfos
            *
            akVsSoftDrop6CaloSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop6CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop6CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop6CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop6CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop6CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop6CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop6CaloJetBtaggingMu = cms.Sequence(akVsSoftDrop6CaloSoftPFMuonsTagInfos * (akVsSoftDrop6CaloSoftPFMuonBJetTags
                +
                akVsSoftDrop6CaloSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop6CaloSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop6CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop6CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop6CaloJetBtagging = cms.Sequence(akVsSoftDrop6CaloJetBtaggingIP
            *akVsSoftDrop6CaloJetBtaggingSV
            *akVsSoftDrop6CaloJetBtaggingNegSV
#            *akVsSoftDrop6CaloJetBtaggingMu
            )

akVsSoftDrop6CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop6CaloJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop6Calomatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop6Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop6Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop6CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop6CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop6CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop6CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop6CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop6CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop6CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop6CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop6CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop6CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop6CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop6CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop6CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop6CaloJetID"),
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

akVsSoftDrop6CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop6CaloJets"),
           	    R0  = cms.double( 0.6)
)
akVsSoftDrop6CalopatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop6CaloNjettiness:tau1','akVsSoftDrop6CaloNjettiness:tau2','akVsSoftDrop6CaloNjettiness:tau3']

akVsSoftDrop6CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop6CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak6HiGenJets',
                                                             rParam = 0.6,
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop6Calo"),
                                                             jetName = cms.untracked.string("akVsSoftDrop6Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop6GenJets"),
                                                             doGenTaus = True
                                                             )

akVsSoftDrop6CaloJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop6Caloclean
                                                  #*
                                                  akVsSoftDrop6Calomatch
                                                  #*
                                                  #akVsSoftDrop6CalomatchGroomed
                                                  *
                                                  akVsSoftDrop6Caloparton
                                                  *
                                                  akVsSoftDrop6Calocorr
                                                  *
                                                  #akVsSoftDrop6CaloJetID
                                                  #*
                                                  akVsSoftDrop6CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop6CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop6CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop6CaloJetBtagging
                                                  *
                                                  akVsSoftDrop6CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop6CalopatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop6CaloJetAnalyzer
                                                  )

akVsSoftDrop6CaloJetSequence_data = cms.Sequence(akVsSoftDrop6Calocorr
                                                    *
                                                    #akVsSoftDrop6CaloJetID
                                                    #*
                                                    akVsSoftDrop6CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop6CaloJetBtagging
                                                    *
                                                    akVsSoftDrop6CaloNjettiness 
                                                    *
                                                    akVsSoftDrop6CalopatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop6CaloJetAnalyzer
                                                    )

akVsSoftDrop6CaloJetSequence_jec = cms.Sequence(akVsSoftDrop6CaloJetSequence_mc)
akVsSoftDrop6CaloJetSequence_mb = cms.Sequence(akVsSoftDrop6CaloJetSequence_mc)

akVsSoftDrop6CaloJetSequence = cms.Sequence(akVsSoftDrop6CaloJetSequence_jec)
akVsSoftDrop6CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akVsSoftDrop6CaloJetAnalyzer.jetPtMin = cms.double(1)
