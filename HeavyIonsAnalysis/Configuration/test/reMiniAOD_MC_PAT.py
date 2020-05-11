# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: reMiniAOD_MC --conditions auto:phase1_2018_realistic_hi -s PAT --process PAT -n 100 --era Run2_2018_pp_on_AA --eventcontent MINIAODSIM --runUnscheduled --scenario pp --datatier MINIAODSIM --mc --filein /store/himc/HINPbPbAutumn18DR/DiJet_pThat-15_TuneCP5_HydjetDrumMB_5p02TeV_Pythia8/AODSIM/mva98_103X_upgrade2018_realistic_HI_v11-v1/50000/FF707B12-46F8-8C45-8D10-A336E1260A24.root
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('PAT',eras.Run2_2018_pp_on_AA)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.PATMC_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('HeavyIonsAnalysis.Configuration.hfCoincFilter_cff') #add centrality filter cfg file



process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    #input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring('/store/himc/HINPbPbAutumn18DR/DiJet_pThat-15_TuneCP5_HydjetDrumMB_5p02TeV_Pythia8/AODSIM/mva98_103X_upgrade2018_realistic_HI_v11-v1/50000/FF707B12-46F8-8C45-8D10-A336E1260A24.root'),
                            #fileNames = cms.untracked.vstring('/store/himc/HINPbPbAutumn18DR/JPsi_pThat-2_TuneCP5_HydjetDrumMB_5p02TeV_Pythia8/AODSIM/mva98_103X_upgrade2018_realistic_HI_v11-v1/40001/EC02B6A4-B279-1846-BE66-38B0A10217CA.root'),
                            fileNames = cms.untracked.vstring('file:/tmp/mnguyen/EC02B6A4-B279-1846-BE66-38B0A10217CA.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('reMiniAOD_MC nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAODSIM'),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(-900),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('/tmp/mnguyen/reMiniAOD_MC_PAT_JPsi.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    overrideBranchesSplitLevel = cms.untracked.VPSet(
        cms.untracked.PSet(
            branch = cms.untracked.string('patPackedCandidates_packedPFCandidates__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('recoGenParticles_prunedGenParticles__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('patTriggerObjectStandAlones_slimmedPatTrigger__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('patPackedGenParticles_packedGenParticles__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('patJets_slimmedJets__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('recoVertexs_offlineSlimmedPrimaryVertices__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('recoCaloClusters_reducedEgamma_reducedESClusters_*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedEBRecHits_*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedEERecHits_*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('recoGenJets_slimmedGenJets__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('patJets_slimmedJetsPuppi__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedESRecHits_*'),
            splitLevel = cms.untracked.int32(99)
        )
    ),
    overrideInputFileSplitLevels = cms.untracked.bool(True),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2018_realistic_hi', '')

# Path and EndPath definitions
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_globalSuperTightHalo2016Filter = cms.Path(process.globalSuperTightHalo2016Filter)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_globalTightHalo2016Filter = cms.Path(process.globalTightHalo2016Filter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_BadChargedCandidateSummer16Filter = cms.Path(process.BadChargedCandidateSummer16Filter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_BadPFMuonFilter = cms.Path(process.BadPFMuonFilter)
process.Flag_ecalBadCalibFilter = cms.Path(process.ecalBadCalibFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_BadChargedCandidateFilter = cms.Path(process.BadChargedCandidateFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_BadPFMuonSummer16Filter = cms.Path(process.BadPFMuonSummer16Filter)
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
#---------------add centrality filters here---------------------
# make calotowers into candidates
process.Flag_towersAboveThreshold = cms.Path(process.towersAboveThreshold)
# make calotowers into candidates with threshold 2, 4 and 5
process.Flag_towersAboveThresholdTh2 = cms.Path(process.towersAboveThresholdTh2)
process.Flag_towersAboveThresholdTh4 = cms.Path(process.towersAboveThresholdTh4)
process.Flag_towersAboveThresholdTh5 = cms.Path(process.towersAboveThresholdTh5)
# select HF+ towers above threshold
process.Flag_hfPosTowers = cms.Path(process.hfPosTowers)
# select HF- towers above threshold
process.Flag_hfNegTowers = cms.Path(process.hfNegTowers)
# select HF+/HF- towers above threshold 2, 4 and 5
process.Flag_hfPosTowersTh2 = cms.Path(process.hfPosTowersTh2)
process.Flag_hfNegTowersTh2 = cms.Path(process.hfNegTowersTh2)
process.Flag_hfPosTowersTh4 = cms.Path(process.hfPosTowersTh4)
process.Flag_hfNegTowersTh4 = cms.Path(process.hfNegTowersTh4)
process.Flag_hfPosTowersTh5 = cms.Path(process.hfPosTowersTh5)
process.Flag_hfNegTowersTh5 = cms.Path(process.hfNegTowersTh5)
# require at least one HF+ tower above threshold
process.Flag_hfPosFilter = cms.Path(process.hfPosFilter)
process.Flag_hfNegFilter = cms.Path(process.hfNegFilter)
# require at least one HF+/HF- tower above threshold 2, 4and 5
process.Flag_hfPosFilterTh2 = cms.Path(process.hfPosFilterTh2)
process.Flag_hfNegFilterTh2 = cms.Path(process.hfNegFilterTh2)
process.Flag_hfPosFilterTh4 = cms.Path(process.hfPosFilterTh4)
process.Flag_hfNegFilterTh4 = cms.Path(process.hfNegFilterTh4)
process.Flag_hfPosFilterTh5 = cms.Path(process.hfPosFilterTh5)
process.Flag_hfNegFilterTh5 = cms.Path(process.hfNegFilterTh5)
# one HF tower above threshold on each side
process.Flag_hfCoincFilterTh2 = cms.Path(process.hfCoincFilterTh2)
process.Flag_hfCoincFilterTh3 = cms.Path(process.hfCoincFilterTh3)
process.Flag_hfCoincFilterTh4 = cms.Path(process.hfCoincFilterTh4)
process.Flag_hfCoincFilterTh5 = cms.Path(process.hfCoincFilterTh5)
# two HF towers above threshold on each side
process.Flag_hfPosFilter2 = cms.Path(process.hfPosFilter2)
process.Flag_hfNegFilter2 = cms.Path(process.hfNegFilter2)
process.Flag_hfPosFilter2Th2 = cms.Path(process.hfPosFilter2Th2)
process.Flag_hfNegFilter2Th2 = cms.Path(process.hfNegFilter2Th2)
process.Flag_hfPosFilter2Th4 = cms.Path(process.hfPosFilter2Th4)
process.Flag_hfNegFilter2Th4 = cms.Path(process.hfNegFilter2Th4)
process.Flag_hfPosFilter2Th5 = cms.Path(process.hfPosFilter2Th5)
process.Flag_hfNegFilter2Th5 = cms.Path(process.hfNegFilter2Th5)
process.Flag_hfCoincFilter2Th2 = cms.Path(process.hfCoincFilter2Th2)
process.Flag_hfCoincFilter2Th3 = cms.Path(process.hfCoincFilter2Th3)
process.Flag_hfCoincFilter2Th4 = cms.Path(process.hfCoincFilter2Th4)
process.Flag_hfCoincFilter2Th5 = cms.Path(process.hfCoincFilter2Th5)
#three HF towers above threshold on each side
process.Flag_hfPosFilter3 = cms.Path(process.hfPosFilter3)
process.Flag_hfNegFilter3 = cms.Path(process.hfNegFilter3)
process.Flag_hfPosFilter3Th2 = cms.Path(process.hfPosFilter3Th2)
process.Flag_hfNegFilter3Th2 = cms.Path(process.hfNegFilter3Th2)
process.Flag_hfPosFilter3Th4 = cms.Path(process.hfPosFilter3Th4)
process.Flag_hfNegFilter3Th4 = cms.Path(process.hfNegFilter3Th4)
process.Flag_hfPosFilter3Th5 = cms.Path(process.hfPosFilter3Th5)
process.Flag_hfNegFilter3Th5 = cms.Path(process.hfNegFilter3Th5)
process.Flag_hfCoincFilter3Th2 = cms.Path(process.hfCoincFilter3Th2)
process.Flag_hfCoincFilter3Th3 = cms.Path(process.hfCoincFilter3Th3)
process.Flag_hfCoincFilter3Th4 = cms.Path(process.hfCoincFilter3Th4)
process.Flag_hfCoincFilter3Th5 = cms.Path(process.hfCoincFilter3Th5)
#four HF towers above threshold on each side
process.Flag_hfPosFilter4 = cms.Path(process.hfPosFilter4)
process.Flag_hfNegFilter4 = cms.Path(process.hfNegFilter4)
process.Flag_hfPosFilter4Th2 = cms.Path(process.hfPosFilter4Th2)
process.Flag_hfNegFilter4Th2 = cms.Path(process.hfNegFilter4Th2)
process.Flag_hfPosFilter4Th4 = cms.Path(process.hfPosFilter4Th4)
process.Flag_hfNegFilter4Th4 = cms.Path(process.hfNegFilter4Th4)
process.Flag_hfPosFilter4Th5 = cms.Path(process.hfPosFilter4Th5)
process.Flag_hfNegFilter4Th5 = cms.Path(process.hfNegFilter4Th5)
process.Flag_hfCoincFilter4Th2 = cms.Path(process.hfCoincFilter4Th2)
process.Flag_hfCoincFilter4Th3 = cms.Path(process.hfCoincFilter4Th3)
process.Flag_hfCoincFilter4Th4 = cms.Path(process.hfCoincFilter4Th4)
process.Flag_hfCoincFilter4Th5 = cms.Path(process.hfCoincFilter4Th5)
#five hf towers above threshold on each side
process.Flag_hfPosFilter5 = cms.Path(process.hfPosFilter5)
process.Flag_hfNegFilter5 = cms.Path(process.hfNegFilter5)
process.Flag_hfPosFilter5Th2 = cms.Path(process.hfPosFilter5Th2)
process.Flag_hfNegFilter5Th2 = cms.Path(process.hfNegFilter5Th2)
process.Flag_hfPosFilter5Th4 = cms.Path(process.hfPosFilter5Th4)
process.Flag_hfNegFilter5Th4 = cms.Path(process.hfNegFilter5Th4)
process.Flag_hfPosFilter5Th5 = cms.Path(process.hfPosFilter5Th5)
process.Flag_hfNegFilter5Th5 = cms.Path(process.hfNegFilter5Th5)
process.Flag_hfCoincFilter5Th2 = cms.Path(process.hfCoincFilter5Th2)
process.Flag_hfCoincFilter5Th3 = cms.Path(process.hfCoincFilter5Th3)
process.Flag_hfCoincFilter5Th4 = cms.Path(process.hfCoincFilter5Th4)
process.Flag_hfCoincFilter5Th5 = cms.Path(process.hfCoincFilter5Th5)
#---------------------------------------------------------------
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.Flag_HBHENoiseFilter,process.Flag_HBHENoiseIsoFilter,process.Flag_CSCTightHaloFilter,process.Flag_CSCTightHaloTrkMuUnvetoFilter,process.Flag_CSCTightHalo2015Filter,process.Flag_globalTightHalo2016Filter,process.Flag_globalSuperTightHalo2016Filter,process.Flag_HcalStripHaloFilter,process.Flag_hcalLaserEventFilter,process.Flag_EcalDeadCellTriggerPrimitiveFilter,process.Flag_EcalDeadCellBoundaryEnergyFilter,process.Flag_ecalBadCalibFilter,process.Flag_goodVertices,process.Flag_eeBadScFilter,process.Flag_ecalLaserCorrFilter,process.Flag_trkPOGFilters,process.Flag_chargedHadronTrackResolutionFilter,process.Flag_muonBadTrackFilter,process.Flag_BadChargedCandidateFilter,process.Flag_BadPFMuonFilter,process.Flag_BadChargedCandidateSummer16Filter,process.Flag_BadPFMuonSummer16Filter,process.Flag_trkPOG_manystripclus53X,process.Flag_trkPOG_toomanystripclus53X,process.Flag_trkPOG_logErrorTooManyClusters,process.Flag_METFilters,process.Flag_towersAboveThreshold,process.Flag_towersAboveThresholdTh2,process.Flag_towersAboveThresholdTh4,process.Flag_towersAboveThresholdTh5,process.Flag_hfPosTowers,process.Flag_hfNegTowers,process.Flag_hfPosTowersTh2,process.Flag_hfNegTowersTh2,process.Flag_hfPosTowersTh4,process.Flag_hfNegTowersTh4,process.Flag_hfPosTowersTh5,process.Flag_hfNegTowersTh5,process.Flag_hfPosFilter,process.Flag_hfNegFilter,process.Flag_hfPosFilterTh2,process.Flag_hfNegFilterTh2,process.Flag_hfPosFilterTh4,process.Flag_hfNegFilterTh4,process.Flag_hfPosFilterTh5,process.Flag_hfNegFilterTh5,process.Flag_hfCoincFilterTh2,process.Flag_hfCoincFilterTh3,process.Flag_hfCoincFilterTh4,process.Flag_hfCoincFilterTh5,process.Flag_hfPosFilter2,process.Flag_hfNegFilter2,process.Flag_hfPosFilter2Th2,process.Flag_hfNegFilter2Th2,process.Flag_hfPosFilter2Th4,process.Flag_hfNegFilter2Th4,process.Flag_hfPosFilter2Th5,process.Flag_hfNegFilter2Th5,process.Flag_hfCoincFilter2Th2,process.Flag_hfCoincFilter2Th3,process.Flag_hfCoincFilter2Th4,process.Flag_hfCoincFilter2Th5,process.Flag_hfPosFilter3,process.Flag_hfNegFilter3,process.Flag_hfPosFilter3Th2,process.Flag_hfNegFilter3Th2,process.Flag_hfPosFilter3Th4,process.Flag_hfNegFilter3Th4,process.Flag_hfPosFilter3Th5,process.Flag_hfNegFilter3Th5,process.Flag_hfCoincFilter3Th2,process.Flag_hfCoincFilter3Th3,process.Flag_hfCoincFilter3Th4,process.Flag_hfCoincFilter3Th5,process.Flag_hfPosFilter4,process.Flag_hfNegFilter4,process.Flag_hfPosFilter4Th2,process.Flag_hfNegFilter4Th2,process.Flag_hfPosFilter4Th4,process.Flag_hfNegFilter4Th4,process.Flag_hfPosFilter4Th5,process.Flag_hfNegFilter4Th5,process.Flag_hfCoincFilter4Th2,process.Flag_hfCoincFilter4Th3,process.Flag_hfCoincFilter4Th4,process.Flag_hfCoincFilter4Th5,process.Flag_hfPosFilter5,process.Flag_hfNegFilter5,process.Flag_hfPosFilter5Th2,process.Flag_hfNegFilter5Th2,process.Flag_hfPosFilter5Th4,process.Flag_hfNegFilter5Th4,process.Flag_hfPosFilter5Th5,process.Flag_hfNegFilter5Th5,process.Flag_hfCoincFilter5Th2,process.Flag_hfCoincFilter5Th3,process.Flag_hfCoincFilter5Th4,process.Flag_hfCoincFilter5Th5,process.endjob_step,process.MINIAODSIMoutput_step)

process.schedule.associate(process.patTask)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
#Setup FWK for multithreaded                                                                                                        
process.options.numberOfThreads=cms.untracked.uint32(8)
process.options.numberOfStreams=cms.untracked.uint32(0)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
