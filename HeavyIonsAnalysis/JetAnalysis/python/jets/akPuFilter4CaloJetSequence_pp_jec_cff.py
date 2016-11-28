

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *
from HeavyIonsAnalysis.JetAnalysis.bTaggers_cff import *
from RecoJets.JetProducers.JetIDParams_cfi import *
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

akPuFilter4Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akPuFilter4CaloJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akPuFilter4CalomatchGroomed = patJetGenJetMatch.clone(
    src = cms.InputTag("akFilter4GenJets"),
    matched = cms.InputTag("ak4GenJets"),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = 0.4
    )

akPuFilter4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter4CaloJets")
                                                        )

akPuFilter4Calocorr = patJetCorrFactors.clone(
    useNPV = cms.bool(False),
    useRho = cms.bool(False),
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akPuFilter4CaloJets"),
    payload = "AKPu4Calo_offline"
    )

akPuFilter4CaloJetID= cms.EDProducer('JetIDProducer', JetIDParams, src = cms.InputTag('akPuFilter4CaloJets'))

#akPuFilter4Caloclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak4GenJets'))

akPuFilter4CalobTagger = bTaggers("akPuFilter4Calo",0.4)

#create objects locally since they dont load properly otherwise
#akPuFilter4Calomatch = akPuFilter4CalobTagger.match
akPuFilter4Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akPuFilter4CaloJets"), matched = cms.InputTag("genParticles"))
akPuFilter4CaloPatJetFlavourAssociationLegacy = akPuFilter4CalobTagger.PatJetFlavourAssociationLegacy
akPuFilter4CaloPatJetPartons = akPuFilter4CalobTagger.PatJetPartons
akPuFilter4CaloJetTracksAssociatorAtVertex = akPuFilter4CalobTagger.JetTracksAssociatorAtVertex
akPuFilter4CaloJetTracksAssociatorAtVertex.tracks = cms.InputTag("highPurityTracks")
akPuFilter4CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter4CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter4CaloCombinedSecondaryVertexBJetTags = akPuFilter4CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter4CaloCombinedSecondaryVertexV2BJetTags = akPuFilter4CalobTagger.CombinedSecondaryVertexV2BJetTags
akPuFilter4CaloJetBProbabilityBJetTags = akPuFilter4CalobTagger.JetBProbabilityBJetTags
akPuFilter4CaloSoftPFMuonByPtBJetTags = akPuFilter4CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter4CaloSoftPFMuonByIP3dBJetTags = akPuFilter4CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter4CaloTrackCountingHighEffBJetTags = akPuFilter4CalobTagger.TrackCountingHighEffBJetTags
akPuFilter4CaloTrackCountingHighPurBJetTags = akPuFilter4CalobTagger.TrackCountingHighPurBJetTags
akPuFilter4CaloPatJetPartonAssociationLegacy = akPuFilter4CalobTagger.PatJetPartonAssociationLegacy

akPuFilter4CaloImpactParameterTagInfos = akPuFilter4CalobTagger.ImpactParameterTagInfos
akPuFilter4CaloImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter4CaloJetProbabilityBJetTags = akPuFilter4CalobTagger.JetProbabilityBJetTags

akPuFilter4CaloSecondaryVertexTagInfos = akPuFilter4CalobTagger.SecondaryVertexTagInfos
akPuFilter4CaloSimpleSecondaryVertexHighEffBJetTags = akPuFilter4CalobTagger.SimpleSecondaryVertexHighEffBJetTags
akPuFilter4CaloSimpleSecondaryVertexHighPurBJetTags = akPuFilter4CalobTagger.SimpleSecondaryVertexHighPurBJetTags
akPuFilter4CaloCombinedSecondaryVertexBJetTags = akPuFilter4CalobTagger.CombinedSecondaryVertexBJetTags
akPuFilter4CaloCombinedSecondaryVertexV2BJetTags = akPuFilter4CalobTagger.CombinedSecondaryVertexV2BJetTags

akPuFilter4CaloSecondaryVertexNegativeTagInfos = akPuFilter4CalobTagger.SecondaryVertexNegativeTagInfos
akPuFilter4CaloNegativeSimpleSecondaryVertexHighEffBJetTags = akPuFilter4CalobTagger.NegativeSimpleSecondaryVertexHighEffBJetTags
akPuFilter4CaloNegativeSimpleSecondaryVertexHighPurBJetTags = akPuFilter4CalobTagger.NegativeSimpleSecondaryVertexHighPurBJetTags
akPuFilter4CaloNegativeCombinedSecondaryVertexBJetTags = akPuFilter4CalobTagger.NegativeCombinedSecondaryVertexBJetTags
akPuFilter4CaloPositiveCombinedSecondaryVertexBJetTags = akPuFilter4CalobTagger.PositiveCombinedSecondaryVertexBJetTags
akPuFilter4CaloNegativeCombinedSecondaryVertexV2BJetTags = akPuFilter4CalobTagger.NegativeCombinedSecondaryVertexV2BJetTags
akPuFilter4CaloPositiveCombinedSecondaryVertexV2BJetTags = akPuFilter4CalobTagger.PositiveCombinedSecondaryVertexV2BJetTags

akPuFilter4CaloSoftPFMuonsTagInfos = akPuFilter4CalobTagger.SoftPFMuonsTagInfos
akPuFilter4CaloSoftPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPuFilter4CaloSoftPFMuonBJetTags = akPuFilter4CalobTagger.SoftPFMuonBJetTags
akPuFilter4CaloSoftPFMuonByIP3dBJetTags = akPuFilter4CalobTagger.SoftPFMuonByIP3dBJetTags
akPuFilter4CaloSoftPFMuonByPtBJetTags = akPuFilter4CalobTagger.SoftPFMuonByPtBJetTags
akPuFilter4CaloNegativeSoftPFMuonByPtBJetTags = akPuFilter4CalobTagger.NegativeSoftPFMuonByPtBJetTags
akPuFilter4CaloPositiveSoftPFMuonByPtBJetTags = akPuFilter4CalobTagger.PositiveSoftPFMuonByPtBJetTags
akPuFilter4CaloPatJetFlavourIdLegacy = cms.Sequence(akPuFilter4CaloPatJetPartonAssociationLegacy*akPuFilter4CaloPatJetFlavourAssociationLegacy)
#Not working with our PU sub, but keep it here for reference
#akPuFilter4CaloPatJetFlavourAssociation = akPuFilter4CalobTagger.PatJetFlavourAssociation
#akPuFilter4CaloPatJetFlavourId = cms.Sequence(akPuFilter4CaloPatJetPartons*akPuFilter4CaloPatJetFlavourAssociation)

akPuFilter4CaloJetBtaggingIP       = cms.Sequence(akPuFilter4CaloImpactParameterTagInfos *
            (akPuFilter4CaloTrackCountingHighEffBJetTags +
             akPuFilter4CaloTrackCountingHighPurBJetTags +
             akPuFilter4CaloJetProbabilityBJetTags +
             akPuFilter4CaloJetBProbabilityBJetTags 
            )
            )

akPuFilter4CaloJetBtaggingSV = cms.Sequence(akPuFilter4CaloImpactParameterTagInfos
            *
            akPuFilter4CaloSecondaryVertexTagInfos
            * (akPuFilter4CaloSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter4CaloSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter4CaloCombinedSecondaryVertexBJetTags+
                akPuFilter4CaloCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter4CaloJetBtaggingNegSV = cms.Sequence(akPuFilter4CaloImpactParameterTagInfos
            *
            akPuFilter4CaloSecondaryVertexNegativeTagInfos
            * (akPuFilter4CaloNegativeSimpleSecondaryVertexHighEffBJetTags+
                akPuFilter4CaloNegativeSimpleSecondaryVertexHighPurBJetTags+
                akPuFilter4CaloNegativeCombinedSecondaryVertexBJetTags+
                akPuFilter4CaloPositiveCombinedSecondaryVertexBJetTags+
                akPuFilter4CaloNegativeCombinedSecondaryVertexV2BJetTags+
                akPuFilter4CaloPositiveCombinedSecondaryVertexV2BJetTags
              )
            )

akPuFilter4CaloJetBtaggingMu = cms.Sequence(akPuFilter4CaloSoftPFMuonsTagInfos * (akPuFilter4CaloSoftPFMuonBJetTags
                +
                akPuFilter4CaloSoftPFMuonByIP3dBJetTags
                +
                akPuFilter4CaloSoftPFMuonByPtBJetTags
                +
                akPuFilter4CaloNegativeSoftPFMuonByPtBJetTags
                +
                akPuFilter4CaloPositiveSoftPFMuonByPtBJetTags
              )
            )

akPuFilter4CaloJetBtagging = cms.Sequence(akPuFilter4CaloJetBtaggingIP
            *akPuFilter4CaloJetBtaggingSV
            *akPuFilter4CaloJetBtaggingNegSV
#            *akPuFilter4CaloJetBtaggingMu
            )

akPuFilter4CalopatJetsWithBtagging = patJets.clone(jetSource = cms.InputTag("akPuFilter4CaloJets"),
        genJetMatch          = cms.InputTag("akPuFilter4Calomatch"),
        genPartonMatch       = cms.InputTag("akPuFilter4Caloparton"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPuFilter4Calocorr")),
        JetPartonMapSource   = cms.InputTag("akPuFilter4CaloPatJetFlavourAssociationLegacy"),
	JetFlavourInfoSource   = cms.InputTag("akPuFilter4CaloPatJetFlavourAssociation"),
        trackAssociationSource = cms.InputTag("akPuFilter4CaloJetTracksAssociatorAtVertex"),
	useLegacyJetMCFlavour = True,
        discriminatorSources = cms.VInputTag(cms.InputTag("akPuFilter4CaloSimpleSecondaryVertexHighEffBJetTags"),
            cms.InputTag("akPuFilter4CaloSimpleSecondaryVertexHighPurBJetTags"),
            cms.InputTag("akPuFilter4CaloCombinedSecondaryVertexBJetTags"),
            cms.InputTag("akPuFilter4CaloCombinedSecondaryVertexV2BJetTags"),
            cms.InputTag("akPuFilter4CaloJetBProbabilityBJetTags"),
            cms.InputTag("akPuFilter4CaloJetProbabilityBJetTags"),
            #cms.InputTag("akPuFilter4CaloSoftPFMuonByPtBJetTags"),
            #cms.InputTag("akPuFilter4CaloSoftPFMuonByIP3dBJetTags"),
            cms.InputTag("akPuFilter4CaloTrackCountingHighEffBJetTags"),
            cms.InputTag("akPuFilter4CaloTrackCountingHighPurBJetTags"),
            ),
        jetIDMap = cms.InputTag("akPuFilter4CaloJetID"),
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

akPuFilter4CaloNjettiness = Njettiness.clone(
		    src = cms.InputTag("akPuFilter4CaloJets"),
           	    R0  = cms.double( 0.4)
)
akPuFilter4CalopatJetsWithBtagging.userData.userFloats.src += ['akPuFilter4CaloNjettiness:tau1','akPuFilter4CaloNjettiness:tau2','akPuFilter4CaloNjettiness:tau3']

akPuFilter4CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akPuFilter4CalopatJetsWithBtagging"),
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
                                                             bTagJetName = cms.untracked.string("akPuFilter4Calo"),
                                                             jetName = cms.untracked.string("akPuFilter4Calo"),
                                                             genPtMin = cms.untracked.double(5),
                                                             hltTrgResults = cms.untracked.string('TriggerResults::'+'HISIGNAL'),
							     doTower = cms.untracked.bool(False),
							     doSubJets = cms.untracked.bool(True),
                                                             doGenSubJets = cms.untracked.bool(False),     
                                                             subjetGenTag = cms.untracked.InputTag("akFilter4GenJets"),
                                                             doGenTaus = True
                                                             )

akPuFilter4CaloJetSequence_mc = cms.Sequence(
                                                  #akPuFilter4Caloclean
                                                  #*
                                                  akPuFilter4Calomatch
                                                  #*
                                                  #akPuFilter4CalomatchGroomed
                                                  *
                                                  akPuFilter4Caloparton
                                                  *
                                                  akPuFilter4Calocorr
                                                  *
                                                  #akPuFilter4CaloJetID
                                                  #*
                                                  akPuFilter4CaloPatJetFlavourIdLegacy
                                                  #*
			                          #akPuFilter4CaloPatJetFlavourId  # Use legacy algo till PU implemented
                                                  *
                                                  akPuFilter4CaloJetTracksAssociatorAtVertex
                                                  *
                                                  akPuFilter4CaloJetBtagging
                                                  *
                                                  akPuFilter4CaloNjettiness #No constituents for calo jets in pp. Must be removed for pp calo jets but I'm not sure how to do this transparently (Marta)
                                                  *
                                                  akPuFilter4CalopatJetsWithBtagging
                                                  *
                                                  akPuFilter4CaloJetAnalyzer
                                                  )

akPuFilter4CaloJetSequence_data = cms.Sequence(akPuFilter4Calocorr
                                                    *
                                                    #akPuFilter4CaloJetID
                                                    #*
                                                    akPuFilter4CaloJetTracksAssociatorAtVertex
                                                    *
                                                    akPuFilter4CaloJetBtagging
                                                    *
                                                    akPuFilter4CaloNjettiness 
                                                    *
                                                    akPuFilter4CalopatJetsWithBtagging
                                                    *
                                                    akPuFilter4CaloJetAnalyzer
                                                    )

akPuFilter4CaloJetSequence_jec = cms.Sequence(akPuFilter4CaloJetSequence_mc)
akPuFilter4CaloJetSequence_mb = cms.Sequence(akPuFilter4CaloJetSequence_mc)

akPuFilter4CaloJetSequence = cms.Sequence(akPuFilter4CaloJetSequence_jec)
akPuFilter4CaloJetAnalyzer.genPtMin = cms.untracked.double(1)
akPuFilter4CaloJetAnalyzer.jetPtMin = cms.double(1)
