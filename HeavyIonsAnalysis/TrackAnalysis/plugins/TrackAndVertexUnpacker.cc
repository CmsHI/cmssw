#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"

namespace pat {

  class TrackAndVertexUnpacker : public edm::global::EDProducer<> {
  public:
    explicit TrackAndVertexUnpacker(const edm::ParameterSet& iConfig)
        : packedPFCandidateToken_(
              consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("packedPFCandidates"))),
          lostTrackToken_(consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("lostTracks"))),
          packedPFCandidateNormChi2MapToken_(
              consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("packedPFCandidateNormChi2Map"))),
          lostTrackNormChi2MapToken_(
              consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("lostTrackNormChi2Map"))),
          primaryVertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("primaryVertices"))),
          secondaryVertexToken_(consumes<reco::VertexCompositePtrCandidateCollection>(
              iConfig.getParameter<edm::InputTag>("secondaryVertices"))),
          recoverTracks_(iConfig.getParameter<bool>("recoverTracks")){
      produces<reco::TrackCollection>();
      produces<reco::VertexCollection>();
      produces<reco::VertexCollection>("secondary");
      produces<edm::Association<reco::TrackCollection> >();
    };
    ~TrackAndVertexUnpacker() override{};

    void produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const override;

    static void fillDescriptions(edm::ConfigurationDescriptions&);

  private:
    const edm::EDGetTokenT<pat::PackedCandidateCollection> packedPFCandidateToken_;
    const edm::EDGetTokenT<pat::PackedCandidateCollection> lostTrackToken_;
    const edm::EDGetTokenT<edm::ValueMap<float> > packedPFCandidateNormChi2MapToken_;
    const edm::EDGetTokenT<edm::ValueMap<float> > lostTrackNormChi2MapToken_;
    const edm::EDGetTokenT<reco::VertexCollection> primaryVertexToken_;
    const edm::EDGetTokenT<reco::VertexCompositePtrCandidateCollection> secondaryVertexToken_;
    const bool recoverTracks_;
  };

}  // namespace pat

void pat::TrackAndVertexUnpacker::produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  // extract input information
  const auto& packedPFCandidates = iEvent.getHandle(packedPFCandidateToken_);
  const auto& lostTracks = iEvent.getHandle(lostTrackToken_);
  const auto& packedPFCandidateNormChi2Map = iEvent.get(packedPFCandidateNormChi2MapToken_);
  const auto& lostTrackNormChi2Map = iEvent.get(lostTrackNormChi2MapToken_);
  const auto& primaryVertices = iEvent.getHandle(primaryVertexToken_);
  const auto& secondaryVertices = iEvent.get(secondaryVertexToken_);

  // create output track collection
  auto outTracks = std::make_unique<reco::TrackCollection>();
  std::map<bool, std::vector<int> > pcAssoc;
  std::map<size_t, std::vector<size_t> > pvAssoc;
  std::map<reco::CandidatePtr, size_t> trackKeys;
  for (const auto& isPF : {true, false}) {
    const auto& cands = isPF ? packedPFCandidates : lostTracks;
    const auto& normChi2Map = isPF ? packedPFCandidateNormChi2Map : lostTrackNormChi2Map;
    pcAssoc[isPF] = std::vector<int>(cands->size(), -1);
    for (size_t iC = 0; iC < cands->size(); iC++) {
      const auto& cand = (*cands)[iC];
      if (cand.charge() == 0) continue;
      const auto& normChi2 = normChi2Map.get(cands.id(), iC);
      // case: track from packed candidate with track information
      if (cand.hasTrackDetails()) {
        const auto& track = cand.pseudoTrack();
        const auto ndof = track.ndof() != 0 ? track.ndof() : 0.1;
        // create output track
        outTracks->emplace_back(normChi2 * ndof,
                                ndof,
                                track.referencePoint(),
                                track.momentum(),
                                track.charge(),
                                track.covariance(),
                                track.algo(),
                                reco::TrackBase::loose,
                                track.t0(),
                                track.beta(),
                                track.covt0t0(),
                                track.covBetaBeta());
        auto& outTrack = outTracks->back();
        outTrack.setQualityMask(track.qualityMask());
        outTrack.setOriginalAlgorithm(track.originalAlgo());
        outTrack.setAlgoMask(track.algoMask());
        outTrack.setNLoops(track.nLoops());
        outTrack.setStopReason(track.stopReason());
        const_cast<reco::HitPattern&>(outTrack.hitPattern()) = track.hitPattern();
      }
      // case: track from packed candidate without track information
      else if (recoverTracks_ && (!isPF || cand.covarianceVersion() > 0)) {
        const auto& lostHits = cand.lostInnerHits();
        math::RhoEtaPhiVector p3(cand.ptTrk(), cand.etaAtVtx(), cand.phiAtVtx());
        // create output track
        outTracks->emplace_back((normChi2!=0 ? normChi2 : 1.E12) * 0.1,
                                0.1,
                                cand.vertex(),
                                math::XYZVector(p3.x(), p3.y(), p3.z()),
                                cand.charge(),
                                reco::TrackBase::CovarianceMatrix(ROOT::Math::SMatrixIdentity()) * 1.E12,
                                reco::TrackBase::initialStep,
                                cand.trackHighPurity() ? reco::TrackBase::highPurity : reco::TrackBase::loose);
        auto& outTrack = outTracks->back();
        if (lostHits == pat::PackedCandidate::validHitInFirstPixelBarrelLayer)
          outTrack.appendTrackerHitPattern(PixelSubdetector::PixelBarrel, 1, 0, TrackingRecHit::valid);
        else if (lostHits >= pat::PackedCandidate::oneLostInnerHit)
          outTrack.appendTrackerHitPattern(PixelSubdetector::PixelBarrel, 1, 0, TrackingRecHit::missing_inner);
        if (lostHits == pat::PackedCandidate::moreLostInnerHits)
          outTrack.appendTrackerHitPattern(PixelSubdetector::PixelBarrel, 2, 0, TrackingRecHit::missing_inner);
      }
      else continue;
      const size_t iT = outTracks->size() - 1;
      // associate track to primary vertices
      const auto& pvRef = cand.vertexRef();
      if (pvRef.id() != primaryVertices.id())
        throw(cms::Exception("TrackAndVertexUnpacker")
              << "Primary vertex collection not associated to packed candidates!");
      else if (cand.pvAssociationQuality() >= pat::PackedCandidate::UsedInFitLoose)
        pvAssoc[pvRef.key()].emplace_back(iT);
      // associate track to candidates
      reco::CandidatePtr candRef(cands.id(), &cand, iC);
      trackKeys[candRef] = iT;
      pcAssoc[isPF][iC] = iT;
    }
  }
  const auto& outTracksHandle = iEvent.put(std::move(outTracks));

  // create output primary vertex collection
  auto outPrimaryVertices = std::make_unique<reco::VertexCollection>();
  for (size_t iPV = 0; iPV < primaryVertices->size(); iPV++) {
    auto vtx = (*primaryVertices)[iPV];
    for (const auto& iT : pvAssoc[iPV]) {
      reco::TrackRef trkRef(outTracksHandle, iT);
      vtx.add(reco::TrackBaseRef(trkRef));
    }
    outPrimaryVertices->emplace_back(vtx);
  }
  iEvent.put(std::move(outPrimaryVertices));

  // create output secondary vertex collection
  auto outSecondaryVertices = std::make_unique<reco::VertexCollection>();
  for (const auto& sv : secondaryVertices) {
    reco::Vertex vtx(
        sv.vertex(), sv.vertexCovariance4D(), sv.t(), sv.vertexChi2(), sv.vertexNdof(), sv.numberOfDaughters());
    for (size_t j = 0; j < sv.numberOfDaughters(); j++) {
      const auto& dau = sv.daughterPtr(j);
      reco::TrackRef trkRef(outTracksHandle, trackKeys.at(dau));
      vtx.add(reco::TrackBaseRef(trkRef));
    }
    outSecondaryVertices->emplace_back(vtx);
  }
  iEvent.put(std::move(outSecondaryVertices), "secondary");

  // create output association packed candidate -> track
  auto assoc_pc2track = std::make_unique<edm::Association<reco::TrackCollection> >(outTracksHandle);
  edm::Association<reco::TrackCollection>::Filler pc2track_filler(*assoc_pc2track);
  pc2track_filler.insert(packedPFCandidates, pcAssoc[true].begin(), pcAssoc[true].end());
  pc2track_filler.insert(lostTracks, pcAssoc[false].begin(), pcAssoc[false].end());
  pc2track_filler.fill();
  iEvent.put(std::move(assoc_pc2track));
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void pat::TrackAndVertexUnpacker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("packedPFCandidates", edm::InputTag("packedPFCandidates"))
      ->setComment("packed PF candidates collection");
  desc.add<edm::InputTag>("lostTracks", edm::InputTag("lostTracks"))->setComment("lost tracks collection");
  desc.add<edm::InputTag>("packedPFCandidateNormChi2Map", edm::InputTag("packedPFCandidateTrackChi2"))
      ->setComment("packed PF candidates normChi2 map");
  desc.add<edm::InputTag>("lostTrackNormChi2Map", edm::InputTag("lostTrackChi2"))
      ->setComment("lost tracks normChi2 map");
  desc.add<edm::InputTag>("primaryVertices", edm::InputTag("offlineSlimmedPrimaryVertices"))
      ->setComment("primary vertex collection");
  desc.add<edm::InputTag>("secondaryVertices", edm::InputTag("slimmedSecondaryVertices"))
      ->setComment("secondary vertex collection");
  desc.add<bool>("recoverTracks", false)->setComment("recover tracks");
  descriptions.add("unpackedTracksAndVertices", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(TrackAndVertexUnpacker);
