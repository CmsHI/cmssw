
#include "DataFormats/Math/interface/deltaPhi.h"
#include "HeavyIonsAnalysis/PhotonAnalysis/interface/trkIsoCalculator.h"

trkIsoCalculator::trkIsoCalculator()
{
  applyMVA = true;
  doMapTrk2PfCand = true;

  strTrkQuality = "highPurity";

  collSys = CollisionSystem::undef;

  track_pfcand_map = std::unordered_map<int, int>();
}

void trkIsoCalculator::set(const edm::Event &iEvent,
                           const edm::EDGetTokenT<std::vector<reco::Track>> & trackSrc,
                           const edm::EDGetTokenT<std::vector<float>> & mvaSrc,
                           const edm::EDGetTokenT<edm::View<reco::PFCandidate>> & pfCandidates,
                           const reco::Vertex& pv,
                           std::string strCollision)
{
  iEvent.getByToken(trackSrc, tracks_);
  iEvent.getByToken(pfCandidates, pfCands);

  if (applyMVA) {
    iEvent.getByToken(mvaSrc, mvas_);
  }

  if (doMapTrk2PfCand) {
    makeMapTrk2PfCand();
  }

  vtx_ = pv;

  if (strCollision == "pp15") {
    collSys = CollisionSystem::pp15;
  }
  else if (strCollision == "pbpb15") {
    collSys = CollisionSystem::pbpb15;
  }
  else if (strCollision == "pp17") {
    collSys = CollisionSystem::pp17;
  }
  else if (strCollision == "pbpb18") {
    collSys = CollisionSystem::pbpb18;
  }
  else {
    std::cout << "trkIsoCalculator::set WARNING : collision system could not be assigned." << std::endl;
  }
}

double trkIsoCalculator::getTrkIso(double egEta, double egPhi, double r1, double r2, double threshold, double jWidth, bool applyTrkID)
{
  double totalEt = 0;

  for (unsigned it = 0; it<tracks_->size(); ++it) {
    const reco::Track & etrk = (*tracks_)[it];

    double teta = etrk.eta();
    double tphi = etrk.phi();

    double dEta = std::abs(egEta - teta);
    double dPhi = reco::deltaPhi(tphi, egPhi);
    double dR2 = dEta*dEta + dPhi*dPhi;
    double tpt = etrk.pt();

    // Jurassic Cone /////
    if (dR2 > r1 * r1) continue;
    if (dR2 < r2 * r2) continue;
    if (std::abs(dEta) < jWidth)  continue;
    if (tpt < threshold) continue;

    if (strTrkQuality.size() > 0 && !etrk.quality(reco::TrackBase::qualityByName(strTrkQuality))) continue;

    if (applyTrkID) {
      if (!passedTrkSelection(etrk, it))  continue;
    }

    totalEt += tpt;
  }

  return totalEt;
}

double trkIsoCalculator::getTrkIsoSubUE(double egEta, double egPhi, double r1, double r2, double threshold, double jWidth, bool applyTrkID, bool excludeCone)
{
    double totalEt = 0;

    for (unsigned it = 0; it<tracks_->size(); ++it) {
        const reco::Track & etrk = (*tracks_)[it];

        double teta = etrk.eta();
        double tphi = etrk.phi();

        double dEta = std::abs(egEta - teta);
        if (dEta > r1) continue;
        if (dEta < jWidth)  continue;

       if (strTrkQuality.size() > 0 && !etrk.quality(reco::TrackBase::qualityByName(strTrkQuality))) continue;
        if (applyTrkID) {
            if (!passedTrkSelection(etrk, it))  continue;
        }

        double dPhi = reco::deltaPhi(tphi, egPhi);
        double dR2 = dEta*dEta + dPhi*dPhi;
        double tpt = etrk.pt();

        // Jurassic Cone /////
        if (dR2 < r2 * r2) continue;
        if (tpt < threshold) continue;
        totalEt += tpt;
    }

    double areaStrip = 4*M_PI*(r1-jWidth);   // strip area over which UE is estimated
    double areaCone = M_PI*r1*r1;       // area inside which isolation is to be applied
    if (jWidth > 0) {
        // calculate overlap area between disk with radius r2 and rectangle of width jwidth
        double angTmp = std::acos(jWidth / r1);
        double lenTmp = std::sqrt(r1*r1 - jWidth*jWidth) * 2;
        double areaTwoTriangles = lenTmp * jWidth;
        double areaTwoArcs = (M_PI - 2*angTmp) * r1 * r1;
        areaCone -= (areaTwoTriangles + areaTwoArcs);
    }

    double areaInnerCone = 0;
    if (r2 > jWidth) {
        areaInnerCone = M_PI*r2*r2;
        if (jWidth > 0) {
            double angTmp = std::acos(jWidth / r2);
            double lenTmp = std::sqrt(r2*r2 - jWidth*jWidth) * 2;
            double areaTwoTriangles = lenTmp * jWidth;
            double areaTwoArcs = (M_PI - 2*angTmp) * r2 * r2;
            areaInnerCone -= (areaTwoTriangles + areaTwoArcs);
        }
    }
    areaStrip -= areaInnerCone;
    areaCone -= areaInnerCone;

    double coneEt = getTrkIso(egEta, egPhi, r1, r2, threshold, jWidth, applyTrkID);
    double ueEt = totalEt;
    double ueArea = areaStrip;
    if (excludeCone) {
        // Note the result for excludeCone=True is a scaled version ofthe result for excludeCone=False
        // In particular : f[excludeCone=True] = f[excludeCone=False] * 4 / (4 - R)
        ueEt = totalEt - coneEt;
        ueArea = areaStrip - areaCone;
    }

    return coneEt - ueEt * (areaCone / ueArea);
}

bool trkIsoCalculator::passedTrkSelection(const reco::Track & trk, unsigned index)
{

    if (collSys == CollisionSystem::pbpb18) {
        // cuts for 2018
        if ((trk.algo() == 6 && (*mvas_)[index] < 0.98)) return false;

        if (!(trk.quality(reco::TrackBase::qualityByName(strTrkQuality)) == 1)) return false;
        if (!(trk.ptError() / trk.pt() < 0.1 &&
              std::fabs(trk.dz(vtx_.position()) / std::sqrt( trk.dzError()*trk.dzError() + vtx_.zError()*vtx_.zError() )) < 3 &&
              std::fabs(trk.dxy(vtx_.position()) / std::sqrt( trk.dxyError()*trk.dxyError() + vtx_.xError()*vtx_.yError() )) < 3))  return false;
        if (!(trk.numberOfValidHits() >= 11))  return false;
        if (!(trk.chi2() / (float)trk.ndof() / (float)trk.hitPattern().trackerLayersWithMeasurement() < 0.18))  return false;

        if (trk.pt() > 20) {

          int iPF = getMatchedPfCand(index);
          if (iPF >= 0) {
            float Et = (((*pfCands)[iPF]).ecalEnergy() + ((*pfCands)[iPF]).hcalEnergy()) / std::cosh(trk.eta());
            if ( !(Et > 0.5 * trk.pt()) )  return false;
          }
        }
    }
    else if (collSys == CollisionSystem::pbpb15) {
        // cuts for 2015
        if (!(trk.pt() <= 300 && std::fabs(trk.eta()) < 2.4)) return false;
        if (!(trk.quality(reco::TrackBase::qualityByName(strTrkQuality)) == 1)) return false;
        if (!(trk.ptError() / trk.pt() < 0.1 &&
              std::fabs(trk.dz(vtx_.position()) / std::sqrt( trk.dzError()*trk.dzError() + vtx_.zError()*vtx_.zError() )) < 3 &&
              std::fabs(trk.dxy(vtx_.position()) / std::sqrt( trk.dxyError()*trk.dxyError() + vtx_.xError()*vtx_.yError() )) < 3))  return false;
        if (!(trk.chi2() / (float)trk.ndof() / (float)trk.hitPattern().trackerLayersWithMeasurement() < 0.15))  return false;
        if (!(trk.numberOfValidHits() >= 11))  return false;

        if (trk.pt() > 20) {

          int iPF = getMatchedPfCand(index);
          if (iPF >= 0) {
            float Et = (((*pfCands)[iPF]).ecalEnergy() + ((*pfCands)[iPF]).hcalEnergy()) / std::cosh(trk.eta());
            if ( !(Et > 0.5 * trk.pt()) )  return false;
          }
        }
    }
    else if (collSys == CollisionSystem::pp17) {
        // cuts for pp 2017
        if (!(trk.quality(reco::TrackBase::qualityByName(strTrkQuality)) == 1)) return false;
        if (!(trk.ptError() / trk.pt() < 0.1 &&
              std::fabs(trk.dz(vtx_.position()) / std::sqrt( trk.dzError()*trk.dzError() + vtx_.zError()*vtx_.zError() )) < 3 &&
              std::fabs(trk.dxy(vtx_.position()) / std::sqrt( trk.dxyError()*trk.dxyError() + vtx_.xError()*vtx_.yError() )) < 3))  return false;
    }
    else if (collSys == CollisionSystem::pp15) {
        // cuts for pp 2015
        if (!(trk.pt() <= 300 && std::fabs(trk.eta()) < 2.4)) return false;
        if (!(trk.quality(reco::TrackBase::qualityByName(strTrkQuality)) == 1)) return false;
        if (!(trk.ptError() / trk.pt() < 0.1 &&
              std::fabs(trk.dz(vtx_.position()) / std::sqrt( trk.dzError()*trk.dzError() + vtx_.zError()*vtx_.zError() )) < 3 &&
              std::fabs(trk.dxy(vtx_.position()) / std::sqrt( trk.dxyError()*trk.dxyError() + vtx_.xError()*vtx_.yError() )) < 3))  return false;

        if (trk.pt() > 20) {

          int iPF = getMatchedPfCand(index);
          if (iPF >= 0) {
            float Et = (((*pfCands)[iPF]).ecalEnergy() + ((*pfCands)[iPF]).hcalEnergy()) / std::cosh(trk.eta());
            if ( !(Et > 0.5 * trk.pt()) )  return false;
          }
        }
    }
    else {
        return false;
    }

    return true;
}

int trkIsoCalculator::getMatchedPfCand(unsigned indexTrk)
{
  if (doMapTrk2PfCand) {
    //edm::Ref<reco::TrackCollection>::key_type trk_key = reco::TrackRef(tracks_, indexTrk).key();

    reco::TrackRef trackRef = reco::TrackRef(tracks_,indexTrk);
    auto indexTrkRef = trackRef.key();

    auto it = track_pfcand_map.find(indexTrkRef);
    if (it == track_pfcand_map.end()) { 
      return -1;
    }
    else {
      return it->second;
    }
  }

  return -1;
}

void trkIsoCalculator::makeMapTrk2PfCand() 
{
  // https://github.com/cms-sw/cmssw/blob/master/DataFormats/Common/interface/Ref.h : typedef unsigned int edm::Ref<reco::TrackCollection>::key_type;

  for (std::size_t iPF = 0; iPF < pfCands->size(); ++iPF) {
    auto const& pfCand = (*pfCands)[iPF];

    int type = pfCand.particleId();
    // only charged hadrons and leptons can be asscociated with a track
    if (!(type == reco::PFCandidate::h ||
          type == reco::PFCandidate::e ||
          type == reco::PFCandidate::mu)
        ) {
      continue;
    }

    auto keyTrkRef = pfCand.trackRef().key();
    track_pfcand_map[keyTrkRef] = iPF;
  }
}

