// system include files
#include <memory>
#include <numeric>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexTools/interface/GeometricAnnealing.h"
#include "RecoVertex/VertexTools/interface/VertexCompatibleWithBeam.h"
#include "RecoVertex/PrimaryVertexProducer/interface/TrackFilterForPVFindingBase.h"
#include "RecoVertex/PrimaryVertexProducer/interface/TrackFilterForPVFinding.h"
#include "RecoVertex/PrimaryVertexProducer/interface/HITrackFilterForPVFinding.h"
#include "RecoVertex/PrimaryVertexProducer/interface/TrackClusterizerInZ.h"
#include "RecoVertex/PrimaryVertexProducer/interface/DAClusterizerInZ_vect.h"
#include "RecoVertex/PrimaryVertexProducer/interface/DAClusterizerInZT_vect.h"
#include "RecoVertex/PrimaryVertexProducer/interface/GapClusterizerInZ.h"
#include "RecoVertex/PrimaryVertexProducer/interface/DAClusterizerInZ.h"
#include "RecoVertex/PrimaryVertexProducer/interface/VertexHigherPtSquared.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"

//
// class declaration
//
class PrimaryVertexRecoveryForUPC : public edm::stream::EDProducer<> {
public:
  PrimaryVertexRecoveryForUPC(const edm::ParameterSet&);
  ~PrimaryVertexRecoveryForUPC() override {};

  void produce(edm::Event&, const edm::EventSetup&) override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // ----------functions ---------------------------
  const auto getTrackFilters(const std::vector<edm::ParameterSet>& conf) const
  {
    std::vector<FILTER_t> res(conf.size());
    size_t i(0);
    for (const auto& filter : conf) {
      auto& r = res[i++];
      const auto& algo = filter.getParameter<std::string>("algorithm");
      if (algo == "filter")
        r.filter.reset(new TrackFilterForPVFinding(filter));
      else if (algo == "filterWithThreshold")
        r.filter.reset(new HITrackFilterForPVFinding(filter));
      else if (algo != "none")
        throw std::logic_error("[ERROR] Invalid cluster algorithm: "+algo);
      r.minNtracks = filter.getParameter<int>("minNtracks");
      r.maxNtracks = filter.getParameter<int>("maxNtracks");
    }
    return res;
  };

  const auto getTrackClusterizers(const std::vector<edm::ParameterSet>& conf) const
  {
    std::vector<CLUS_t> res(conf.size());
    size_t i(0);
    for (const auto& clusterizer : conf) {
      auto& r = res[i++];
      const auto& algo = clusterizer.getParameter<std::string>("algorithm");
      if (algo == "gap")
        r.clusterizer.reset(new GapClusterizerInZ(clusterizer));
      else if (algo == "DA")
        r.clusterizer.reset(new DAClusterizerInZ(clusterizer));
      else if (algo == "DA_vect")
        r.clusterizer.reset(new DAClusterizerInZ_vect(clusterizer));
      else if (algo == "DA2D_vect")
        r.clusterizer.reset(new DAClusterizerInZT_vect(clusterizer));
      else if (algo != "none")
        throw std::logic_error("[ERROR] Invalid cluster algorithm: "+algo);
      r.minNtracks = clusterizer.getParameter<int>("minNtracks");
      r.maxNtracks = clusterizer.getParameter<int>("maxNtracks");
    }
    return res;
  };

  const auto getVertexFitters(const std::vector<edm::ParameterSet>& conf) const
  {
    std::vector<FIT_t> res(conf.size());
    size_t i(0);
    for (const auto& fitter : conf) {
      auto& r = res[i++];
      const auto& algo = fitter.getParameter<std::string>("algorithm");
      if (algo == "KalmanVertexFitter")
        r.fitter.reset(new KalmanVertexFitter());
      else if (algo == "AdaptiveVertexFitter")
        r.fitter.reset(new AdaptiveVertexFitter(GeometricAnnealing(fitter.getParameter<double>("chi2cutoff"))));
      r.vertexSelector.reset(new VertexCompatibleWithBeam(VertexDistanceXY(), fitter.getParameter<double>("maxDistanceToBeam")));
      r.minNdof = fitter.getParameter<double>("minNdof");
      r.useBeamConstraint = fitter.getParameter<bool>("useBeamConstraint");
      r.minNclusters = fitter.getParameter<int>("minNclusters");
    }
    return res;
  };

  const bool goodVertex(const reco::Vertex& pv) {
    return (!pv.isFake() && std::abs(pv.z()) <= 25 && pv.position().Rho() <= 2 && pv.tracksSize() >= 2);
  };

  // ----------member data ---------------------------
  const edm::EDGetTokenT<reco::VertexCollection> pvToken_;
  const edm::EDGetTokenT<reco::TrackCollection> trkToken_;
  const edm::EDGetTokenT<reco::BeamSpot> bsToken_;
  const edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> theTTBToken_;

  struct FILTER_t {
    std::unique_ptr<TrackFilterForPVFindingBase> filter;
    int minNtracks;
    int maxNtracks;
  };
  const std::vector<FILTER_t> trackFilters_;

  struct CLUS_t {
    std::unique_ptr<TrackClusterizerInZ> clusterizer;
    int minNtracks;
    int maxNtracks;
  };
  const std::vector<CLUS_t> trackClusterizers_;

  struct FIT_t {
    std::unique_ptr<VertexFitter<5> > fitter;
    std::unique_ptr<VertexCompatibleWithBeam> vertexSelector;
    bool useBeamConstraint;
    double minNdof;
    int minNclusters;
  };
  const std::vector<FIT_t> vertexFitters_;
};

PrimaryVertexRecoveryForUPC::PrimaryVertexRecoveryForUPC(const edm::ParameterSet& conf) :
    pvToken_(consumes<reco::VertexCollection>(conf.getParameter<edm::InputTag>("primaryVertexLabel"))),
    trkToken_(consumes<reco::TrackCollection>(conf.getParameter<edm::InputTag>("TrackLabel"))),
    bsToken_(consumes<reco::BeamSpot>(conf.getParameter<edm::InputTag>("beamSpotLabel"))),
    theTTBToken_(esConsumes(edm::ESInputTag("", "TransientTrackBuilder"))),
    trackFilters_(getTrackFilters(conf.getParameter<std::vector<edm::ParameterSet> >("TkFilterParameters"))),
    trackClusterizers_(getTrackClusterizers(conf.getParameter<std::vector<edm::ParameterSet> >("TkClusParameters"))),
    vertexFitters_(getVertexFitters(conf.getParameter<std::vector<edm::ParameterSet> >("VtxFitParameters")))
{
  produces<reco::VertexCollection>();
}

void PrimaryVertexRecoveryForUPC::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // get the input collections
  const auto& origPVs = iEvent.get(pvToken_);
  const auto& tracks = iEvent.getHandle(trkToken_);
  const auto& beamSpot = iEvent.get(bsToken_);

  if (tracks->size() < 2) {
    auto result = std::make_unique<reco::VertexCollection>(origPVs);
    iEvent.put(std::move(result));
    return;
  }

  // get primary vertices passing PV filter
  reco::VertexCollection selPVs;
  for (const auto& pv : origPVs)
    if (goodVertex(pv))
      selPVs.emplace_back(pv);

  if (selPVs.size() == 1) {
    auto result = std::make_unique<reco::VertexCollection>(selPVs);
    iEvent.put(std::move(result));
    return;
  }

  // get beamspot and transient tracks
  VertexState bsState(beamSpot);
  const bool validBS = (bsState.error().cxx() > 0. && bsState.error().cyy() > 0. && bsState.error().czz() > 0.);
  const auto allTrk = iSetup.getData(theTTBToken_).build(tracks, beamSpot);
  const int& nAllTrk = allTrk.size();

  // select tracks
  int prevNtrk(1);
  size_t u1(0);
  for (const auto& trackFilter : trackFilters_) {
    u1 += 1;
    if (nAllTrk < trackFilter.minNtracks || nAllTrk > trackFilter.maxNtracks)
      continue;
    const auto& selTrk = trackFilter.filter ? trackFilter.filter->select(allTrk) : allTrk;
    const int& nSelTrk = selTrk.size();
    if (nSelTrk <= prevNtrk)
      continue;
    prevNtrk = nSelTrk;

    // clusterize tracks in Z
    int prevNcltrk(1);
    size_t u2(0);
    for (const auto& trackClusterizer : trackClusterizers_) {
      u2 += 1;
      if (nSelTrk < trackClusterizer.minNtracks || nSelTrk > trackClusterizer.maxNtracks)
        continue;
      auto clusters = trackClusterizer.clusterizer ? trackClusterizer.clusterizer->clusterize(selTrk) : std::vector<std::vector<reco::TransientTrack> >({selTrk});
      clusters.erase(std::remove_if(clusters.begin(), clusters.end(), [](const auto& x) { return x.size() < 2; }), clusters.end());
      const auto& nClTrk = std::accumulate(clusters.cbegin(), clusters.cend(), 0, [](int s, const auto& x){ return s + x.size(); });
      if (nClTrk <= prevNcltrk)
        continue;
      prevNcltrk = nClTrk;
      const int& nCls = clusters.size();

      // fit vertex
      size_t u3(0);
      for (const auto& vertexFitter : vertexFitters_) {
        u3 += 1;
        if (nCls < vertexFitter.minNclusters)
          continue;
        auto result = std::make_unique<reco::VertexCollection>();
        for (const auto& iclus : clusters) {
          if (iclus.size() < 2)
            continue;
          const TransientVertex v(vertexFitter.useBeamConstraint ? vertexFitter.fitter->vertex(iclus, beamSpot) : vertexFitter.fitter->vertex(iclus));
          if (v.isValid() && v.degreesOfFreedom() >= vertexFitter.minNdof && (!validBS || (*vertexFitter.vertexSelector)(v, bsState)) && goodVertex(v)) {
            reco::Vertex p(v);
            reco::Vertex o(p.position(), p.error4D(), u1 + u2*10 + u3*100, p.chi2(), p.ndof(), p.tracks().size());
            for (const auto& t : p.tracks())
              o.add(t, p.trackWeight(t));
            result->emplace_back(o);
          }
        }

        // return new collection if vertices found
        if (!result->empty()) {
          // sort vertices by pt**2 vertex (aka signal vertex tagging)
          std::sort(result->begin(), result->end(), VertexHigherPtSquared());
          iEvent.put(std::move(result));
          return;
        }
      }
    }
  }

  if (selPVs.size() > 1)
    throw std::logic_error("[ERROR] No vertex found even if originally there wrere more than one!");

  // return original collection if no vertices found
  auto result = std::make_unique<reco::VertexCollection>(selPVs.empty() ? origPVs : selPVs);
  iEvent.put(std::move(result));
}

void PrimaryVertexRecoveryForUPC::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  // offlinePrimaryVertices
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("primaryVertexLabel", edm::InputTag("offlinePrimaryVertices"));
  desc.add<edm::InputTag>("beamSpotLabel", edm::InputTag("offlineBeamSpot"));
  desc.add<edm::InputTag>("TrackLabel", edm::InputTag("generalTracks"));
  edm::ParameterSetDescription psd0, psd1, psd2;
  std::vector<edm::ParameterSet> vpsd0, vpsd1, vpsd2;
  // track filters
  psd0.add<std::string>("algorithm", "");
  psd0.add<double>("maxNormalizedChi2", 1.E9);
  psd0.add<double>("minPt", -1.0);
  psd0.add<double>("maxEta", 1.E9);
  psd0.add<double>("maxD0Significance", 1.E9);
  psd0.add<double>("maxD0Error", 1.E9);
  psd0.add<double>("maxDzError", 1.E9);
  psd0.add<std::string>("trackQuality", "any");
  psd0.add<int>("minPixelLayersWithHits", -1);
  psd0.add<int>("minSiliconLayersWithHits", -1);
  psd0.add<int>("numTracksThreshold", -1);
  psd0.add<int>("maxNumTracksThreshold", 1E9);
  psd0.add<double>("minPtTight", -1.0);
  psd0.add<int>("minNtracks", -1);
  psd0.add<int>("maxNtracks", 1E9);
  vpsd0.reserve(5);
  { // PbPb tight parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "filter");
    psd.addParameter<double>("maxNormalizedChi2", 10.0);
    psd.addParameter<double>("minPt", 1.0);
    psd.addParameter<double>("maxEta", 2.4);
    psd.addParameter<double>("maxD0Significance", 2.0);
    psd.addParameter<double>("maxD0Error", 10.0);
    psd.addParameter<double>("maxDzError", 10.0);
    psd.addParameter<std::string>("trackQuality", "highPurity");
    psd.addParameter<int>("minPixelLayersWithHits", 3);
    psd.addParameter<int>("minSiliconLayersWithHits", 5);
    psd.addParameter<int>("minNtracks", 500);
    psd.addParameter<int>("maxNtracks", 1E9);
    vpsd0.emplace_back(psd);
  }{ // PbPb parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "filter");
    psd.addParameter<double>("maxNormalizedChi2", 10.0);
    psd.addParameter<double>("minPt", 0.7);
    psd.addParameter<double>("maxEta", 2.4);
    psd.addParameter<double>("maxD0Significance", 2.0);
    psd.addParameter<double>("maxD0Error", 10.0);
    psd.addParameter<double>("maxDzError", 10.0);
    psd.addParameter<std::string>("trackQuality", "highPurity");
    psd.addParameter<int>("minPixelLayersWithHits", 3);
    psd.addParameter<int>("minSiliconLayersWithHits", 5);
    psd.addParameter<int>("minNtracks", 10);
    psd.addParameter<int>("maxNtracks", 1E9);
    vpsd0.emplace_back(psd);
  }{ // pp parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "filter");
    psd.addParameter<double>("maxNormalizedChi2", 10.0);
    psd.addParameter<double>("minPt", 0.0);
    psd.addParameter<double>("maxEta", 2.4);
    psd.addParameter<double>("maxD0Significance", 4.0);
    psd.addParameter<double>("maxD0Error", 1.0);
    psd.addParameter<double>("maxDzError", 1.0);
    psd.addParameter<std::string>("trackQuality", "any");
    psd.addParameter<int>("minPixelLayersWithHits", 2);
    psd.addParameter<int>("minSiliconLayersWithHits", 5);
    psd.addParameter<int>("minNtracks", 3);
    psd.addParameter<int>("maxNtracks", 1E9);
    vpsd0.emplace_back(psd);
  }{ // high beta* parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "filter");
    psd.addParameter<double>("maxNormalizedChi2", 80.0);
    psd.addParameter<double>("minPt", 0.0);
    psd.addParameter<double>("maxEta", 2.5);
    psd.addParameter<double>("maxD0Significance", 7.0);
    psd.addParameter<double>("maxD0Error", 10.0);
    psd.addParameter<double>("maxDzError", 10.0);
    psd.addParameter<std::string>("trackQuality", "any");
    psd.addParameter<int>("minPixelLayersWithHits", 1);
    psd.addParameter<int>("minSiliconLayersWithHits", 3);
    psd.addParameter<int>("minNtracks", 3);
    psd.addParameter<int>("maxNtracks", 1E9);
    vpsd0.emplace_back(psd);
  }{
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "none");
    psd.addParameter<int>("minNtracks", 2);
    psd.addParameter<int>("maxNtracks", 10);
    vpsd0.emplace_back(psd);
  }
  desc.addVPSet("TkFilterParameters", psd0, vpsd0);
  // track clusterizers
  psd1.add<std::string>("algorithm", "");
  psd1.add<double>("d0CutOff", 3.0);
  psd1.add<double>("Tmin", 2.0);
  psd1.add<double>("delta_lowT", 0.001);
  psd1.add<double>("zmerge", 0.01);
  psd1.add<double>("dzCutOff", 3.0);
  psd1.add<double>("Tpurge", 2.0);
  psd1.add<int>("convergence_mode", 0);
  psd1.add<double>("delta_highT", 0.01);
  psd1.add<double>("Tstop", 0.5);
  psd1.add<double>("coolingFactor", 0.6);
  psd1.add<double>("vertexSize", 0.006);
  psd1.add<double>("uniquetrkweight", 0.8);
  psd1.add<double>("uniquetrkminp", 0.0);
  psd1.add<double>("zrange", 4.0);
  psd1.add<bool>("runInBlocks", false);
  psd1.add<unsigned int>("block_size", 10000);
  psd1.add<double>("overlap_frac", 0.0);
  psd1.add<double>("zSeparation", 1.0);
  psd1.add<int>("minNtracks", -1);
  psd1.add<int>("maxNtracks", 1E9);
  vpsd1.reserve(4);
  { // PbPb parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "gap");
    psd.addParameter<double>("zSeparation", 1.0);
    psd.addParameter<int>("minNtracks", 3);
    psd.addParameter<int>("maxNtracks", 1E9);
    vpsd1.emplace_back(psd);
  }{ // pp parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "DA_vect");
    psd.addParameter<double>("d0CutOff", 3.0);
    psd.addParameter<double>("Tmin", 2.0);
    psd.addParameter<double>("delta_lowT", 0.001);
    psd.addParameter<double>("zmerge", 0.01);
    psd.addParameter<double>("dzCutOff", 3.0);
    psd.addParameter<double>("Tpurge", 2.0);
    psd.addParameter<int>("convergence_mode", 0);
    psd.addParameter<double>("delta_highT", 0.01);
    psd.addParameter<double>("Tstop", 0.5);
    psd.addParameter<double>("coolingFactor", 0.6);
    psd.addParameter<double>("vertexSize", 0.006);
    psd.addParameter<double>("uniquetrkweight", 0.8);
    psd.addParameter<double>("uniquetrkminp", 0.0);
    psd.addParameter<double>("zrange", 4.0);
    psd.addParameter<bool>("runInBlocks", false);
    psd.addParameter<unsigned int>("block_size", 10000);
    psd.addParameter<double>("overlap_frac", 0.0);
    psd.addParameter<int>("minNtracks", 3);
    psd.addParameter<int>("maxNtracks", 1E9);
    vpsd1.emplace_back(psd);
  }{ // high beta* parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "DA_vect");
    psd.addParameter<double>("d0CutOff", 4.0);
    psd.addParameter<double>("Tmin", 4.0);
    psd.addParameter<double>("delta_lowT", 0.001);
    psd.addParameter<double>("zmerge", 0.02);
    psd.addParameter<double>("dzCutOff", 5.0);
    psd.addParameter<double>("Tpurge", 1.0);
    psd.addParameter<int>("convergence_mode", 0);
    psd.addParameter<double>("delta_highT", 0.01);
    psd.addParameter<double>("Tstop", 1.0);
    psd.addParameter<double>("coolingFactor", 0.6);
    psd.addParameter<double>("vertexSize", 0.01);
    psd.addParameter<double>("uniquetrkweight", 0.9);
    psd.addParameter<double>("uniquetrkminp", 0.0);
    psd.addParameter<double>("zrange", 4.0);
    psd.addParameter<bool>("runInBlocks", false);
    psd.addParameter<unsigned int>("block_size", 10000);
    psd.addParameter<double>("overlap_frac", 0.0);
    psd.addParameter<int>("minNtracks", 3);
    psd.addParameter<int>("maxNtracks", 1E9);
    vpsd1.emplace_back(psd);
  }{
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "none");
    psd.addParameter<int>("minNtracks", 2);
    psd.addParameter<int>("maxNtracks", 4);
    vpsd1.emplace_back(psd);
  }
  desc.addVPSet("TkClusParameters", psd1, vpsd1);
  // vertex fitters
  psd2.add<std::string>("algorithm", "");
  psd2.add<double>("maxDistanceToBeam", 1.E9);
  psd2.add<double>("chi2cutoff", 1.E9);
  psd2.add<double>("minNdof", -1.0);
  psd2.add<bool>("useBeamConstraint", false);
  psd2.add<int>("minNclusters", -1);
  vpsd2.reserve(6);
  { // PbPb and pp parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "AdaptiveVertexFitter");
    psd.addParameter<double>("maxDistanceToBeam", 1.0);
    psd.addParameter<double>("chi2cutoff", 2.5);
    psd.addParameter<double>("minNdof", 0.0);
    psd.addParameter<bool>("useBeamConstraint", false);
    psd.addParameter<int>("minNclusters", 2);
    vpsd2.emplace_back(psd);
  }{ // high beta* parameters
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "AdaptiveVertexFitter");
    psd.addParameter<double>("maxDistanceToBeam", 1.0);
    psd.addParameter<double>("chi2cutoff", 4.0);
    psd.addParameter<double>("minNdof", -1.1);
    psd.addParameter<bool>("useBeamConstraint", false);
    psd.addParameter<int>("minNclusters", 2);
    vpsd2.emplace_back(psd);
  }{ // high beta* parameters + extended beam distance
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "AdaptiveVertexFitter");
    psd.addParameter<double>("maxDistanceToBeam", 2.0);
    psd.addParameter<double>("chi2cutoff", 4.0);
    psd.addParameter<double>("minNdof", -1.1);
    psd.addParameter<bool>("useBeamConstraint", false);
    psd.addParameter<int>("minNclusters", 1);
    vpsd2.emplace_back(psd);
  }{ // kalman vertex fitter
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "KalmanVertexFitter");
    psd.addParameter<double>("maxDistanceToBeam", 2.0);
    psd.addParameter<double>("minNdof", 0.0);
    psd.addParameter<bool>("useBeamConstraint", false);
    psd.addParameter<int>("minNclusters", 1);
    vpsd2.emplace_back(psd);
  }{ // high beta* parameters + beam constraint
    edm::ParameterSet psd;
    psd.addParameter<std::string>("algorithm", "AdaptiveVertexFitter");
    psd.addParameter<double>("maxDistanceToBeam", 1.0);
    psd.addParameter<double>("chi2cutoff", 4.0);
    psd.addParameter<double>("minNdof", 1.0);
    psd.addParameter<bool>("useBeamConstraint", true);
    psd.addParameter<int>("minNclusters", 1);
    vpsd2.emplace_back(psd);
  }
  desc.addVPSet("VtxFitParameters", psd2, vpsd2);
  descriptions.add("primaryVertexRecoveryForUPC", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
//define this as a plug-in
DEFINE_FWK_MODULE(PrimaryVertexRecoveryForUPC);
