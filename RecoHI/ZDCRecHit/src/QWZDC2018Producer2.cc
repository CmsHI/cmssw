#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CalibCalorimetry/HcalAlgos/interface/HcalPulseShapes.h"

#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "iostream"

#include "QWZDC2018Helper.h"
#include "boost/bimap.hpp"

using namespace std;
class QWZDC2018Producer2 : public edm::EDProducer {
public:
	explicit QWZDC2018Producer2(const edm::ParameterSet&);
	~QWZDC2018Producer2();

private:
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	virtual void beginRun(const edm::Run&, const edm::EventSetup&) override;
	///

	edm::InputTag	Src_;
	int		SOI_;
	bool		bHardCode_;
	bool		bDebug_;

	std::map<uint32_t, std::vector<double>> pedestal_;
	std::map<std::string, uint32_t>		cname_;

};


QWZDC2018Producer2::QWZDC2018Producer2(const edm::ParameterSet& pset) :
	Src_(pset.getUntrackedParameter<edm::InputTag>("Src")),
	SOI_(pset.getUntrackedParameter<int>("SOI", 4)),
	bHardCode_(pset.getUntrackedParameter<bool>("HardCode", true)), // has to be hard coded now, calibration format is not working at the moment =_=
	bDebug_(pset.getUntrackedParameter<bool>("Debug", false))
{
	consumes<QIE10DigiCollection>(Src_);

	for ( int channel = 0; channel < 16; channel++ ) {
		HcalZDCDetId did(HcalZDCDetId::EM, true, channel);
		cname_[ std::string("hZDCP_EM") + std::to_string(channel) ] = did();

		did = HcalZDCDetId(HcalZDCDetId::EM, false, channel);
		cname_[ std::string("hZDCM_EM") + std::to_string(channel) ] = did();

		did = HcalZDCDetId(HcalZDCDetId::HAD, true, channel);
		cname_[ std::string("hZDCP_HAD") + std::to_string(channel) ] = did();

		did = HcalZDCDetId(HcalZDCDetId::HAD, false, channel);
		cname_[ std::string("hZDCM_HAD") + std::to_string(channel) ] = did();

		did = HcalZDCDetId(HcalZDCDetId::RPD, true, channel+1);
		cname_[ std::string("hZDCP_RPD") + std::to_string(channel) ] = did();

		did = HcalZDCDetId(HcalZDCDetId::RPD, false, channel+1);
		cname_[ std::string("hZDCM_RPD") + std::to_string(channel) ] = did();
	}


	std::vector<double>	ped0{0.,0.,0.,0.};
	if ( pset.exists("Pedestal") ) {
		std::vector<edm::ParameterSet> ped = pset.getParameter<std::vector<edm::ParameterSet> >("Pedestal");
		for ( auto ch = ped.begin(); ch != ped.end(); ch++ ) {
			auto ch_str = ch->getUntrackedParameter<std::string>("object");
			pedestal_[cname_[ch->getUntrackedParameter<std::string>("object")]] =
				ch->getUntrackedParameter<std::vector<double>>("ped");
		}
	} else {
		for ( auto it = cname_.begin(); it != cname_.end(); it++ ) {
			pedestal_[it->second] = ped0;
		}
	}

	produces<std::vector<double> >("ADC");
	produces<std::vector<double> >("nominalfC");
	produces<std::vector<double> >("regularfC");
	produces<std::vector<double> >("DetId");
	produces<std::vector<double> >("CapId");
	produces<std::vector<double> >("overflow");

	produces<std::vector<double> >("chargeHigh");
	produces<std::vector<double> >("chargeLow");
	produces<std::vector<double> >("chargeSum");

	produces<std::vector<double> >("ratio5o4");
	produces<std::vector<double> >("ratio6o5");
//
//	produces< double >("Sum");
//	produces< double >("SumP");
//	produces< double >("SumN");
//
//	produces< double >("emSumP");
//	produces< double >("emSumN");
//
//	produces< double >("hadSumP");
//	produces< double >("hadSumN");
}

QWZDC2018Producer2::~QWZDC2018Producer2()
{
	return;
}

void QWZDC2018Producer2::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;

	std::unique_ptr<std::vector<double> > pADC( new std::vector<double> );
	std::unique_ptr<std::vector<double> > pnfC( new std::vector<double> );
	std::unique_ptr<std::vector<double> > pfC( new std::vector<double> );
	std::unique_ptr<std::vector<double> > pDid( new std::vector<double> );
	std::unique_ptr<std::vector<double> > pCap( new std::vector<double> );
	std::unique_ptr<std::vector<double> > poverflow( new std::vector<double> );
	std::unique_ptr<std::vector<double> > pChargeHigh( new std::vector<double> );
	std::unique_ptr<std::vector<double> > pChargeLow( new std::vector<double> );
	std::unique_ptr<std::vector<double> > pChargeSum( new std::vector<double> );

	std::unique_ptr<std::vector<double> > pratio5o4( new std::vector<double> );
	std::unique_ptr<std::vector<double> > pratio6o5( new std::vector<double> );

	ESHandle<HcalDbService> conditions;
	if ( !bHardCode_ )
		iSetup.get<HcalDbRecord>().get(conditions);


	Handle<QIE10DigiCollection> digis;
	iEvent.getByLabel(Src_, digis);

//	double adc[50][10] = {};
//
	int idx = 0;
	for ( auto it = digis->begin(); it != digis->end(); it++ ) {
		const QIE10DataFrame digi = static_cast<const QIE10DataFrame>(*it);
		HcalZDCDetId const& did = digi.detid();
		if ( bDebug_ ) {
			cout << __LINE__ << "\t idx = " << idx << did << "\n";
			cout << std::hex << digi << std::dec << "\n";
		}

		pDid->push_back( double(did()) );
		if ( bDebug_ ) cout << __LINE__ << "\n";

//		const HcalCalibrations& calibrations(conditions->getHcalCalibrations(did));
		CaloSamples cs;
		if ( !bHardCode_ ) {
			const HcalQIECoder* channelCoder = conditions->getHcalCoder(did);
			const HcalQIEShape* shape = conditions->getHcalShape(channelCoder);
			const HcalCoderDb coder(*channelCoder, *shape);
			coder.adc2fC(digi, cs);
		}
		double chargeSOI_high = 0;
		double chargeSOI_low = 0;
		double chargeSOI_sum = 0;
		double regular_fC[10] = {}; // hard coded 10TS maximum;
		if ( bDebug_ ) cout << __LINE__ << "\n";
		for ( int i = 0; i < digi.samples(); i++ ) {
			if ( bDebug_ ) cout << __LINE__ << "\n";
			pADC->push_back( digi[i].adc() );
			pCap->push_back(digi[i].capid());
			if ( digi[i].adc() >= 255 ) {
				poverflow->push_back(1.);
			} else {
				poverflow->push_back(0.);
			}

			if ( bDebug_ ) cout << __LINE__ << " i = " << i << digi[i].adc() << "\n";
			pnfC->push_back(QWAna::ZDC2018::QIE10_nominal_fC[ int( digi[i].adc() ) ]);

			double charge = 0;
			if ( bDebug_ ) cout << __LINE__ << "\n";
			if ( bHardCode_ ) {
				charge = QWAna::ZDC2018::QIE10_regular_fC[digi[i].adc()][digi[i].capid()] - pedestal_[did()][digi[i].capid()];
			} else {
				charge = cs[i] - pedestal_[did()][digi[i].capid()];
			}
			if ( bDebug_ ) cout << __LINE__ << "\n";
			regular_fC[i] = charge;
			pfC->push_back(charge);
			if ( i == SOI_ ) {
				chargeSOI_high = charge;
				chargeSOI_sum = charge;
			} else if ( i == SOI_+1 ) {
				chargeSOI_low = charge;
				chargeSOI_sum += charge;
			}

			if ( bDebug_ ) std::cout << " !!! " << std::hex << did() << " CapId = " << digi[i].capid() << " -> Ped = " << pedestal_[did()][digi[i].capid()] << "\n";
		}
		if ( bDebug_ ) cout << __LINE__ << "\n";
		pChargeHigh->push_back(chargeSOI_high);
		pChargeLow->push_back(chargeSOI_low);
		pChargeSum->push_back(chargeSOI_sum);

		if (regular_fC[4] != 0) pratio5o4->push_back( regular_fC[5] / regular_fC[4] );
		else pratio5o4->push_back(-1.);
		if (regular_fC[5] != 0) pratio6o5->push_back( regular_fC[6] / regular_fC[5] );
		else pratio6o5->push_back(-1.);

		idx++;
	}
	if ( bDebug_ ) cout << __LINE__ << "\n";

	iEvent.put(move(pADC), std::string("ADC"));
	iEvent.put(move(pnfC), std::string("nominalfC"));
	iEvent.put(move(pfC), std::string("regularfC"));
	iEvent.put(move(pDid), std::string("DetId"));
	iEvent.put(move(pCap), std::string("CapId"));
	iEvent.put(move(poverflow), std::string("overflow"));
	iEvent.put(move(pChargeHigh), std::string("chargeHigh"));
	iEvent.put(move(pChargeLow), std::string("chargeLow"));
	iEvent.put(move(pChargeSum), std::string("chargeSum"));

	iEvent.put(move(pratio5o4), std::string("ratio5o4"));
	iEvent.put(move(pratio6o5), std::string("ratio6o5"));
}


void QWZDC2018Producer2::beginRun(const edm::Run &r, const edm::EventSetup & iSetup)
{
	return;
}


DEFINE_FWK_MODULE(QWZDC2018Producer2);
