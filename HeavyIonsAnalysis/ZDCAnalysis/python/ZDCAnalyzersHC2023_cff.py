import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.ZDCAnalysis.zdcreco2023_cfi import *
zdcreco2023HardCode.zdcDigiSrc = cms.InputTag('hcalDigis', 'ZDC')
zdcreco2023HardCode.calZDCDigi = False
zdcreco2023HardCode.skipRPD = True
from HeavyIonsAnalysis.ZDCAnalysis.ZDCRecHitAnalyzerHC_cfi import *
zdcanalyzer.ZDCRecHitSource = cms.InputTag('zdcreco2023HardCode')
zdcanalyzer.doZdcDigis = cms.bool(False)

zdcSequencePbPb = cms.Sequence(zdcreco2023HardCode + zdcanalyzer)
