import FWCore.ParameterSet.Config as cms

fscanalyzer = cms.EDAnalyzer(
   "FSCAnalyzerHC",
   ZDCDigiSource    = cms.InputTag('hcalDigis', 'ZDC'),
   doHardcodedFSC = cms.bool(True) # FSC only loaded into EMAP
)

