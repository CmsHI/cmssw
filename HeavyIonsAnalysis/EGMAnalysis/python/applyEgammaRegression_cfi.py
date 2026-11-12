import FWCore.ParameterSet.Config as cms

def applyEgammaRegression(process, era = ''):
    if era not in ['Run3_2023_PbPb','Run3_2024_PbPb','Run3_2025_PbPb','Run3_2026_PbPb']:
        raise Exception(f"Era {era} is not supported by candidateBtaggingMiniAOD!")

    from RecoEgamma.EgammaTools.regressionModifier_cfi import regressionModifier as _reg
    regressionModifier = _reg.clone(
        rhoMaps = ["hiPuRho:mapEtaEdges", "hiPuRho:mapToRho"],
        eleRegs = dict(
            ecalOnlyMean = dict(
                ebLowEtForestName = cms.ESInputTag("", "electron_eb_ecalOnly_HIN_1To500_0p2To2_mean"),
                ebHighEtForestName = cms.ESInputTag("", "electron_eb_ecalOnly_HIN_1To500_0p2To2_mean"),
                eeLowEtForestName = cms.ESInputTag("", "electron_ee_ecalOnly_HIN_1To500_0p2To2_mean"),
                eeHighEtForestName = cms.ESInputTag("", "electron_ee_ecalOnly_HIN_1To500_0p2To2_mean"),
            ),
            ecalOnlySigma = dict(
                ebLowEtForestName = cms.ESInputTag("", "electron_eb_ecalOnly_HIN_1To500_0p0002To0p5_sigma"),
                ebHighEtForestName = cms.ESInputTag("", "electron_eb_ecalOnly_HIN_1To500_0p0002To0p5_sigma"),
                eeLowEtForestName = cms.ESInputTag("", "electron_ee_ecalOnly_HIN_1To500_0p0002To0p5_sigma"),
                eeHighEtForestName = cms.ESInputTag("", "electron_ee_ecalOnly_HIN_1To500_0p0002To0p5_sigma"),
            ),
            epComb = dict(
                ecalTrkRegressionConfig = dict(
                    ebLowEtForestName = cms.ESInputTag("", 'electron_eb_ecalTrk_HIN_1To500_0p2To2_mean'),
                    ebHighEtForestName = cms.ESInputTag("", 'electron_eb_ecalTrk_HIN_1To500_0p2To2_mean'),
                    eeLowEtForestName = cms.ESInputTag("", 'electron_ee_ecalTrk_HIN_1To500_0p2To2_mean'),
                    eeHighEtForestName = cms.ESInputTag("", 'electron_ee_ecalTrk_HIN_1To500_0p2To2_mean'),
                ),
                ecalTrkRegressionUncertConfig = dict(
                    ebLowEtForestName = cms.ESInputTag("", 'electron_eb_ecalTrk_HIN_1To500_0p0002To0p5_sigma'),
                    ebHighEtForestName = cms.ESInputTag("", 'electron_eb_ecalTrk_HIN_1To500_0p0002To0p5_sigma'),
                    eeLowEtForestName = cms.ESInputTag("", 'electron_ee_ecalTrk_HIN_1To500_0p0002To0p5_sigma'),
                    eeHighEtForestName = cms.ESInputTag("", 'electron_ee_ecalTrk_HIN_1To500_0p0002To0p5_sigma'),
                )
            )
        ),
        phoRegs = dict(
            ecalOnlyMean = dict(
                ebLowEtForestName = cms.ESInputTag("", "photon_eb_ecalOnly_HIN_10To500_0p2To2_mean"),
                ebHighEtForestName = cms.ESInputTag("", "photon_eb_ecalOnly_HIN_10To500_0p2To2_mean"),
                eeLowEtForestName = cms.ESInputTag("", "photon_ee_ecalOnly_HIN_10To500_0p2To2_mean"),
                eeHighEtForestName = cms.ESInputTag("", "photon_ee_ecalOnly_HIN_10To500_0p2To2_mean"),
            ),
            ecalOnlySigma = dict(
                ebLowEtForestName = cms.ESInputTag("", "photon_eb_ecalOnly_HIN_10To500_0p0002To0p5_sigma"),
                ebHighEtForestName = cms.ESInputTag("", "photon_eb_ecalOnly_HIN_10To500_0p0002To0p5_sigma"),
                eeLowEtForestName = cms.ESInputTag("", "photon_ee_ecalOnly_HIN_10To500_0p0002To0p5_sigma"),
                eeHighEtForestName = cms.ESInputTag("", "photon_ee_ecalOnly_HIN_10To500_0p0002To0p5_sigma"),
            )
        )
    )

    process.slimmedElectrons = cms.EDProducer("ModifiedElectronProducer",
        src = cms.InputTag("slimmedElectrons::@skipCurrentProcess"),
        modifierConfig = cms.PSet(modifications = cms.VPSet(regressionModifier))
    )

    process.slimmedPhotons = cms.EDProducer("ModifiedPhotonProducer",
        src = cms.InputTag("slimmedPhotons::@skipCurrentProcess"),
        modifierConfig = cms.PSet(modifications = cms.VPSet(regressionModifier))
    )

    from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import PackedPFTowers, hiPuRho
    process.PackedPFTowers = PackedPFTowers.clone()
    process.hiPuRho = hiPuRho.clone(src = 'PackedPFTowers')

    process.egammaRegressionSeq = cms.Sequence(process.PackedPFTowers * process.hiPuRho * process.slimmedElectrons * process.slimmedPhotons)
    process.forest.insert(0, process.egammaRegressionSeq)
    
    for label in ['photon_eb_ecalOnly_HIN_10To500_0p2To2_mean','photon_ee_ecalOnly_HIN_10To500_0p2To2_mean','photon_eb_ecalOnly_HIN_10To500_0p0002To0p5_sigma','photon_ee_ecalOnly_HIN_10To500_0p0002To0p5_sigma','electron_eb_ecalOnly_HIN_1To500_0p2To2_mean','electron_ee_ecalOnly_HIN_1To500_0p2To2_mean','electron_eb_ecalOnly_HIN_1To500_0p0002To0p5_sigma','electron_ee_ecalOnly_HIN_1To500_0p0002To0p5_sigma','electron_eb_ecalTrk_HIN_1To500_0p2To2_mean','electron_ee_ecalTrk_HIN_1To500_0p2To2_mean','electron_eb_ecalTrk_HIN_1To500_0p0002To0p5_sigma','electron_ee_ecalTrk_HIN_1To500_0p0002To0p5_sigma']:
        process.GlobalTag.toGet.extend([
            cms.PSet(
                record = cms.string("GBRDWrapperRcd"),
                connect = cms.string(f'sqlite_file:phoEleReg_{era}.db'),
                tag = cms.string(f'{label}_{era}'),
                label = cms.untracked.string(label),
            )
        ])

    return process
