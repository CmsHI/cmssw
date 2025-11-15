import FWCore.ParameterSet.Config as cms

fscanalyzer = cms.EDAnalyzer(
   "FSCAnalyzerHC",
   ZDCDigiSource    = cms.InputTag('hcalDigis', 'ZDC'),
   do50nsRecoFSC = cms.bool(True), # reconstruction used for 50ns bunch spacing
   doHardcodedFSC = cms.bool(True) # FSC only loaded into EMAP
)

