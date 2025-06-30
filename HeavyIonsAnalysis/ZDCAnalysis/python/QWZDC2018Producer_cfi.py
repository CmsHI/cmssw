import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.ZDCAnalysis.ZDC2018Pedestal_cfg import ZDC2018Pedestal_0


zdcdigi = cms.EDProducer('QWZDC2018Producer2',
		Src = cms.untracked.InputTag('hcalDigis', 'ZDC'),
		SOI = cms.untracked.int32(4),
		Pedestal = ZDC2018Pedestal_0,
		HardCode = cms.untracked.bool(True),
		Debug = cms.untracked.bool(False)
		)
