### HiForest Configuration
# Collisions: XeXe
# Type: Data
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
        'root://cms-xrd-global.cern.ch//store/hidata/XeXeRun2017/HIMinimumBias9/AOD/13Dec2017-v1/70000/FCCCBE1E-B4F2-E711-BD4C-008CFAFBF00C.root'
    ),
)

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1))

#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(
    process.GlobalTag, '94X_dataRun2_ReReco_EOY17_v2', '')
process.HiForest.GlobalTagLabel = process.GlobalTag.globaltag

process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
   cms.PSet(record = cms.string("HeavyIonRcd"),
      tag = cms.string("CentralityTable_HFtowers200_DataXeXe_eff95_run2v941x02_offline"),
      connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
      label = cms.untracked.string("HFtowersEPOSLHC")
   ),
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
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak4CaloJetSequence_pp_data_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak4PFJetSequence_pp_data_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu4PFJetSequence_pp_data_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akCs4PFJetSequence_pp_data_cff')

process.akPu4PFcorr.payload = "AK4PF"
process.akCs4PFcorr.payload = "AK4PF"
process.ak4PFcorr.payload = "AK4PF"
process.ak4Calocorr.payload = "AK4PF"

process.load('HeavyIonsAnalysis.JetAnalysis.jets.HiRecoPFJets_cff')
process.akCs4PFJets.src = cms.InputTag('particleFlow')
process.PFTowers.src = cms.InputTag("particleFlow")

process.load('RecoJets.JetProducers.kt4PFJets_cfi')
process.kt4PFJetsForRho.src           = cms.InputTag('particleFlow')
process.kt4PFJetsForRho.doAreaFastjet = True
process.kt4PFJetsForRho.jetPtMin      = cms.double(0.0)
process.kt4PFJetsForRho.GhostArea     = cms.double(0.005)

process.load('RecoHI.HiJetAlgos.hiFJGridEmptyAreaCalculator_cff')
process.hiFJGridEmptyAreaCalculator.doCentrality = cms.bool(False)

process.highPurityTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("generalTracks"),
    cut = cms.string('quality("highPurity")')
)

# process.akPu4PFJetsNoLimits = akPu4PFJets.clone(
#     subtractorName = 'PuWithNtuple',
#     minimumTowersFraction = cms.double(0.)
# )

process.akPu4PFJets.subtractorName = 'PuWithNtuple'
process.akPu4PFJets.minimumTowersFraction = cms.double(0.5)

process.jetSequences = cms.Sequence(
    process.kt4PFJetsForRho +
    process.hiFJRhoProducer +
    process.hiFJGridEmptyAreaCalculator +
    # process.akPu4PFJetsNoLimits +
    process.akCs4PFJets +
    process.highPurityTracks +
    process.ak4CaloJetSequence +
    process.PFTowers +
    process.akPu4PFJets +
    process.ak4PFJetSequence +
    process.akPu4PFJetSequence +
    process.akCs4PFJetSequence 
)

#####################################################################################

############################
# Event Analysis
############################
process.load('RecoHI.HiCentralityAlgos.HiCentrality_cfi')
process.hiCentrality.produceHFhits = False
process.hiCentrality.produceHFtowers = False
process.hiCentrality.produceEcalhits = False
process.hiCentrality.produceZDChits = False
process.hiCentrality.produceETmidRapidity = False
process.hiCentrality.producePixelhits = False
process.hiCentrality.produceTracks = False
process.hiCentrality.producePixelTracks = False
process.hiCentrality.reUseCentrality = True
process.hiCentrality.srcReUse = cms.InputTag("hiCentrality","","RECO")
process.hiCentrality.srcTracks = cms.InputTag("generalTracks")
process.hiCentrality.srcVertex = cms.InputTag("offlinePrimaryVertices")

process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")
process.centralityBin.nonDefaultGlauberModel = cms.string("EPOSLHC")

process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlinePrimaryVertices")
process.hiEvtAnalyzer.doCentrality = cms.bool(False)
process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)

process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')

process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_cfi")
process.pfcandAnalyzer.skipCharged      = False
process.pfcandAnalyzer.pfPtMin          = 0
process.pfcandAnalyzer.pfCandidateLabel = cms.InputTag("particleFlow")
process.pfcandAnalyzer.doVS             = cms.untracked.bool(False)
process.pfcandAnalyzer.doUEraw_         = cms.untracked.bool(False)
process.pfcandAnalyzer.genLabel         = cms.InputTag("genParticles")

process.pfcandAnalyzerCS = process.pfcandAnalyzer.clone(
    pfCandidateLabel = cms.InputTag("akCs4PFJets","pfParticlesCs"))

process.load("HeavyIonsAnalysis.JetAnalysis.hcalNoise_cff")

#####################################################################################

#########################
# Track Analyzer
#########################
process.load('HeavyIonsAnalysis.JetAnalysis.ExtraTrackReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_cff')

####################################################################################

#####################
# Photons
#####################
process.load('HeavyIonsAnalysis.PhotonAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.gsfElectronLabel         = "gedGsfElectrons"
process.ggHiNtuplizer.recoPhotonSrc            = "islandPhotons"
process.ggHiNtuplizer.recoPhotonHiIsolationMap = "photonIsolationHIProducerppIsland"
process.ggHiNtuplizer.useValMapIso             = True
process.ggHiNtuplizer.VtxLabel                 = "offlinePrimaryVertices"
process.ggHiNtuplizer.particleFlowCollection   = "particleFlow"
process.ggHiNtuplizer.doGenParticles           = False
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
    setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)

#####################################################################################

process.load('HeavyIonsAnalysis.JetAnalysis.rechitanalyzer_pp_cfi')
process.rechitanalyzer.doEcal = False
process.rechitanalyzer.doHBHE = False
process.rechitanalyzer.doHF = False
process.rechitanalyzer.doCASTOR = False
process.rechitanalyzer.JetSrc = "ak4CaloJets"

process.pfTowers.JetSrc = "ak4CaloJets"

#########################
# Main analysis list
#########################

process.ana_step = cms.Path(
    process.hltanalysisReco *
    # process.hltobject *
    process.hiEvtAnalyzer *
    process.jetSequences +
    # Should be added in the path for VID module
    # process.egmGsfElectronIDSequence +
    process.ggHiNtuplizer +
    process.ggHiNtuplizerGED +
    process.pfcandAnalyzer +
    process.pfcandAnalyzerCS +
    process.rechitanalyzer +
    process.HiForest +
    process.trackSequencesPP
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
process.pBeamScrapingFilter = cms.Path(process.NoScraping)

process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")
process.pVertexFilterCutG = cms.Path(process.pileupVertexFilterCutG)
process.pVertexFilterCutGloose = cms.Path(process.pileupVertexFilterCutGloose)
process.pVertexFilterCutGtight = cms.Path(process.pileupVertexFilterCutGtight)
process.pVertexFilterCutGplus = cms.Path(process.pileupVertexFilterCutGplus)
process.pVertexFilterCutE = cms.Path(process.pileupVertexFilterCutE)
process.pVertexFilterCutEandG = cms.Path(process.pileupVertexFilterCutEandG)

process.pAna = cms.EndPath(process.skimanalysis)

# Customization
process.akPu4PFJetAnalyzer.trackSelection = process.ak4PFSecondaryVertexTagInfos.trackSelection
process.akPu4PFJetAnalyzer.trackPairV0Filter = process.ak4PFSecondaryVertexTagInfos.vertexCuts.v0Filter
process.akCs4PFJetAnalyzer.trackSelection = process.ak4PFSecondaryVertexTagInfos.trackSelection
process.akCs4PFJetAnalyzer.trackPairV0Filter = process.ak4PFSecondaryVertexTagInfos.vertexCuts.v0Filter
process.ak4CaloJetAnalyzer.trackSelection = process.ak4PFSecondaryVertexTagInfos.trackSelection
process.ak4CaloJetAnalyzer.trackPairV0Filter = process.ak4PFSecondaryVertexTagInfos.vertexCuts.v0Filter
process.ak4PFJetAnalyzer.trackSelection = process.ak4PFSecondaryVertexTagInfos.trackSelection
process.ak4PFJetAnalyzer.trackPairV0Filter = process.ak4PFSecondaryVertexTagInfos.vertexCuts.v0Filter
