import FWCore.ParameterSet.Config as cms

# import and alias calo jet producers
from HeavyIonsAnalysis.JetAnalysis.akCaloJets_cfi import (
    ak1CaloJets, akPu1CaloJets,
    ak2CaloJets, akPu2CaloJets,
    ak3CaloJets, akPu3CaloJets,
    ak4CaloJets, akPu4CaloJets,
    ak5CaloJets, akPu5CaloJets,
    ak6CaloJets, akPu6CaloJets)

# import and alias particle flow jet producers
from HeavyIonsAnalysis.JetAnalysis.akPFJets_cfi import (
    ak1PFJets, akPu1PFJets, akCs1PFJets, akFlowPuCs1PFJets,
    ak2PFJets, akPu2PFJets, akCs2PFJets, akFlowPuCs2PFJets,
    ak3PFJets, akPu3PFJets, akCs3PFJets, akFlowPuCs3PFJets,
    ak4PFJets, akPu4PFJets, akCs4PFJets, akFlowPuCs4PFJets,
    ak5PFJets, akPu5PFJets, akCs5PFJets, akFlowPuCs5PFJets,
    ak6PFJets, akPu6PFJets, akCs6PFJets, akFlowPuCs6PFJets)
