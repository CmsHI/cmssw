import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.ZDCAnalysis.zdcrecoRun3_cfi import *
from HeavyIonsAnalysis.ZDCAnalysis.ZDCRecHitAnalyzerHC_cfi import *

zdcSequencePbPb = cms.Sequence(zdcrecoRun3 + zdcanalyzer)
