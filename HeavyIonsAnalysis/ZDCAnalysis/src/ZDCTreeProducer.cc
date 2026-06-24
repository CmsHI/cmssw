// -*- C++ -*-
//
// Package:    ZDCTreeProducer
// Class:      ZDCTreeProducer
//
/**\class ZDCTreeProducer ZDCTreeProducer.cc CmsHi/ZDCTreeProducer/src/ZDCTreeProducer.cc
   Description: [one line class summary]
   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  Yetkin Yilmaz
// Modified: Frank Ma, Yen-Jie Lee
//         Created:  Tue Sep  7 11:38:19 EDT 2010
// $Id: RecHitTreeProducer.cc,v 1.27 2013/01/22 16:36:27 yilmaz Exp $
//
//

// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibCalorimetry/HcalAlgos/interface/HcalPulseShapes.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/METReco/interface/HcalCaloFlagLabels.h"

#include "DataFormats/HcalDigi/interface/HcalQIESample.h"
#include "HeavyIonsAnalysis/ZDCAnalysis/src/QWZDC2018Helper.h"

#include "TTree.h"
#include "TNtuple.h"

#define MAXHITS 100000
#define MAXMOD 56
#define NZDCTS 6

struct MyZDCRecHit {
  int n;
  float e[MAXMOD];
  int zside[MAXMOD];
  int section[MAXMOD];
  int channel[MAXMOD];
  int saturation[MAXMOD];
  float sumPlus;
  float sumMinus;
};

struct MyZDCDigi {
  int n;
  float chargefC[NZDCTS][MAXMOD];
  int adc[NZDCTS][MAXMOD];
  int zside[MAXMOD];
  int section[MAXMOD];
  int channel[MAXMOD];
  float sumPlus;
  float sumMinus;
};

//
// class declaration
//

class ZDCTreeProducer : public edm::one::EDAnalyzer<> {
public:
  explicit ZDCTreeProducer(const edm::ParameterSet&);
  ~ZDCTreeProducer() override;

private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  // ----------member data ---------------------------

  // Inputs
  const edm::EDGetTokenT<QIE10DigiCollection> zdcDigiSrc_;
  const edm::EDGetTokenT<ZDCRecHitCollection> zdcRecHitSrc_;
  bool doZDCDigi_;
  bool doZDCRecHit_;
  bool calZDCDigi_;
  bool skipRPD_;
  bool verbose_;

  // Conditions
  edm::ESGetToken<HcalDbService, HcalDbRecord> hcalDatabaseToken_;

  // Helpers
  MyZDCRecHit zdcRecHit;
  MyZDCDigi zdcDigi;

  // Outputs
  TNtuple* nt;
  TTree* zdcRecHitTree;
  TTree* zdcDigiTree;

  edm::Service<TFileService> fs;
};

//
// constants, enums and typedefs
//
// static data member definitions
//
// constructors and destructor
//
ZDCTreeProducer::ZDCTreeProducer(const edm::ParameterSet& iConfig)
    : zdcDigiSrc_(consumes<QIE10DigiCollection>(iConfig.getParameter<edm::InputTag>("zdcDigiSrc"))),
      zdcRecHitSrc_(consumes<ZDCRecHitCollection>(iConfig.getParameter<edm::InputTag>("zdcRecHitSrc"))),
      doZDCDigi_(iConfig.getParameter<bool>("doZDCDigi")),
      doZDCRecHit_(iConfig.getParameter<bool>("doZDCRecHit")),
      calZDCDigi_(iConfig.getParameter<bool>("calZDCDigi")),
      skipRPD_(iConfig.getParameter<bool>("skipRPD")),
      verbose_(iConfig.getParameter<bool>("verbose")),
      hcalDatabaseToken_(esConsumes<HcalDbService, HcalDbRecord>()) {
  ;
}

ZDCTreeProducer::~ZDCTreeProducer() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called to for each event  ------------
void ZDCTreeProducer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if (doZDCRecHit_) {
    edm::Handle<ZDCRecHitCollection> zdcrechits;
    iEvent.getByToken(zdcRecHitSrc_, zdcrechits);

    int nhits = 0;
    zdcRecHit.sumPlus = 0;
    zdcRecHit.sumMinus = 0;

    for (auto const& rh : *zdcrechits) {
      HcalZDCDetId zdcid = rh.id();

      if (skipRPD_ && zdcid.section() == 4)
        continue;
      if (zdcid.section() == 1 && zdcid.channel() > 5)
        continue;  // ignore extra EM channels

      zdcRecHit.e[nhits] = rh.energy();
      zdcRecHit.zside[nhits] = zdcid.zside();
      zdcRecHit.section[nhits] = zdcid.section();
      zdcRecHit.channel[nhits] = zdcid.channel();
      zdcRecHit.saturation[nhits] = static_cast<int>(rh.flagField(HcalCaloFlagLabels::ADCSaturationBit));

      if ((zdcid.section() == 1 && zdcid.channel() <= 5) || zdcid.section() == 2) {  // safely exclude extra EM channels
        if (zdcid.zside() > 0) {
          zdcRecHit.sumPlus += rh.energy();
        }
        if (zdcid.zside() < 0) {
          zdcRecHit.sumMinus += rh.energy();
        }
      }

      nhits++;
    }  // for (auto const& rh : *zdcrechits) {

    zdcRecHit.n = nhits;
    zdcRecHitTree->Fill();
  }  // if (doZDCRecHit_) {

  if (doZDCDigi_) {
    edm::Handle<QIE10DigiCollection> zdcdigis;
    iEvent.getByToken(zdcDigiSrc_, zdcdigis);

    edm::ESHandle<HcalDbService> conditions = iSetup.getHandle(hcalDatabaseToken_);

    if (verbose_) {
      std::cout << "zdcdigis->size() : " << zdcdigis->size() << std::endl;
      std::cout << "zdcdigis->samples() : " << zdcdigis->samples() << std::endl;
      std::cout << std::left << " " << std::setw(6) << "nhits"
                << " " << std::setw(8) << "section"
                << " " << std::setw(6) << "zside"
                << " " << std::setw(8) << "channel" << std::endl;
    }

    float sumcEMP = 0, sumcEMN = 0, sumcHDP = 0, sumcHDN = 0;

    int nhits = 0;
    for (auto it = zdcdigis->begin(); it != zdcdigis->end(); it++) {
      const QIE10DataFrame digi = static_cast<const QIE10DataFrame>(*it);
      HcalZDCDetId zdcid = digi.id();

      if (verbose_) {
        std::cout << std::left << " " << std::setw(6) << nhits << " " << std::setw(8) << zdcid.section() << " "
                  << std::setw(6) << zdcid.zside() << " " << std::setw(8) << zdcid.channel() << std::endl;
      }

      if (skipRPD_ && zdcid.section() == 4)
        continue;
      if (zdcid.section() == 1 && zdcid.channel() > 5)
        continue;  // ignore extra EM channels

      CaloSamples caldigi;
      if (calZDCDigi_) {
        const HcalQIECoder* qiecoder = conditions->getHcalCoder(zdcid);
        const HcalQIEShape* qieshape = conditions->getHcalShape(qiecoder);
        HcalCoderDb coder(*qiecoder, *qieshape);
        coder.adc2fC(digi, caldigi);
      }

      zdcDigi.zside[nhits] = zdcid.zside();
      zdcDigi.section[nhits] = zdcid.section();
      zdcDigi.channel[nhits] = zdcid.channel();

      for (int ts = 0; ts < digi.samples(); ts++) {
        zdcDigi.chargefC[ts][nhits] =
            calZDCDigi_ ? caldigi[ts] : QWAna::ZDC2018::QIE10_regular_fC[digi[ts].adc()][digi[ts].capid()];
        zdcDigi.adc[ts][nhits] = digi[ts].adc();
      }

      if ((zdcid.section() == 1 && zdcid.channel() <= 5) || zdcid.section() == 2) {  // safely exclude extra EM channels
        if (zdcid.section() == 1 && zdcid.zside() > 0)
          sumcEMP += (zdcDigi.chargefC[2][nhits] - zdcDigi.chargefC[1][nhits]);
        if (zdcid.section() == 1 && zdcid.zside() < 0)
          sumcEMN += (zdcDigi.chargefC[2][nhits] - zdcDigi.chargefC[1][nhits]);
        if (zdcid.section() == 2 && zdcid.zside() > 0)
          sumcHDP += (zdcDigi.chargefC[2][nhits] - zdcDigi.chargefC[1][nhits]);
        if (zdcid.section() == 2 && zdcid.zside() < 0)
          sumcHDN += (zdcDigi.chargefC[2][nhits] - zdcDigi.chargefC[1][nhits]);
      }

      nhits++;
    }  // for (auto it = zdcdigis->begin(); it != zdcdigis->end(); it++) {

    // Very preliminary calibration
    zdcDigi.sumMinus = (sumcEMN * 0.1 + sumcHDN) * 0.5031;
    zdcDigi.sumPlus = (sumcEMP * 0.1 + sumcHDP) * 0.9397;

    zdcDigi.n = nhits;
    zdcDigiTree->Fill();
  }
}

// ------------ method called once each job just before starting event loop  ------------
void ZDCTreeProducer::beginJob() {
  if (doZDCRecHit_) {
    zdcRecHitTree = fs->make<TTree>("zdcrechit", "zdc");
    zdcRecHitTree->Branch("n", &zdcRecHit.n, "n/I");
    zdcRecHitTree->Branch("e", zdcRecHit.e, "e[n]/F");
    zdcRecHitTree->Branch("saturation", zdcRecHit.saturation, "saturation[n]/F");
    zdcRecHitTree->Branch("zside", zdcRecHit.zside, "zside[n]/I");
    zdcRecHitTree->Branch("section", zdcRecHit.section, "section[n]/I");
    zdcRecHitTree->Branch("channel", zdcRecHit.channel, "channel[n]/I");
    zdcRecHitTree->Branch("sumPlus", &zdcRecHit.sumPlus, "sumPlus/F");
    zdcRecHitTree->Branch("sumMinus", &zdcRecHit.sumMinus, "sumMinus/F");
  }

  if (doZDCDigi_) {
    zdcDigiTree = fs->make<TTree>("zdcdigi", "zdc");
    zdcDigiTree->Branch("n", &zdcDigi.n, "n/I");
    zdcDigiTree->Branch("zside", zdcDigi.zside, "zside[n]/I");
    zdcDigiTree->Branch("section", zdcDigi.section, "section[n]/I");
    zdcDigiTree->Branch("channel", zdcDigi.channel, "channel[n]/I");
    for (int i = 0; i < NZDCTS; i++) {
      TString adcTsSt("adcTs"), chargefCTsSt("chargefCTs");
      adcTsSt += i;
      chargefCTsSt += i;

      zdcDigiTree->Branch(adcTsSt, zdcDigi.adc[i], adcTsSt + "[n]/I");
      zdcDigiTree->Branch(chargefCTsSt, zdcDigi.chargefC[i], chargefCTsSt + "[n]/F");
    }
    zdcDigiTree->Branch("sumPlus", &zdcDigi.sumPlus, "sumPlus/F");
    zdcDigiTree->Branch("sumMinus", &zdcDigi.sumMinus, "sumMinus/F");
  }
}

// ------------ method called once each job just after ending the event loop  ------------
void ZDCTreeProducer::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(ZDCTreeProducer);
