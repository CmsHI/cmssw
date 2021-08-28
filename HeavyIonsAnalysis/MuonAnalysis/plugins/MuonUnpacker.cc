#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/IPTools/interface/IPTools.h"

namespace pat {

  class MuonUnpacker : public edm::stream::EDProducer<> {

  public:

    explicit MuonUnpacker(const edm::ParameterSet & iConfig):
      muonToken_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
      trackToken_(consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("tracks"))),
      primaryVertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("primaryVertices"))),
      beamSpotToken_(consumes<reco::BeamSpot>(iConfig.getParameter<edm::InputTag>("beamSpot"))),
      triggerResultToken_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerResults"))),
      candidateToken_({
	  {"packedPFCandidate", consumes<edm::View<pat::PackedCandidate> >(iConfig.getParameter<edm::InputTag>("packedPFCandidates"))},
	    {"lostTrack", consumes<edm::View<pat::PackedCandidate> >(iConfig.getParameter<edm::InputTag>("lostTracks"))}
	}),
      candidateMuonIDLabel_({
	  {"packedPFCandidate", iConfig.getParameter<std::string>("packedPFCandidateMuonIDLabel")},
	    {"lostTrack", iConfig.getParameter<std::string>("lostTrackMuonIDLabel")}
	}),
      muonSelectors_(iConfig.getParameter<std::vector<std::string> >("muonSelectors"))
    {
      for (const auto& c: candidateMuonIDLabel_) {
	for (const auto& sel: muonSelectors_) {
	  candidateMuonIDToken_[c.first][sel] = consumes<edm::ValueMap<bool> >(edm::InputTag(c.second, sel));
	}
      }
      produces<pat::MuonCollection>();
    }
    ~MuonUnpacker() override {};

    void produce(edm::Event&, const edm::EventSetup&) override;

    void addMuon(pat::Muon&, const pat::PackedCandidate&, const std::string&,
		 const reco::TrackRef&, const edm::ESHandle<TransientTrackBuilder>&,
		 const reco::Vertex&, const reco::BeamSpot&, std::map<std::string, bool>);

    static void fillDescriptions(edm::ConfigurationDescriptions&);

  private:

    edm::EDGetTokenT<pat::MuonCollection> muonToken_;
    edm::EDGetTokenT<reco::TrackCollection> trackToken_;
    edm::EDGetTokenT<reco::VertexCollection> primaryVertexToken_;
    edm::EDGetTokenT<reco::BeamSpot> beamSpotToken_;
    edm::EDGetTokenT<edm::TriggerResults> triggerResultToken_;
    std::map<std::string, edm::EDGetTokenT<edm::View<pat::PackedCandidate> > > candidateToken_;
    std::map<std::string, std::map<std::string, edm::EDGetTokenT<edm::ValueMap<bool> > > > candidateMuonIDToken_;

    const std::map<std::string, std::string> candidateMuonIDLabel_;
    const std::vector<std::string> muonSelectors_;

  };

}

void pat::MuonUnpacker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<pat::MuonCollection> muons;
  edm::Handle<reco::TrackCollection> tracks;
  edm::Handle<reco::VertexCollection> primaryVertices;
  edm::Handle<reco::BeamSpot> beamSpotH;
  edm::Handle<edm::TriggerResults> triggerResults;
  std::map<std::string, edm::Handle<edm::View<pat::PackedCandidate> > > candidates;
  std::map<std::string, std::map<std::string, edm::ValueMap<bool> > > candidateMuonIDs;

  iEvent.getByToken(muonToken_, muons);
  iEvent.getByToken(trackToken_, tracks);
  iEvent.getByToken(primaryVertexToken_, primaryVertices);
  iEvent.getByToken(beamSpotToken_, beamSpotH);
  iEvent.getByToken(triggerResultToken_, triggerResults);
  for (auto& c : candidateToken_) {
    for (const auto& s: candidateMuonIDToken_[c.first]) {
      edm::Handle<edm::ValueMap<bool> > coll;
      iEvent.getByToken(s.second, coll);
      if (coll.isValid()) {
        candidateMuonIDs[c.first][s.first] = *coll;
      }
    }
    if (candidateMuonIDs.count(c.first)>0) {
      iEvent.getByToken(c.second, candidates[c.first]);
    }
  }

  // extract primary vertex and beamspot
  const auto& primaryVertex = primaryVertices->at(0);
  const auto& beamSpot = *beamSpotH;

  // extract the transient track builder
  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder);

  // extract muons from packedCandidate collections
  pat::MuonCollection candMuons;
  for (auto& c : candidates) {
    for (size_t i=0; i<c.second->size(); i++) {
      auto cand = c.second->ptrAt(i);
      // ignore neutral candidates or without track
      if (cand->charge()==0 || !cand->hasTrackDetails()) continue;
      const auto& candTrack = cand->pseudoTrack();

      // check if candidate is muon
      bool isMuon = false;
      std::map<std::string, bool> selMap;
      for (const auto& s: candidateMuonIDs[c.first]) {
        selMap[s.first] = s.second[cand];
        isMuon = isMuon || selMap[s.first];
      }
      if (!isMuon) continue;

      // find track in track collection associated to candidate
      reco::TrackRef track;
      for (size_t j=0; j<tracks->size(); j++) {
        const auto& trk = tracks->at(j);
        if (trk.charge()==candTrack.charge() && trk.pt()==candTrack.pt() && trk.eta()==candTrack.eta() && trk.phi()==candTrack.phi()) {
          track = reco::TrackRef(tracks, j);
          break;
        }
      }

      // create and add the muon object
      pat::Muon muon;
      addMuon(muon, *cand, c.first, track, trackBuilder, primaryVertex, beamSpot, selMap);
      candMuons.push_back(muon);
    }
  }

  std::unique_ptr<pat::MuonCollection> output(new pat::MuonCollection(*muons));

  // add the extra muons from packedCandidate collections
  for (const auto& candMuon : candMuons) {
    const auto& candTrack = *candMuon.innerTrack();
    bool isIncluded = false;
    for (const auto& muon : *muons) {
      if (muon.innerTrack().isNull()) continue;
      // ignore muons without high purity inner track
      if (muon.innerTrack().isNull() || !muon.innerTrack()->quality(reco::TrackBase::qualityByName("highPurity"))) continue;
      const auto& muonTrack = *muon.innerTrack();
      if (muonTrack.charge()==candTrack.charge() && muonTrack.numberOfValidHits()==candTrack.numberOfValidHits() &&
          std::abs(muonTrack.eta()-candTrack.eta())<1E-3 && std::abs(muonTrack.phi()-candTrack.phi())<1E-3 && std::abs((muonTrack.pt()-candTrack.pt())/muonTrack.pt())<1E-2) {
        isIncluded = true;
        break;
      }
    }
    if (!isIncluded) {
      output->push_back(candMuon);
    }
  } 
  
  // unpack trigger data for MiniAOD
  for (auto& muon : *output) {
    for(auto& o : muon.triggerObjectMatches()) {
      const_cast<pat::TriggerObjectStandAlone*>(&o)->unpackNamesAndLabels(iEvent, *triggerResults);
    }
  }

  iEvent.put(std::move(output));
}

void pat::MuonUnpacker::addMuon(pat::Muon& muon, const pat::PackedCandidate& cand, const std::string& lbl,
                                const reco::TrackRef& track, const edm::ESHandle<TransientTrackBuilder>& trackBuilder,
                                const reco::Vertex& primaryVertex, const reco::BeamSpot& beamSpot,
                                std::map<std::string, bool> selMap) {
  // add basic information
  muon.setP4(cand.p4());
  muon.setCharge(cand.charge());
  muon.setVertex(cand.vertex());
  muon.setPdgId(-13 * cand.charge());

  // add track information
  muon.setInnerTrack(track);
  muon.setMuonTrack(reco::Muon::InnerTrack, track);
  muon.setTrack(track);
  muon.setBestTrack(reco::Muon::InnerTrack);
  muon.embedTrack();
  muon.embedMuonBestTrack();
  muon.setNumberOfValidHits(track->numberOfValidHits());
  const auto& muonTrack = *muon.track();

  // add vertex information
  auto tt = trackBuilder->build(muonTrack);
  auto result = IPTools::signedTransverseImpactParameter(tt, GlobalVector(muonTrack.px(), muonTrack.py(), muonTrack.pz()), primaryVertex);
  muon.setDB(result.second.value(), result.second.error(), pat::Muon::PV2D);
  result = IPTools::signedImpactParameter3D(tt, GlobalVector(muonTrack.px(), muonTrack.py(), muonTrack.pz()), primaryVertex);
  muon.setDB(result.second.value(), result.second.error(), pat::Muon::PV3D);
  reco::Vertex beamSpotVertex(beamSpot.position(), beamSpot.rotatedCovariance3D());
  result = IPTools::signedTransverseImpactParameter(tt, GlobalVector(muonTrack.px(), muonTrack.py(), muonTrack.pz()), beamSpotVertex);
  muon.setDB(result.second.value(), result.second.error(), pat::Muon::BS2D);
  result = IPTools::signedImpactParameter3D(tt, GlobalVector(muonTrack.px(), muonTrack.py(), muonTrack.pz()), beamSpotVertex);
  muon.setDB(result.second.value(), result.second.error(), pat::Muon::BS3D);
  muon.setDB(muonTrack.dz(primaryVertex.position()), std::hypot(muonTrack.dzError(), primaryVertex.zError()), pat::Muon::PVDZ);

  // determine muon selectors
  bool isTrackerMuon = selMap["AllTrackerMuons"] || selMap["TMOneStationTight"];
  bool isGlobalMuon = selMap["AllGlobalMuons"] || cand.isGlobalMuon();
  bool isStandAloneMuon = selMap["AllStandAloneMuons"] || cand.isStandAloneMuon();
  bool isPFMuon = (lbl=="packedPFCandidate" && std::abs(cand.pdgId())==13);
  bool isHPMuon = (lbl=="lostTrack" ? true : muonTrack.quality(reco::Track::highPurity));
  bool isLooseMuon = isPFMuon || isGlobalMuon || isTrackerMuon;
  bool isTMOneStationTight = selMap["TMOneStationTight"];
  bool isSoftMuon = isTMOneStationTight && isHPMuon &&
    muonTrack.hitPattern().trackerLayersWithMeasurement()>5 && muonTrack.hitPattern().pixelLayersWithMeasurement()>0 &&
    fabs(muonTrack.dxy(primaryVertex.position()))<0.3 && fabs(muonTrack.dz(primaryVertex.position()))<20.;

  // add muon selectors
  unsigned int type = 0;
  unsigned int selectors = 0;
  std::vector<bool> selVec(muon::TriggerIdLoose+1, false);
  if (isLooseMuon) {
    selectors |= reco::Muon::CutBasedIdLoose;
  }
  if (isSoftMuon) {
    selectors |= reco::Muon::SoftCutBasedId;
  }
  selVec[muon::All] = true;
  if (isTrackerMuon) {
    type |= reco::Muon::TrackerMuon;
    selVec[muon::AllTrackerMuons] = true;
  }
  if (isStandAloneMuon) {
    type |= reco::Muon::StandAloneMuon;
    selVec[muon::AllStandAloneMuons] = true;
  }
  if (isGlobalMuon) {
    //type |= reco::Muon::GlobalMuon;
    selVec[muon::AllGlobalMuons] = true;
  }
  if (isPFMuon) {
    type |= reco::Muon::PFMuon;
    muon.setPFP4(cand.p4());
  }
  if (isTMOneStationTight) {
    selVec[muon::TMOneStationTight] = true;
  }
  muon.setType(type);
  muon.setSelectors(selectors);
  for (int i=muon::All; i<=muon::TriggerIdLoose; i++) {
    muon.addUserInt(Form("muonID_%d", i), selVec[i]);
  }

  // add candidate information
  unsigned int candType = 0;
  if (lbl=="packedPFCandidate") {
    candType = 1;
  }
  else if (lbl=="lostTrack") {
    candType = 2;
  }
  muon.addUserInt("candType", candType);
}
  

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void pat::MuonUnpacker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("muons", edm::InputTag("slimmedMuons"))->setComment("muon input collection");
  desc.add<edm::InputTag>("tracks", edm::InputTag("unpackedTracksAndVertices"))->setComment("track input collection");
  desc.add<edm::InputTag>("primaryVertices", edm::InputTag("unpackedTracksAndVertices"))->setComment("primary vertex input collection");
  desc.add<edm::InputTag>("beamSpot", edm::InputTag("offlineBeamSpot"))->setComment("beam spot collection");
  desc.add<edm::InputTag>("triggerResults", edm::InputTag("TriggerResults::HLT"))->setComment("trigger result collection");
  desc.add<edm::InputTag>("packedPFCandidates", edm::InputTag("packedPFCandidates"))->setComment("packed PF candidates input collection");
  desc.add<edm::InputTag>("lostTracks", edm::InputTag("lostTracks"))->setComment("lost tracks input collection");
  desc.add<std::string>("packedPFCandidateMuonIDLabel", "packedPFCandidateMuonID")->setComment("packed PF candidate Muon ID label");
  desc.add<std::string>("lostTrackMuonIDLabel", "lostTrackMuonID")->setComment("lost track Muon ID label");
  desc.add<std::vector<std::string> >("muonSelectors", {"AllTrackerMuons", "TMOneStationTight"})->setComment("muon selectors");
  descriptions.add("unpackedMuons", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(MuonUnpacker);
