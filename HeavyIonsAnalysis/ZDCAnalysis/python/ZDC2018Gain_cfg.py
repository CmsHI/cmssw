import FWCore.ParameterSet.Config as cms

# ZDC 2018 PbPb run, gain for Fill7427

gainFill7427 = cms.VPSet(
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM1'),
			calib = cms.untracked.double(0.1)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM2'),
			calib = cms.untracked.double(0.1)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM3'),
			calib = cms.untracked.double(0.07)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM4'),
			calib = cms.untracked.double(0.08)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM5'),
			calib = cms.untracked.double(0.06)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD1'),
			calib = cms.untracked.double(1.)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD2'),
			calib = cms.untracked.double(0.81)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD3'),
			calib = cms.untracked.double(0.67)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD4'),
			calib = cms.untracked.double(0.81)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM1'),
			calib = cms.untracked.double(0.1)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM2'),
			calib = cms.untracked.double(0.1)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM3'),
			calib = cms.untracked.double(0.1)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM4'),
			calib = cms.untracked.double(0.08)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM5'),
			calib = cms.untracked.double(0.06)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD1'),
			calib = cms.untracked.double(1.)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD2'),
			calib = cms.untracked.double(0.62)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD3'),
			calib = cms.untracked.double(0.67)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD4'),
			calib = cms.untracked.double(0.87)
		),
		cms.PSet(
			object = cms.untracked.string('Pscale'),
			calib = cms.untracked.double(4.25)
		),
		cms.PSet(
			object = cms.untracked.string('Mscale'),
			calib = cms.untracked.double(6.77)
		),
        )

gainFill7435 = cms.VPSet(
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM1'),
			calib = cms.untracked.double(0.11)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM2'),
			calib = cms.untracked.double(0.11)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM3'),
			calib = cms.untracked.double(0.08)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM4'),
			calib = cms.untracked.double(0.10)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM5'),
			calib = cms.untracked.double(0.06)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD1'),
			calib = cms.untracked.double(1.)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD2'),
			calib = cms.untracked.double(0.61)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD3'),
			calib = cms.untracked.double(0.46)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD4'),
			calib = cms.untracked.double(0.52)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM1'),
			calib = cms.untracked.double(0.12)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM2'),
			calib = cms.untracked.double(0.12)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM3'),
			calib = cms.untracked.double(0.08)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM4'),
			calib = cms.untracked.double(0.10)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM5'),
			calib = cms.untracked.double(0.11)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD1'),
			calib = cms.untracked.double(1.)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD2'),
			calib = cms.untracked.double(0.81)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD3'),
			calib = cms.untracked.double(0.46)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD4'),
			calib = cms.untracked.double(0.58)
		),
		cms.PSet(
			object = cms.untracked.string('Pscale'),
			calib = cms.untracked.double(2.67)
			#calib = cms.untracked.double(1.)
		),
		cms.PSet(
			object = cms.untracked.string('Mscale'),
			calib = cms.untracked.double(4.45)
			#calib = cms.untracked.double(1.)
		),
        )

gainPreset = cms.VPSet(
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM1'),
			calib = cms.untracked.double(0.11096590)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM2'),
			calib = cms.untracked.double(0.12292624)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM3'),
			calib = cms.untracked.double(0.093249696)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM4'),
			calib = cms.untracked.double(0.10451228)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_EM5'),
			calib = cms.untracked.double(0.10)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD1'),
			calib = cms.untracked.double(1.)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD2'),
			calib = cms.untracked.double(0.61)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD3'),
			calib = cms.untracked.double(0.46)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCP_HAD4'),
			calib = cms.untracked.double(0.50)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM1'),
			calib = cms.untracked.double(0.083302228)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM2'),
			calib = cms.untracked.double(0.085790654)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM3'),
			calib = cms.untracked.double(0.094278081)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM4'),
			calib = cms.untracked.double(0.092705166)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_EM5'),
			calib = cms.untracked.double(0.10)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD1'),
			calib = cms.untracked.double(1.)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD2'),
			calib = cms.untracked.double(0.72)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD3'),
			calib = cms.untracked.double(0.46)
		),
		cms.PSet(
			object = cms.untracked.string('hZDCM_HAD4'),
			calib = cms.untracked.double(0.58)
		),
		cms.PSet(
			object = cms.untracked.string('Pscale'),
			#calib = cms.untracked.double(2.67)
			calib = cms.untracked.double(1.)
		),
		cms.PSet(
			object = cms.untracked.string('Mscale'),
			#calib = cms.untracked.double(4.45)
			calib = cms.untracked.double(1.)
		),
        )
