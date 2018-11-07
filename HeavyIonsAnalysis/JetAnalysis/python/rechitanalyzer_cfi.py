import FWCore.ParameterSet.Config as cms

rechitanalyzer = cms.EDAnalyzer("RecHitTreeProducer",
    EBRecHitSrc = cms.untracked.InputTag("ecalRecHit","EcalRecHitsEB"),
    EERecHitSrc = cms.untracked.InputTag("ecalRecHit","EcalRecHitsEE"),
    BasicClusterSrc1 = cms.untracked.InputTag("islandBasicClusters","islandBarrelBasicClusters"),
    hcalHFRecHitSrc = cms.untracked.InputTag("hfreco"),
    hcalHBHERecHitSrc = cms.untracked.InputTag("hbhereco"),
    towersSrc = cms.untracked.InputTag("towerMaker"),
    JetSrc = cms.untracked.InputTag("iterativeConePu5CaloJets"),
    zdcRecHitSrc = cms.untracked.InputTag("zdcreco"),
    castorRecHitSrc = cms.untracked.InputTag("castorreco"),
    zdcDigiSrc = cms.untracked.InputTag("hcalDigis"),
    vtxSrc = cms.untracked.InputTag("hiSelectedVertex"),
    useJets = cms.untracked.bool(True),
    doBasicClusters = cms.untracked.bool(False),
    doTowers = cms.untracked.bool(True),
    doEcal = cms.untracked.bool(False),
    doHcal = cms.untracked.bool(False),
    hasVtx = cms.untracked.bool(True),
    doFastJet = cms.untracked.bool(False),
    FastJetTag = cms.untracked.InputTag("kt4CaloJets"),
    doEbyEonly = cms.untracked.bool(False),
    HFtowerMin = cms.untracked.double(3),
    HFlongMin = cms.untracked.double(0.5),
    HFshortMin = cms.untracked.double(0.85),     
    HBHETreePtMin = cms.untracked.double(15),
    HFTreePtMin = cms.untracked.double(15),
    EBTreePtMin = cms.untracked.double(15),
    EETreePtMin = cms.untracked.double(15),
    TowerTreePtMin = cms.untracked.double(-9999),
    doHF = cms.untracked.bool(True)
    )

pfTowers = rechitanalyzer.clone(
    doEcal  = cms.untracked.bool(False),
    doHcal  = cms.untracked.bool(False),
    hasVtx  = cms.untracked.bool(False),
    doFastJet = cms.untracked.bool(False),
    towersSrc = cms.untracked.InputTag("PFTowers"),
    TowerTreePtMin = cms.untracked.double(-99),
    )

rechitanalyzerpp = rechitanalyzer.clone(
    vtxSrc = cms.untracked.InputTag("offlinePrimaryVerticesWithBS"),
    JetSrc = cms.untracked.InputTag("ak4CaloJets"),
    doHF = cms.untracked.bool(False)
    )

pfTowerspp = pfTowers.clone(
    vtxSrc = cms.untracked.InputTag("offlinePrimaryVerticesWithBS"),
    JetSrc = cms.untracked.InputTag("ak4CaloJets"),
    doHF = cms.untracked.bool(False),
    doTowers = cms.untracked.bool(False)
    )
