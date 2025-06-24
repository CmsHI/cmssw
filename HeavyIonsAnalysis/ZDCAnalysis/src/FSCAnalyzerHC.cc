// -*- C++ -*-
//
// Package:    HeavyIonAnalyzer/ZDCAnalysis/FSCAnalyzerHC
// Class:      FSCAnalyzerHC
//
/**\class FSCAnalyzerHC FSCAnalyzerHC.cc HeavyIonAnalyzer/ZDCAnalysis/plugins/FSCAnalyzerHC

   Description: Produced Tree with ZDC RecHit and zdcdigi information 
*/
//
// Original Author:  Matthew Nickel, University of Kansas
//         Created:  23-06-2025
//         Modified from ZDCRecHitAnalyzerHC
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/METReco/interface/HcalCaloFlagLabels.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TTree.h"

#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"

#include "ZDCstruct.h"
#include "ZDCHardCodeHelper.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.

using reco::TrackCollection;

class FSCAnalyzerHC : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit FSCAnalyzerHC(const edm::ParameterSet&);
  ~FSCAnalyzerHC();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  // ----------member data ---------------------------
  const edm::EDGetTokenT<QIE10DigiCollection> ZDCDigiToken_;
  edm::ESGetToken<HcalDbService, HcalDbRecord> hcalDatabaseToken_;
  bool doHardcodedFSC_;
  edm::Service<TFileService> fs;
  TTree* t1;

  MyZDCDigi zdcDigi;

#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  edm::ESGetToken<SetupData, SetupRecord> setupToken_;
#endif
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
FSCAnalyzerHC::FSCAnalyzerHC(const edm::ParameterSet& iConfig)
    : ZDCDigiToken_(consumes<QIE10DigiCollection>(iConfig.getParameter<edm::InputTag>("ZDCDigiSource"))),
      hcalDatabaseToken_(esConsumes<HcalDbService, HcalDbRecord>()),
      doHardcodedFSC_(iConfig.getParameter<bool>("doHardcodedFSC")) {
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  setupDataToken_ = esConsumes<SetupData, SetupRecord>();
#endif
  //now do what ever initialization is needed
}

FSCAnalyzerHC::~FSCAnalyzerHC() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
  //
  // please remove this method altogether if it would be left empty
}

//
// member functions
//

// ------------ method called for each event  ------------
void FSCAnalyzerHC::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;
  using namespace std;
  ZDCHardCodeHelper HardCodeZDC;
  edm::Handle<QIE10DigiCollection> zdcdigis;

  iEvent.getByToken(ZDCDigiToken_, zdcdigis);

  edm::ESHandle<HcalDbService> conditions = iSetup.getHandle(hcalDatabaseToken_);

  zdcDigi.n = 0;
  for (unsigned int i = 0; i < NMOD; i++) {
    zdcDigi.zside[i] = -99;
    zdcDigi.section[i] = -99;
    zdcDigi.channel[i] = -99;
    for (int ts = 0; ts < NTS; ts++) {
      zdcDigi.chargefC[ts][i] = -99;
      zdcDigi.adc[ts][i] = -99;
      zdcDigi.tdc[ts][i] = -99;
    }
  }

  int nhits = 0;
  for (auto it = zdcdigis->begin(); it != zdcdigis->end(); it++) {
    const QIE10DataFrame digi = static_cast<const QIE10DataFrame>(*it);

    HcalZDCDetId zdcid = digi.id();
    int zside = zdcid.zside();
    int section = zdcid.section();
    int channel = zdcid.channel();

    if (nhits >= NMOD)
      break;
    if (!(section == 1 && channel > 5))
      continue;  // Only consider FSC channel located in dummy ECAL

    CaloSamples caldigi;

    //const ZDCDataFrame & rh = (*zdcdigis)[it];

    if (!(doHardcodedFSC_)) {
      const HcalQIECoder* qiecoder = conditions->getHcalCoder(zdcid);
      const HcalQIEShape* qieshape = conditions->getHcalShape(qiecoder);
      HcalCoderDb coder(*qiecoder, *qieshape);
      // coder.adc2fC(rh,caldigi);
      coder.adc2fC(digi, caldigi);
    }

    zdcDigi.zside[nhits] = zside;
    zdcDigi.section[nhits] = section;
    zdcDigi.channel[nhits] = channel;

    for (int ts = 0; ts < digi.samples(); ts++) {
      zdcDigi.adc[ts][nhits] = digi[ts].adc();
      zdcDigi.tdc[ts][nhits] = digi[ts].le_tdc();
      if (doHardcodedFSC_) {
        zdcDigi.chargefC[ts][nhits] = HardCodeZDC.charge(digi[ts].adc(), digi[ts].capid());
      } else {
        zdcDigi.chargefC[ts][nhits] = caldigi[ts];
      }
    }

    nhits++;
  }  // end loop zdc digis

  zdcDigi.n = nhits;

  t1->Fill();

  // #ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  // // if the SetupData is always needed
  // auto setup = iSetup.getData(setupToken_);
  // // if need the ESHandle to check if the SetupData was there or not
  // auto pSetup = iSetup.getHandle(setupToken_);
  // #endif
}

// ------------ method called once each job just before starting event loop  ------------
void FSCAnalyzerHC::beginJob() {
  t1 = fs->make<TTree>("fscdigi", "fscdigi");

  t1->Branch("n", &zdcDigi.n, "n/I");
  t1->Branch("zside", zdcDigi.zside, "zside[n]/I");
  t1->Branch("section", zdcDigi.section, "section[n]/I");
  t1->Branch("channel", zdcDigi.channel, "channel[n]/I");

  for (int i = 0; i < NTS; i++) {
    TString adcTsSt("adcTs"), chargefCTsSt("chargefCTs"), tdcTsSt("tdcTs");
    adcTsSt += i;
    chargefCTsSt += i;
    tdcTsSt += i;

    t1->Branch(adcTsSt, zdcDigi.adc[i], adcTsSt + "[n]/I");
    t1->Branch(chargefCTsSt, zdcDigi.chargefC[i], chargefCTsSt + "[n]/F");
    t1->Branch(tdcTsSt, zdcDigi.tdc[i], tdcTsSt + "[n]/I");
  }
}

// ------------ method called once each job just after ending the event loop  ------------
void FSCAnalyzerHC::endJob() {
  // please remove this method if not needed
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void FSCAnalyzerHC::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addWithDefaultLabel(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(FSCAnalyzerHC);
