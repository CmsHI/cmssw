import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.JetAnalysis.jets.HiReRecoJets_pPb_cff import *

from HeavyIonsAnalysis.JetAnalysis.jets.ak4PFJetSequence_pPb_data_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak3PFJetSequence_pPb_data_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akPu4PFJetSequence_pPb_data_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.ak4CaloJetSequence_pPb_data_cff import *
from HeavyIonsAnalysis.JetAnalysis.jets.akPu4CaloJetSequence_pPb_data_cff import *

## put this back in if you need to rebuild the rho analyzer eta maps...
#from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
#from RecoHI.HiJetAlgos.hiFJRhoProducer import hiFJRhoProducer
#from RecoHI.HiJetAlgos.hiFJGridEmptyAreaCalculator_cff import hiFJGridEmptyAreaCalculator
#kt4PFJets.src = cms.InputTag('particleFlow')
#kt4PFJets.doAreaFastjet = True
#kt4PFJets.jetPtMin      = cms.double(0.0)
#kt4PFJets.GhostArea     = cms.double(0.005)
#kt2PFJets = kt4PFJets.clone(rParam       = cms.double(0.2))

ak4PFJetAnalyzer.doSubEvent = True
ak4CaloJetAnalyzer.doSubEvent = True

from HeavyIonsAnalysis.JetAnalysis.makePartons_cff import *
highPurityTracks = cms.EDFilter("TrackSelector",
                                src = cms.InputTag("generalTracks"),
                                cut = cms.string('quality("highPurity")')
)

#custom for 80X
PFTowers.src = cms.InputTag("particleFlow")

jetSequences = cms.Sequence(
    hiReRecoCaloJets +
    PFTowers +
    hiReRecoPFJets +
    highPurityTracks +
    ak3PFJetSequence +
    ak4PFJetSequence +
    akPu4PFJetSequence +
    ak4CaloJetSequence +
    akPu4CaloJetSequence  
    )
