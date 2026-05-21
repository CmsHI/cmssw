import FWCore.ParameterSet.Config as cms

# module
zdcEnergyFilterHC1nOr = cms.EDFilter(
    'HiZDCFilter',
    ZDCRecHitSource = cms.InputTag('zdcreco2023HardCode'),
    threshold4ltPlus = cms.double(1500), # threshold for less than for ZDC+
    threshold4gtPlus = cms.double(900), # threshold for greater than for ZDC+
    threshold4ltMinus = cms.double(1500), # threshold for less than for ZDC-
    threshold4gtMinus = cms.double(900), # threshold for greater than for ZDC-
    algorithm = cms.string('gt OR') # [lt/gt][AND/OR], XOR (not case-sensitive)
)
zdcEnergyFilterHC0nOr = zdcEnergyFilterHC1nOr.clone( algorithm = 'lt OR' )
zdcEnergyFilterHC0nAnd = zdcEnergyFilterHC1nOr.clone( algorithm = 'lt AND' )
zdcEnergyFilterHCXOr = zdcEnergyFilterHC1nOr.clone( algorithm = 'XOR' )

# path
pzdcEnergyFilterHC1nOr = cms.Path(zdcEnergyFilterHC1nOr)
pzdcEnergyFilterHC0nOr = cms.Path(zdcEnergyFilterHC0nOr)
pzdcEnergyFilterHC0nAnd = cms.Path(zdcEnergyFilterHC0nAnd)
pzdcEnergyFilterHCXOr = cms.Path(zdcEnergyFilterHCXOr)
