import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.ZDCAnalysis.zdcreco2023_cfi import *
zdcrecoRun3.zdcDigiSrc = cms.InputTag('hcalDigis', 'ZDC')
zdcrecoRun3.calZDCDigi = False
zdcrecoRun3.skipRPD = True
from HeavyIonsAnalysis.ZDCAnalysis.ZDCRecHitAnalyzerHC_cfi import *
zdcanalyzer.ZDCRecHitSource = cms.InputTag('zdcrecoRun3')
zdcanalyzer.doZdcDigis = cms.bool(False)

zdcSequencePbPb = cms.Sequence(zdcrecoRun3 + zdcanalyzer)
