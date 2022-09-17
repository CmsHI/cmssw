import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3
from Configuration.Eras.Modifier_ppRef_run3_cff import ppRef_run3
from Configuration.Eras.ModifierChain_trackingMkFitProd_cff import trackingMkFitProd
from Configuration.ProcessModifiers.trackingNoLoopers_cff import trackingNoLoopers

Run3_ppRef = cms.ModifierChain(Run3.copyAndExclude([trackingMkFitProd, trackingNoLoopers]), ppRef_run3)
