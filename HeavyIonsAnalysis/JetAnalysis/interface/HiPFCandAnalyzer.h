#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include <vector>
#include <cmath>

#include "TTree.h"

class TreePFCandEventData
{
  public:
    void SetTree(TTree * t) { tree_ = t; }
    void SetBranches(bool doJets, bool doMC, bool doCaloEnergy);
    void Clear();

    Int_t nPFpart_;
    std::vector<Int_t> pfId_;
    std::vector<Float_t> pfPt_;
    std::vector<Float_t> pfEnergy_;
    std::vector<Float_t> pfEta_;
    std::vector<Float_t> pfPhi_;
    std::vector<Float_t> pfM_;

    std::vector<Float_t> pfEcalE_;
    std::vector<Float_t> pfEcalEraw_;
    std::vector<Float_t> pfHcalE_;
    std::vector<Float_t> pfHcalEraw_;
    
    Int_t nGENpart_;
    std::vector<Int_t> genPDGId_;
    std::vector<Float_t> genPt_;
    std::vector<Float_t> genEta_;
    std::vector<Float_t> genPhi_;

    Int_t njets_;
    std::vector<Float_t> jetEnergy_;
    std::vector<Float_t> jetPt_;
    std::vector<Float_t> jetEta_;
    std::vector<Float_t> jetPhi_;

  private:
    TTree* tree_;
};

class HiPFCandAnalyzer : public edm::EDAnalyzer {
  public:
    explicit HiPFCandAnalyzer(const edm::ParameterSet&);
    ~HiPFCandAnalyzer();

  private:
    virtual void beginJob() ;
    virtual void analyze(const edm::Event&, const edm::EventSetup&);
    virtual void endJob() ;

    // ----------member data ---------------------------
    edm::Service<TFileService> fs;

    // Event Info
    edm::EDGetTokenT<reco::PFCandidateCollection> pfCandidatePF_;
    edm::EDGetTokenT<reco::GenParticleCollection> genLabel_;
    edm::EDGetTokenT<pat::JetCollection> jetLabel_;

    TreePFCandEventData pfEvt_;
    TTree *pfTree_;

    // cuts
    Double_t pfPtMin_;
    Double_t pfAbsEtaMax_;
    Double_t jetPtMin_;
    Double_t genPtMin_;

    bool doJets_;
    bool doMC_;
    bool doCaloEnergy_;
    bool skipCharged_;
};
