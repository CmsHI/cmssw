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
    void SetBranches(bool doJets, bool doMC, bool doCaloEnergy, bool doTrackMatching, bool doTrackMVA, bool doTrackVtx);
    void Clear(bool doJets, bool doMC, bool doCaloEnergy, bool doTrackMatching, bool doTrackMVA, bool doTrackVtx);

    Int_t nPFpart_;
    std::vector<unsigned long> pfKey_;   // key for this PF cand, ref https://github.com/cms-sw/cmssw/blob/master/DataFormats/Common/interface/Ptr.h#L163
    std::vector<Int_t> pfId_;
    std::vector<Float_t> pfPt_;
    std::vector<Float_t> pfEnergy_;
    std::vector<Float_t> pfEta_;
    std::vector<Float_t> pfPhi_;
    std::vector<Float_t> pfM_;

    std::vector<Float_t> pfvx_;
    std::vector<Float_t> pfvy_;
    std::vector<Float_t> pfvz_;

    std::vector<Float_t> pfEcalE_;
    std::vector<Float_t> pfEcalEraw_;
    std::vector<Float_t> pfHcalE_;
    std::vector<Float_t> pfHcalEraw_;

    std::vector<unsigned long> trkKey_;
    std::vector<Float_t> trkPt_;
    std::vector<Float_t> trkEta_;
    std::vector<Float_t> trkPhi_;
    std::vector<unsigned char> trkAlgo_;
    std::vector<Float_t> trkPtError_;
    std::vector<unsigned char> trkNHit_;
    std::vector<Float_t> trkChi2_;
    std::vector<unsigned char> trkNdof_;
    std::vector<unsigned char> trkNlayer_;
    std::vector<bool> highPurity_;

    std::vector<Float_t> trkMVA_;

    std::vector<Float_t> trkDz1_;
    std::vector<Float_t> trkDzError1_;
    std::vector<Float_t> trkDxy1_;
    std::vector<Float_t> trkDxyError1_;
    
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
    edm::EDGetTokenT<reco::TrackCollection> trkLabel_;
    edm::EDGetTokenT<std::vector<float>> mvaSrc_;
    edm::EDGetTokenT<std::vector<reco::Vertex>> vtxCollection_;

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
    bool doTrackMatching_;
    bool doTrackMVA_;  // effective only if track matching flag is enabled
    bool doTrackVtx_;  // effective only if track matching flag is enabled
};
