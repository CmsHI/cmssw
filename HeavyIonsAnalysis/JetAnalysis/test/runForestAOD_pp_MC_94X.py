### HiForest Configuration
# Collisions: pp
# Type: MC
# Input: AOD

import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet()

#####################################################################################
# HiForest labelling info
#####################################################################################

process.load("HeavyIonsAnalysis.JetAnalysis.HiForest_cff")
process.HiForest.inputLines = cms.vstring("HiForest 94X",)
import subprocess, os
version = subprocess.check_output(['git',
    '-C', os.path.expandvars('$CMSSW_BASE/src'), 'describe', '--tags'])
if version == '':
    version = 'no git info'
process.HiForest.HiForestVersion = cms.string(version)

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	'file:/afs/cern.ch/work/r/rbi/public/forest/RunIIpp5Spring18DR_DYJetsToLL_MLL-50_TuneCP5_5020GeV-amcatnloFXFX-pythia8_AODSIM.root'
    )
)

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(8))

#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_forppRef5TeV', '')
process.HiForest.GlobalTagLabel = process.GlobalTag.globaltag

process.GlobalTag.toGet.extend([
    cms.PSet(record = cms.string("BTagTrackProbability3DRcd"),
             tag = cms.string("JPcalib_MC94X_2017pp_v2"),
             connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")

         )
      ])

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestAOD.root"))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

#############################
# Jets
#############################
process.load("HeavyIonsAnalysis.JetAnalysis.fullJetSequence_pp_mc_cff")

# Use this version for JEC
# process.load("HeavyIonsAnalysis.JetAnalysis.fullJetSequence_pp_jec_cff")

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import overrideJEC_MC_pp5020_2017  
process = overrideJEC_MC_pp5020_2017(process)
#####################################################################################

############################
# Event Analysis
############################
# use data version to avoid PbPb MC
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlinePrimaryVertices")
process.hiEvtAnalyzer.doCentrality = cms.bool(False)
process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)
process.hiEvtAnalyzer.doMC = cms.bool(True) # general MC info
process.hiEvtAnalyzer.doHiMC = cms.bool(False) # HI specific MC info

process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

process.load('HeavyIonsAnalysis.JetAnalysis.HiGenAnalyzer_cfi')
process.HiGenParticleAna.genParticleSrc = cms.untracked.InputTag("genParticles")
process.HiGenParticleAna.doHI = False

process.load('HeavyIonsAnalysis.EventAnalysis.runanalyzer_cff')

process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_pp_cfi")
process.pfcandAnalyzer.skipCharged      = False
process.pfcandAnalyzer.pfPtMin          = 0
process.pfcandAnalyzer.pfCandidateLabel = cms.InputTag("particleFlow")
process.pfcandAnalyzer.doVS             = cms.untracked.bool(False)
process.pfcandAnalyzer.doUEraw_         = cms.untracked.bool(False)
process.pfcandAnalyzer.genLabel         = cms.InputTag("genParticles")

#####################################################################################

#########################
# Track Analyzer
#########################
process.load('HeavyIonsAnalysis.JetAnalysis.ExtraTrackReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_cff')

# Use this instead for track corrections
# process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_Corr_cff')

#####################################################################################

#####################
# photons
######################
process.load('HeavyIonsAnalysis.PhotonAnalysis.ggHiNtuplizer_cfi')

####################################################################################

#####################
# Electron ID
#####################

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format to be processed
# DataFormat.AOD or DataFormat.MiniAOD
dataFormat = DataFormat.AOD
switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce. https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Recipe_for_regular_users_for_7_4
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff']

# add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

#####################################################################################

#########################
# Main analysis list
#########################

process.ana_step = cms.Path(
    process.hltanalysis *
    process.hiEvtAnalyzer *
    process.hltobject +
    # process.l1object +
    process.HiGenParticleAna*
    process.genJetSequence +
    process.jetSequence +
    # Should be added in the path for VID module
    # process.egmGsfElectronIDSequence +
    process.ggHiNtuplizer +
    process.ggHiNtuplizerGED +
    process.pfcandAnalyzer +
    process.HiForest +
    process.trackSequencesPP +
    process.runAnalyzer
)

#####################################################################################

#########################
# Event Selection
#########################

process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')
process.pHBHENoiseFilterResultProducer = cms.Path(process.HBHENoiseFilterResultProducer)
process.HBHENoiseFilterResult = cms.Path(process.fHBHENoiseFilterResult)
process.HBHENoiseFilterResultRun1 = cms.Path(process.fHBHENoiseFilterResultRun1)
process.HBHENoiseFilterResultRun2Loose = cms.Path(process.fHBHENoiseFilterResultRun2Loose)
process.HBHENoiseFilterResultRun2Tight = cms.Path(process.fHBHENoiseFilterResultRun2Tight)
process.HBHEIsoNoiseFilterResult = cms.Path(process.fHBHEIsoNoiseFilterResult)

process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True), # otherwise it won't filter the events
)

process.NoScraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
)

process.pPAprimaryVertexFilter = cms.Path(process.PAprimaryVertexFilter)
process.pBeamScrapingFilter=cms.Path(process.NoScraping)

process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")
process.pVertexFilterCutG = cms.Path(process.pileupVertexFilterCutG)
process.pVertexFilterCutGloose = cms.Path(process.pileupVertexFilterCutGloose)
process.pVertexFilterCutGtight = cms.Path(process.pileupVertexFilterCutGtight)
process.pVertexFilterCutGplus = cms.Path(process.pileupVertexFilterCutGplus)
process.pVertexFilterCutE = cms.Path(process.pileupVertexFilterCutE)
process.pVertexFilterCutEandG = cms.Path(process.pileupVertexFilterCutEandG)

process.pAna = cms.EndPath(process.skimanalysis)

# Customization
