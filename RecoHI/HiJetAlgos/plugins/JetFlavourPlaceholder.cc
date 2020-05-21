// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/JetCollection.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourInfo.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourInfoMatching.h"

//
// constants, enums and typedefs
//

//
// class declaration
//

class JetFlavourPlaceholder : public edm::stream::EDProducer<> {
public:
  explicit JetFlavourPlaceholder(edm::ParameterSet const&);
  ~JetFlavourPlaceholder() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  // ----------member data ---------------------------
  const edm::EDGetTokenT<edm::View<reco::Jet>> jetsToken_;
};

//
// static data member definitions
//

//
// constructors and destructor
//
JetFlavourPlaceholder::JetFlavourPlaceholder(const edm::ParameterSet& iConfig)
    : jetsToken_(consumes<edm::View<reco::Jet>>(iConfig.getParameter<edm::InputTag>("jets"))) {
  // register your products
  produces<reco::JetFlavourInfoMatchingCollection>();
}

JetFlavourPlaceholder::~JetFlavourPlaceholder() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called to produce the data  ------------
void JetFlavourPlaceholder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Jet>> jets;
  iEvent.getByToken(jetsToken_, jets);

  auto jetFlavourInfos = std::make_unique<reco::JetFlavourInfoMatchingCollection>(reco::JetRefBaseProd(jets));

  for (size_t i = 0; i < jets->size(); ++i) {
    (*jetFlavourInfos)[jets->refAt(i)] = reco::JetFlavourInfo();
  }

  iEvent.put(std::move(jetFlavourInfos));
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void JetFlavourPlaceholder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetFlavourPlaceholder);
