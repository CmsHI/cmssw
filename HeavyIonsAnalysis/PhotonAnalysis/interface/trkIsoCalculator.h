#ifndef trkIsoCalculator_h
#define trkIsoCalculator_h

//#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"

class trkIsoCalculator
{
  public:
    trkIsoCalculator();
    void set(const edm::Event &iEvent, const edm::EDGetTokenT<std::vector<reco::Track>> & trackSrc,
                                       const edm::EDGetTokenT<std::vector<float>> & mvaSrc,
                                       const edm::EDGetTokenT<edm::View<reco::PFCandidate>> & pfCandidates,
                                       const reco::Vertex& pv,
                                       std::string strCollision);
    double getTrkIso(double egEta, double egPhi, double r1=0.4, double r2=0.00, double threshold=0, double jWidth=0.0, bool applyTrkID = false);
    double getTrkIsoSubUE(double egEta, double egPhi, double r1=0.4, double r2=0.00, double threshold=0, double jWidth=0.0, bool applyTrkID = false, bool excludeCone = false);

    std::string strTrkQuality;
    bool applyMVA;
    bool doMapTrk2PfCand;

    enum CollisionSystem {
      undef = 0,
      pp15 = 1,
      pbpb15 = 2,
      pp17 = 3,
      pbpb18 = 4,
     };

    CollisionSystem collSys;

  private:
    bool passedTrkSelection(const reco::Track & trk, unsigned index);
    int getMatchedPfCand(unsigned indexTrk);
    void makeMapTrk2PfCand();

    edm::Handle<std::vector<reco::Track>> tracks_;
    edm::Handle<std::vector<float>> mvas_;
    edm::Handle<edm::View<reco::PFCandidate>> pfCands;
    reco::Vertex vtx_;

    std::unordered_map<int, int> track_pfcand_map;
};

#endif
