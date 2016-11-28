

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akFilter6Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter6CaloJets"),
    matched = cms.InputTag("ak6HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akFilter6CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter6HiGenJets"),
    matched = cms.InputTag("ak6HiSignalGenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.6
    )

akFilter6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter6CaloJets")
                                                        )

akFilter6Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akFilter6CaloJets"),
    payload = "AK6Calo_offline"
    )

akFilter6CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akFilter6CaloJets'))

#akFilter6Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak6HiSignalGenJets'))

akFilter6CalobTagger = bTaggers("akFilter6Calo",0.6)

#create objects locally since they dont load properly otherwise
#akFilter6Calomatch = akFilter6CalobTagger.match
akFilter6Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akFilter6CaloJets"), matched = cms.InputTag("hiSignalGenParticles"))
akFilter6CaloPatJetFlavourAssociationLegacy = akFilter6CalobTagger.PatJetFlavourAssociationLegacy
akFilter6CaloPatJetPartons = akFilter6CalobTagger.PatJetPartons
akFilter6CaloJetTracksAssociatorAtVertex = akFilter6CalobTagger.JetTracksAssociatorAtVertex
akFilter6CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akFilter6CaloSimpleSecondaryVertexHighEffBJetTags = akFilter6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter6CaloSimpleSecondaryVertexHighPurBJetTags = akFilter6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter6CaloCombinedSecondaryVertexBJetTags = akFilter6CalobTagger.CombinedSecondaryVertexBJetTags
akFilter6CaloCombinedSecondaryVertexV2BJetTags = akFilter6CalobTagger.CombinedSecondaryVertexV2BJetTags
akFilter6CaloJetBProbabilityBJetTags = akFilter6CalobTagger.JetBProbabilityBJetTags
akFilter6CaloSoftPFMuonByPtBJetTags = akFilter6CalobTagger.SoftPFMuonByPtBJetTags
akFilter6CaloSoftPFMuonByIP3dBJetTags = akFilter6CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter6CaloTrackCountingHighEffBJetTags = akFilter6CalobTagger.TrackCountingHighEffBJetTags
akFilter6CaloTrackCountingHighPurBJetTags = akFilter6CalobTagger.TrackCountingHighPurBJetTags
akFilter6CaloPatJetPartonAssociationLegacy = akFilter6CalobTagger.PatJetPartonAssociationLegacy

akFilter6CaloImpactParameterTagInfos = akFilter6CalobTagger.ImpactParameterTagInfos
akFilter6CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter6CaloJetProbabilityBJetTags = akFilter6CalobTagger.JetProbabilityBJetTags

akFilter6CaloSecondaryVertexTagInfos = akFilter6CalobTagger.SecondaryVertexTagInfos
akFilter6CaloSimpleSecondaryVertexHighEffBJetTags = akFilter6CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akFilter6CaloSimpleSecondaryVertexHighPurBJetTags = akFilter6CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akFilter6CaloCombinedSecondaryVertexBJetTags = akFilter6CalobTagger.CombinedSecondaryVertexBJetTags
akFilter6CaloCombinedSecondaryVertexV2BJetTags = akFilter6CalobTagger.CombinedSecondaryVertexV2BJetTags

akFilter6CaloSecondaryVertexNegativeTagInfos = akFilter6CalobTagger.SecondaryVertexNegativeTagInfos
akFilter6CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akFilter6CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akFilter6CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akFilter6CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akFilter6CaloNegativeCombinedSecondaryVertexBJetTags = akFilter6CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akFilter6CaloPositiveCombinedSecondaryVertexBJetTags = akFilter6CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akFilter6CaloNegativeCombinedSecondaryVertexV2BJetTags = akFilter6CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akFilter6CaloPositiveCombinedSecondaryVertexV2BJetTags = akFilter6CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akFilter6CaloSoftPFMuonsTagInfos = akFilter6CalobTagger.SoftPFMuonsTagInfos
akFilter6CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akFilter6CaloSoftPFMuonBJetTags = akFilter6CalobTagger.SoftPFMuonBJetTags
akFilter6CaloSoftPFMuonByIP3dBJetTags = akFilter6CalobTagger.SoftPFMuonByIP3dBJetTags
akFilter6CaloSoftPFMuonByPtBJetTags = akFilter6CalobTagger.SoftPFMuonByPtBJetTags
akFilter6CaloNegativeSoftPFMuonByPtBJetTags = akFilter6CalobTagger.NegativeSoftPFMuonByPtBJetTags
akFilter6CaloPositiveSoftPFMuonByPtBJetTags = akFilter6CalobTagger.PositiveSoftPFMuonByPtBJetTags
akFilter6CaloPatJetFlavourIdLegacy = cms.Sequence(akFilter6CaloPatJetPartonAssociationLegacy*akFilter6CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akFilter6CaloPatJetFlavourAssociation = akFilter6CalobTagger.PatJetFlavourAssociation
#akFilter6CaloPatJetFlavourId = cms.Sequence(akFilter6CaloPatJetPartons*akFilter6CaloPatJetFlavourAssociation)

akFilter6CaloJetBtaggingIP       = cms.Sequence(akFilter6CaloImpactParameterTagInfos *
            (akFilter6CaloTrackCountingHighEffBJetTags +
             akFilter6CaloTrackCountingHighPurBJetTags +
             akFilter6CaloJetProbabilityBJetTags +
             akFilter6CaloJetBProbabilityBJetTags 
            )
            )

akFilter6CaloJetBtaggingSV = cms.Sequence(akFilter6CaloImpactParameterTagInfos
            *
            akFilter6CaloSecondaryVertexTagInfos
            * (akFilter6CaloSimpleSecondaryVertexHighEffBJetTags+
                akFilter6CaloSimpleSecondaryVertexHighPurBJetTags+
                akFilter6CaloCombinedSecondaryVertexBJetTags+
                akFilter6CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter6CaloJetBtaggingNegSV = cms.Sequence(akFilter6CaloImpactParameterTagInfos
            *
            akFilter6CaloSecondaryVertexNegativeTagInfos
            * (akFilter6CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akFilter6CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akFilter6CaloNegativeCombinedSecondaryVertexBJetTags+
                akFilter6CaloPositiveCombinedSecondaryVertexBJetTags+
                akFilter6CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akFilter6CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akFilter6CaloJetBtaggingMu = cms.Sequence(akFilter6CaloSoftPFMuonsTagInfos * (akFilter6CaloSoftPFMuonBJetTags
                +
                akFilter6CaloSoftPFMuonByIP3dBJetTags
                +
                akFilter6CaloSoftPFMuonByPtBJetTags
                +
                akFilter6CaloNegativeSoftPFMuonByPtBJetTags
                +
                akFilter6CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akFilter6CaloJetBtagging = cms.Sequence(akFilter6CaloJetBtaggingIP
            *akFilter6CaloJetBtaggingSV
            *akFilter6CaloJetBtaggingNegSV
#            *akFilter6CaloJetBtaggingMu
            )

akFilter6CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akFilter6CaloJets"),
        genJetMatch          = cms.InputTag("akFilter6Calomatch"),
        genPartonMatch       = cms.InputTag("akFilter6Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akFilter6Calocorr")),
        JetPartonMapSource   = cms.InputTag("akFilter6CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akFilter6CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akFilter6CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akFilter6CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akFilter6CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akFilter6CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akFilter6CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akFilter6CaloJetBProbabilityBJetTags"),
            cms.InputTag("akFilter6CaloJetProbabilityBJetTags"),
            #cms.InputTag("akFilter6CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akFilter6CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akFilter6CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akFilter6CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akFilter6CaloJetID"),
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

akFilter6CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akFilter6CaloJets"),
           	    R0  = cms.double( 0.6)
)
akFilter6CalopatJetsWithBtagging.userData.userFloats.src += ['akFilter6CaloNjettiness:tau1','akFilter6CaloNjettiness:tau2','akFilter6CaloNjettiness:tau3']

akFilter6CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akFilter6CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akFilter6Calo"),
                                                             jetName = cms.untracked.string("akFilter6Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(True),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter6GenJets"),
                                                             doGenTaus = True
                                                             )

akFilter6CaloJetSequence_mc = cms.Sequence(
                                                  #akFilter6Caloclean
                                                  #*
                                                  akFilter6Calomatch
                                                  #*
                                                  #akFilter6CalomatchGroomed
                                                  *
                                                  akFilter6Caloparton
                                                  *
                                                  akFilter6Calocorr
                                                  *
                                                  #akFilter6CaloJetID
                                                  #*
                                                  akFilter6CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akFilter6CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akFilter6CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akFilter6CaloJetBtagging
                                                  *
                                                  akFilter6CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akFilter6CalopatJetsWithBtagging
                                                  *
                                                  akFilter6CaloJetAnalyzer
                                                  )

akFilter6CaloJetSequence_data = cms.Sequence(akFilter6Calocorr
                                                    *
                                                    #akFilter6CaloJetID
                                                    #*
                                                    akFilter6CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akFilter6CaloJetBtagging
                                                    *
                                                    akFilter6CaloNjettiness 
                                                    *
                                                    akFilter6CalopatJetsWithBtagging
                                                    *
                                                    akFilter6CaloJetAnalyzer
                                                    )

akFilter6CaloJetSequence_jec = cms.Sequence(akFilter6CaloJetSequence_mc)
akFilter6CaloJetSequence_mb = cms.Sequence(akFilter6CaloJetSequence_mc)

akFilter6CaloJetSequence = cms.Sequence(akFilter6CaloJetSequence_mc)
