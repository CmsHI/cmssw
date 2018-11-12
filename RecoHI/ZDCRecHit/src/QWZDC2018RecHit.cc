/*
 * =====================================================================================
 *
 *       Filename:  QWZDC2018RecHit.cc
 *
 *    Description:  ZDCRecHitCollection producer for 2018 PbPb runs.
 *
 *        Version:  1.0
 *        Created:  11/08/2018 17:02:12
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Quan Wang quan.wang@cern.ch
 *   Organization:  Univ. of Kansas
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HcalRecHit/interface/HcalRecHitDefs.h"
#include "DataFormats/HcalDetId/interface/HcalZDCDetId.h"

#include <iostream>

class QWZDC2018RecHit : public edm::EDProducer {
public:
	explicit QWZDC2018RecHit(const edm::ParameterSet&);
	~QWZDC2018RecHit();

private:
	virtual void produce(edm::Event&, const edm::EventSetup&) override;


	// tags
	edm::InputTag		srcDid_;
	edm::InputTag		srcfC_;
	bool			bNpeak_;

	std::map<uint32_t, std::string>		cname2str_;
	std::map<uint32_t, double>		calib_;
	double			Pscale_;
	double			Mscale_;
};


QWZDC2018RecHit::QWZDC2018RecHit(const edm::ParameterSet& pset) :
	srcDid_(pset.getUntrackedParameter<edm::InputTag>("srcDetId")),
	srcfC_(pset.getUntrackedParameter<edm::InputTag>("srcfC")),
	bNpeak_(pset.getUntrackedParameter<bool>("bFilter", false))
{
	consumes<std::vector<double>>(srcDid_);
	consumes<std::vector<double>>(srcfC_);

	// Care only ZDC EM and HAD channels
	// RPD channels not considered now
	std::map<std::string, uint32_t>		cname2did_;
	for ( int channel = 1; channel < 5; channel++ ) {
		// HAD
		auto did = HcalZDCDetId(HcalZDCDetId::HAD, true, channel);
		cname2did_[ std::string("hZDCP_HAD") + std::to_string(channel) ] = did();
		cname2str_[ did() ] = std::string("hZDCP_HAD") + std::to_string(channel);

		did = HcalZDCDetId(HcalZDCDetId::HAD, false, channel);
		cname2did_[ std::string("hZDCM_HAD") + std::to_string(channel) ] = did();
		cname2str_[ did() ] = std::string("hZDCM_HAD") + std::to_string(channel);
	}

	for ( int channel = 1; channel < 6; channel++ ) {
		// EM
		auto did = HcalZDCDetId(HcalZDCDetId::EM, true, channel);
		cname2did_[ std::string("hZDCP_EM") + std::to_string(channel) ] = did();
		cname2str_[ did() ] = std::string("hZDCP_EM") + std::to_string(channel);

		did = HcalZDCDetId(HcalZDCDetId::EM, false, channel);
		cname2did_[ std::string("hZDCM_EM") + std::to_string(channel) ] = did();
		cname2str_[ did() ] = std::string("hZDCM_EM") + std::to_string(channel);
	}

	std::vector<edm::ParameterSet> calib = pset.getParameter<std::vector<edm::ParameterSet> >("ZDCCalib");

	for ( auto ch = calib.begin(); ch != calib.end(); ch++ ) {
		auto ch_str = ch->getUntrackedParameter<std::string>("object");
		if ( ch_str == "Pscale" ) {
			Pscale_ = ch->getUntrackedParameter<double>("calib");
		} else if ( ch_str == "Mscale" ) {
			Mscale_ = ch->getUntrackedParameter<double>("calib");
		} else {
			calib_[cname2did_[ch_str]] = ch->getUntrackedParameter<double>("calib");
		}
	}

	produces<ZDCRecHitCollection>();
	if ( bNpeak_ ) {
		produces<double>("NpeakM");
		produces<double>("NpeakP");
	}
	return;
}

QWZDC2018RecHit::~QWZDC2018RecHit()
{
	return;
}


void QWZDC2018RecHit::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	auto prec = std::make_unique<ZDCRecHitCollection>();

	edm::Handle<std::vector<double>> psrcDid;
	edm::Handle<std::vector<double>> psrcfC;

	iEvent.getByLabel( srcDid_, psrcDid );
	iEvent.getByLabel( srcfC_,  psrcfC );

	std::map<std::string, double*> charge;
	std::map<uint32_t, double*> energy;

	int NS = psrcfC->size() / psrcDid->size();

	int idx = 0;
	for ( auto it = psrcDid->begin(); it != psrcDid->end(); it++ ) {
		if ( cname2str_.find(uint32_t(*it)) == cname2str_.end() ) continue;

		charge[ cname2str_[uint32_t(*it)] ] = new double[NS];
		energy[ uint32_t(*it) ] = new double[NS];
		for ( int ts = 0; ts < NS; ts++ ) {
			charge[ cname2str_[uint32_t(*it)] ][ts] = (*psrcfC)[idx];
			energy[ uint32_t(*it) ][ts] = (*psrcfC)[idx] * calib_[uint32_t(*it)];
			idx++;
		}
	}

	for ( auto it = psrcDid->begin(); it != psrcDid->end(); it++ ) {
		if ( energy.find(uint32_t(*it)) == energy.end() ) continue;
		double E = energy[uint32_t(*it)][4] + energy[uint32_t(*it)][5] + energy[uint32_t(*it)][6];
		HcalZDCDetId did = HcalZDCDetId( uint32_t(*it) );
		if ( did.zside() > 0 ) {
			E /= Pscale_;
		} else {
			E /= Mscale_;
		}
		prec->push_back( ZDCRecHit( HcalZDCDetId(uint32_t(*it)), E, 0, E) );
	}

	iEvent.put(std::move(prec));

	if ( bNpeak_ ) {
		int ts1 = std::distance( charge[std::string("hZDCP_HAD1")], std::max_element(charge[std::string("hZDCP_HAD1")], charge[std::string("hZDCP_HAD1")]+NS) );
		int ts2 = std::distance( charge[std::string("hZDCP_HAD2")], std::max_element(charge[std::string("hZDCP_HAD2")], charge[std::string("hZDCP_HAD2")]+NS) );
		if ( (ts1==4 or ts1==5) and (ts2==4 or ts2==5) ) {
			iEvent.put(std::make_unique<double>(1.), "NpeakP");
		} else {
			iEvent.put(std::make_unique<double>(0.), "NpeakP");
		}

		ts1 = std::distance( charge[std::string("hZDCM_HAD1")], std::max_element(charge[std::string("hZDCM_HAD1")], charge[std::string("hZDCM_HAD1")]+NS) );
		ts2 = std::distance( charge[std::string("hZDCM_HAD2")], std::max_element(charge[std::string("hZDCM_HAD2")], charge[std::string("hZDCM_HAD2")]+NS) );
		if ( (ts1==4 or ts1==5) and (ts2==4 or ts2==5) ) {
			iEvent.put(std::make_unique<double>(1.), "NpeakM");
		} else {
			iEvent.put(std::make_unique<double>(0.), "NpeakM");
		}
	}

	return;
}

DEFINE_FWK_MODULE(QWZDC2018RecHit);
