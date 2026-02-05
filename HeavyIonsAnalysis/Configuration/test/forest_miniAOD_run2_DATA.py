### HiForest Configuration
# Input: miniAOD
# Type: data

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run2_2018_pp_on_AA_cff import Run2_2018_pp_on_AA
from Configuration.ProcessModifiers.run2_miniAOD_pp_on_AA_103X_cff import run2_miniAOD_pp_on_AA_103X
process = cms.Process('HiForest', Run2_2018_pp_on_AA,run2_miniAOD_pp_on_AA_103X)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 125X, data")

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        "root://xrootd-cms.infn.it//store/hidata/HIRun2018A/HIHardProbes/MINIAOD/PbPb18_MiniAODv1-v1/240000/c83bc22b-3863-441b-8910-991b300c2fe8.root"
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
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data_promptlike_hi', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

# This is the default centrality tag built-in in the miniAOD forest.
# The tag is given here for reference. Changing it has no effect on your analysis.
centralityTag = "CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run2v1033p1x01_offline"
process.HiForestInfo.info.append(centralityTag)

print('\n')
print('\033[31m~*~ CENTRALITY TABLE FOR 2018 PBPB DATA ~*~\033[0m')
print('\033[36m~*~ TAG: ' + centralityTag + ' ~*~\033[0m')
print('\n')
process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")

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

# event analysis
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_data
process.hltobject.triggerNames = trigger_list_data

process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
################################
# electrons, photons, muons
SSHIRun2018A = "HeavyIonsAnalysis/EGMAnalysis/data/SSHIRun2018A.dat"
process.load('HeavyIonsAnalysis.EGMAnalysis.correctedElectronProducer_cfi')
process.correctedElectrons.correctionFile = SSHIRun2018A

#process.load('HeavyIonsAnalysis.MuonAnalysis.unpackedMuons_cfi')
#process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doMuons = cms.bool(False)
process.ggHiNtuplizer.electronSrc = "correctedElectrons"
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
################################
# jet reco sequence
process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_data_cff')
################################
# tracks
process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
###############################################################################

# ZDC RecHit Producer
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018Producer_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018RecHit_cfi')

process.load('HeavyIonsAnalysis.ZDCAnalysis.zdcanalyzer_cfi')
process.zdcanalyzer.doZDCRecHit = True
process.zdcanalyzer.doZDCDigi = False
process.zdcanalyzer.zdcRecHitSrc = cms.InputTag("QWzdcreco")
process.zdcanalyzer.calZDCDigi = True
################################


###############################################################################
# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo +
    process.hiEvtAnalyzer +
    process.hltanalysis +
    #process.hltobject +
    #process.l1object +
    process.trackSequencePbPb +
    process.particleFlowAnalyser +
    process.correctedElectrons +
    process.ggHiNtuplizer +
    process.zdcdigi +
    process.QWzdcreco +
    process.zdcanalyzer #+
    #process.unpackedMuons +
    #process.muonAnalyzer
    )

#customisation

addR3Jets = False
addR3FlowJets = False
addR4Jets = True
addR4FlowJets = True

# Configuration for jet flow subtraction
iterativeFlow = True         # Iterative jetty region exclusion. Default = True
pfCandidateEtaCut = 2        # Eta range for PF candidates used in flow fit. Default = 2
minPfCandidatesPerEvent = 60 # Minimum number of PF candidates to make the flow fit. Default = 60
minPfCandidatePt = 0.3       # Minimum pT for PF candidates in flow fit. Default = 0.3
maxPfCandidatePt = 3         # Maximum pT for PF candidates in flow fit. Default = 3
minFitQuality = 0            # Minimum flow fit quality score. Default = 0
maxFitQuality = 1            # Maximum flow fit quality score. Default = 1
firstFittedVn = 2            # First fitted vn component. Default = 2
lastFittedVn = 3             # Last fitted vn component. Default = 3

# this is only for non-reclustered jets
addCandidateTagging = False


if addR3Jets or addR3FlowJets or addR4Jets or addR4FlowJets :
    process.load("HeavyIonsAnalysis.JetAnalysis.extraJets_cff")
    from HeavyIonsAnalysis.JetAnalysis.clusterJetsFromMiniAOD_cff import setupHeavyIonJets
    process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")

    if addR3Jets :
        process.jetsR3 = cms.Sequence()
        setupHeavyIonJets('akCs3PF', process.jetsR3, process, isMC = 0, radius = 0.30, JECTag = 'AK3PF', doFlow = False)
        process.akCs3PFpatJetCorrFactors.levels = ['L2Relative', 'L2L3Residual']
        process.akCs3PFJetAnalyzer = process.akCs4PFJetAnalyzer.clone(jetTag = "akCs3PFpatJets", jetName = 'akCs3PF')
        process.forest += process.extraJetsData * process.jetsR3 * process.akCs3PFJetAnalyzer

    if addR3FlowJets :
        process.jetsR3flow = cms.Sequence()
        setupHeavyIonJets('akCs3PFFlow', process.jetsR3flow, process, isMC = 0, radius = 0.30, JECTag = 'AK3PF', doFlow = True)
        process.akCs3PFFlowpatJetCorrFactors.levels = ['L2Relative', 'L2L3Residual']
        process.akFlowPuCs3PFJetAnalyzer = process.akCs4PFJetAnalyzer.clone(jetTag = "akCs3PFFlowpatJets", jetName = 'akCs3PFFlow')
        process.forest += process.extraFlowJetsData * process.jetsR3flow * process.akFlowPuCs3PFJetAnalyzer 

    if addR4Jets :
        # Recluster using an alias "0" in order not to get mixed up with the default AK4 collections
        process.jetsR4 = cms.Sequence()
        setupHeavyIonJets('akCs0PF', process.jetsR4, process, isMC = 0, radius = 0.40, JECTag = 'AK4PF', doFlow = False)
        process.akCs0PFpatJetCorrFactors.levels = ['L2Relative', 'L2L3Residual']
        process.akCs4PFJetAnalyzer.jetTag = 'akCs0PFpatJets'
        process.akCs4PFJetAnalyzer.jetName = 'akCs0PF'
        process.forest += process.extraJetsData * process.jetsR4 * process.akCs4PFJetAnalyzer
 
    if addR4FlowJets :
        process.jetsR4flow = cms.Sequence()
        setupHeavyIonJets('akCs4PFFlow', process.jetsR4flow, process, isMC = 0, radius = 0.40, JECTag = 'AK4PF', doFlow = True)
        process.akCs4PFFlowpatJetCorrFactors.levels = ['L2Relative', 'L2L3Residual']
        process.akFlowPuCs4PFJetAnalyzer.jetTag = 'akCs4PFFlowpatJets'
        process.akFlowPuCs4PFJetAnalyzer.jetName = 'akCs4PFFlow'
        process.akFlowPuCs4PFJetAnalyzer.doHiJetID = True
        process.akFlowPuCs4PFJetAnalyzer.doWTARecluster = True

        #############################################
        # Configuration for flow modulation details #
        #############################################

        # Exclude jetty regions iteratively
        process.hiFJRhoFlowModulation.doJettyExclusion = False
        if iterativeFlow:
            process.hiFJRhoFlowModulation.doJettyExclusion = True

        # Particle flow candidates to be included in the fit
        process.hiFJRhoFlowModulation.minPfCandidatesPerEvent = minPfCandidatesPerEvent
        process.hiFJRhoFlowModulation.pfCandidateEtaCut = pfCandidateEtaCut
        process.hiFJRhoFlowModulation.pfCandidateMinPtCut = minPfCandidatePt
        process.hiFJRhoFlowModulation.pfCandidateMaxPtCut = maxPfCandidatePt

        # Range of flow components extracted from the fit
        process.hiFJRhoFlowModulation.firstFittedVn = firstFittedVn
        process.hiFJRhoFlowModulation.lastFittedVn = lastFittedVn

        # Reliability parameters for the fit to be applied
        process.akCs4PFFlowJets.minFlowChi2Prob = minFitQuality;
        process.akCs4PFFlowJets.maxFlowChi2Prob = maxFitQuality;

        # Set the parameters for the first iteration in case of iterative jetty region exclusion
        if iterativeFlow:

            # Flow modulation configuration for the first iteration

            # Particle flow candidates to be included in the fit
            process.hiFJRhoFlowModulationIteration.minPfCandidatesPerEvent = minPfCandidatesPerEvent
            process.hiFJRhoFlowModulationIteration.pfCandidateEtaCut = pfCandidateEtaCut
            process.hiFJRhoFlowModulationIteration.pfCandidateMinPtCut = minPfCandidatePt
            process.hiFJRhoFlowModulationIteration.pfCandidateMaxPtCut = maxPfCandidatePt
            process.hiFJRhoFlowModulationIteration.firstFittedVn = firstFittedVn  # First flow component included in the fit
            process.hiFJRhoFlowModulationIteration.lastFittedVn = lastFittedVn  # Last flow component included in the fit

            # Configure CS subtracted jets for jetty region subtraction
            process.akCs4PFJetsForFlow.src = "packedPFCandidates" # Packed candidates as a source for jets for flow subtraction in second iteration
            process.akCs4PFJetsForFlow.jetPtMin = 40 # Minimum jet pT to exclude area around it in second iteration
            process.akCs4PFJetsForFlow.minFlowChi2Prob = minFitQuality
            process.akCs4PFJetsForFlow.maxFlowChi2Prob = maxFitQuality
            process.akCs4PFJetsForFlow.rhoFlowFitParams = cms.InputTag('hiFJRhoFlowModulationIteration', 'rhoFlowFitParams') # Minimum jet pT to exclude area around it in second iteration

            # Configure the second iteration of the flow modulation to use CS subtracted jets as the jet collection
            process.hiFJRhoFlowModulation.jetTag = "akCs4PFJetsForFlow"

            # Updated process for iterative jetty region determination for flow modulation
            process.forest += process.extraIterativeFlowJetsData * process.jetsR4flow * process.akFlowPuCs4PFJetAnalyzer

        else:
            process.forest += process.extraFlowJetsData * process.jetsR4flow * process.akFlowPuCs4PFJetAnalyzer


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
process.load('HeavyIonsAnalysis.EventAnalysis.hffilter_cfi')
process.pphfCoincFilter2Th4 = cms.Path(process.phfCoincFilter2Th4)
process.pAna = cms.EndPath(process.skimanalysis)
