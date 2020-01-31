import FWCore.ParameterSet.Config as cms

# import calo jet producers
from HeavyIonsAnalysis.JetAnalysis.akCaloJets_cfi import (
    ak1CaloJets, ak2CaloJets, ak3CaloJets,
    ak4CaloJets, ak5CaloJets, ak6CaloJets)

# import particle flow jet producers
from HeavyIonsAnalysis.JetAnalysis.akPFJets_cfi import (
    ak1PFJets, ak2PFJets, ak3PFJets, ak4PFJets, ak5PFJets, ak6PFJets,
    akSoftDrop1PFJets, akSoftDrop2PFJets, akSoftDrop3PFJets,
    akSoftDrop4PFJets, akSoftDrop5PFJets, akSoftDrop6PFJets,
    akFilter1PFJets, akFilter2PFJets, akFilter3PFJets,
    akFilter4PFJets, akFilter5PFJets, akFilter6PFJets)
