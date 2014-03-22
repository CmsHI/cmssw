

import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.patHeavyIonSequences_cff import *
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *

ak2PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("ak2PFJets"),
    matched = cms.InputTag("ak2HiGenJets")
    )

ak2PFparton = patJetPartonMatch.clone(src = cms.InputTag("ak2PFJets"),
                                                        matched = cms.InputTag("genParticles")
                                                        )

ak2PFcorr = patJetCorrFactors.clone(
    useNPV = False,
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),                                                                
    src = cms.InputTag("ak2PFJets"),
    payload = "AK2PF_generalTracks"
    )

ak2PFpatJets = patJets.clone(jetSource = cms.InputTag("ak2PFJets"),
                                               jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak2PFcorr")),
                                               genJetMatch = cms.InputTag("ak2PFmatch"),
                                               genPartonMatch = cms.InputTag("ak2PFparton"),
                                               jetIDMap = cms.InputTag("ak2PFJetID"),
                                               addBTagInfo         = False,
                                               addTagInfos         = False,
                                               addDiscriminators   = False,
                                               addAssociatedTracks = False,
                                               addJetCharge        = False,
                                               addJetID            = False,
                                               getJetMCFlavour     = False,
                                               addGenPartonMatch   = True,
                                               addGenJetMatch      = True,
                                               embedGenJetMatch    = True,
                                               embedGenPartonMatch = True,
                                               embedCaloTowers     = False,
                                               embedPFCandidates = False
				            )

ak2PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("ak2PFpatJets"),
                                                             genjetTag = 'ak2HiGenJets',
                                                             rParam = 0.2,
                                                             matchJets = cms.untracked.bool(True),
                                                             matchTag = 'ak2CalopatJets',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlowTmp'),
                                                             trackTag = cms.InputTag("hiGeneralTracks"),
                                                             fillGenJets = True,
                                                             isMC = True,
                                                             genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator")
                                                             )

ak2PFJetSequence_mc = cms.Sequence(
						  ak2PFmatch
                                                  *
                                                  ak2PFparton
                                                  *
                                                  ak2PFcorr
                                                  *
                                                  ak2PFpatJets
                                                  *
                                                  ak2PFJetAnalyzer
                                                  )

ak2PFJetSequence_data = cms.Sequence(ak2PFcorr
                                                    *
                                                    ak2PFpatJets
                                                    *
                                                    ak2PFJetAnalyzer
                                                    )

ak2PFJetSequence_jec = ak2PFJetSequence_mc

ak2PFJetSequence = cms.Sequence(ak2PFJetSequence_mc)
