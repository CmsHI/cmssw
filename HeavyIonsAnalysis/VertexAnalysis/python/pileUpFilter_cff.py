import FWCore.ParameterSet.Config as cms

import HeavyIonsAnalysis.VertexAnalysis.pileUpFilter_cfi as puFilter

pileUpFilter_default = puFilter.pileupVertexFilter.clone() 

### define your own filter ###

pileUpFilter_pp5TeV_vtx1 = pileUpFilter_default.clone(
                                                           dzCutByNtrk = cms.vdouble(
                                                                                     999.,0.0,0.0,0.0,0.0
                                                                                    ),
                                                           dzTolerance = cms.double(9999.0)
                                                )    


pileUpFilter_pp5TeV_Gplus = pileUpFilter_default.clone(
                                                           dzCutByNtrk = cms.vdouble(
                                                                                    999.,999.,4.0,1.5,1.0,
                                                                                     0.6, 0.5,0.4,0.3,0.3,
                                                                                     0.3, 0.2,0.2,0.2,0.1,
                                                                                     0.1, 0.1,0.1,0.1,0.1,
                                                                                     0.1, 0.1,0.1,0.0
                                                                                    )
                                                       )
# OLVfilter stands for overlapping vertex filter
olvFilter_pp5TeV_dz1p0 = pileUpFilter_default.clone(
                                                           dzCutByNtrk = cms.vdouble(
                                                                                    999.,999.,4.0,1.5,1.0,
                                                                                     0.6, 0.5,0.4,0.3,0.3,
                                                                                     0.3, 0.2,0.2,0.2,0.1,
                                                                                     0.1, 0.1,0.1,0.1,0.1,
                                                                                     0.1, 0.1,0.1,0.0
                                                                                    ),
                                                           dzTolerance = cms.double(1.0)
                                              )  

                          
pileUpFilter_pPb8TeV_vtx1 = pileUpFilter_default.clone(
                                                           dzCutByNtrk = cms.vdouble(
                                                                                     999.,0.0,0.0,0.0,0.0
                                                                                    ),
                                                           dzTolerance = cms.double(9999.0)
                                                )    


pileUpFilter_pPb8TeV_Gplus = pileUpFilter_default.clone(
                                                           dzCutByNtrk = cms.vdouble(
                                                                                    999.,999.,999.,999.,999.0,
                                                                                     4.0, 1.5,1.0,0.8,0.6,
                                                                                     0.5, 0.4,0.3,0.2,0.2,
                                                                                     0.2, 0.2,0.1,0.1,0.1,
                                                                                     0.0, 0.0,0.0,0.0
                                                                                    )
                                                       )
# OLVfilter stands for overlapping vertex filter
olvFilter_pPb8TeV_dz1p0 = pileUpFilter_default.clone(
                                                           dzCutByNtrk = cms.vdouble(
                                                                                    999.,999.,999.,999.,999.0,
                                                                                     4.0, 1.5,1.0,0.8,0.6,
                                                                                     0.5, 0.4,0.3,0.2,0.2,
                                                                                     0.2, 0.2,0.1,0.1,0.1,
                                                                                     0.0, 0.0,0.0,0.0
                                                                                    ),
                                                           dzTolerance = cms.double(1.0)
                                              )         



