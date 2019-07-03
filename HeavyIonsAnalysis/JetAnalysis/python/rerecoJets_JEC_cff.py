import FWCore.ParameterSet.Config as cms

# import and alias calo jet producers
from HeavyIonsAnalysis.JetAnalysis.akCaloJets_cfi import (
    ak1CaloJECJets, ak2CaloJECJets, ak3CaloJECJets,
    ak4CaloJECJets, ak5CaloJECJets, ak6CaloJECJets)

ak1CaloJets = cms.EDAlias(ak1CaloJECJets = cms.VPSet(cms.PSet(type = cms.string('recoCaloJets'))))
ak2CaloJets = cms.EDAlias(ak2CaloJECJets = cms.VPSet(cms.PSet(type = cms.string('recoCaloJets'))))
ak3CaloJets = cms.EDAlias(ak3CaloJECJets = cms.VPSet(cms.PSet(type = cms.string('recoCaloJets'))))
ak4CaloJets = cms.EDAlias(ak4CaloJECJets = cms.VPSet(cms.PSet(type = cms.string('recoCaloJets'))))
ak5CaloJets = cms.EDAlias(ak5CaloJECJets = cms.VPSet(cms.PSet(type = cms.string('recoCaloJets'))))
ak6CaloJets = cms.EDAlias(ak6CaloJECJets = cms.VPSet(cms.PSet(type = cms.string('recoCaloJets'))))

# import and alias particle flow jet producers
from HeavyIonsAnalysis.JetAnalysis.akPFJets_cfi import (
    ak1PFJECJets, ak2PFJECJets, ak3PFJECJets,
    ak4PFJECJets, ak5PFJECJets, ak6PFJECJets)

ak1PFJets = cms.EDAlias(ak1PFJECJets = cms.VPSet(cms.PSet(type = cms.string('recoPFJets'))))
ak2PFJets = cms.EDAlias(ak2PFJECJets = cms.VPSet(cms.PSet(type = cms.string('recoPFJets'))))
ak3PFJets = cms.EDAlias(ak3PFJECJets = cms.VPSet(cms.PSet(type = cms.string('recoPFJets'))))
ak4PFJets = cms.EDAlias(ak4PFJECJets = cms.VPSet(cms.PSet(type = cms.string('recoPFJets'))))
ak5PFJets = cms.EDAlias(ak5PFJECJets = cms.VPSet(cms.PSet(type = cms.string('recoPFJets'))))
ak6PFJets = cms.EDAlias(ak6PFJECJets = cms.VPSet(cms.PSet(type = cms.string('recoPFJets'))))
