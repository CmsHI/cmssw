### HiForest Configuration
# Input: miniAOD
# Type: mc

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_pp_on_PbPb_2023_cff import Run3_pp_on_PbPb_2023
process = cms.Process('HiForest', Run3_pp_on_PbPb_2023)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 132X, mc")

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        '/store/group/phys_heavyions/jviinika/PythiaHydjetRun3_5p36TeV_dijet_ptHat15_100kEvents_miniAOD_2023_08_30/PythiaHydjetDijetRun3/PythiaHydjetRun3_dijet_ptHat15_5p36TeV_miniAOD/230830_165931/0000/pythiaHydjet_miniAOD_11.root'
    ),
)

# number of events to process, set to -1 to process all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
    )

###############################################################################

# load Global Tag, geometry, etc.
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')


from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '132X_mcRun3_2023_realistic_HI_v10', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag
process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
    cms.PSet(record = cms.string("BTagTrackProbability3DRcd"),
             tag = cms.string("JPcalib_MC103X_2018PbPb_v4"),
             connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
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

#############################
# Gen Analyzer
#############################
process.load('HeavyIonsAnalysis.EventAnalysis.HiGenAnalyzer_cfi')

# event analysis
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_mc_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

#from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_mc
#process.hltobject.triggerNames = trigger_list_mc

################################
# electrons, photons, muons
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doGenParticles = cms.bool(True)
process.ggHiNtuplizer.doMuons = cms.bool(True)
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
################################
# jet reco sequence
process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_mc_cff')
################################
# tracks
process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
#muons
process.load('HeavyIonsAnalysis.JetAnalysis.hiFJRhoAnalyzer_cff')
process.load('HeavyIonsAnalysis.MuonAnalysis.hiIsoMuons_cfi')
process.load("HeavyIonsAnalysis.MuonAnalysis.unpackedMuons_cfi")
process.unpackedMuons.muons = "hiIsoMuons"
process.muonSequence = cms.Sequence(process.rhoSequence * process.hiIsoMuons * process.unpackedMuons)
process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")
process.muonAnalyzer.doGen = cms.bool(True)

###############################################################################

# ZDC analyzer
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018Producer_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018RecHit_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.zdcanalyzer_cfi')

process.zdcanalyzer.doZDCRecHit = False
process.zdcanalyzer.doZDCDigi = True
process.zdcanalyzer.zdcRecHitSrc = cms.InputTag("QWzdcreco")
process.zdcanalyzer.zdcDigiSrc = cms.InputTag("hcalDigis", "ZDC")
process.zdcanalyzer.calZDCDigi = False
process.zdcanalyzer.verbose = False

###############################################################################
# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo +
    process.hltanalysis +
#    process.hltobject +
#    process.l1object +
    process.trackSequencePbPb +
#    process.particleFlowAnalyser +
    process.hiEvtAnalyzer +
    process.HiGenParticleAna +
    process.muonSequence +
    process.ggHiNtuplizer +
#    process.zdcdigi +
#    process.QWzdcreco +
    #process.akCs4PFJetAnalyzer +
    process.zdcanalyzer #+
#    process.unpackedMuons +
#    process.muonAnalyzer
    )

#customisation
process.particleFlowAnalyser.ptMin = 0.0
process.ggHiNtuplizer.muonPtMin = 0.0

# Select the types of jets filled
matchJets = True             # Enables q/g and heavy flavor jet identification in MC
jetPtMin = 15
jetAbsEtaMax = 2.5

# Choose which additional information is added to jet trees
doHIJetID = True             # Fill jet ID and composition information branches
doWTARecluster = False        # Add jet phi and eta for WTA axis
doBtagging = False           # Note that setting to True increases computing time a lot

# 0 means use original mini-AOD jets, otherwise use R value, e.g., 3,4,8
# Generator level jets in original miniAOD jets contain neutrinos
# You will need to do reclustering with R-value to get generator level jets without neutrinos
# Add all the values you want to process to the list
# These will create collections of CS subtracted jets (only eta dependent background)
jetLabelsCS = ["4"]

# For this list, give the R-values for flow subtracted CS jets (eta and phi dependent background)
jetLabelsFlowCS = ["4"]

# Combine the two lists such that all selected jets can be easily looped over
# Also add "Flow" tag for the flow jets to distinguish them from non-flow jets
allJetLabels = jetLabelsCS + [flowR + "Flow" for flowR in jetLabelsFlowCS]

# add candidate tagging, copy/paste to add other jet radii
from HeavyIonsAnalysis.JetAnalysis.setupJets_PbPb_cff import candidateBtaggingMiniAOD

for jetLabel in allJetLabels:
    candidateBtaggingMiniAOD(process, isMC = True, jetPtMin = jetPtMin, jetCorrLevels = ['L2Relative', 'L3Absolute'], doBtagging = doBtagging, labelR = jetLabel)

    # setup jet analyzer
    setattr(process,"akCs"+jetLabel+"PFJetAnalyzer",process.akCs4PFJetAnalyzer.clone())
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetTag =  "selectedUpdatedPatJetsAK"+jetLabel+"PFBtag"
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetName = 'akCs'+jetLabel+'PF'
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").matchJets = matchJets
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").matchTag = 'patJetsAK'+jetLabel+'PFUnsubJets'
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").doHiJetID = doHIJetID
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").doWTARecluster = doWTARecluster
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetPtMin = jetPtMin
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetAbsEtaMax = cms.untracked.double(jetAbsEtaMax)
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").rParam = 0.4 if jetLabel=="0" else  float(jetLabel.replace("Flow",""))*0.1
    getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetFlavourInfos = "ak"+jetLabel+"PFUnsubJetFlavourInfos"
    if jetLabel != "0": getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").genjetTag = "ak"+jetLabel+"GenJetsReclusterNoNu"
    if doBtagging:
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").useNewBtaggers = True
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").pfJetProbabilityBJetTag = cms.untracked.string("pfJetProbabilityBJetTagsAK"+jetLabel+"PFBtag")
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").pfUnifiedParticleTransformerAK4JetTags = cms.untracked.string("pfUnifiedParticleTransformerAK4JetTagsAK"+jetLabel+"PFBtag")
    process.forest += getattr(process,"akCs"+jetLabel+"PFJetAnalyzer")


#########################
# Event Selection -> add the needed filters here
#########################

process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
process.load('HeavyIonsAnalysis.EventAnalysis.hffilter_cfi')
process.pphfCoincFilter2Th4 = cms.Path(process.phfCoincFilter2Th4)
process.pAna = cms.EndPath(process.skimanalysis)

