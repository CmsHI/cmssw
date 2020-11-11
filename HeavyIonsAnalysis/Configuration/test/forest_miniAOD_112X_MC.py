### HiForest Configuration
# Input: miniAOD
# Type: data

import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 103X, data")

# import subprocess, os
# version = subprocess.check_output(
#     ['git', '-C', os.path.expandvars('$CMSSW_BASE/src'), 'describe', '--tags'])
# if version == '':
#     version = 'no git info'
# process.HiForestInfo.HiForestVersion = cms.string(version)

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        "file:/eos/cms/store/relval/CMSSW_11_2_0_pre8/RelValPyquen_DiJet_pt80to120_2760GeV_2021/MINIAODSIM/PU_112X_mcRun3_2021_realistic_HI_v11-v1/00000/2485ec38-a42f-4499-bb9f-cba185edd85a.root"
        ),
    )

# number of events to process, set to -1 to process all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
    )

###############################################################################

# load Global Tag, geometry, etc.
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

# from Configuration.AlCa.GlobalTag import GlobalTag
# process.GlobalTag = GlobalTag(process.GlobalTag, '103X_dataRun2_Prompt_v2', '')
#process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data_promptlike_hi', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

centralityTag = "CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run2v1031x02_offline"
process.HiForestInfo.info.append(centralityTag)

print('\n')
print('\033[31m~*~ CENTRALITY TABLE FOR 2018 PBPB DATA ~*~\033[0m')
print('\033[36m~*~ TAG: ' + centralityTag + ' ~*~\033[0m')
print('\n')
process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
    cms.PSet(
        record = cms.string("HeavyIonRcd"),
        tag = cms.string(centralityTag),
        label = cms.untracked.string("HFtowers"),
        connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
        ),
    ])

process.GlobalTag.toGet.extend([
    cms.PSet(
        record = cms.string("BTagTrackProbability3DRcd"),
        tag = cms.string("JPcalib_Data103X_2018PbPb_v1"),
        connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
        )
    ])

###############################################################################

# root output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestMiniAOD.root"))

# # edm output for debugging purposes
# process.output = cms.OutputModule(
#     "PoolOutputModule",
#     fileName = cms.untracked.string('HiForestEDM.root'),
#     outputCommands = cms.untracked.vstring(
#         'keep *',
#         )
#     )

# process.output_path = cms.EndPath(process.output)

###############################################################################

# reconstruction and analysis
################################

# event analysis
# process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
# process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')

################################

# electrons, photons, muons
# process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')

# process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

################################

# jets

# jet reco sequence
process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_mc_cff')

################################

# b-tagging

################################

# tracks
# process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")


################################

# forward (HF, Castor, ZDC)

###############################################################################



###############################################################################
# main forest sequence
process.forest = cms.Path(
    #process.HiForestInfo
    #+
    # process.hltanalysis
    # +
    # process.trackSequencePbPb
    # +
    # process.particleFlowAnalyser
    # +
    # process.ggHiNtuplizer
    #+
    process.akCs4PFJetSequence
    )

#customisation
