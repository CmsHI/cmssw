// system include files
#include <memory>

// stl
#include <algorithm>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// ana
#include "HeavyIonsAnalysis/JetAnalysis/interface/HiPFCandCleaner.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "TMath.h"
#include "TStopwatch.h"

using namespace std;
using namespace edm;
using namespace reco;

//
// constructors and destructor
//
HiPFCandCleaner::HiPFCandCleaner(const edm::ParameterSet& iConfig)
{
  // Event source
  // Event Info
  pfCandidateLabel_ = iConfig.getParameter<edm::InputTag>("pfCandidateLabel");
  pfCandidatePF_ = consumes<reco::PFCandidateCollection> (pfCandidateLabel_);
  pfPtMin_ = iConfig.getParameter<double>("pfPtMin");
  pfAbsEtaMax_ = iConfig.getParameter<double>("pfAbsEtaMax");

  produces<reco::PFCandidateCollection>("particleFlowCleaned");
}


HiPFCandCleaner::~HiPFCandCleaner()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
HiPFCandCleaner::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<reco::PFCandidateCollection> pfCandidates;
  iEvent.getByToken(pfCandidatePF_,pfCandidates);
  const reco::PFCandidateCollection *pfCandidateColl = pfCandidates.product();

  //  reco::PFCandidateCollection* outCand = new reco::PFCandidateCollection();

  std::unique_ptr<reco::PFCandidateCollection> outCand(new reco::PFCandidateCollection());

  for(unsigned icand=0;icand<pfCandidateColl->size(); icand++) {
    const reco::PFCandidate pfCandidate = pfCandidateColl->at(icand);

    if(pfCandidate.pt() < pfPtMin_) continue;
    if(TMath::Abs(pfCandidate.eta()) > pfAbsEtaMax_) continue;
    if(pfCandidate.particleId() != 1) continue;

    outCand->push_back(pfCandidate);
  }

  iEvent.put(std::move(outCand), "particleFlowCleaned");
}

void HiPFCandCleaner::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
HiPFCandCleaner::endJob() {
}

DEFINE_FWK_MODULE(HiPFCandCleaner);
