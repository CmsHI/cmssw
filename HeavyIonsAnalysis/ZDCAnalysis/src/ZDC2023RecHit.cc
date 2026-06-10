/*
 * =====================================================================================
 *
 *       Filename:  ZDC2023RecHit.cc
 *
 *    Description:  ZDCRecHitCollection producer for 2023 PbPb runs.
 *
 *        Version:  1.0
 *        Created:  01/29/2026 22:11:12
 *
 *         Author:  jing.wang@cern.ch
 *   Organization:  MIT
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"
#include "CalibCalorimetry/HcalAlgos/interface/HcalPulseShapes.h"

#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/HcalDetId/interface/HcalZDCDetId.h"
#include "DataFormats/HcalRecHit/interface/HcalRecHitDefs.h"

#include "HeavyIonsAnalysis/ZDCAnalysis/src/QWZDC2018Helper.h"

#include <iostream>
#include <iomanip>

/*** Incomplete ZDCRechit only with energy
     What are not writen: 
     rh.setTDCtime();
     rh.setChargeWeightedTime();
     rh.setEnergySOIp1();
     rh.setRatioSOIp1();
     saturation
***/

class ZDC2023RecHit : public edm::one::EDProducer<> {
public:
  explicit ZDC2023RecHit(const edm::ParameterSet&);
  ~ZDC2023RecHit() override;

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  // Inputs
  edm::EDGetTokenT<QIE10DigiCollection> tok_input_QIE10_;
  bool calZDCDigi_;
  bool skipRPD_;

  // Consts
  const unsigned int signalTs_ = 3, noiseTs_ = 2;
  const float ratioNoise_ = -1., fracEM_ = 0.1, fracHAD_ = 1., fracRPD_ = 1., corrPlus_ = 0.9397, corrMinus_ = 0.5031;
  /**** Hard coded calibration
        https://github.com/CmsHI/cmssw/blob/fb599d384eb19890240466d9bba3520419ae3b2a/HeavyIonsAnalysis/ZDCAnalysis/src/ZDCTreeProducer.cc#L268-L283
        Ts3 - 1.*Ts2:
        charge = zdcDigi.chargefC[2] - zdcDigi.chargefC[1]
        sumMinus = (sumcEMN * 0.1 + sumcHDN * 1.) * 0.5031;
        sumPlus= (sumcEMP * 0.1 + sumcHDP * 1.) * 0.9397;
  ****/

  // Conditions
  edm::ESGetToken<HcalDbService, HcalDbRecord> hcalDatabaseToken_;
};

ZDC2023RecHit::ZDC2023RecHit(const edm::ParameterSet& iConfig)
    : tok_input_QIE10_(consumes<QIE10DigiCollection>(iConfig.getParameter<edm::InputTag>("zdcDigiSrc"))),
      calZDCDigi_(iConfig.getParameter<bool>("calZDCDigi")),
      skipRPD_(iConfig.getParameter<bool>("skipRPD")),
      hcalDatabaseToken_(esConsumes<HcalDbService, HcalDbRecord>()) {
  produces<ZDCRecHitCollection>();
}

ZDC2023RecHit::~ZDC2023RecHit() { return; }

void ZDC2023RecHit::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<QIE10DigiCollection> zdcdigis;
  iEvent.getByToken(tok_input_QIE10_, zdcdigis);
  edm::ESHandle<HcalDbService> conditions =
      iSetup.getHandle(hcalDatabaseToken_);  // is only used when calZDCDigi_ is true

  auto prec = std::make_unique<ZDCRecHitCollection>();
  // prec->reserve(zdcdigis->size());

  int nhits = 0;
  for (auto it = zdcdigis->begin(); it != zdcdigis->end(); it++) {
    const auto digi = static_cast<const QIE10DataFrame>(*it);
    const HcalZDCDetId zdcid = digi.id();

    auto section = zdcid.section();
    bool is_EM =
             (section == 1),  // extra EM channels are still kept which should be excluded in energy sum in the analyzer
        is_HAD = (section == 2), is_RPD = (section == 4);

    if (skipRPD_ && is_RPD)
      continue;

    // Prepare digi calibration if calZDCDigi_;
    // Default calZDCDigi_ is False, i.e. this is not used
    CaloSamples caldigi;
    if (calZDCDigi_) {
      const HcalQIECoder* qiecoder = conditions->getHcalCoder(zdcid);
      const HcalQIEShape* qieshape = conditions->getHcalShape(qiecoder);
      HcalCoderDb coder(*qiecoder, *qieshape);
      coder.adc2fC(digi, caldigi);
    }

    unsigned int nTs = digi.samples();
    if (nTs < signalTs_ || nTs < noiseTs_) {
      std::cout << __FUNCTION__ << " error: Number of Ts (" << nTs << ") is too small for signal Ts (" << signalTs_
                << ") or noise Ts (" << noiseTs_ << ")" << std::endl;
      continue;
    }

    // Outpu subtraction: Ts3 + (-1.)*Ts2, Ts starts from Ts1 rather than Ts0 :
    float signalfC =
        calZDCDigi_ ? caldigi[signalTs_ - 1] :  // by default not used
            QWAna::ZDC2018::QIE10_regular_fC[digi[signalTs_ - 1].adc()][digi[signalTs_ - 1].capid()];  // by default used
    float noisefC =
        calZDCDigi_ ? caldigi[noiseTs_ - 1] :  // by default not used
            QWAna::ZDC2018::QIE10_regular_fC[digi[noiseTs_ - 1].adc()][digi[noiseTs_ - 1].capid()];  // by default used
    float energy = signalfC + ratioNoise_ * noisefC;

    if (is_EM) {
      energy *= fracEM_;
    } else if (is_HAD) {
      energy *= fracHAD_;
    } else if (is_RPD) {
      energy *= fracRPD_;
    }

    if (zdcid.zside() > 0) {
      energy *= corrPlus_;
    } else {
      energy *= corrMinus_;
    }

    // Make ZDCRechit https://github.com/cms-sw/cmssw/blob/master/DataFormats/HcalRecHit/interface/ZDCRecHit.h
    auto rh = ZDCRecHit(digi.id(), energy, -99, -99);
    // (HcalZDCDetId&, energy, time, lowGainEnergy)
    rh.setFlags(0);  // saturation
    /*** What are not writen: 
         rh.setTDCtime(tmp_tdctime);
         rh.setChargeWeightedTime(chargeWeightedTime);
         rh.setEnergySOIp1(energySOIp1);
         rh.setRatioSOIp1(ratioSOIp1);
    ***/

    prec->push_back(rh);

    nhits++;
  }  // for (auto it = zdcdigis->begin(); it != zdcdigis->end(); it++) {

  iEvent.put(std::move(prec));

  return;
}

DEFINE_FWK_MODULE(ZDC2023RecHit);
