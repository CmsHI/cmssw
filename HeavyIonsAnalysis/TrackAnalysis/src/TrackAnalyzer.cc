#include "HeavyIonsAnalysis/TrackAnalysis/interface/TrackAnalyzer.h"

TrackAnalyzer::TrackAnalyzer(const edm::ParameterSet& iConfig)
{
  doTrack_ = iConfig.getUntrackedParameter<bool>("doTrack",true);

  trackPtMin_ = iConfig.getUntrackedParameter<double>("trackPtMin",0.01);

  vertexSrcLabel_ = iConfig.getParameter<edm::InputTag>("vertexSrc");
  vertexSrc_ = consumes<reco::VertexCollection>(vertexSrcLabel_);

  packedCandLabel_ = iConfig.getParameter<edm::InputTag>("packedCandSrc");
  packedCandSrc_ = consumes<edm::View<pat::PackedCandidate>>(packedCandLabel_);
  
  lostTracksLabel_ = iConfig.getParameter<edm::InputTag>("lostTracksSrc");
  lostTracksSrc_ = consumes<edm::View<pat::PackedCandidate>>(lostTracksLabel_);
  
  beamSpotProducer_ = consumes<reco::BeamSpot>(iConfig.getUntrackedParameter<edm::InputTag>("beamSpotSrc",edm::InputTag("offlineBeamSpot")));

  chi2MapLabel_ = iConfig.getParameter<edm::InputTag>("chi2Map");
  chi2Map_ = consumes<edm::ValueMap<float>>(chi2MapLabel_);
  chi2MapLostLabel_ = iConfig.getParameter<edm::InputTag>("chi2MapLost");
  chi2MapLost_ = consumes<edm::ValueMap<float>>(chi2MapLostLabel_);

}

//--------------------------------------------------------------------------------------------------
TrackAnalyzer::~TrackAnalyzer()
{
}

//--------------------------------------------------------------------------------------------------
void TrackAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  nEv = (int)iEvent.id().event();
  nRun = (int)iEvent.id().run();
  nLumi = (int)iEvent.luminosityBlock();

  clearVectors();

  fillVertices(iEvent);

  if(doTrack_) fillTracks(iEvent, iSetup);
  
  trackTree_->Fill();
}

//--------------------------------------------------------------------------------------------------
void TrackAnalyzer::fillVertices(const edm::Event& iEvent) {
  // Fill reconstructed vertices.
  const reco::VertexCollection* recoVertices;
  edm::Handle<reco::VertexCollection> vertexCollection;
  iEvent.getByToken(vertexSrc_,vertexCollection);
  recoVertices = vertexCollection.product();

  iMaxPtSumVtx = -1;
  float maxPtSum = -999;
  nVtx = (int)recoVertices->size();
  for (int i = 0; i < nVtx; ++i) {
    xVtx.push_back( recoVertices->at(i).position().x() );
    yVtx.push_back( recoVertices->at(i).position().y() );
    zVtx.push_back( recoVertices->at(i).position().z() );
    xErrVtx.push_back( recoVertices->at(i).xError() );
    yErrVtx.push_back( recoVertices->at(i).yError() );
    zErrVtx.push_back( recoVertices->at(i).zError() );
  
    chi2Vtx.push_back( recoVertices->at(i).chi2() );
    ndofVtx.push_back( recoVertices->at(i).ndof() );

    isFakeVtx.push_back( recoVertices->at(i).isFake() );

    //number of tracks having a weight in vtx fit above 0.5
    nTracksVtx.push_back( recoVertices->at(i).nTracks() );

    float ptSum = 0;
    for( auto ref = recoVertices->at(i).tracks_begin(); ref != recoVertices->at(i).tracks_end(); ref++){
      ptSum += (*ref)->pt();
    }
    ptSumVtx.push_back( ptSum );
    if (ptSum > maxPtSum) {
      iMaxPtSumVtx = i;
      maxPtSum = ptSum;
    }
  }   
}

//--------------------------------------------------------------------------------------------------
void
TrackAnalyzer::fillTracks(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  
  edm::Handle<edm::View<pat::PackedCandidate>> cands;
  edm::Handle<edm::ValueMap<float>> chi2Map;
  
  //loop over packed cands, then loop over lost tracks
  for(int i = 0; i<2; i++){

    if(i==0){
      iEvent.getByToken(packedCandSrc_,cands);
      iEvent.getByToken(chi2Map_,chi2Map);
    }
    if(i==1){
      iEvent.getByToken(lostTracksSrc_,cands);
      iEvent.getByToken(chi2MapLost_,chi2Map);
    }

    for(unsigned it = 0; it<cands->size(); ++it){
      const pat::PackedCandidate & c = (*cands)[it];

      if(!c.hasTrackDetails()) continue;

      reco::Track const& t = c.pseudoTrack();

      if(t.pt() < trackPtMin_) continue;

      trkPt.push_back( t.pt() );
      trkPtError.push_back( t.ptError() );
      trkEta.push_back( t.eta() );
      trkPhi.push_back( t.phi() );
      trkCharge.push_back( (char) t.charge() );
      trkPDGId.push_back( c.pdgId() );
      trkNHits.push_back( (char) t.numberOfValidHits() );
      trkNPixHits.push_back( (char) t.hitPattern().numberOfValidPixelHits() );
      trkNLayers.push_back( (char) t.hitPattern().trackerLayersWithMeasurement() );
      highPurity.push_back( t.quality(reco::TrackBase::qualityByName("highPurity")));
      trkNormChi2.push_back( (*chi2Map)[cands->ptrAt(it)] );

      pfEnergy.push_back( c.energy() );
      pfEcal.push_back( c.energy() * (c.caloFraction() - c.hcalFraction()) );
      pfHcal.push_back( c.energy() * c.hcalFraction() );

      //DCA info for associated vtx
      trkAssociatedVtxIndx.push_back( c.vertexRef().key() );
      trkAssociatedVtxQuality.push_back( c.fromPV(c.vertexRef().key() ));
      trkDzAssociatedVtx.push_back( c.dz( c.vertexRef()->position() ) );
      trkDzErrAssociatedVtx.push_back( sqrt( c.dzError()*c.dzError() + c.vertexRef()->zError() * c.vertexRef()->zError() ) );
      trkDxyAssociatedVtx.push_back( c.dxy( c.vertexRef()->position() ) );
      trkDxyErrAssociatedVtx.push_back( sqrt( c.dxyError()*c.dxyError() + c.vertexRef()->xError() * c.vertexRef()->yError() ) );
   
      //DCA info for first (highest pt) vtx
      if( iMaxPtSumVtx >= 0 ){
        math::XYZPoint v(xVtx.at(iMaxPtSumVtx),yVtx.at(iMaxPtSumVtx), zVtx.at(iMaxPtSumVtx));
        trkFirstVtxQuality.push_back( c.fromPV( iMaxPtSumVtx ));
        trkDzFirstVtx.push_back( t.dz( v ) );
        trkDzErrFirstVtx.push_back( sqrt( t.dzError()*t.dzError() + zErrVtx.at(iMaxPtSumVtx) * zErrVtx.at(iMaxPtSumVtx) ) ); // WARNING !! reco::Track::dzError() and pat::PackedCandidate::dzError() give different values. Former must be used for HIN track ID.
        trkDxyFirstVtx.push_back( t.dxy( v ) );
        trkDxyErrFirstVtx.push_back( sqrt( t.dxyError()*t.dxyError() + xErrVtx.at(iMaxPtSumVtx) * yErrVtx.at(iMaxPtSumVtx) ) );
      }
      else {
        trkFirstVtxQuality.push_back( -999999 );
        trkDzFirstVtx.push_back( -999999 );
        trkDzErrFirstVtx.push_back( -999999 );
        trkDxyFirstVtx.push_back( -999999 );
        trkDxyErrFirstVtx.push_back( -999999 );
      }

      nTrk++;
    }
  }
}


// ------------ method called once each job just before starting event loop  ------------
void TrackAnalyzer::beginJob()
{
  trackTree_ = fs->make<TTree>("trackTree","v1");

  // event
  trackTree_->Branch("nRun",&nRun,"nRun/I");
  trackTree_->Branch("nEv",&nEv,"nRun/I");
  trackTree_->Branch("nLumi",&nLumi,"nLumi/I");

  // vertex
  trackTree_->Branch("nVtx",&nVtx);
  trackTree_->Branch("xVtx",&xVtx);
  trackTree_->Branch("yVtx",&yVtx);
  trackTree_->Branch("zVtx",&zVtx);
  trackTree_->Branch("xErrVtx",&xErrVtx);
  trackTree_->Branch("yErrVtx",&yErrVtx);
  trackTree_->Branch("zErrVtx",&zErrVtx);
  trackTree_->Branch("chi2Vtx",&chi2Vtx);
  trackTree_->Branch("ndofVtx",&ndofVtx);
  trackTree_->Branch("isFakeVtx",&isFakeVtx);
  trackTree_->Branch("nTracksVtx",&nTracksVtx);
  trackTree_->Branch("ptSumVtx",&ptSumVtx);

  // Tracks
  trackTree_->Branch("nTrk",&nTrk);
  trackTree_->Branch("trkPt",&trkPt);
  trackTree_->Branch("trkPtError",&trkPtError);
  trackTree_->Branch("trkEta",&trkEta);
  trackTree_->Branch("trkPhi",&trkPhi);
  trackTree_->Branch("trkCharge",&trkCharge);
  trackTree_->Branch("trkPDGId",&trkPDGId);
  trackTree_->Branch("trkNHits",&trkNHits);
  trackTree_->Branch("trkNPixHits",&trkNPixHits);
  trackTree_->Branch("trkNLayers",&trkNLayers);
  trackTree_->Branch("trkNormChi2",&trkNormChi2);
  trackTree_->Branch("highPurity",&highPurity);

  trackTree_->Branch("pfEnergy",&pfEnergy);
  trackTree_->Branch("pfEcal",&pfEcal);
  trackTree_->Branch("pfHcal",&pfHcal);

  trackTree_->Branch("trkAssociatedVtxIndx",&trkAssociatedVtxIndx);
  trackTree_->Branch("trkAssociatedVtxQuality",&trkAssociatedVtxQuality);
  trackTree_->Branch("trkDzAssociatedVtx",&trkDzAssociatedVtx);
  trackTree_->Branch("trkDzErrAssociatedVtx",&trkDzErrAssociatedVtx);
  trackTree_->Branch("trkDxyAssociatedVtx",&trkDxyAssociatedVtx);
  trackTree_->Branch("trkDxyErrAssociatedVtx",&trkDxyErrAssociatedVtx);
  trackTree_->Branch("trkFirstVtxQuality",&trkFirstVtxQuality);
  trackTree_->Branch("trkDzFirstVtx",&trkDzFirstVtx);
  trackTree_->Branch("trkDzErrFirstVtx",&trkDzErrFirstVtx);
  trackTree_->Branch("trkDxyFirstVtx",&trkDxyFirstVtx);
  trackTree_->Branch("trkDxyErrFirstVtx",&trkDxyErrFirstVtx);
}

// ------------ method called once each job just after ending the event loop  ------------
void
TrackAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackAnalyzer);
