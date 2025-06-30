import FWCore.ParameterSet.Config as cms

phfCoincFilter2Th4  = cms.EDFilter('HiHFFilter',
   HFfilters      = cms.InputTag("hiHFfilters","hiHFfilters"),
   threshold      = cms.int32(4),
   minnumtowers  = cms.int32(2)
)

phfCoincFilter1Th4 = phfCoincFilter2Th4.clone(minnumtowers = 1)
phfCoincFilter3Th4 = phfCoincFilter2Th4.clone(minnumtowers = 3)
phfCoincFilter4Th4 = phfCoincFilter2Th4.clone(minnumtowers = 4)
phfCoincFilter5Th4 = phfCoincFilter2Th4.clone(minnumtowers = 5)

phfCoincFilter1Th3 = phfCoincFilter2Th4.clone(threshold = 3, minnumtowers = 1)
phfCoincFilter2Th3 = phfCoincFilter2Th4.clone(threshold = 3, minnumtowers = 2)
phfCoincFilter3Th3 = phfCoincFilter2Th4.clone(threshold = 3, minnumtowers = 3)
phfCoincFilter4Th3 = phfCoincFilter2Th4.clone(threshold = 3, minnumtowers = 4)
phfCoincFilter5Th3 = phfCoincFilter2Th4.clone(threshold = 3, minnumtowers = 5)

phfCoincFilter1Th5 = phfCoincFilter2Th4.clone(threshold = 5, minnumtowers = 1)
phfCoincFilter2Th5 = phfCoincFilter2Th4.clone(threshold = 5, minnumtowers = 2)
phfCoincFilter3Th5 = phfCoincFilter2Th4.clone(threshold = 5, minnumtowers = 3)
phfCoincFilter4Th5 = phfCoincFilter2Th4.clone(threshold = 5, minnumtowers = 4)
phfCoincFilter5Th5 = phfCoincFilter2Th4.clone(threshold = 5, minnumtowers = 5)

phfCoincFilter1Th6 = phfCoincFilter2Th4.clone(threshold = 6, minnumtowers = 1)
phfCoincFilter2Th6 = phfCoincFilter2Th4.clone(threshold = 6, minnumtowers = 2)
phfCoincFilter3Th6 = phfCoincFilter2Th4.clone(threshold = 6, minnumtowers = 3)
phfCoincFilter4Th6 = phfCoincFilter2Th4.clone(threshold = 6, minnumtowers = 4)
phfCoincFilter5Th6 = phfCoincFilter2Th4.clone(threshold = 6, minnumtowers = 5)

phfCoincFilter4Th2 = phfCoincFilter2Th4.clone(threshold = 2, minnumtowers = 4)

