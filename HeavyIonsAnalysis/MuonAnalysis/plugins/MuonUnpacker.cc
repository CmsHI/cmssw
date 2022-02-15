#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "MuonAnalysis/MuonAssociators/interface/PropagateToMuon.h"


namespace pat {

  class MuonUnpacker : public edm::stream::EDProducer<> {

    public:

      explicit MuonUnpacker(const edm::ParameterSet & iConfig):
          muonSelectors_(iConfig.getParameter<std::vector<std::string> >("muonSelectors")),
          muonToken_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
          pc2TrackToken_(consumes<edm::Association<reco::TrackCollection> >(iConfig.getParameter<edm::InputTag>("tracks"))),
          primaryVertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("primaryVertices"))),
          beamSpotToken_(consumes<reco::BeamSpot>(iConfig.getParameter<edm::InputTag>("beamSpot"))),
          trackBuilderToken_(esConsumes(edm::ESInputTag("", "TransientTrackBuilder"))),
          candidateMuonIDToken_(getPackedCandidateMap(muonSelectors_)),
          propToMuon_(getMuonPropagator(iConfig))
      {
        produces<pat::MuonCollection>();
      };
      ~MuonUnpacker() override {};

      void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override;

      static void fillDescriptions(edm::ConfigurationDescriptions&);

    private:

      typedef std::map<std::string, std::map<std::string, edm::EDGetTokenT<pat::PackedCandidateRefVector> > > PackedCandidateRefVectorMap;

      const std::vector<std::string> muonSelectors_;
      const edm::EDGetTokenT<pat::MuonCollection> muonToken_;
      const edm::EDGetTokenT<edm::Association<reco::TrackCollection> > pc2TrackToken_;
      const edm::EDGetTokenT<reco::VertexCollection> primaryVertexToken_;
      const edm::EDGetTokenT<reco::BeamSpot> beamSpotToken_;
      const edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> trackBuilderToken_;
      const PackedCandidateRefVectorMap candidateMuonIDToken_;
      const std::unique_ptr<PropagateToMuon> propToMuon_;

      PackedCandidateRefVectorMap getPackedCandidateMap(const std::vector<std::string>& v)
      {
        PackedCandidateRefVectorMap m;
        for (const auto& sel: v) {
          m["packedPFCandidate"][sel] = consumes<pat::PackedCandidateRefVector>(edm::InputTag("packedCandidateMuonID", "pfCandidates"+sel));
          m["lostTrack"][sel] = consumes<pat::PackedCandidateRefVector>(edm::InputTag("packedCandidateMuonID", "lostTracks"+sel));
        }
        return m;
      };

      PropagateToMuon* getMuonPropagator(const edm::ParameterSet& iConfig)
      {
        if (iConfig.getParameter<bool>("addPropToMuonSt")) {
          edm::ParameterSet conf;
          conf.addParameter("useSimpleGeometry", true);
          conf.addParameter("useTrack", std::string("none"));
          conf.addParameter("useState", std::string("atVertex"));
          conf.addParameter("fallbackToME1", true);
          conf.addParameter("useMB2InOverlap", true);
          conf.addParameter("useStation2", true);
          return new PropagateToMuon(conf);
        }
        return nullptr;
      };

      void addMuon(pat::Muon&, const pat::PackedCandidateRef&, const bool&,
                   const reco::TrackRef&, const TransientTrackBuilder&,
                   const reco::Vertex&, const reco::BeamSpot&, std::map<std::string, bool>) const;

  };

}

void pat::MuonUnpacker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // extract input information
  const auto& muons = iEvent.get(muonToken_);
  const auto& pc2Track = iEvent.get(pc2TrackToken_);
  const auto& primaryVertex = iEvent.get(primaryVertexToken_)[0];
  const auto& beamSpot = iEvent.get(beamSpotToken_);
  const auto& trackBuilder = iSetup.getData(trackBuilderToken_);

  // extract candidate map
  std::map<std::string, std::map<pat::PackedCandidateRef, std::map<std::string, bool> > > candidateMuonIDs;
  for (const auto& n : candidateMuonIDToken_) {
    for (const auto& s: n.second)
      for (const auto& c : iEvent.get(s.second))
        candidateMuonIDs[n.first][c][s.first] = true;
  }

  // initialize output muon collection
  auto output = std::make_unique<pat::MuonCollection>(muons);
  // clear trigger info
  for (auto& muon : *output)
    const_cast<TriggerObjectStandAloneCollection&>(muon.triggerObjectMatches()).clear();

  // find high-purity muons
  std::vector<size_t> hpMuonIndexV;
  for (size_t i=0; i<output->size(); i++) {
    const auto& muon = output->at(i);
    if (muon.innerTrack().isNonnull() && muon.innerTrack()->quality(reco::TrackBase::highPurity))
      hpMuonIndexV.emplace_back(i);
  }

  // extract muons from packedCandidate collections
  for (const auto& n : candidateMuonIDs) {
    const bool isLostTrack = (n.first=="lostTrack");
    // loop over packed candidates
    for (const auto& c : n.second) {
      const auto& cand = c.first;
      const auto& selMap = c.second;
      const auto& track = pc2Track.get(cand.id(), cand.key());
      const bool isEGamma = (std::abs(cand->pdgId())==11 || cand->pdgId()==22);

      // check if candidate is in muon collection
      bool isIncluded(false);
      for (const auto& i : hpMuonIndexV) {
        const auto& muon = output->at(i);
        const auto& obj = muon.originalObjectRef();
        if (obj.id()==cand.id())
          isIncluded = (obj.key()==cand.key());
        else if (isLostTrack || obj.isNull()) {
          const auto& mtrk = muon.innerTrack();
          if (mtrk->charge()!=track->charge() || std::abs(mtrk->eta()-track->eta())>1E-3) continue;
          if (isLostTrack || !isEGamma)
            isIncluded = (mtrk->numberOfValidHits()==track->numberOfValidHits() && std::abs(deltaPhi(mtrk->phi(), track->phi()))<1E-3 && std::abs((mtrk->pt()-track->pt())/mtrk->pt())<1E-2);
          else
            isIncluded = (std::abs(mtrk->dz()-track->dz())<2E-2 && std::abs(deltaPhi(mtrk->phi(), track->phi()))<2E-2);
          // if found, assing candidate reference to muon
          if (isIncluded)
            const_cast<reco::CandidatePtr&>(obj) = reco::CandidatePtr(cand.id(), cand.get(), cand.key());
        }
        if (isIncluded) break;
      }
      if (isIncluded) continue;

      // create muon object
      pat::Muon muon;
      addMuon(muon, cand, !isLostTrack, track, trackBuilder, primaryVertex, beamSpot, selMap);
      output->emplace_back(muon);
    }
  }

  // propagate muon position to 2nd muon station (used for L1 muon matching)
  if (propToMuon_) {
    propToMuon_->init(iSetup);
    for (auto& muon : *output) {
      if (muon.track().isNull()) continue;
      const auto& fts = propToMuon_->extrapolate(*muon.track());
      if (!fts.isValid()) continue;
      muon.addUserFloat("l1Eta", fts.globalPosition().eta());
      muon.addUserFloat("l1Phi", fts.globalPosition().phi());
    }
  }
  
  iEvent.put(std::move(output));
}

void pat::MuonUnpacker::addMuon(pat::Muon& muon, const pat::PackedCandidateRef& cand, const bool& isPF,
                                const reco::TrackRef& track, const TransientTrackBuilder& trackBuilder,
                                const reco::Vertex& primaryVertex, const reco::BeamSpot& beamSpot, std::map<std::string, bool> selMap) const {
  // add basic information
  muon.setP4(math::PtEtaPhiMLorentzVector(track->pt(), track->eta(), track->phi(), 0.105658369));
  muon.setCharge(track->charge());
  muon.setVertex(track->vertex());
  muon.setPdgId(-13 * muon.charge());
  muon.setStatus(isPF ? 1 : 2);

  // add candidate reference
  const_cast<reco::CandidatePtr&>(muon.originalObjectRef()) = reco::CandidatePtr(cand.id(), cand.get(), cand.key());

  // add track information
  muon.setInnerTrack(track);
  muon.setBestTrack(reco::Muon::InnerTrack);
  muon.setTunePBestTrack(reco::Muon::InnerTrack);
  muon.embedTrack();
  muon.setNumberOfValidHits(track->numberOfValidHits());
  muon.setNormChi2(track->normalizedChi2());

  // add vertex information
  muon.setDB(track->dxy(primaryVertex.position()), track->dxyError(primaryVertex.position(), primaryVertex.covariance()), pat::Muon::PV2D);
  muon.setDB(track->dxy(beamSpot), track->dxyError(beamSpot), pat::Muon::BS2D);
  muon.setDB(track->dz(primaryVertex.position()), std::hypot(track->dzError(), primaryVertex.zError()), pat::Muon::PVDZ);

  const auto& tt = trackBuilder.build(*track);
  const auto& resultPV = IPTools::signedImpactParameter3D(tt, GlobalVector(track->px(), track->py(), track->pz()), primaryVertex);
  muon.setDB(resultPV.second.value(), resultPV.second.error(), pat::Muon::PV3D);
  reco::Vertex vBeamspot(beamSpot.position(), beamSpot.rotatedCovariance3D());
  const auto& resultBS = IPTools::signedImpactParameter3D(tt, GlobalVector(track->px(), track->py(), track->pz()), vBeamspot);
  muon.setDB(resultBS.second.value(), resultBS.second.error(), pat::Muon::BS3D);

  // determine muon selectors
  bool isTrackerMuon = selMap["AllTrackerMuons"] || selMap["TMOneStationTight"];
  bool isGlobalMuon = selMap["AllGlobalMuons"] || cand->isGlobalMuon();
  bool isStandAloneMuon = selMap["AllStandAloneMuons"] || cand->isStandAloneMuon();
  bool isPFMuon = isPF && std::abs(cand->pdgId())==13;
  bool isHPMuon = track->quality(reco::Track::highPurity);
  bool isLooseMuon = isPFMuon || isGlobalMuon || isTrackerMuon;
  bool isTMOneStationTight = selMap["TMOneStationTight"];
  bool isSoftMuon = isTMOneStationTight && isHPMuon &&
                    track->hitPattern().trackerLayersWithMeasurement()>5 && track->hitPattern().pixelLayersWithMeasurement()>0 &&
                    std::abs(track->dxy(primaryVertex.position()))<0.3 && std::abs(track->dz(primaryVertex.position()))<20.;

  // add muon selectors
  unsigned int selectors(0);
  if (isLooseMuon)
    selectors |= reco::Muon::CutBasedIdLoose;
  if (isSoftMuon)
    selectors |= reco::Muon::SoftCutBasedId;
  muon.setSelectors(selectors);

  // add muon types
  unsigned int type(0);
  if (isTrackerMuon)
    type |= reco::Muon::TrackerMuon;
  if (isStandAloneMuon)
    type |= reco::Muon::StandAloneMuon;
  if (isGlobalMuon) {
    type |= reco::Muon::GlobalMuon;
    muon.setGlobalTrack(track);
    muon.embedCombinedMuon();
  }
  if (isPFMuon) {
    type |= reco::Muon::PFMuon;
    muon.setPFP4(cand->p4());
    muon.setPfEcalEnergy(cand->energy()*cand->caloFraction()*(1. - cand->hcalFraction()));
  }
  muon.setType(type);

  // add TMOneStationTight
  if (isTMOneStationTight) {
    reco::MuonSegmentMatch seg;
    seg.hasZed_ = true; seg.hasPhi_ = true; seg.t0 = 0;
    seg.mask = (reco::MuonSegmentMatch::BelongsToTrackByDR | reco::MuonSegmentMatch::BestInStationByDR | reco::MuonSegmentMatch::BestInChamberByDR);
    reco::MuonChamberMatch match({{seg}, {}, {}, {}, {}, 1E9, 1E9, 0, 0, -1, -1, 1E9, 1E9, -1, -1, DTChamberId(0, 1, 0), -1});
    muon.setMatches({match});
    if (!muon::isGoodMuon(muon, muon::TMOneStationTight)) throw(cms::Exception("MuonUnpacker") << "Failed to add TMOneStationTight!");
  }
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void pat::MuonUnpacker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("muons", edm::InputTag("slimmedMuons"))->setComment("muon input collection");
  desc.add<edm::InputTag>("tracks", edm::InputTag("unpackedTracksAndVertices"))->setComment("track input collection");
  desc.add<edm::InputTag>("primaryVertices", edm::InputTag("unpackedTracksAndVertices"))->setComment("primary vertex input collection");
  desc.add<edm::InputTag>("beamSpot", edm::InputTag("offlineBeamSpot"))->setComment("beam spot collection");
  desc.add<std::vector<std::string> >("muonSelectors", {"AllTrackerMuons", "TMOneStationTight"})->setComment("muon selectors");
  desc.add<bool>("addPropToMuonSt", false)->setComment("add eta/phi propagated to 2nd muon station for L1 matching");
  descriptions.add("unpackedMuons", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(MuonUnpacker);
