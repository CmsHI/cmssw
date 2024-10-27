// -*- C++ -*-
//
// Package:    HeavyIonAnalyzer/ZDCAnalysis/ZDCRecHitAnalyzer
// Class:      ZDCRecHitAnalyzer
//
/**\class ZDCRecHitAnalyzer ZDCRecHitAnalyzer.cc HeavyIonAnalyzer/ZDCAnalysis/plugins/ZDCRecHitAnalyzer

 Description: Produced Tree with ZDC RecHit and zdcdigi information 
*/
//
// Original Author:  Matthew Nickel, University of Kansas
//         Created:  08-10-2024
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

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.

struct MyZDCDigi {
  int n;
  float chargefC[10][50];
  int adc[10][50];
  int tdc[10][50];
  int zside[50];
  int section[50];
  int channel[50];
};

using reco::TrackCollection;



class ZDCRecHitAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit ZDCRecHitAnalyzer(const edm::ParameterSet&);
  ~ZDCRecHitAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  // ----------member data ---------------------------
   const edm::EDGetTokenT<QIE10DigiCollection> ZDCDigiToken_; 
   const edm::EDGetTokenT<edm::SortedCollection<ZDCRecHit>> ZDCRecHitToken_; 
   edm::ESGetToken<HcalDbService, HcalDbRecord> hcalDatabaseToken_;
  bool doZdcRecHits_;
  bool doZdcDigis_;
  bool skipRPD_;
   edm::Service<TFileService> fs;
   TTree* t1;
   
   
     MyZDCDigi zdcDigi;
   
   // tree branch variables
   int zdc_n;
   int zdc_side[50];
   int zdc_section[50];
   int zdc_channel[50];
   float zdc_Energy[50];
   float zdc_Time[50];
   float zdc_TDCtime[50];
   float zdc_ChargeWeightedTime[50];
   float zdc_EnergySOIp1[50];
   float zdc_RatioSOIp1[50];
   int zdc_Saturation[50];

   float ZDCp_Energy;
   float ZDCm_Energy;  
   

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
ZDCRecHitAnalyzer::ZDCRecHitAnalyzer(const edm::ParameterSet& iConfig) :
      ZDCDigiToken_(consumes<QIE10DigiCollection>(iConfig.getParameter<edm::InputTag>("ZDCDigiSource"))), 
      ZDCRecHitToken_(consumes<edm::SortedCollection<ZDCRecHit>>(iConfig.getParameter<edm::InputTag>("ZDCRecHitSource"))), 
      hcalDatabaseToken_(esConsumes<HcalDbService, HcalDbRecord>()),
      doZdcRecHits_(iConfig.getParameter<bool>("doZdcRecHits")),
      doZdcDigis_(iConfig.getParameter<bool>("doZdcDigis")),
      skipRPD_(iConfig.getParameter<bool>("skipRPD"))
      {
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  setupDataToken_ = esConsumes<SetupData, SetupRecord>();

#endif
  //now do what ever initialization is needed
}

ZDCRecHitAnalyzer::~ZDCRecHitAnalyzer() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
  //
  // please remove this method altogether if it would be left empty
}

//
// member functions
//

// ------------ method called for each event  ------------
void ZDCRecHitAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;
  using namespace std;
  
  
  if(doZdcRecHits_){
     zdc_n = 0;
     ZDCp_Energy = 0;
     ZDCm_Energy = 0;
     for (unsigned int i = 0; i < 50; i++) {
     zdc_side[i] = -99;
     zdc_section [i]= -99;
     zdc_channel[i] = -99;

     zdc_Energy[i] = -99;
     zdc_Time[i] = -99;
     zdc_TDCtime[i] = -99;
     zdc_ChargeWeightedTime[i] = -99;
     zdc_EnergySOIp1[i] = -99;
     zdc_RatioSOIp1[i] = -99;
     zdc_Saturation[i] = -99;
       
     }
     
       edm::Handle<ZDCRecHitCollection> zdcrechits;
      iEvent.getByToken(ZDCRecHitToken_, zdcrechits);
       // zdc_n = zdcrechits->size();   
       int nhits = 0;
       for (auto const& rh : *zdcrechits) {
          
         if (nhits  >= 50) break;          
         HcalZDCDetId zdcid = rh.id();
          int side = zdcid.zside();
          int section = zdcid.section();
          int channel =zdcid.channel(); 
          float energy = rh.energy();
          
          if(section ==4 && skipRPD_ ) continue;
          
          zdc_side[nhits] = side;
          zdc_section[nhits] = section;
          zdc_channel[nhits] = channel;
          
          zdc_Energy[nhits]  = energy;
          zdc_Time[nhits]  = rh.time();
          zdc_TDCtime[nhits]  = rh.TDCtime();
          zdc_ChargeWeightedTime[nhits] = rh.chargeWeightedTime();
          zdc_EnergySOIp1[nhits]  = rh.energySOIp1();
          zdc_RatioSOIp1[nhits]  = rh.ratioSOIp1();
          zdc_Saturation[nhits] = static_cast<int>( rh.flagField(HcalCaloFlagLabels::ADCSaturationBit) );
          
          if(side <0 && (section ==1 || section ==2)) ZDCm_Energy += energy;
          if(side >0 && (section ==1 || section ==2)) ZDCp_Energy += energy;

         nhits++;
       } // end loop zdc rechits 
       
       zdc_n = nhits;  
  }
  
  if(doZdcDigis_){
    edm::Handle<QIE10DigiCollection> zdcdigis;
    iEvent.getByToken(ZDCDigiToken_, zdcdigis);
    
    edm::ESHandle<HcalDbService> conditions = iSetup.getHandle(hcalDatabaseToken_);
    
    int nhits = 0;


    for (auto it = zdcdigis->begin(); it != zdcdigis->end(); it++) {      
      const QIE10DataFrame digi = static_cast<const QIE10DataFrame>(*it);

      HcalZDCDetId zdcid = digi.id();
       int side = zdcid.zside();
       int section = zdcid.section();
       int channel = zdcid.channel();
      if(section== 1 && channel> 5) continue; // ignore extra EM channels 
      if(section ==4 && skipRPD_ ) continue;
      
      if (nhits  >= 50) break;       

      CaloSamples caldigi;

      //const ZDCDataFrame & rh = (*zdcdigis)[it];

        const HcalQIECoder* qiecoder = conditions->getHcalCoder(zdcid);
        const HcalQIEShape* qieshape = conditions->getHcalShape(qiecoder);
        HcalCoderDb coder(*qiecoder, *qieshape);
        //        coder.adc2fC(rh,caldigi);
        coder.adc2fC(digi, caldigi);


        zdcDigi.zside[nhits] = side;
        zdcDigi.section[nhits] = section;
        zdcDigi.channel[nhits] = channel;

        for (int ts = 0; ts < digi.samples(); ts++) {

          zdcDigi.chargefC[ts][nhits] = caldigi[ts];
          zdcDigi.adc[ts][nhits] = digi[ts].adc();
          zdcDigi.tdc[ts][nhits] = digi[ts].le_tdc();
        }
      nhits++;
    }  // end loop zdc digis

    zdcDigi.n = nhits;
  }    
    t1->Fill();

// #ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  // // if the SetupData is always needed
  // auto setup = iSetup.getData(setupToken_);
  // // if need the ESHandle to check if the SetupData was there or not
  // auto pSetup = iSetup.getHandle(setupToken_);
// #endif                                       
}

// ------------ method called once each job just before starting event loop  ------------
void ZDCRecHitAnalyzer::beginJob() {
  // please remove this method if not needed
  t1 = fs->make<TTree>("zdcrechit", "zdcrechit");
   if(doZdcRecHits_){
     
     t1->Branch("ZDCp_Energy",&ZDCp_Energy); 
     t1->Branch("ZDCm_Energy",&ZDCm_Energy);
     
     t1->Branch("zdcrechit_n",&zdc_n);
     t1->Branch("zdcrechit_side",zdc_side,"zdcrechit_side[zdcrechit_n]/I");
     t1->Branch("zdcrechit_section",zdc_section,"zdcrechit_section[zdcrechit_n]/I");
     t1->Branch("zdcrechit_channel",zdc_channel,"zdcrechit_channel[zdcrechit_n]/I");
     t1->Branch("zdcrechit_Energy",zdc_Energy,"zdcrechit_Energy[zdcrechit_n]/F");    
     t1->Branch("zdcrechit_Time",zdc_Time,"zdcrechit_Time[zdcrechit_n]/F");    
     t1->Branch("zdcrechit_TDCtime",zdc_TDCtime,"zdcrechit_TDCtime[zdcrechit_n]/F");    
     t1->Branch("zdcrechit_ChargeWeightedTime",zdc_ChargeWeightedTime,"zdcrechit_ChargeWeightedTime[zdcrechit_n]/F");    
     t1->Branch("zdcrechit_EnergySOIp1",zdc_EnergySOIp1,"zdcrechit_EnergySOIp1[zdcrechit_n]/F");    
     t1->Branch("zdcrechit_RatioSOIp1",zdc_RatioSOIp1,"zdcrechit_RatioSOIp1[zdcrechit_n]/F");    
     t1->Branch("zdcrechit_Saturation",zdc_Saturation,"zdcrechit_Saturation[zdcrechit_n]/I");    
     

     
  }
  
  if(doZdcDigis_){
    t1->Branch("zdcdigi_n", &zdcDigi.n, "zdcdigi_n/I");
    t1->Branch("zdcdigi_zside", zdcDigi.zside, "zdcdigi_zside[zdcdigi_n]/I");
    t1->Branch("zdcdigi_section", zdcDigi.section, "zdcdigi_section[zdcdigi_n]/I");
    t1->Branch("zdcdigi_channel", zdcDigi.channel, "zdcdigi_channel[zdcdigi_n]/I");
    for (int i = 0; i < 6; i++) {
      TString adcTsSt("zdcdigi_adcTs"), chargefCTsSt("zdcdigi_chargefCTs"), tdcTsSt("zdcdigi_tdcTs");
      adcTsSt += i;
      chargefCTsSt += i;
      tdcTsSt += i;

      t1->Branch(adcTsSt, zdcDigi.adc[i], adcTsSt + "[zdcdigi_n]/I");
      t1->Branch(chargefCTsSt, zdcDigi.chargefC[i], chargefCTsSt + "[zdcdigi_n]/F");
      t1->Branch(tdcTsSt, zdcDigi.tdc[i], tdcTsSt + "[zdcdigi_n]/I");
    }
  }
  
}

// ------------ method called once each job just after ending the event loop  ------------
void ZDCRecHitAnalyzer::endJob() {
  // please remove this method if not needed
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void ZDCRecHitAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
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
DEFINE_FWK_MODULE(ZDCRecHitAnalyzer);