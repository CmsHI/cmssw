// -*- C++ -*-
//
// Package:    HiSignalParticleProducer
// Class:      HiSignalParticleProducer
//
/**\class HiSignalParticleProducer HiSignalParticleProducer.cc yetkin/HiSignalParticleProducer/src/HiSignalParticleProducer.cc
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
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

//
// class decleration
//

class HiSignalParticleProducer : public edm::EDProducer {
public:
  explicit HiSignalParticleProducer(const edm::ParameterSet&);
  ~HiSignalParticleProducer() override;

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  // ----------member data ---------------------------

  edm::EDGetTokenT<edm::View<reco::GenParticle> > genParticleSrc_;
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

HiSignalParticleProducer::HiSignalParticleProducer(const edm::ParameterSet& iConfig)
    : genParticleSrc_(consumes<edm::View<reco::GenParticle> >(iConfig.getParameter<edm::InputTag>("src"))) {
  std::string alias = (iConfig.getParameter<edm::InputTag>("src")).label();
  produces<reco::GenParticleCollection>().setBranchAlias(alias);
}

HiSignalParticleProducer::~HiSignalParticleProducer() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called to produce the data  ------------

void HiSignalParticleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto signalGenParticles = std::make_unique<reco::GenParticleCollection>();

  edm::Handle<edm::View<reco::GenParticle> > genParticles;
  iEvent.getByToken(genParticleSrc_, genParticles);

  for (auto const& genParticle : *genParticles) {
    if (genParticle.collisionId() == 0)
      signalGenParticles->push_back(genParticle);
  }

  iEvent.put(std::move(signalGenParticles));
}

DEFINE_FWK_MODULE(HiSignalParticleProducer);
