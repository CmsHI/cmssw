import FWCore.ParameterSet.Config as cms

hiFJRhoAnalyzer = cms.EDAnalyzer('HiFJRhoAnalyzer',
                                 etaMap             = cms.InputTag('hiFJRhoProducer','mapEtaEdges','HiForest'),
                                 rho                = cms.InputTag('hiFJRhoProducer','mapToRho'),
                                 rhom               = cms.InputTag('hiFJRhoProducer','mapToRhoM'),
                                 rhoCorr            = cms.InputTag('hiFJGridEmptyAreaCalculator','mapToRhoCorr'),
                                 rhomCorr           = cms.InputTag('hiFJGridEmptyAreaCalculator','mapToRhoMCorr'),
                                 corrWKtArea        = cms.InputTag('hiFJGridEmptyAreaCalculator','corrWKtArea'),
                                 rhoGrid            = cms.InputTag('hiFJGridEmptyAreaCalculator','mapRhoVsEtaGrid'),
                                 meanRhoGrid            = cms.InputTag('hiFJGridEmptyAreaCalculator','mapMeanRhoVsEtaGrid'),
)

