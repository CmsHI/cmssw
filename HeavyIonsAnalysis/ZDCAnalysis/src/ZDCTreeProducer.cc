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
//#include "DataFormats/FWLite/interface/ChainEvent.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/METReco/interface/HcalCaloFlagLabels.h"
//#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"

#include "DataFormats/HcalDigi/interface/HcalQIESample.h"
//#include "QWAna/QWZDC2018RecHit/src/QWZDC2018Helper.h"
#include "HeavyIonsAnalysis/ZDCAnalysis/src/QWZDC2018Helper.h"

#include "TTree.h"
#include "TNtuple.h"

#define MAXHITS 100000
#define MAXMOD 56

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
  float chargefC[6][MAXMOD];
  int adc[6][MAXMOD];
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

  math::XYZPoint getPosition(const DetId& id, reco::Vertex::Point& vtx);
  double getEt(math::XYZPoint& pos, double energy);
  double getEt(const DetId& id, double energy);
  double getEta(const DetId& id);
  double getPhi(const DetId& id);
  double getPerp(const DetId& id);

private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  // ----------member data ---------------------------

  MyZDCRecHit zdcRecHit;
  MyZDCDigi zdcDigi;

  TNtuple* nt;
  TTree* zdcRecHitTree;
  TTree* zdcDigiTree;

  int nZdcTs_;
  bool calZDCDigi_;
  bool verbose_;

  edm::Service<TFileService> fs;
  const CaloGeometry* geo;

  edm::InputTag zdcDigiSrc_;
  edm::EDGetTokenT<ZDCRecHitCollection> zdcRecHitSrc_;
  edm::ESGetToken<CaloGeometry, CaloGeometryRecord> geometryToken_;
  edm::ESGetToken<HcalDbService, HcalDbRecord> hcalDatabaseToken_;

  bool doZDCRecHit_;
  bool doZDCDigi_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//
constexpr double cone2 = 0.5 * 0.5;

//
// constructors and destructor
//
ZDCTreeProducer::ZDCTreeProducer(const edm::ParameterSet& iConfig):
  hcalDatabaseToken_(esConsumes<HcalDbService, HcalDbRecord>())
{
  //now do what ever initialization is needed
  doZDCRecHit_ = iConfig.getParameter<bool>("doZDCRecHit");
  doZDCDigi_ = iConfig.getParameter<bool>("doZDCDigi");

  if (doZDCDigi_)
    //    zdcDigiSrc_ = consumes<ZDCDigiCollection>(iConfig.getParameter<edm::InputTag>("zdcDigiSrc"));
    zdcDigiSrc_ = iConfig.getParameter<edm::InputTag>("zdcDigiSrc");
  consumes<QIE10DigiCollection>(zdcDigiSrc_);

  if (doZDCRecHit_)
    zdcRecHitSrc_ = consumes<ZDCRecHitCollection>(iConfig.getParameter<edm::InputTag>("zdcRecHitSrc"));

  nZdcTs_ = iConfig.getParameter<int>("nZdcTs");
  calZDCDigi_ = iConfig.getParameter<bool>("calZDCDigi");
  verbose_ = iConfig.getParameter<bool>("verbose");
  geometryToken_ = esConsumes();
}

ZDCTreeProducer::~ZDCTreeProducer() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called to for each event  ------------
void ZDCTreeProducer::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {
  //iSetup.get<CaloGeometryRecord>().get(geo);
  geo = &iSetup.getData(geometryToken_);
  if (doZDCRecHit_) {
    edm::Handle<ZDCRecHitCollection> zdcrechits;
    ev.getByToken(zdcRecHitSrc_, zdcrechits);

    int nhits = 0;
    zdcRecHit.sumPlus = 0;
    zdcRecHit.sumMinus = 0;

    for (auto const& rh : *zdcrechits) {
      HcalZDCDetId zdcid = rh.id();
      // if (nhits < 18) {
      zdcRecHit.e[nhits] = rh.energy();
      zdcRecHit.zside[nhits] = zdcid.zside();
      zdcRecHit.section[nhits] = zdcid.section();
      zdcRecHit.channel[nhits] = zdcid.channel();
      zdcRecHit.saturation[nhits] = static_cast<int>(rh.flagField(HcalCaloFlagLabels::ADCSaturationBit));
      // }

      if (rh.id().zside() > 0) {
        zdcRecHit.sumPlus += rh.energy();
      }
      if (rh.id().zside() < 0) {
        zdcRecHit.sumMinus += rh.energy();
      }

      nhits++;
    }  // end loop zdc rechits

    zdcRecHit.n = nhits;
    zdcRecHitTree->Fill();
  }

  if (doZDCDigi_) {
    //    edm::Handle<ZDCDigiCollection> zdcdigis;
    edm::Handle<QIE10DigiCollection> zdcdigis;
    ev.getByLabel(zdcDigiSrc_, zdcdigis);

    edm::ESHandle<HcalDbService> conditions = iSetup.getHandle(hcalDatabaseToken_);

    int nhits = 0;
    //    for (auto const& rh : *zdcdigis)  {

    if(verbose_)
    {
      std::cout << "zdcdigis->size() : " << zdcdigis->size() << std::endl;
      std::cout << "zdcdigis->samples() : " << zdcdigis->samples() << std::endl;
    }

    for (auto it = zdcdigis->begin(); it != zdcdigis->end(); it++) {


      const QIE10DataFrame digi = static_cast<const QIE10DataFrame>(*it);

      HcalZDCDetId zdcid = digi.id();
      std::string cc = zdcid.section() == 1?"\e[34m":(zdcid.section() == 2?"\e[32m":"\e[31m");
      if(verbose_) std::cout << "--- nhits/DetId : " << std::left << std::setw(3) << nhits << cc.c_str() << "section | zside | channel : " << zdcid.section() <<" | " << std::setw(3) << zdcid.zside() << "| " << zdcid.channel() << "\e[0m" << std::endl;

      CaloSamples caldigi;

      //const ZDCDataFrame & rh = (*zdcdigis)[it];
      if (calZDCDigi_) {
        if(verbose_) std::cout << "###DIGI1?" << std::endl;

        const HcalQIECoder* qiecoder = conditions->getHcalCoder(zdcid);
        const HcalQIEShape* qieshape = conditions->getHcalShape(qiecoder);
        HcalCoderDb coder(*qiecoder, *qieshape);
        coder.adc2fC(digi, caldigi);
        if(verbose_) std::cout << "###--- END DIGI1?" << std::endl;
      }

        zdcDigi.zside[nhits] = zdcid.zside();
        zdcDigi.section[nhits] = zdcid.section();
        zdcDigi.channel[nhits] = zdcid.channel();

        for (int ts = 0; ts < digi.samples(); ts++) {
          if(verbose_) std::cout << "###DIGI2? --- ts : " << ts <<", "<<digi[ts].capid()<< std::endl;

          // zdcDigi.chargefC[ts][nhits] = calZDCDigi_ ? caldigi[ts] : QWAna::ZDC2018::QIE10_nominal_fC[digi[ts].adc()];
          zdcDigi.chargefC[ts][nhits] = calZDCDigi_ ? caldigi[ts] : QWAna::ZDC2018::QIE10_regular_fC[digi[ts].adc()][digi[ts].capid()];
          // zdcDigi.chargefC[ts][nhits] = calZDCDigi_ ? caldigi[ts] : (QWAna::ZDC2018::QIE10_regular_fC[digi[ts].adc()][digi[ts].capid()] - pedestal_[did()][digi[i].capid()]);
          
          zdcDigi.adc[ts][nhits] = digi[ts].adc();
          if(verbose_) std::cout << "###--- END DIGI2?" << std::endl;
        }

      nhits++;
    }  // end loop zdc rechits
    if(verbose_) std::cout << "###DIGI END?" << std::endl;

    // Very preliminary calibration
    float sumcEMP = 0, sumcEMN = 0, sumcHDP = 0, sumcHDN = 0;
    // 2023 EM: idet = 0-5 and 12-16
    for (int idet = 0; idet < 5; idet++) {
      auto idet_m = idet, idet_p = idet + 12;
      sumcEMN += (zdcDigi.chargefC[2][idet_m] - zdcDigi.chargefC[1][idet_m]);
      sumcEMP += (zdcDigi.chargefC[2][idet_p] - zdcDigi.chargefC[1][idet_p]);
    }
    // 2023 HAD: idet = 8-11 and 20-23
    for (int idet = 8; idet < 12; idet++) {
      auto idet_m = idet, idet_p = idet + 12;
      sumcHDN += (zdcDigi.chargefC[2][idet_m] - zdcDigi.chargefC[1][idet_m]);
      sumcHDP += (zdcDigi.chargefC[2][idet_p] - zdcDigi.chargefC[1][idet_p]);
    }

    zdcDigi.sumMinus = (sumcEMN * 0.1 + sumcHDN) * 0.5031;
    zdcDigi.sumPlus= (sumcEMP * 0.1 + sumcHDP) * 0.9397;

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
    for (int i = 0; i < nZdcTs_; i++) {
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

math::XYZPoint ZDCTreeProducer::getPosition(const DetId& id, reco::Vertex::Point& vtx) {
  const GlobalPoint& pos = geo->getPosition(id);
  return math::XYZPoint(pos.x() - vtx.x(), pos.y() - vtx.y(), pos.z() - vtx.z());
}

inline double ZDCTreeProducer::getEt(math::XYZPoint& pos, double energy) { return energy * sin(pos.theta()); }

inline double ZDCTreeProducer::getEt(const DetId& id, double energy) {
  const GlobalPoint& pos = geo->getPosition(id);
  return energy * sin(pos.theta());
}

inline double ZDCTreeProducer::getEta(const DetId& id) {
  const GlobalPoint& pos = geo->getPosition(id);
  return pos.eta();
}

inline double ZDCTreeProducer::getPhi(const DetId& id) {
  const GlobalPoint& pos = geo->getPosition(id);
  return pos.phi();
}

inline double ZDCTreeProducer::getPerp(const DetId& id) {
  const GlobalPoint& pos = geo->getPosition(id);
  return pos.perp();
}

//define this as a plug-in
DEFINE_FWK_MODULE(ZDCTreeProducer);
