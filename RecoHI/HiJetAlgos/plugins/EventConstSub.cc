// -*- C++ -*-
//
// Package:    CommonTools/PileupAlgos
// Class:      EventConstSub
// 
/**\class EventConstSub EventConstSub.cc CommonTools/PileupAlgos/plugins/EventConstSub.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Leticia Cunqueiro
//         Created:  Friday, 18 Feb 2022 15:14:20 GMT
//
//


// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/Selector.hh"
#include "fastjet/tools/GridMedianBackgroundEstimator.hh"
#include "fastjet/contrib/ConstituentSubtractor.hh" 
#include "Math/ProbFuncMathCore.h"

//
// class declaration
//

class EventConstSub : public edm::stream::EDProducer<> {
public:
  typedef math::XYZTLorentzVector LorentzVector;
  typedef std::vector<LorentzVector> LorentzVectorCollection;
  typedef std::vector< reco::PFCandidate >   PFOutputCollection;

  explicit EventConstSub(const edm::ParameterSet&);
  ~EventConstSub() override;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT< reco::CandidateView > tokenPFCandidates_;
  edm::EDGetTokenT<std::vector<double>>                       etaToken_;
  edm::EDGetTokenT<std::vector<double>>                       rhoToken_;
  edm::EDGetTokenT<std::vector<double>>                       rhomToken_;
  edm::EDGetTokenT<std::vector<double>>                       rhoFlowFitParamsToken_;

  double ecsRho_EtaMax_;
  double ecsrParam_;
  double ecsrMax_;
  double ecsalpha_;
  double ecsghostarea_;
  bool ecsUseModulatedRho_;
  bool  ecsUseEtaBandsRho_;
  double minFlowChi2Prob_;/// flowFit chi2/ndof minimum compatability requirement                                                                        
  double maxFlowChi2Prob_;/// flowFit chi2/ndof minimum compatability requirement     
  double getModulatedRhoFactor(const double phi, const double eventPlane2, const double eventPlane3, const double par1, const double par2);
};



EventConstSub::EventConstSub(const edm::ParameterSet& iConfig) : 
  ecsRho_EtaMax_( iConfig.getParameter<double>("ecsRho_EtaMax") ),
  ecsrParam_ ( iConfig.getParameter<double>("ecsrParam") ),
  ecsrMax_ ( iConfig.getParameter<double>("ecsrMax") ),
  ecsalpha_ ( iConfig.getParameter<double>("ecsalpha")),
  ecsghostarea_ ( iConfig.getParameter<double>("ecsghostarea")),
  ecsUseModulatedRho_ ( iConfig.getParameter<bool>("ecsUseModulatedRho")),
  ecsUseEtaBandsRho_ ( iConfig.getParameter<bool>("ecsUseEtaBandsRho"))

{

  etaToken_ = consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>( "etaMap" ));
  rhoToken_ = consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>( "rho" ));
  rhomToken_ = consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>( "rhom" ));
  minFlowChi2Prob_ = iConfig.getParameter<double>("minFlowChi2Prob");
  maxFlowChi2Prob_ = iConfig.getParameter<double>("maxFlowChi2Prob");
  if(ecsUseModulatedRho_) rhoFlowFitParamsToken_ = consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>( "rhoFlowFitParams" ));
  tokenPFCandidates_
    = consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("PFCandidates"));

  produces<edm::ValueMap<LorentzVector> > ("EventConstSubP4s");
  produces< PFOutputCollection >();

}


EventConstSub::~EventConstSub()
{

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
EventConstSub::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  std::unique_ptr< PFOutputCollection > pOutput( new PFOutputCollection );

  // get PF Candidates
  edm::Handle<reco::CandidateView> pfCandidates;
  iEvent.getByToken( tokenPFCandidates_, pfCandidates);
  //fill the fastjet input 
  std::vector<fastjet::PseudoJet> fjInputs;
  for ( auto i = pfCandidates->begin(), 
	  ibegin = pfCandidates->begin(),
	  iend = pfCandidates->end(); i != iend; ++i ) {
    fjInputs.push_back( fastjet::PseudoJet( i->px(), i->py(), i->pz(), i->energy() ) );
    fjInputs.back().set_user_index( i - ibegin );
  }

  

  //get local maps
  //Get local rho and rhom map                                                                                                                             
  edm::Handle<std::vector<double>> etaRanges;
  edm::Handle<std::vector<double>> rhoRanges;
  edm::Handle<std::vector<double>> rhomRanges;
  edm::Handle<std::vector<double>> rhoFlowFitParams;

  iEvent.getByToken(etaToken_, etaRanges);
  iEvent.getByToken(rhoToken_, rhoRanges);
  iEvent.getByToken(rhomToken_, rhomRanges);
  if(ecsUseModulatedRho_) iEvent.getByToken(rhoFlowFitParamsToken_, rhoFlowFitParams);
  

  //Check if size of eta and background density vectors is the same                                                                                        
  unsigned int bkgVecSize = etaRanges->size();
  if(bkgVecSize<1) { throw cms::Exception("WrongBkgInput") << "Producer needs vector with background estimates\n"; }
  if(bkgVecSize != (rhoRanges->size()+1) || bkgVecSize != (rhomRanges->size()+1) ) {
    throw cms::Exception("WrongBkgInput") << "Size of etaRanges (" << bkgVecSize << ") and rhoRanges (" << rhoRanges->size() << ") and/or rhomRanges (" <<\
      rhomRanges->size() << ") vectors inconsistent\n";
  }

   
  //setup the subtractor
  fastjet::contrib::ConstituentSubtractor subtractor;
  subtractor.set_distance_type(fastjet::contrib::ConstituentSubtractor::deltaR);
  subtractor.set_max_distance(ecsrMax_);
  subtractor.set_alpha(ecsalpha_);
  subtractor.set_ghost_area(ecsghostarea_);
  subtractor.set_do_mass_subtraction();
  std::vector<fastjet::PseudoJet> ecsghosts;
   std::vector<fastjet::PseudoJet> ecsghosts_modulated;

  if(ecsUseEtaBandsRho_){
   
      //first distribute ghosts uniformly
      subtractor.construct_ghosts_uniformly(ecsRho_EtaMax_);
      ecsghosts=subtractor.get_ghosts();          
      //then modulate their distribution in eta-phi

      for(fastjet::PseudoJet& ighost : ecsghosts){
	double rhoModulationFactor = 1.;
        double ghostPhi = ighost.phi_std();


	if(ecsUseModulatedRho_){
	  if(rhoFlowFitParams->size() > 0){
	    
	    double val = ROOT::Math::chisquared_cdf_c(rhoFlowFitParams->at(5), rhoFlowFitParams->at(6));
	    bool minProb = val > minFlowChi2Prob_;
	    bool maxProb = val < maxFlowChi2Prob_;

	    if(minProb && maxProb)
	      rhoModulationFactor = getModulatedRhoFactor(ghostPhi,
							  rhoFlowFitParams->at(2),
							  rhoFlowFitParams->at(4),
							  rhoFlowFitParams->at(1),
							  rhoFlowFitParams->at(3)
							  );
	  }
	}


	 int ghostPos = -1;
	 if(ighost.eta()<=etaRanges->at(0)) ghostPos = 0;
	 else if(ighost.eta()>=etaRanges->at(etaRanges->size()-1)) ghostPos = rhoRanges->size()-1;
	  else{
	   for(unsigned int ie = 0; ie < etaRanges->size()-1; ++ie){
	      if(ighost.eta()>=etaRanges->at(ie) && ighost.eta()<etaRanges->at(ie+1)){
				      ghostPos = ie;
				      break;
	      }
	   }
	  }

	

	double pt = rhoRanges->at(ghostPos) * ecsghostarea_ * rhoModulationFactor;
	double mass_squared = std::pow(rhoModulationFactor * rhomRanges->at(ghostPos) * ecsghostarea_ + pt, 2) - std::pow(pt, 2);

	double mass = (mass_squared > 0) ? sqrt(mass_squared) : 0; 
	ighost.reset_momentum_PtYPhiM(pt, ighost.rap(), ighost.phi(), mass);
        ecsghosts_modulated.push_back(ighost);
      } //ghost loop

  }

  
       
  

   std::vector<fastjet::PseudoJet> corrected_event;

  if(ecsUseEtaBandsRho_) corrected_event = sorted_by_pt(subtractor.do_subtraction(fjInputs, ecsghosts_modulated));
  if(!ecsUseEtaBandsRho_){
    //this is just standard subtraction using fastjet default rho
    fastjet::GridMedianBackgroundEstimator bge_rho(ecsRho_EtaMax_,ecsrParam_); 
    subtractor.set_background_estimator(&bge_rho);
    bge_rho.set_particles(fjInputs); 
    corrected_event=subtractor.subtract_event(fjInputs,ecsRho_EtaMax_);}





  std::unique_ptr<edm::ValueMap<LorentzVector> > p4ECSOut(new edm::ValueMap<LorentzVector>());
  LorentzVectorCollection ecsP4s;

  static const reco::PFCandidate dummySinceTranslateIsNotStatic;

  // To satisfy the value map, the size of the subtracted collection needs to be the                                                                 
  // same size as the input collection, so if the constituent was removed, just set E = 0                                                            
  for ( auto j = fjInputs.begin(),
          jend = fjInputs.end(); j != jend; ++j ) {
    const reco::Candidate& cand = pfCandidates->at(j->user_index());
    auto id = dummySinceTranslateIsNotStatic.translatePdgIdToType(cand.pdgId());
    const reco::PFCandidate *pPF = dynamic_cast<const reco::PFCandidate*>(&cand);
    reco::PFCandidate pCand( pPF ? *pPF : reco::PFCandidate(cand.charge(), cand.p4(), id) );
    auto val = j->user_index();
    auto skmatch = find_if( corrected_event.begin(), corrected_event.end(), [&val](fastjet::PseudoJet const & i){return i.user_index() == val;} );

    LorentzVector pVec;
    if ( skmatch != corrected_event.end() ) {
      pVec.SetPxPyPzE(skmatch->px(),skmatch->py(),skmatch->pz(),skmatch->E());
    } else {
      pVec.SetPxPyPzE( 0., 0., 0., 0.);
    }
    pCand.setP4(pVec);
    ecsP4s.push_back( pVec );
    pOutput->push_back(pCand);
  }


  //Compute the modified p4s
  edm::ValueMap<LorentzVector>::Filler  p4ECSFiller(*p4ECSOut);
  p4ECSFiller.insert(pfCandidates,ecsP4s.begin(), ecsP4s.end() );
  p4ECSFiller.fill();

  iEvent.put(std::move(p4ECSOut),"EventConstSubP4s");
  iEvent.put(std::move(pOutput));

}


double EventConstSub::getModulatedRhoFactor(const double phi, const double eventPlane2, const double eventPlane3, const double par1, const double par2) {
  //get the rho modulation as function of phi                                                                                                              
  //flow modulation fit is done in HiJetBackground/HiFJRhoFlowModulationProducer                                                                           
  double mod = 1. + 2.*(par1*cos(2.*(phi - eventPlane2))) + par2*cos(3.*(phi - eventPlane3));

  return mod;
}


void EventConstSub::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setComment("Eventwise constituent subtractions");
  desc.add<edm::InputTag>("PFCandidates", edm::InputTag("packedPFCandidates"));
  desc.add<double>("ecsRho_EtaMax", 2.4);
  desc.add<double>("ecsrParam", 0.4);
  desc.add<double>("ecsrMax", 0.25);
  desc.add<double>("ecsalpha", 0.);
  desc.add<double>("ecsghostarea", 0.005);
  desc.add<bool>("ecsUseModulatedRho", false);
  desc.add<bool>("ecsUseEtaBandsRho", true);
  desc.add<edm::InputTag>("etaMap", edm::InputTag("hiPuRho:mapEtaEdges"));
  desc.add<edm::InputTag>("rho", edm::InputTag("hiPuRho:mapToRho"));
  desc.add<edm::InputTag>("rhom", edm::InputTag("hiPuRho:mapToRhoM"));
  desc.add<double>("minFlowChi2Prob", 0.05);
  desc.add<double>("maxFlowChi2Prob", 0.95);
  desc.add<edm::InputTag>("rhoFlowFitParams", edm::InputTag("hiFJRhoFlowModulationProducer:rhoFlowFitParams"));
  descriptions.add("EventConstSub", desc);
}



//define this as a plug-in
DEFINE_FWK_MODULE(EventConstSub);
