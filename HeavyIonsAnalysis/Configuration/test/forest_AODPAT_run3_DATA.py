### HiForest Configuration
# Input: miniAOD
# Type: data

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_pp_on_PbPb_2023_cff import Run3_pp_on_PbPb_2023
process = cms.Process('HiForest',Run3_pp_on_PbPb_2023)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 132X, data")


###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        '/store/hidata/HIRun2022A/HITestRaw0/AOD/PromptReco-v1/000/362/293/00000/397cc4f3-4eb7-41b9-b2d1-baa004c7f61a.root'
    ), 
)

# number of events to process, set to -1 to process all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
    )

###############################################################################

# load Global Tag, geometry, etc.
#process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

#stuff for PAT
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.StandardSequences.PAT_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '132X_dataRun3_Prompt_v7', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag


#PAT stuff

# event analysis
# process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
#process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
#process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
#process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

#from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_mc
#process.hltobject.triggerNames = trigger_list_mc

process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
################################
# electrons, photons, muons
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doMuons = cms.bool(False)
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
################################
# jet reco sequence
process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_data_cff')
################################
# tracks
process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
# muons (FTW)
process.load("HeavyIonsAnalysis.MuonAnalysis.unpackedMuons_cfi")
process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")
###############################################################################



###############################################################################
# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo + 
    # process.hltanalysis +
    process.trackSequencePbPb +
    process.particleFlowAnalyser +
    process.hiEvtAnalyzer +
    process.ggHiNtuplizer +
    process.akCs4PFJetAnalyzer +
    process.unpackedMuons +
    process.muonAnalyzer
    )


# Schedule definition
process.schedule = cms.Schedule(process.forest)
process.schedule.associate(process.patTask)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)


# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllData 

#call to customisation function miniAOD_customizeAllData imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllData(process)

# End of customisation functions

# Customisation from command line



# root output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestMiniAOD.root"))


###############################################################################


#customisation



#########################
# Event Selection -> add the needed filters here
#########################


# Selection of at least a two-track fitted vertex                                                                                                                                                                     
process.primaryVertexFilterHI = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlineSlimmedPrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2"), #in miniADO trackSize()==0, however there is no influence.                                                                                      
    filter = cms.bool(True), # otherwise it won't filter the events                                                                                                                                                   
)

process.load("HeavyIonsAnalysis.EventAnalysis.clusterCompatibilityFilter_cfi")

process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilterHI = cms.Path(process.primaryVertexFilterHI)
process.pAna = cms.EndPath(process.skimanalysis)

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltfilter = hltHighLevel.clone(
    HLTPaths = [
        "HLT_HIZeroBias_v4",                                                                                                                                                                                  
        #"HLT_HIMinimumBias_v2",
    ]
)
process.filterSequence = cms.Sequence(
    process.hltfilter
)

process.superFilterPath = cms.Path(process.filterSequence)
process.skimanalysis.superFilters = cms.vstring("superFilterPath")

for path in process.paths:
    getattr(process, path)._seq = process.filterSequence * getattr(process,path)._seq

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
