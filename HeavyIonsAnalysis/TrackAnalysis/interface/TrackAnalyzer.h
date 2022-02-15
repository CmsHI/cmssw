#ifndef TRKANALYZER_H
#define TRKANALYZER_H

// system include files
#include <memory>
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <functional>

// CMSSW user include files
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/RecoCandidate/interface/TrackAssociation.h"
#include "DataFormats/TrackReco/interface/DeDxData.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit1D.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticleFwd.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingVertex.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingVertexContainer.h"
#include "SimDataFormats/TrackingHit/interface/PSimHit.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "SimTracker/Records/interface/TrackAssociatorRecord.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Common/interface/ValueMap.h"

// Particle Flow
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/ParticleFlowReco/interface/PFCluster.h"
#include "DataFormats/ParticleFlowReco/interface/PFClusterFwd.h"

// Vertex significance
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"

// Root include files
#include "TTree.h"

class TrackAnalyzer : public edm::EDAnalyzer {

  public:
    explicit TrackAnalyzer(const edm::ParameterSet&);
    ~TrackAnalyzer() override;

  private:
    void beginJob() override;
    void analyze(const edm::Event&, const edm::EventSetup&) override;
    void endJob() override;

    void fillVertices(const edm::Event& iEvent);
    void fillTracks(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    void clearVectors();

     // ----------member data ---------------------------
     bool doTrack_;
     double trackPtMin_; 

     edm::InputTag vertexSrcLabel_;
     edm::EDGetTokenT<reco::VertexCollection> vertexSrc_;

     edm::InputTag packedCandLabel_;
     edm::EDGetTokenT<edm::View<pat::PackedCandidate>> packedCandSrc_;
     
     edm::InputTag lostTracksLabel_;
     edm::EDGetTokenT<edm::View<pat::PackedCandidate>> lostTracksSrc_;

     edm::EDGetTokenT<reco::BeamSpot> beamSpotProducer_;

     edm::InputTag chi2MapLabel_;
     edm::EDGetTokenT<edm::ValueMap<float>> chi2Map_;
     edm::InputTag chi2MapLostLabel_;
     edm::EDGetTokenT<edm::ValueMap<float>> chi2MapLost_;

     edm::Service<TFileService> fs;

     int iMaxPtSumVtx;
 
     // Root object
     TTree* trackTree_;

     //Branch entries
     int nRun;
     int nEv;
     int nLumi;

     int nVtx;
     std::vector< float > xVtx;
     std::vector< float > yVtx;
     std::vector< float > zVtx;
     std::vector< float > xErrVtx;
     std::vector< float > yErrVtx;
     std::vector< float > zErrVtx;
     std::vector< float > chi2Vtx;
     std::vector< float > ndofVtx;
     std::vector< bool > isFakeVtx;
     std::vector< int > nTracksVtx;
     std::vector< float > ptSumVtx;

     int nTrk;
     std::vector< float > trkPt;
     std::vector< float > trkPtError;
     std::vector< float > trkEta;
     std::vector< float > trkPhi;
     std::vector< char > trkCharge;
     std::vector< int > trkPDGId;
     std::vector< char > trkNHits;
     std::vector< char > trkNLostHits;
     std::vector< char > trkNPixHits;
     std::vector< char > trkNLayers;
     std::vector< bool > highPurity;
     std::vector< float > trkNormChi2;

     std::vector< float > pfEnergy;
     std::vector< float > pfEcal;
     std::vector< float > pfHcal;

     std::vector< int > trkAssociatedVtxIndx;
     std::vector< int > trkAssociatedVtxQuality;
     std::vector< float > trkDzAssociatedVtx;
     std::vector< float > trkDzErrAssociatedVtx;
     std::vector< float > trkDxyAssociatedVtx;
     std::vector< float > trkDxyErrAssociatedVtx;
     
     std::vector< int > trkFirstVtxQuality;
     std::vector< float > trkDzFirstVtx;
     std::vector< float > trkDzErrFirstVtx;
     std::vector< float > trkDxyFirstVtx;
     std::vector< float > trkDxyErrFirstVtx;
};

void TrackAnalyzer::clearVectors(){
  nVtx = 0;
  xVtx.clear();
  yVtx.clear();
  zVtx.clear();
  xErrVtx.clear();
  yErrVtx.clear();
  zErrVtx.clear();
  chi2Vtx.clear();
  ndofVtx.clear();
  isFakeVtx.clear();
  nTracksVtx.clear();
  ptSumVtx.clear();

  nTrk = 0;
  trkPt.clear();
  trkPtError.clear();
  trkEta.clear();
  trkPhi.clear();
  trkCharge.clear();
  trkPDGId.clear();
  trkNHits.clear();
  trkNPixHits.clear();
  trkNLayers.clear();
  trkNormChi2.clear();
  highPurity.clear();

  pfEnergy.clear();
  pfEcal.clear();
  pfHcal.clear();

  trkAssociatedVtxIndx.clear();
  trkAssociatedVtxQuality.clear();
  trkDzAssociatedVtx.clear();
  trkDzErrAssociatedVtx.clear();
  trkDxyAssociatedVtx.clear();
  trkDxyErrAssociatedVtx.clear();
  
  trkFirstVtxQuality.clear();
  trkDzFirstVtx.clear();
  trkDzErrFirstVtx.clear();
  trkDxyFirstVtx.clear();
  trkDxyErrFirstVtx.clear();
}

#endif     
