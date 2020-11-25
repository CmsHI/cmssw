// -*- C++ -*-
//
// Package:    ParticleTowerProducer
// Class:      ParticleTowerProducer
// 
/**\class ParticleTowerProducer ParticleTowerProducer.cc RecoHI/ParticleTowerProducer/src/ParticleTowerProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Yetkin Yilmaz,32 4-A08,+41227673039,
//         Created:  Thu Jan 20 19:53:58 CET 2011
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "RecoHI/HiJetAlgos/interface/ParticleTowerProducer.h"

#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/CaloTowers/interface/CaloTowerCollection.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloTopology/interface/CaloTopology.h"

#include "TMath.h"
#include "TRandom.h"



//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
ParticleTowerProducer::ParticleTowerProducer(const edm::ParameterSet& iConfig):
   geo_(nullptr)
{
   //register your products  
  src_ = consumes<reco::PFCandidateCollection>(iConfig.getParameter<edm::InputTag>("src"));
  useHF_ = iConfig.getParameter<bool>("useHF");
  
  produces<CaloTowerCollection>();
  
  //now do what ever other initialization is needed
  random_ = new TRandom();
  PI = TMath::Pi();
  


}


ParticleTowerProducer::~ParticleTowerProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
  delete random_;
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
ParticleTowerProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   if(!geo_){
      edm::ESHandle<CaloGeometry> pG;
      iSetup.get<CaloGeometryRecord>().get(pG);
      geo_ = pG.product();
   }


   resetTowers(iEvent, iSetup);

   edm::Handle<reco::PFCandidateCollection> inputsHandle;
   iEvent.getByToken(src_, inputsHandle);
   
   for(reco::PFCandidateCollection::const_iterator ci  = inputsHandle->begin(); ci!=inputsHandle->end(); ++ci)  {

    const reco::PFCandidate& particle = *ci;
    
    // put a cutoff if you want
    //if(particle.et() < 0.3) continue;      
    
    double eta = particle.eta();

    int ieta = eta2ieta(eta);
    int iphi = phi2iphi(particle.phi(),ieta);
       
    if(!useHF_ && abs(ieta) > 29 ) continue;

    EtaPhi ep(ieta,iphi);
    towers_[ep] += particle.et();

   }
   
   
   auto prod = std::make_unique<CaloTowerCollection>();

   for ( EtaPhiMap::const_iterator iter = towers_.begin();
	 iter != towers_.end(); ++iter ){
     
     EtaPhi ep = iter->first;
     double et = iter->second;

     int ieta = ep.first;
     int iphi = ep.second;

     CaloTowerDetId newTowerId(ieta,iphi); // totally dummy id

     if(et>0){

       if(!useHF_ && abs(ieta) > 29) continue;

       // currently sets et =  pt, mass to zero
       // pt, eta , phi, mass
       reco::Particle::PolarLorentzVector p4(et,ieta2eta(ieta),iphi2phi(iphi,ieta),0.);

       GlobalPoint dummypoint(p4.x(),p4.y(),p4.z());
       CaloTower newTower(newTowerId,et,0,0,0,0,p4,dummypoint,dummypoint);
       prod->push_back(newTower);     
     }
   }

   
   //For reference, Calo Tower Constructors

   /*
   CaloTower(const CaloTowerDetId& id, 
             double emE, double hadE, double outerE,
             int ecal_tp, int hcal_tp,
             const PolarLorentzVector p4,
       GlobalPoint emPosition, GlobalPoint hadPosition);
 
   CaloTower(const CaloTowerDetId& id, 
             double emE, double hadE, double outerE,
             int ecal_tp, int hcal_tp,
             const LorentzVector p4,
       GlobalPoint emPosition, GlobalPoint hadPosition);
   */


   iEvent.put(std::move(prod));


}

// ------------ method called once each job just before starting event loop  ------------
void 
ParticleTowerProducer::beginJob()
{
  // tower edges from fast sim, used starting at index 30 for the HF
  const double etatow[42] = {0.000, 0.087, 0.174, 0.261, 0.348, 0.435, 0.522, 0.609, 0.696, 0.783, 0.870, 0.957, 1.044, 1.131, 1.218, 1.305, 1.392, 1.479, 1.566, 1.653, 1.740, 1.830, 1.930, 2.043, 2.172, 2.322, 2.500, 2.650, 2.853, 3.000, 3.139, 3.314, 3.489, 3.664, 3.839, 4.013, 4.191, 4.363, 4.538, 4.716, 4.889, 5.191};
  
  for(int i=0;i<42;i++){
    etaedge[i]=etatow[i];
  }

}

// ------------ method called once each job just after ending the event loop  ------------
void 
ParticleTowerProducer::endJob() {
}


void ParticleTowerProducer::resetTowers(edm::Event& iEvent,const edm::EventSetup& iSetup)
{

  towers_.clear();

}



// Taken from FastSimulation/CalorimeterProperties/src/HCALProperties.cc
// Note this returns an abs(ieta)
int ParticleTowerProducer::eta2ieta(double eta) const {
  // binary search in the array of towers eta edges

  int ieta = 1;
  double xeta = fabs(eta);
  while (xeta > etaedge[ieta] && ieta < ietaMax - 1) {
    ++ieta;
  }

  if (eta < 0)
    ieta = -ieta;
  return ieta;
}

int ParticleTowerProducer::phi2iphi(double phi, int ieta) const {
  
  if(phi<0) phi += 2.*PI;
  else if(phi> 2.*PI) phi -= 2.*PI;

  int Nphi = 72;
  int n = 1;
  if(abs(ieta)>20) n = 2;
  if(abs(ieta)>=40) n = 4;

  int iphi = (int) TMath::Ceil(phi/2.0/PI*Nphi/n);

  iphi = n * (iphi - 1) + 1;

  return iphi;

}

double ParticleTowerProducer::iphi2phi(int iphi, int ieta) const {


  double phi = 0;
  int Nphi = 72;

  int n = 1;
  if(abs(ieta)>20) n = 2;
  if(abs(ieta)>=40) n = 4;

  int myphi = (iphi - 1)/n + 1;

  phi = 2.*PI*(myphi-0.5)/Nphi*n;
  while(phi > PI) phi -= 2.*PI;

  return phi;

}



double ParticleTowerProducer::ieta2eta(int ieta) const {

  int sign = 1;
  if(ieta < 0){
    sign = -1;
    ieta = -ieta;
  }

  double eta = sign*(etaedge[ieta] + etaedge[ieta-1])/2.;
  return eta;
}




