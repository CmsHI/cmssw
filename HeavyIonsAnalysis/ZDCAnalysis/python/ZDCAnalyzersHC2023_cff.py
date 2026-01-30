import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.ZDCAnalysis.zdcreco2023_cfi import *
zdcreco2023HardCode.calZDCDigi = False
# zdcreco2023HardCode.skipRPD = True
from HeavyIonsAnalysis.ZDCAnalysis.zdcanalyzer_cfi import *
zdcanalyzer.zdcRecHitSrc = cms.InputTag('zdcreco2023HardCode')
zdcanalyzer.nZdcTs = cms.int32(6)
zdcanalyzer.doZDCDigi = True
zdcanalyzer.doZDCRecHit = True
zdcanalyzer.calZDCDigi = False
zdcanalyzer.skipRPD = True

zdcSequence = cms.Sequence(zdcreco2023HardCode + zdcanalyzer)
