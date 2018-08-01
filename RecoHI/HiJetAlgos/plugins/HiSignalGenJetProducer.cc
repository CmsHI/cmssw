// -*- C++ -*-
//
// Package:    HiSignalGenJetProducer
// Class:      HiSignalGenJetProducer
//
/**\class HiSignalGenJetProducer HiSignalGenJetProducer.cc yetkin/HiSignalGenJetProducer/src/HiSignalGenJetProducer.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Yetkin Yilmaz
//         Created:  Tue Jul 21 04:26:01 EDT 2009
//
//

// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

//
// class decleration
//

class HiSignalGenJetProducer : public edm::EDProducer {
public:
  explicit HiSignalGenJetProducer(const edm::ParameterSet&);
  ~HiSignalGenJetProducer() override;

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  // ----------member data ---------------------------

  edm::EDGetTokenT<edm::View<reco::GenJet>> jetSrc_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//

HiSignalGenJetProducer::HiSignalGenJetProducer(const edm::ParameterSet& iConfig)
    : jetSrc_(consumes<edm::View<reco::GenJet> >(iConfig.getParameter<edm::InputTag>("src"))) {
  std::string alias = (iConfig.getParameter<edm::InputTag>("src")).label();
  produces<reco::GenJetCollection>().setBranchAlias(alias);
}

HiSignalGenJetProducer::~HiSignalGenJetProducer() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called to produce the data  ------------

void HiSignalGenJetProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto jets = std::make_unique<reco::GenJetCollection>();

  edm::Handle<edm::View<reco::GenJet>> genjets;
  iEvent.getByToken(jetSrc_, genjets);

  for (auto const& jet : *genjets) {
    const reco::GenParticle* gencon = jet.getGenConstituent(0);

    if (gencon == nullptr)
      throw cms::Exception("GenConstituent", "GenJet is missing its constituents");
    else if (gencon->collisionId() == 0)
      jets->push_back(jet);
  }

  iEvent.put(std::move(jets));
}

DEFINE_FWK_MODULE(HiSignalGenJetProducer);
