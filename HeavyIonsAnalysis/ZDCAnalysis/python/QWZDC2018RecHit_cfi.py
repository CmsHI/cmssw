import FWCore.ParameterSet.Config as cms

#from ZDC2018Gain_cfg import gainPreset
from HeavyIonsAnalysis.ZDCAnalysis.ZDC2018Gain_cfg import gainFill7435

QWzdcreco = cms.EDProducer('QWZDC2018RecHit',
        srcDetId = cms.untracked.InputTag("zdcdigi", "DetId"),
        srcfC = cms.untracked.InputTag("zdcdigi", "regularfC"),
#        ZDCCalib = gainPreset
		  ZDCCalib = gainFill7435
        )

