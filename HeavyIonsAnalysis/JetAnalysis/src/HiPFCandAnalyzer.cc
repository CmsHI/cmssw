#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "HeavyIonsAnalysis/JetAnalysis/interface/HiPFCandAnalyzer.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"


//
// constructors and destructor
//
HiPFCandAnalyzer::HiPFCandAnalyzer(const edm::ParameterSet& iConfig)
{
  pfCandidatePF_ = consumes<reco::PFCandidateCollection>(
    iConfig.getParameter<edm::InputTag>("pfCandidateLabel"));
  pfPtMin_ = iConfig.getParameter<double>("pfPtMin");
  pfAbsEtaMax_ = iConfig.getParameter<double>("pfAbsEtaMax");
  genPtMin_ = iConfig.getParameter<double>("genPtMin");
  jetPtMin_ = iConfig.getParameter<double>("jetPtMin");

  doJets_ = iConfig.getParameter<bool>("doJets");
  if (doJets_) {
    jetLabel_ = consumes<pat::JetCollection>(
      iConfig.getParameter<edm::InputTag>("jetLabel"));
  }

  doMC_ = iConfig.getParameter<bool>("doMC");
  if (doMC_) {
    genLabel_ = consumes<reco::GenParticleCollection>(
      iConfig.getParameter<edm::InputTag>("genLabel"));
  }

  doCaloEnergy_ = iConfig.getParameter<bool>("doCaloEnergy");

  skipCharged_ = iConfig.getParameter<bool>("skipCharged");
  
  doTrackMatching_ = iConfig.getParameter<bool>("doTrackMatching");
  if (doTrackMatching_) {
    trkLabel_ = consumes<reco::TrackCollection>(
      iConfig.getParameter<edm::InputTag>("trackLabel"));
  }

  doTrackMVA_ = doTrackMatching_ && (iConfig.getParameter<bool>("doTrackMVA"));
  if (doTrackMVA_) {
    mvaSrc_ = consumes<std::vector<float>>(iConfig.getParameter<edm::InputTag>("mvaSrc"));
  }

  doTrackVtx_ = doTrackMatching_ && (iConfig.getParameter<bool>("doTrackVtx"));
  if (doTrackVtx_) {
    vtxCollection_ = consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("vtxLabel"));
  }
}

HiPFCandAnalyzer::~HiPFCandAnalyzer()
{
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called to for each event  ------------
void
HiPFCandAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  pfEvt_.Clear(doJets_, doMC_, doCaloEnergy_, doTrackMatching_, doTrackMVA_, doTrackVtx_);

  edm::Handle<reco::PFCandidateCollection> pfCandidates;
  iEvent.getByToken(pfCandidatePF_, pfCandidates);

  edm::Handle<reco::TrackCollection > tracks;
  if (doTrackMatching_) {
    iEvent.getByToken(trkLabel_, tracks);
  }

  edm::Handle<std::vector<float>> trkmvaH;
  if (doTrackMVA_) {
    iEvent.getByToken(mvaSrc_, trkmvaH);
  }

  edm::Handle<std::vector<reco::Vertex> > vtxHandle;
  reco::Vertex pv(math::XYZPoint(0, 0, -999), math::Error<3>::type());
  if (doTrackVtx_) {
    iEvent.getByToken(vtxCollection_, vtxHandle);
    for (const auto& v : *vtxHandle)
      if (!v.isFake()) {
        pv = v;
        break;
    }
  }

  for (const auto& pfcand : *pfCandidates) {
    double pt = pfcand.pt();
    double eta = pfcand.eta();

    if (pt <= pfPtMin_) continue;
    if (std::abs(eta) > pfAbsEtaMax_) continue;

    int id = pfcand.particleId();
    if (skipCharged_ && (abs(id) == 1 || abs(id) == 3)) continue;

    pfEvt_.pfKey_.push_back( pfcand.sourceCandidatePtr(0).key() );
    pfEvt_.pfId_.push_back( id );
    pfEvt_.pfPt_.push_back( pt );
    pfEvt_.pfEnergy_.push_back( pfcand.energy() );
    pfEvt_.pfEta_.push_back( pfcand.eta() );
    pfEvt_.pfPhi_.push_back( pfcand.phi() );
    pfEvt_.pfM_.push_back( pfcand.mass() );

    if (id == 1 || id == 3) {
      pfEvt_.pfvx_.push_back( pfcand.vx() );
      pfEvt_.pfvy_.push_back( pfcand.vy() );
      pfEvt_.pfvz_.push_back( pfcand.vz() );
    }
    else {
      pfEvt_.pfvx_.push_back(-999);
      pfEvt_.pfvy_.push_back(-999);
      pfEvt_.pfvz_.push_back(-999);
    }
    
    if (doCaloEnergy_) {
      pfEvt_.pfEcalE_.push_back( pfcand.ecalEnergy() );
      pfEvt_.pfEcalEraw_.push_back( pfcand.rawEcalEnergy() );
      pfEvt_.pfHcalE_.push_back( pfcand.hcalEnergy() );
      pfEvt_.pfHcalEraw_.push_back( pfcand.rawHcalEnergy() );
    }
    
    pfEvt_.nPFpart_++;

    if(doTrackMatching_){
      // only charged hadrons and leptons can be asscociated with a track
      int type = pfcand.particleId();
      if(!(type == reco::PFCandidate::h ||     //type1
	 type == reco::PFCandidate::e ||     //type2
	 type == reco::PFCandidate::mu      //type3
	 )
      ){
        pfEvt_.trkKey_.push_back( 0 );
        pfEvt_.trkPt_.push_back( -999 );
        pfEvt_.trkEta_.push_back( -999 );
        pfEvt_.trkPhi_.push_back( -999 );
        pfEvt_.trkAlgo_.push_back( 0 );
        pfEvt_.trkPtError_.push_back( -999 );  
        pfEvt_.trkNHit_.push_back( 0 );
        pfEvt_.trkChi2_.push_back( 0 );  
        pfEvt_.trkNdof_.push_back( 0 );
        pfEvt_.trkNlayer_.push_back( 0 );
        pfEvt_.highPurity_.push_back( 0 );
        if (doTrackMVA_) {
          pfEvt_.trkMVA_.push_back( -999 );
        }
        if (doTrackVtx_) {
          pfEvt_.trkDz1_.push_back( -999 );
          pfEvt_.trkDzError1_.push_back( -999 );
          pfEvt_.trkDxy1_.push_back( -999 );
          pfEvt_.trkDxyError1_.push_back( -999 );
        }
        continue;
      }

      //find the track key
      unsigned long trackKey = pfcand.trackRef().key();

      if(trackKey < tracks->size()){
          const reco::Track & trk = (*tracks)[trackKey];
          pfEvt_.trkKey_.push_back( trackKey );
          pfEvt_.trkPt_.push_back( trk.pt() );
          pfEvt_.trkEta_.push_back( trk.eta() );
          pfEvt_.trkPhi_.push_back( trk.phi() );
          pfEvt_.trkAlgo_.push_back( trk.algo() );  
          pfEvt_.trkPtError_.push_back( trk.ptError() );  
          pfEvt_.trkNHit_.push_back( trk.numberOfValidHits() );  
          pfEvt_.trkChi2_.push_back( trk.chi2() );  
          pfEvt_.trkNdof_.push_back( trk.ndof() );
          pfEvt_.trkNlayer_.push_back( trk.hitPattern().trackerLayersWithMeasurement() );
          bool isHighPurity = (trk.quality(reco::TrackBase::qualityByName("highPurity"))) ? 1 : 0;
          pfEvt_.highPurity_.push_back( isHighPurity );

          if (doTrackMVA_) {
            if (trk.algo() == 11) { //sets jet-core iteration tracks to MVA of +/-1 based on their highPurity bit (even though no MVA is used)
              pfEvt_.trkMVA_.push_back( (isHighPurity ? 1 : -1) );
            } else {
              pfEvt_.trkMVA_.push_back( (*trkmvaH)[trackKey] );
            }
          }

          if (doTrackVtx_) {
            math::XYZPoint v1(pv.position().x(), pv.position().y(), pv.position().z());
            pfEvt_.trkDz1_.push_back( trk.dz(v1) );
            pfEvt_.trkDzError1_.push_back( std::sqrt(trk.dzError()*trk.dzError()+pv.zError()*pv.zError()) );
            pfEvt_.trkDxy1_.push_back( trk.dxy(v1) );
            pfEvt_.trkDxyError1_.push_back( std::sqrt(trk.dxyError()*trk.dxyError()+pv.xError()*pv.yError()) );
          }
      }
      else{
        pfEvt_.trkKey_.push_back( 0 );
        pfEvt_.trkPt_.push_back( -999 );
        pfEvt_.trkEta_.push_back( -999 );
        pfEvt_.trkPhi_.push_back( -999 );
        pfEvt_.trkAlgo_.push_back( 0 );
        pfEvt_.trkPtError_.push_back( -999 );  
        pfEvt_.trkNHit_.push_back( 0 );
        pfEvt_.trkChi2_.push_back( 0 );  
        pfEvt_.trkNdof_.push_back( 0 );
        pfEvt_.trkNlayer_.push_back( 0 );
        pfEvt_.highPurity_.push_back( 0 );

        if (doTrackMVA_) {
          pfEvt_.trkMVA_.push_back( -999 );
        }

        if (doTrackVtx_) {
          pfEvt_.trkDz1_.push_back( -999 );
          pfEvt_.trkDzError1_.push_back( -999 );
          pfEvt_.trkDxy1_.push_back( -999 );
          pfEvt_.trkDxyError1_.push_back( -999 );
        }
      }
    }
  }

  // Fill GEN info
  if (doMC_) {
    edm::Handle<reco::GenParticleCollection> genParticles;
    iEvent.getByToken(genLabel_, genParticles);

    for (const auto& gen : *genParticles) {
      double pt = gen.pt();
      double eta = gen.eta();

      if (gen.status() == 1 && std::abs(eta) < 3 && pt > genPtMin_) {
	pfEvt_.genPDGId_.push_back( gen.pdgId() );
	pfEvt_.genPt_.push_back(pt);
	pfEvt_.genEta_.push_back(eta);
	pfEvt_.genPhi_.push_back(gen.phi());
	pfEvt_.nGENpart_++;
      }
    }
  }

  // Fill Jet info
  if (doJets_) {
    edm::Handle<pat::JetCollection> jets;
    iEvent.getByToken(jetLabel_, jets);

    for (const auto& jet : *jets) {
      double pt = jet.pt();

      if (pt > jetPtMin_) {
	pfEvt_.jetPt_.push_back( pt );
	pfEvt_.jetEnergy_.push_back( jet.energy() );
	pfEvt_.jetEta_.push_back( jet.eta() );
	pfEvt_.jetPhi_.push_back( jet.phi() );
	pfEvt_.njets_++;
      }
    }
  }

  // All done
  pfTree_->Fill();
}

void HiPFCandAnalyzer::beginJob()
{
  pfTree_ = fs->make<TTree>("pfTree", "pf candidate tree");
  pfEvt_.SetTree(pfTree_);
  pfEvt_.SetBranches(doJets_, doMC_, doCaloEnergy_, doTrackMatching_, doTrackMVA_, doTrackVtx_);
}

// ------------ method called once each job just after ending the event loop  ------------
void
HiPFCandAnalyzer::endJob() {
}

// set branches
void TreePFCandEventData::SetBranches(bool doJets, bool doMC, bool doCaloEnergy, bool doTrackMatching, bool doTrackMVA, bool doTrackVtx)
{
  // -- particle info --
  tree_->Branch("nPFpart", &nPFpart_, "nPFpart/I");
  tree_->Branch("pfKey", &pfKey_);
  tree_->Branch("pfId", &pfId_);
  tree_->Branch("pfPt", &pfPt_);
  tree_->Branch("pfEnergy", &pfEnergy_);
  tree_->Branch("pfEta", &pfEta_);
  tree_->Branch("pfPhi", &pfPhi_);
  tree_->Branch("pfM", &pfM_);

  tree_->Branch("pfvx", &pfvx_);
  tree_->Branch("pfvy", &pfvy_);
  tree_->Branch("pfvz", &pfvz_);

  // -- ecal/hcal energy info --
  if (doCaloEnergy) {
    tree_->Branch("pfEcalE", &pfEcalE_);
    tree_->Branch("pfEcalEraw", &pfEcalEraw_);
    tree_->Branch("pfHcalE", &pfHcalE_);
    tree_->Branch("pfHcalEraw", &pfHcalEraw_);
  }

  if(doTrackMatching) {
    tree_->Branch("trkKey",&trkKey_);
    tree_->Branch("trkPt",&trkPt_);
    tree_->Branch("trkEta",&trkEta_);
    tree_->Branch("trkPhi",&trkPhi_);
    tree_->Branch("trkAlgo",&trkAlgo_);
    tree_->Branch("trkPtError",&trkPtError_);
    tree_->Branch("trkNHit",&trkNHit_);
    tree_->Branch("trkChi2",&trkChi2_);
    tree_->Branch("trkNdof",&trkNdof_);
    tree_->Branch("trkNlayer",&trkNlayer_);
    tree_->Branch("highPurity",&highPurity_);
  }

  if (doTrackMVA) {
    tree_->Branch("trkMVA",&trkMVA_);
  }

  if(doTrackVtx) {
    tree_->Branch("trkDz1",&trkDz1_);
    tree_->Branch("trkDzError1",&trkDzError1_);
    tree_->Branch("trkDxy1",&trkDxy1_);
    tree_->Branch("trkDxyError1",&trkDxyError1_);
  }

  // -- jet info --
  if (doJets) {
    tree_->Branch("njets", &njets_, "njets/I");
    tree_->Branch("jetPt", &jetPt_);
    tree_->Branch("jetEta", &jetEta_);
    tree_->Branch("jetPhi", &jetPhi_);
  }

  // -- gen info --
  if (doMC) {
    tree_->Branch("nGENpart", &nGENpart_, "nGENpart/I");
    tree_->Branch("genPDGId", &genPDGId_);
    tree_->Branch("genPt", &genPt_);
    tree_->Branch("genEta", &genEta_);
    tree_->Branch("genPhi", &genPhi_);
  }
}

void TreePFCandEventData::Clear(bool doJets, bool doMC, bool doCaloEnergy, bool doTrackMatching, bool doTrackMVA, bool doTrackVtx)
{
  nPFpart_ = 0;
  pfKey_.clear();
  pfId_.clear();
  pfPt_.clear();
  pfEnergy_.clear();
  pfEta_.clear();
  pfPhi_.clear();
  pfM_.clear();

  pfvx_.clear();
  pfvy_.clear();
  pfvz_.clear();

  if (doCaloEnergy) {
    pfEcalE_.clear();
    pfEcalEraw_.clear();
    pfHcalE_.clear();
    pfHcalEraw_.clear();
  }

  if (doTrackMatching) {
    trkKey_.clear();
    trkPt_.clear();
    trkEta_.clear();
    trkPhi_.clear();
    trkAlgo_.clear();
    trkPtError_.clear();
    trkNHit_.clear();
    trkChi2_.clear();
    trkNdof_.clear();
    trkNlayer_.clear();
    highPurity_.clear();
  }

  if (doTrackMVA) {
    trkMVA_.clear();
  }

  if (doTrackVtx) {
    trkDz1_.clear();
    trkDzError1_.clear();
    trkDxy1_.clear();
    trkDxyError1_.clear();
  }

  if (doMC) {
    nGENpart_ = 0;
    genPDGId_.clear();
    genPt_.clear();
    genEta_.clear();
    genPhi_.clear();
  }

  if (doJets) {
    njets_ = 0;
    jetPt_.clear();
    jetEnergy_.clear();
    jetEta_.clear();
    jetPhi_.clear();
  }
}

DEFINE_FWK_MODULE(HiPFCandAnalyzer);
