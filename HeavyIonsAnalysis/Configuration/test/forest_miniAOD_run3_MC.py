### HiForest Configuration
# Input: miniAOD
# Type: mc

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_pp_on_PbPb_cff import Run3_pp_on_PbPb
process = cms.Process('HiForest', Run3_pp_on_PbPb)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 122X, mc")

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        '/store/user/mnguyen//Run3MC/QCDPhoton_pThat15_Run3_HydjetEmbedded/QCDPhoton_pThat15_Run3_HydjetEmbedded_mAOD/220217_171946/0000/step3_RAW2DIGI_L1Reco_RECO_EI_PAT_PU_113.root'
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


from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic_hi', '')
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
# making cuts looser so that we can actually check dNdEta
process.HiGenParticleAna.ptMin = cms.untracked.double(0.4) # default is 5
process.HiGenParticleAna.etaMax = cms.untracked.double(5.) # default is 2.5

# event analysis
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_mc_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_mc
process.hltobject.triggerNames = trigger_list_mc

# process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
################################
# electrons, photons, muons
SS2018PbPbMC = "HeavyIonsAnalysis/EGMAnalysis/data/SS2018PbPbMC.dat"
process.load('HeavyIonsAnalysis.EGMAnalysis.correctedElectronProducer_cfi')
process.correctedElectrons.correctionFile = SS2018PbPbMC

process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doGenParticles = cms.bool(True)
process.ggHiNtuplizer.doMuons = cms.bool(False)
process.ggHiNtuplizer.electronSrc = "correctedElectrons"
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
################################
# jet reco sequence
process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_mc_cff')
################################
# tracks
process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
#muons
#process.load("HeavyIonsAnalysis.MuonAnalysis.unpackedMuons_cfi")
#process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")
#process.muonAnalyzer.doGen = cms.bool(True)

###############################################################################



###############################################################################
# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo +
    process.hltanalysis +
    #process.hltobject +
    process.l1object +
    process.trackSequencePbPb +
    process.particleFlowAnalyser +
    process.hiEvtAnalyzer +
    process.HiGenParticleAna +
    process.correctedElectrons +
    process.akCs4PFJetAnalyzer +
    process.ggHiNtuplizer #+
    #process.unpackedMuons +
    #process.muonAnalyzer
    )

#customisation

addR3Jets = False
addR4Jets = False

if addR3Jets or addR4Jets :
    process.load("HeavyIonsAnalysis.JetAnalysis.extraJets_cff")
    from HeavyIonsAnalysis.JetAnalysis.clusterJetsFromMiniAOD_cff import setupHeavyIonJets

    if addR3Jets :
        process.jetsR3 = cms.Sequence()
        setupHeavyIonJets('akCs3PF', process.jetsR3, process, isMC = 1, radius = 0.30, JECTag = 'AK3PF')
        process.akCs3PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")
        process.akCs3PFJetAnalyzer = process.akCs4PFJetAnalyzer.clone(jetTag = "akCs3PFpatJets", jetName = 'akCs3PF', genjetTag = "ak3GenJetsNoNu")      
        process.forest += process.extraJetsMC * process.jetsR3 * process.akCs3PFJetAnalyzer

    if addR4Jets :
        # Recluster using an alias "0" in order not to get mixed up with the default AK4 collections
        process.jetsR4 = cms.Sequence()
        setupHeavyIonJets('akCs0PF', process.jetsR4, process, isMC = 1, radius = 0.40, JECTag = 'AK4PF')
        process.akCs0PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")
        process.akCs4PFJetAnalyzer.jetTag = 'akCs0PFpatJets'
        process.akCs4PFJetAnalyzer.jetName = 'akCs0PF'
        process.forest += process.extraJetsMC * process.jetsR4 * process.akCs4PFJetAnalyzer



addCandidateTagging = False

if addCandidateTagging:
    process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")

    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    updateJetCollection(
        process,
        jetSource = cms.InputTag('slimmedJets'),
        jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
        btagDiscriminators = ['pfCombinedSecondaryVertexV2BJetTags', 'pfDeepCSVDiscriminatorsJetTags:BvsAll', 'pfDeepCSVDiscriminatorsJetTags:CvsB', 'pfDeepCSVDiscriminatorsJetTags:CvsL'], ## to add discriminators,
        btagPrefix = 'TEST',
    )

    process.updatedPatJets.addJetCorrFactors = False
    process.updatedPatJets.discriminatorSources = cms.VInputTag(
        cms.InputTag('pfDeepCSVJetTags:probb'),
        cms.InputTag('pfDeepCSVJetTags:probc'),
        cms.InputTag('pfDeepCSVJetTags:probudsg'),
        cms.InputTag('pfDeepCSVJetTags:probbb'),
    )

    process.akCs4PFJetAnalyzer.jetTag = "updatedPatJets"

    process.forest.insert(1,process.candidateBtagging*process.updatedPatJets)


#########################
# Event Selection -> add the needed filters here
#########################

process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
process.pAna = cms.EndPath(process.skimanalysis)
