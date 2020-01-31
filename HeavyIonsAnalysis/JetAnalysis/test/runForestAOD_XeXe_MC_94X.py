### HiForest Configuration
# Collisions: XeXe
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
	'root://cms-xrd-global.cern.ch//store/himc/HINXeXeFall17DR/XeXeMinBias_5p44TeV-ReggeGribovPartonMC_EposLHC/GEN-SIM-RECO/94X_mc2017_realistic_ForXeXe_v7-v1/40000/74797CCC-C901-E811-9D06-B083FED42487.root'
    ),
)

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1))

#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(
    process.GlobalTag, '94X_mc2017_realistic_ForXeXe_v7', '')
process.HiForest.GlobalTagLabel = process.GlobalTag.globaltag

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

process.load("HeavyIonsAnalysis.JetAnalysis.FullJetSequence_XeXe_mc")
process.akPu4PFcorr.payload = "AK4PF"
process.akCs4PFcorr.payload = "AK4PF"
process.ak4PFcorr.payload = "AK4PF"

#####################################################################################

############################
# Event Analysis
############################
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')
# use data version to avoid PbPb MC
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlinePrimaryVertices")
process.hiEvtAnalyzer.doCentrality = cms.bool(False)
process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)
process.hiEvtAnalyzer.doMC = cms.bool(True) # general MC info
process.hiEvtAnalyzer.doHiMC = cms.bool(False) # HI specific MC info

process.load('HeavyIonsAnalysis.JetAnalysis.HiGenAnalyzer_cfi')
process.HiGenParticleAna.genParticleSrc = cms.untracked.InputTag("genParticles")
process.HiGenParticleAna.doHI = False

process.load('HeavyIonsAnalysis.EventAnalysis.runanalyzer_cff')

process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_cfi")
process.pfcandAnalyzer.skipCharged = False
process.pfcandAnalyzer.pfPtMin = 0
process.pfcandAnalyzer.pfCandidateLabel = cms.InputTag("particleFlow")
process.pfcandAnalyzer.doVS = cms.untracked.bool(False)
process.pfcandAnalyzer.doUEraw_ = cms.untracked.bool(False)
process.pfcandAnalyzer.genLabel = cms.InputTag("genParticles")

process.pfcandAnalyzerCS = process.pfcandAnalyzer.clone(
    pfCandidateLabel = cms.InputTag("akCs4PFJets", "pfParticlesCs"))

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
process.ggHiNtuplizer.gsfElectronLabel         = "gedGsfElectrons"
process.ggHiNtuplizer.recoPhotonSrc            = "islandPhotons"
process.ggHiNtuplizer.recoPhotonHiIsolationMap = "photonIsolationHIProducerppIsland"
process.ggHiNtuplizer.useValMapIso             = True
process.ggHiNtuplizer.VtxLabel                 = "offlinePrimaryVertices"
process.ggHiNtuplizer.particleFlowCollection   = "particleFlow"
process.ggHiNtuplizer.doElectronVID            = True

process.ggHiNtuplizerGED = process.ggHiNtuplizer.clone(
    doElectrons = True,
    doMuons = True,
    recoPhotonSrc = cms.InputTag('gedPhotons'),
    recoPhotonHiIsolationMap = cms.InputTag('photonIsolationHIProducerppGED'))

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
    process.hltanalysisReco *
    process.hiEvtAnalyzer *
    process.HiGenParticleAna*
    process.jetSequences +
    # Should be added in the path for VID module
    # process.egmGsfElectronIDSequence +
    process.ggHiNtuplizer +
    process.ggHiNtuplizerGED +
    process.pfcandAnalyzer +
    process.pfcandAnalyzerCS +
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
process.akPu4PFJetAnalyzer.doExtendedFlavorTagging = cms.untracked.bool(False)
process.akPu4PFJetAnalyzer.trackSelection = process.ak4PFSecondaryVertexTagInfos.trackSelection
process.akPu4PFJetAnalyzer.trackPairV0Filter = process.ak4PFSecondaryVertexTagInfos.vertexCuts.v0Filter
process.akCs4PFJetAnalyzer.doExtendedFlavorTagging = cms.untracked.bool(False)
process.akCs4PFJetAnalyzer.trackSelection = process.ak4PFSecondaryVertexTagInfos.trackSelection
process.akCs4PFJetAnalyzer.trackPairV0Filter = process.ak4PFSecondaryVertexTagInfos.vertexCuts.v0Filter
process.ak4CaloJetAnalyzer.doExtendedFlavorTagging = cms.untracked.bool(False)
process.ak4CaloJetAnalyzer.trackSelection = process.ak4PFSecondaryVertexTagInfos.trackSelection
process.ak4CaloJetAnalyzer.trackPairV0Filter = process.ak4PFSecondaryVertexTagInfos.vertexCuts.v0Filter
process.ak4PFJetAnalyzer.doExtendedFlavorTagging = cms.untracked.bool(False)
process.ak4PFJetAnalyzer.trackSelection = process.ak4PFSecondaryVertexTagInfos.trackSelection
process.ak4PFJetAnalyzer.trackPairV0Filter = process.ak4PFSecondaryVertexTagInfos.vertexCuts.v0Filter
