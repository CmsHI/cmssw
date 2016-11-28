

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akVsSoftDrop4Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVsSoftDrop4CaloJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.4
    )

akVsSoftDrop4CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akSoftDrop4GenJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = 0.4
    )

akVsSoftDrop4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop4CaloJets")
                                                        )

akVsSoftDrop4Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVsSoftDrop4CaloJets"),
    payload = "AK4Calo_offline"
    )

akVsSoftDrop4CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akVsSoftDrop4CaloJets'))

#akVsSoftDrop4Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4GenJets'))

akVsSoftDrop4CalobTagger = bTaggers("akVsSoftDrop4Calo",0.4)

#create objects locally since they dont load properly otherwise
#akVsSoftDrop4Calomatch = akVsSoftDrop4CalobTagger.match
akVsSoftDrop4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVsSoftDrop4CaloJets"), matched = cms.InputTag("genParticles"))
akVsSoftDrop4CaloPatJetFlavourAssociationLegacy = akVsSoftDrop4CalobTagger.PatJetFlavourAssociationLegacy
akVsSoftDrop4CaloPatJetPartons = akVsSoftDrop4CalobTagger.PatJetPartons
akVsSoftDrop4CaloJetTracksAssociatorAtVertex = akVsSoftDrop4CalobTagger.JetTracksAssociatorAtVertex
akVsSoftDrop4CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akVsSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop4CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop4CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop4CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop4CalobTagger.CombinedSecondaryVertexV2BJetTags
akVsSoftDrop4CaloJetBProbabilityBJetTags = akVsSoftDrop4CalobTagger.JetBProbabilityBJetTags
akVsSoftDrop4CaloSoftPFMuonByPtBJetTags = akVsSoftDrop4CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop4CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop4CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop4CaloTrackCountingHighEffBJetTags = akVsSoftDrop4CalobTagger.TrackCountingHighEffBJetTags
akVsSoftDrop4CaloTrackCountingHighPurBJetTags = akVsSoftDrop4CalobTagger.TrackCountingHighPurBJetTags
akVsSoftDrop4CaloPatJetPartonAssociationLegacy = akVsSoftDrop4CalobTagger.PatJetPartonAssociationLegacy

akVsSoftDrop4CaloImpactParameterTagInfos = akVsSoftDrop4CalobTagger.ImpactParameterTagInfos
akVsSoftDrop4CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop4CaloJetProbabilityBJetTags = akVsSoftDrop4CalobTagger.JetProbabilityBJetTags

akVsSoftDrop4CaloSecondaryVertexTagInfos = akVsSoftDrop4CalobTagger.SecondaryVertexTagInfos
akVsSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop4CaloCombinedSecondaryVertexBJetTags = akVsSoftDrop4CalobTagger.CombinedSecondaryVertexBJetTags
akVsSoftDrop4CaloCombinedSecondaryVertexV2BJetTags = akVsSoftDrop4CalobTagger.CombinedSecondaryVertexV2BJetTags

akVsSoftDrop4CaloSecondaryVertexNegativeTagInfos = akVsSoftDrop4CalobTagger.SecondaryVertexNegativeTagInfos
akVsSoftDrop4CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akVsSoftDrop4CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akVsSoftDrop4CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akVsSoftDrop4CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akVsSoftDrop4CaloNegativeCombinedSecondaryVertexBJetTags = akVsSoftDrop4CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akVsSoftDrop4CaloPositiveCombinedSecondaryVertexBJetTags = akVsSoftDrop4CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akVsSoftDrop4CaloNegativeCombinedSecondaryVertexV2BJetTags = akVsSoftDrop4CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akVsSoftDrop4CaloPositiveCombinedSecondaryVertexV2BJetTags = akVsSoftDrop4CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akVsSoftDrop4CaloSoftPFMuonsTagInfos = akVsSoftDrop4CalobTagger.SoftPFMuonsTagInfos
akVsSoftDrop4CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akVsSoftDrop4CaloSoftPFMuonBJetTags = akVsSoftDrop4CalobTagger.SoftPFMuonBJetTags
akVsSoftDrop4CaloSoftPFMuonByIP3dBJetTags = akVsSoftDrop4CalobTagger.SoftPFMuonByIP3dBJetTags
akVsSoftDrop4CaloSoftPFMuonByPtBJetTags = akVsSoftDrop4CalobTagger.SoftPFMuonByPtBJetTags
akVsSoftDrop4CaloNegativeSoftPFMuonByPtBJetTags = akVsSoftDrop4CalobTagger.NegativeSoftPFMuonByPtBJetTags
akVsSoftDrop4CaloPositiveSoftPFMuonByPtBJetTags = akVsSoftDrop4CalobTagger.PositiveSoftPFMuonByPtBJetTags
akVsSoftDrop4CaloPatJetFlavourIdLegacy = cms.Sequence(akVsSoftDrop4CaloPatJetPartonAssociationLegacy*akVsSoftDrop4CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akVsSoftDrop4CaloPatJetFlavourAssociation = akVsSoftDrop4CalobTagger.PatJetFlavourAssociation
#akVsSoftDrop4CaloPatJetFlavourId = cms.Sequence(akVsSoftDrop4CaloPatJetPartons*akVsSoftDrop4CaloPatJetFlavourAssociation)

akVsSoftDrop4CaloJetBtaggingIP       = cms.Sequence(akVsSoftDrop4CaloImpactParameterTagInfos *
            (akVsSoftDrop4CaloTrackCountingHighEffBJetTags +
             akVsSoftDrop4CaloTrackCountingHighPurBJetTags +
             akVsSoftDrop4CaloJetProbabilityBJetTags +
             akVsSoftDrop4CaloJetBProbabilityBJetTags 
            )
            )

akVsSoftDrop4CaloJetBtaggingSV = cms.Sequence(akVsSoftDrop4CaloImpactParameterTagInfos
            *
            akVsSoftDrop4CaloSecondaryVertexTagInfos
            * (akVsSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop4CaloCombinedSecondaryVertexBJetTags+
                akVsSoftDrop4CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop4CaloJetBtaggingNegSV = cms.Sequence(akVsSoftDrop4CaloImpactParameterTagInfos
            *
            akVsSoftDrop4CaloSecondaryVertexNegativeTagInfos
            * (akVsSoftDrop4CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akVsSoftDrop4CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akVsSoftDrop4CaloNegativeCombinedSecondaryVertexBJetTags+
                akVsSoftDrop4CaloPositiveCombinedSecondaryVertexBJetTags+
                akVsSoftDrop4CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akVsSoftDrop4CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akVsSoftDrop4CaloJetBtaggingMu = cms.Sequence(akVsSoftDrop4CaloSoftPFMuonsTagInfos * (akVsSoftDrop4CaloSoftPFMuonBJetTags
                +
                akVsSoftDrop4CaloSoftPFMuonByIP3dBJetTags
                +
                akVsSoftDrop4CaloSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop4CaloNegativeSoftPFMuonByPtBJetTags
                +
                akVsSoftDrop4CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akVsSoftDrop4CaloJetBtagging = cms.Sequence(akVsSoftDrop4CaloJetBtaggingIP
            *akVsSoftDrop4CaloJetBtaggingSV
            *akVsSoftDrop4CaloJetBtaggingNegSV
#            *akVsSoftDrop4CaloJetBtaggingMu
            )

akVsSoftDrop4CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akVsSoftDrop4CaloJets"),
        genJetMatch          = cms.InputTag("akVsSoftDrop4Calomatch"),
        genPartonMatch       = cms.InputTag("akVsSoftDrop4Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVsSoftDrop4Calocorr")),
        JetPartonMapSource   = cms.InputTag("akVsSoftDrop4CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akVsSoftDrop4CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akVsSoftDrop4CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akVsSoftDrop4CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop4CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akVsSoftDrop4CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akVsSoftDrop4CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akVsSoftDrop4CaloJetBProbabilityBJetTags"),
            cms.InputTag("akVsSoftDrop4CaloJetProbabilityBJetTags"),
            #cms.InputTag("akVsSoftDrop4CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akVsSoftDrop4CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akVsSoftDrop4CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akVsSoftDrop4CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akVsSoftDrop4CaloJetID"),
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

akVsSoftDrop4CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akVsSoftDrop4CaloJets"),
           	    R0  = cms.double( 0.4)
)
akVsSoftDrop4CalopatJetsWithBtagging.userData.userFloats.src += ['akVsSoftDrop4CaloNjettiness:tau1','akVsSoftDrop4CaloNjettiness:tau2','akVsSoftDrop4CaloNjettiness:tau3']

akVsSoftDrop4CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVsSoftDrop4CalopatJetsWithBtagging"),
                                                             genjetTag = 'ak4GenJets',
                                                             rParam = 0.4,
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
                                                             bTagJetName = cms.untracked.string("akVsSoftDrop4Calo"),
                                                             jetName = cms.untracked.string("akVsSoftDrop4Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akSoftDrop4GenJets"),
                                                             doGenTaus = True
                                                             )

akVsSoftDrop4CaloJetSequence_mc = cms.Sequence(
                                                  #akVsSoftDrop4Caloclean
                                                  #*
                                                  akVsSoftDrop4Calomatch
                                                  #*
                                                  #akVsSoftDrop4CalomatchGroomed
                                                  *
                                                  akVsSoftDrop4Caloparton
                                                  *
                                                  akVsSoftDrop4Calocorr
                                                  *
                                                  #akVsSoftDrop4CaloJetID
                                                  #*
                                                  akVsSoftDrop4CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akVsSoftDrop4CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akVsSoftDrop4CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akVsSoftDrop4CaloJetBtagging
                                                  *
                                                  akVsSoftDrop4CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akVsSoftDrop4CalopatJetsWithBtagging
                                                  *
                                                  akVsSoftDrop4CaloJetAnalyzer
                                                  )

akVsSoftDrop4CaloJetSequence_data = cms.Sequence(akVsSoftDrop4Calocorr
                                                    *
                                                    #akVsSoftDrop4CaloJetID
                                                    #*
                                                    akVsSoftDrop4CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akVsSoftDrop4CaloJetBtagging
                                                    *
                                                    akVsSoftDrop4CaloNjettiness 
                                                    *
                                                    akVsSoftDrop4CalopatJetsWithBtagging
                                                    *
                                                    akVsSoftDrop4CaloJetAnalyzer
                                                    )

akVsSoftDrop4CaloJetSequence_jec = cms.Sequence(akVsSoftDrop4CaloJetSequence_mc)
akVsSoftDrop4CaloJetSequence_mb = cms.Sequence(akVsSoftDrop4CaloJetSequence_mc)

akVsSoftDrop4CaloJetSequence = cms.Sequence(akVsSoftDrop4CaloJetSequence_jec)
akVsSoftDrop4CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akVsSoftDrop4CaloJetAnalyzer.jetPtMin = cms.double(1)
