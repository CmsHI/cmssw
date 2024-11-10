// system include files
#include <memory>
#include <vector>
#include <map>
#include <set>

// user include files
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

class HiHFFilterPF : public edm::one::EDFilter<> {
public:
  explicit HiHFFilterPF(const edm::ParameterSet&);
  ~HiHFFilterPF() override;

private:
  void beginJob() override;
  bool filter(edm::Event&, const edm::EventSetup&) override;

  // edm::EDGetTokenT<reco::HFFilterInfo> HFfilters_;
  edm::EDGetTokenT<pat::PackedCandidateCollection> pfCandidateTag_;
  double threshold_;
  int minnumtowers_;
  int numMinHFTowersP, numMinHFTowersM;

  reco::PFCandidate converter_;
};

using namespace edm;
using namespace std;

HiHFFilterPF::HiHFFilterPF(const edm::ParameterSet& iConfig) :
  pfCandidateTag_(consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("pfCandidateSrc"))),
  threshold_(iConfig.getParameter<double>("threshold")),
  minnumtowers_(iConfig.getParameter<int>("minnumtowers")) { }

HiHFFilterPF::~HiHFFilterPF() {}

bool HiHFFilterPF::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  bool accepted = false;

  numMinHFTowersP = 0;
  numMinHFTowersM = 0;

  edm::Handle<pat::PackedCandidateCollection> pfCandidates;
  iEvent.getByToken(pfCandidateTag_, pfCandidates);

  for (const auto& pfcand : *pfCandidates) {

    /* dummy reco::PFCandidate used to convert pdgId */
    auto id = converter_.translatePdgIdToType(pfcand.pdgId());
    if (!(id == 6 || id == 7)) continue;
        
    // float pt = pfcand.pt();
    float eta = pfcand.eta();
    if (std::abs(eta) > 6 || std::abs(eta) < 3) {
      continue;
    }

    if (pfcand.energy() >= threshold_) {
      if (eta > 0) { numMinHFTowersP++; }
      else { numMinHFTowersM++; }
    }
    
  } // for (const auto& pfcand : *pfCandidates)
  if (std::min(numMinHFTowersP, numMinHFTowersM) >= minnumtowers_)
    accepted = true;

  return accepted;
}

void HiHFFilterPF::beginJob() {
  converter_ = reco::PFCandidate();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HiHFFilterPF);
