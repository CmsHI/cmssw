#include "RecoHI/HiJetAlgos/interface/PuWithNtuple.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
using namespace std;

PuWithNtuple::PuWithNtuple(const edm::ParameterSet& iConfig, edm::ConsumesCollector && iC) : 
  PileUpSubtractor(iConfig, std::move(iC)),
  sumRecHits_(iConfig.getParameter<bool>("sumRecHits")),
  dropZeroTowers_(iConfig.getUntrackedParameter<bool>("dropZeroTowers",true))
{
  
  if(iConfig.exists("minimumTowersFraction")){
    minimumTowersFraction_ = iConfig.getParameter<double>("minimumTowersFraction");
    cout<<"LIMITING THE MINIMUM TOWERS FRACTION TO : "<<minimumTowersFraction_<<endl;
  }else{
    minimumTowersFraction_ = 0;
    cout<<"ATTENTION - NOT LIMITING THE MINIMUM TOWERS FRACTION"<<endl;
  }

  Neta_ = 82;

  isOrphanInputRun_ = false;
  tree_ = fs_->make<TTree>("puTree","");

  tree_->Branch("nref",&nref,"nref/I");
  tree_->Branch("jteta",jteta,"jteta[nref]/F");
  tree_->Branch("jtphi",jtphi,"jtphi[nref]/F");
  tree_->Branch("jtpt",jtpt,"jtpt[nref]/F");
  tree_->Branch("jtexngeom",jtexngeom,"jtexngeom[nref]/I");
  tree_->Branch("jtexntow",jtexntow,"jtexntow[nref]/I");

  tree_->Branch("jtexpt",jtexpt,"jtexpt[nref]/F");
  tree_->Branch("jtpu",jtpu,"jtpu[nref]/F");

  tree_->Branch("ngeom",vngeom,"ngeom[82]/I");
  tree_->Branch("ntow",vntow,"ntow[82]/I");

  tree_->Branch("eta",veta,"eta[82]/F");
  tree_->Branch("ieta",vieta,"ieta[82]/I");

  tree_->Branch("mean0",vmean0,"mean0[82]/F");
  tree_->Branch("rms0",vrms0,"rms0[82]/F");

  tree_->Branch("mean1",vmean1,"mean1[82]/F");
  tree_->Branch("rms1",vrms1,"rms1[82]/F");

  const double etatow[42] = {0.000, 0.087, 0.174, 0.261, 0.348, 0.435, 0.522, 0.609, 0.696, 0.783, 0.870, 0.957, 1.044, 1.131, 1.218, 1.305, 1.392, 1.479, 1.566, 1.653, 1.740, 1.830, 1.930, 2.043, 2.172, 2.322, 2.500, 2.650, 2.853, 3.000, 3.139, 3.314, 3.489, 3.664, 3.839, 4.013, 4.191, 4.363, 4.538, 4.716, 4.889, 5.191};

  for(int i=0;i<42;i++){
    etaedge[i]=etatow[i];
  }

}


void PuWithNtuple::rescaleRMS(double s){
   for ( std::map<int, double>::iterator iter = esigma_.begin();
	 iter != esigma_.end(); ++iter ){
      iter->second = s*(iter->second);
   }
}


void PuWithNtuple::offsetCorrectJets()
{

  LogDebug("PileUpSubtractor")<<"The subtractor correcting jets...\n";
  jetOffset_.clear();

  using namespace reco;
  
  (*fjInputs_) = fjOriginalInputs_;
  rescaleRMS(nSigmaPU_);
  subtractPedestal(*fjInputs_);
  const fastjet::JetDefinition& def = *fjJetDefinition_;
  if ( !doAreaFastjet_ && !doRhoFastjet_) {
    fjClusterSeq_ = ClusterSequencePtr( new fastjet::ClusterSequence( *fjInputs_, def ) );
  } else {
    fjClusterSeq_ = ClusterSequencePtr( new fastjet::ClusterSequenceArea( *fjInputs_, def, *fjActiveArea_ ) );
  }
  
  (*fjJets_) = fastjet::sorted_by_pt(fjClusterSeq_->inclusive_jets(jetPtMin_));
  
  jetOffset_.reserve(fjJets_->size());
  
  vector<fastjet::PseudoJet>::iterator pseudojetTMP = fjJets_->begin (),
    jetsEnd = fjJets_->end();
  for (; pseudojetTMP != jetsEnd; ++pseudojetTMP) {
    
    int ijet = pseudojetTMP - fjJets_->begin();
    jetOffset_[ijet] = 0;
    
    std::vector<fastjet::PseudoJet> towers =
      sorted_by_pt(pseudojetTMP->constituents());
    
    double newjetet = 0.;
    for(vector<fastjet::PseudoJet>::const_iterator ito = towers.begin(),
	  towEnd = towers.end();
	ito != towEnd;
	++ito)
      {
	const reco::CandidatePtr& originalTower = (*inputs_)[ito->user_index()];
	int it = ieta( originalTower );
	double Original_Et = originalTower->et();
	double etnew = Original_Et - (*emean_.find(it)).second - (*esigma_.find(it)).second;
	if(etnew < 0.) etnew = 0;
	newjetet = newjetet + etnew;
	jetOffset_[ijet] += Original_Et - etnew;
      }
  }
}

void PuWithNtuple::subtractPedestal(vector<fastjet::PseudoJet> & coll)
{

   LogDebug("PileUpSubtractor")<<"The subtractor subtracting pedestals...\n";

   int it = -100;

   vector<fastjet::PseudoJet> newcoll;

   for (vector<fastjet::PseudoJet>::iterator input_object = coll.begin (),
	   fjInputsEnd = coll.end(); 
	input_object != fjInputsEnd; ++input_object) {
    
      reco::CandidatePtr const & itow =  (*inputs_)[ input_object->user_index() ];
    
      it = ieta( itow );
      iphi( itow );
    
      double Original_Et = itow->et();
      if(sumRecHits_){
         Original_Et = getEt(itow);
      }

      double etnew = Original_Et - (*(emean_.find(it))).second - (*(esigma_.find(it))).second;
      float mScale = etnew/input_object->Et(); 
      if(etnew < 0.) mScale = 0.;
    
      math::XYZTLorentzVectorD towP4(input_object->px()*mScale, input_object->py()*mScale,
				     input_object->pz()*mScale, input_object->e()*mScale);
    
      int index = input_object->user_index();
      input_object->reset_momentum ( towP4.px(),
				     towP4.py(),
				     towP4.pz(),
				     towP4.energy() );
      input_object->set_user_index(index);

      if(etnew > 0. && dropZeroTowers_) newcoll.push_back(*input_object);
   }

   if(dropZeroTowers_) coll = newcoll;

}

void PuWithNtuple::calculatePedestal( vector<fastjet::PseudoJet> const & coll )
{
   LogDebug("PileUpSubtractor")<<"The subtractor calculating pedestals...\n";

   map<int,double> emean2;
   map<int,int> ntowers;
    
   int ietaold = -10000;
   int ieta0 = -100;
   
   // Initial values for emean_, emean2, esigma_, ntowers


   for(int vi = 0; vi < Neta_; ++vi){
     int it = vi+1;
     if(it > Neta_/2) it = vi - Neta_;

     int sign = 1;
     if(it < 0){
       sign = -1;
     }
     
     vieta[vi] = it;
     veta[vi] = sign*(etaedge[abs(it)] + etaedge[abs(it)-1])/2.;

     vngeom[vi] = -99;
     vntow[vi] = -99;

     vmean1[vi] = -99;
     vrms1[vi] = -99;

     if((*(ntowersWithJets_.find(it))).second == 0){
       vmean0[vi] = -99;
       vrms0[vi] = -99;
     }

   }


   for(int i = ietamin_; i < ietamax_+1; i++)
      {
	 emean_[i] = 0.;
	 emean2[i] = 0.;
	 esigma_[i] = 0.;
	 ntowers[i] = 0;
      }
    
   for (vector<fastjet::PseudoJet>::const_iterator input_object = coll.begin (),
	   fjInputsEnd = coll.end();  
	input_object != fjInputsEnd; ++input_object) {

      const reco::CandidatePtr & originalTower=(*inputs_)[ input_object->user_index()];
      ieta0 = ieta( originalTower );
      double Original_Et = originalTower->et();
      if(sumRecHits_){
         Original_Et = getEt(originalTower);
      }

      if( ieta0-ietaold != 0 )
	 {
	    emean_[ieta0] = emean_[ieta0]+Original_Et;
	    emean2[ieta0] = emean2[ieta0]+Original_Et*Original_Et;
	    ntowers[ieta0] = 1;
	    ietaold = ieta0;
	 }
      else
	 {
	    emean_[ieta0] = emean_[ieta0]+Original_Et;
	    emean2[ieta0] = emean2[ieta0]+Original_Et*Original_Et;
	    ntowers[ieta0]++;
	 }

   }

   for(map<int,int>::const_iterator gt = geomtowers_.begin(); gt != geomtowers_.end(); gt++)    
      {

	 int it = (*gt).first;
	 int vi = it-1;
	 if(it < 0) vi = Neta_ + it;
       
	 double e1 = (*(emean_.find(it))).second;
	 double e2 = (*emean2.find(it)).second;
	 int nt = (*gt).second - (*(ntowersWithJets_.find(it))).second;

	 if(vi < Neta_){
	   vngeom[vi] = (*gt).second;
	   vntow[vi] = nt;
	 }

	 LogDebug("PileUpSubtractor")<<" ieta : "<<it<<" number of towers : "<<nt<<" e1 : "<<e1<<" e2 : "<<e2<<"\n";
        
	 if(nt > 0) {
	    emean_[it] = e1/nt;
	    double eee = e2/nt - e1*e1/(nt*nt);    
	    if(eee<0.) eee = 0.;
	    esigma_[it] = nSigmaPU_*sqrt(eee);

	    if(vi < Neta_){
	      vmean1[vi] = emean_[it];
	      vrms1[vi] = esigma_[it];
	      if(vngeom[vi] == vntow[vi]){
		vmean0[vi] = emean_[it];
		vrms0[vi] = esigma_[it];
	      }
	    }
	 }
	 else
	    {
	       emean_[it] = 0.;
	       esigma_[it] = 0.;
	    }
	 LogDebug("PileUpSubtractor")<<" ieta : "<<it<<" Pedestals : "<<emean_[it]<<"  "<<esigma_[it]<<"\n";
      }

   if(isOrphanInputRun_){   
     tree_->Fill();
     isOrphanInputRun_ = false;
   }
}


void PuWithNtuple::calculateOrphanInput(vector<fastjet::PseudoJet> & orphanInput)
{

  LogDebug("PileUpSubtractor")<<"The subtractor calculating orphan input...\n";

  isOrphanInputRun_= true;
  (*fjInputs_) = fjOriginalInputs_;

  vector<int> jettowers; // vector of towers indexed by "user_index"
  vector<pair<int,int> >  excludedTowers; // vector of excluded ieta, iphi values

  vector <fastjet::PseudoJet>::iterator pseudojetTMP = fjJets_->begin (),
    fjJetsEnd = fjJets_->end();

  //  cout<<"First iteration found N jets : "<<fjJets_->size()<<endl;

  nref = 0;

  for (; pseudojetTMP != fjJetsEnd ; ++pseudojetTMP) {

    //    cout<<"Jet with pt "<<pseudojetTMP->perp()<<" to be excluded"<<endl;


    if(nref < 200){
      jtexngeom[nref] = 0;
      jtexntow[nref] = 0;      
      jtexpt[nref] = 0;
      jtpt[nref] = pseudojetTMP->perp();
      jteta[nref] = pseudojetTMP->eta();
      jtphi[nref] = pseudojetTMP->phi();
    }

    if(pseudojetTMP->perp() < puPtMin_) continue;

    //    cout<<"Looping over towers..."<<endl;

    // find towers within radiusPU_ of this jet
    for(vector<HcalDetId>::const_iterator im = allgeomid_.begin(); im != allgeomid_.end(); im++)
      {
	double dr = reco::deltaR(geo_->getPosition((DetId)(*im)),(*pseudojetTMP));
        vector<pair<int,int> >::const_iterator exclude = find(excludedTowers.begin(),excludedTowers.end(),pair<int,int>(im->ieta(),im->iphi()));
        if( dr < radiusPU_
            &&
            exclude == excludedTowers.end()
            &&
            (geomtowers_[(*im).ieta()] - ntowersWithJets_[(*im).ieta()]) > minimumTowersFraction_*(geomtowers_[(*im).ieta()])) {
          ntowersWithJets_[(*im).ieta()]++;

	  //          cout<<"At ieta : "<<(*im).ieta()<<" -  excluded so far : "<<ntowersWithJets_[(*im).ieta()]<<" out of max "<<geomtowers_[(*im).ieta()]<<endl;
          excludedTowers.push_back(pair<int,int>(im->ieta(),im->iphi()));

	  if(nref < 200) jtexngeom[nref]++;  
        }
      }

    vector<fastjet::PseudoJet>::const_iterator it = fjInputs_->begin(),
      fjInputsEnd = fjInputs_->end();

    for (; it != fjInputsEnd; ++it ) {
      int index = it->user_index();
      int ie = ieta((*inputs_)[index]);
      int ip = iphi((*inputs_)[index]);
      vector<pair<int,int> >::const_iterator exclude = find(excludedTowers.begin(),excludedTowers.end(),pair<int,int>(ie,ip));
      if(exclude != excludedTowers.end()) {
        jettowers.push_back(index);
	//        cout<<"tower with index "<<index<<" excluded."<<endl;
	//        cout<<"jettowers now : "<<jettowers.size()<<endl;
      }
    } // initial input collection


    for (it = fjInputs_->begin(); it != fjInputsEnd; ++it ) {
      int index = it->user_index();
      const reco::CandidatePtr& originalTower = (*inputs_)[index];
      double dr = reco::deltaR((*it),(*pseudojetTMP));

      if(dr < radiusPU_){
	if(nref < 200){
	  jtexntow[nref]++;
	  jtexpt[nref] += originalTower->pt();
	}
      }

    }



    if(nref < 200) nref++;
  } // pseudojets

  //
  // Create a new collections from the towers not included in jets
  //

  for(vector<fastjet::PseudoJet>::const_iterator it = fjInputs_->begin(),
        fjInputsEnd = fjInputs_->end(); it != fjInputsEnd; ++it ) {
    int index = it->user_index();
    vector<int>::const_iterator itjet = find(jettowers.begin(),jettowers.end(),index);
    if( itjet == jettowers.end() ){
      const reco::CandidatePtr& originalTower = (*inputs_)[index];
      fastjet::PseudoJet orphan(originalTower->px(),originalTower->py(),originalTower->pz(),originalTower->energy());
      orphan.set_user_index(index);

      orphanInput.push_back(orphan);
    }
  }

  //  cout<<"Number of jets : "<<nref<<endl;
}









double PuWithNtuple::getEt(const reco::CandidatePtr & in) const {
   const CaloTower* ctc = dynamic_cast<const CaloTower*>(in.get());
   const GlobalPoint& pos=geo_->getPosition(ctc->id());
   double energy = ctc->emEnergy() + ctc->hadEnergy();
   double et = energy*sin(pos.theta());
   return et;
}

double PuWithNtuple::getEta(const reco::CandidatePtr & in) const {
   const CaloTower* ctc = dynamic_cast<const CaloTower*>(in.get());
   const GlobalPoint& pos=geo_->getPosition(ctc->id());
   double eta = pos.eta();
   return eta;
}
