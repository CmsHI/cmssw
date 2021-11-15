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
  pfEvt_.Clear();

  edm::Handle<reco::PFCandidateCollection> pfCandidates;
  iEvent.getByToken(pfCandidatePF_, pfCandidates);

  edm::Handle<reco::TrackCollection > tracks;
  if (doTrackMatching_) {
    iEvent.getByToken(trkLabel_, tracks);
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
        pfEvt_.trkAlgo_.push_back( -999 );  
        pfEvt_.trkPtError_.push_back( -999 );  
        pfEvt_.trkNHit_.push_back( -999 );  
        pfEvt_.trkChi2_.push_back( 0 );  
        pfEvt_.trkNdof_.push_back( -999 );  
        continue;
      }

      //find the track key
      unsigned int trackKey = pfcand.trackRef().key();     

      if(trackKey < tracks->size()){
          const reco::Track & trk = (*tracks)[trackKey];
          pfEvt_.trkAlgo_.push_back( trk.algo() );  
          pfEvt_.trkPtError_.push_back( trk.ptError() );  
          pfEvt_.trkNHit_.push_back( trk.numberOfValidHits() );  
          pfEvt_.trkChi2_.push_back( trk.chi2() );  
          pfEvt_.trkNdof_.push_back( trk.ndof() );  
      }
      else{
        pfEvt_.trkAlgo_.push_back( -999 );  
        pfEvt_.trkPtError_.push_back( -999 );  
        pfEvt_.trkNHit_.push_back( -999 );  
        pfEvt_.trkChi2_.push_back( 0 );  
        pfEvt_.trkNdof_.push_back( -999 );  
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
  pfEvt_.SetBranches(doJets_, doMC_, doCaloEnergy_, doTrackMatching_);
}

// ------------ method called once each job just after ending the event loop  ------------
void
HiPFCandAnalyzer::endJob() {
}

// set branches
void TreePFCandEventData::SetBranches(bool doJets, bool doMC, bool doCaloEnergy, bool doTrackMatching)
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
    tree_->Branch("trkAlgo",&trkAlgo_);
    tree_->Branch("trkPtError",&trkPtError_);
    tree_->Branch("trkNHit",&trkNHit_);
    tree_->Branch("trkChi2",&trkChi2_);
    tree_->Branch("trkNdof",&trkNdof_);
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

void TreePFCandEventData::Clear()
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

  pfEcalE_.clear();
  pfEcalEraw_.clear();
  pfHcalE_.clear();
  pfHcalEraw_.clear();

  trkAlgo_.clear();
  trkPtError_.clear();
  trkNHit_.clear();
  trkChi2_.clear();
  trkNdof_.clear();  

  nGENpart_ = 0;
  genPDGId_.clear();
  genPt_.clear();
  genEta_.clear();
  genPhi_.clear();

  njets_ = 0;
  jetPt_.clear();
  jetEnergy_.clear();
  jetEta_.clear();
  jetPhi_.clear();
}

DEFINE_FWK_MODULE(HiPFCandAnalyzer);
