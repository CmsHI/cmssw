// -*- C++ -*-
//
// Package:    HiJetBackground/HiPuRhoProducer
// Class:      HiPuRhoProducer
// 
/**\class HiPuRhoProducer HiPuRhoProducer.cc HiJetBackground/HiPuRhoProducer/plugins/HiPuRhoProducer.cc

 Description: Producer to dump Pu-jet style rho into event content

 Implementation:
 Just see MultipleAlgoIterator - re-implenting for use in CS jet with sigma subtraction and zeroing
*/
//
// Original Author:  Chris McGinn - in Style of HiFJRhoProducer
//         Created:  Mon, 29 May 2017
//
//

#include <memory>
#include <string>

#include "TMath.h"

#include "RecoHI/HiJetAlgos/plugins/HiPuRhoProducer.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/isFinite.h"

#include "Geometry/Records/interface/CaloGeometryRecord.h"

using namespace edm;
using namespace pat;

//using ival = boost::icl::interval<double>;

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
HiPuRhoProducer::HiPuRhoProducer(const edm::ParameterSet& iConfig) : 
  dropZeroTowers_(iConfig.getUntrackedParameter<bool>("dropZeroTowers",true)),
  nSigmaPU_(iConfig.getParameter<double>("nSigmaPU")),
  radiusPU_(iConfig.getParameter<double>("radiusPU")),
  rParam_(iConfig.getParameter<double>("rParam")),
  src_(iConfig.getParameter<edm::InputTag>("src"))
{
  if(iConfig.exists("puPtMin")) puPtMin_ = iConfig.getParameter<double>("puPtMin");
  else{
    puPtMin_ = 10;
    edm::LogWarning("MisConfiguration")<<"the parameter puPtMin is now necessary for PU substraction. setting it to "<<puPtMin_;
  }

  if(iConfig.exists("minimumTowersFraction")){
    minimumTowersFraction_ = iConfig.getParameter<double>("minimumTowersFraction");
    std::cout << "LIMITING THE MINIMUM TOWERS FRACTION TO: " << minimumTowersFraction_ << std::endl;
  }
  else{
    minimumTowersFraction_ = 0;
    std::cout<< "ATTENTION - NOT LIMITING THE MINIMUM TOWERS FRACTION" << std::endl;
  }

  if(iConfig.exists("medianWindowWidth")) medianWindowWidth_ = iConfig.getParameter<int>("medianWindowWidth");
  else medianWindowWidth_ = 0;

  if(iConfig.exists("towSigmaCut")) towSigmaCut_ = iConfig.getParameter<double>("towSigmaCut");
  else towSigmaCut_ = -1.;

  input_candidateview_token_ = consumes<reco::CandidateView>(src_);

  etaEdgeLow_.reserve(nEtaTow_);
  etaEdgeHi_.reserve(nEtaTow_);
  etaEdges_.reserve(nEtaTow_+1);
  rho_.reserve(nEtaTow_);
  rhoMedian_.reserve(nEtaTow_);
  rhoExtra_.reserve(nEtaTow_);
  rhoM_.reserve(nEtaTow_);
  nTow_.reserve(nEtaTow_);
  towExcludePt_.reserve(nEtaTow_);
  towExcludeEta_.reserve(nEtaTow_);
  towExcludePhi_.reserve(nEtaTow_);

  const double etatow[42] = {0.000, 0.087, 0.174, 0.261, 0.348, 0.435, 0.522, 0.609, 0.696, 0.783, 0.870, 0.957, 1.044, 1.131, 1.218, 1.305, 1.392, 1.479, 1.566, 1.653, 1.740, 1.830, 1.930, 2.043, 2.172, 2.322, 2.500, 2.650, 2.853, 3.000, 3.139, 3.314, 3.489, 3.664, 3.839, 4.013, 4.191, 4.363, 4.538, 4.716, 4.889, 5.191};

  for(int i=0;i<42;i++){
    etaedge[i]=etatow[i];
  }

  //register your products
  produces<std::vector<double> >("mapEtaEdges");
  produces<std::vector<double> >("mapToRho");
  produces<std::vector<double> >("mapToRhoMedian");
  produces<std::vector<double> >("mapToRhoExtra");
  produces<std::vector<double> >("mapToRhoM");
  produces<std::vector<double> >("ptJets");
  produces<std::vector<double> >("areaJets");
  produces<std::vector<double> >("etaJets");
  produces<std::vector<int> >("mapToNTow");
  produces<std::vector<double> >("mapToTowExcludePt");
  produces<std::vector<double> >("mapToTowExcludePhi");
  produces<std::vector<double> >("mapToTowExcludeEta");
}


HiPuRhoProducer::~HiPuRhoProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}

// ------------ method called to produce the data  ------------
void HiPuRhoProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  
  setupGeometryMap(iEvent, iSetup);

  etaEdgeLow_.clear();
  etaEdgeHi_.clear();
  etaEdges_.clear();
  rho_.clear();
  rhoMedian_.clear();
  rhoExtra_.clear();
  rhoM_.clear();
  nTow_.clear();
  towExcludePt_.clear();
  towExcludePhi_.clear();
  towExcludeEta_.clear();

  inputs_.clear();
  fjInputs_.clear();
  fjJets_.clear();

  // Get the particletowers
  edm::Handle<reco::CandidateView> inputsHandle;
  iEvent.getByToken(input_candidateview_token_, inputsHandle);

  for(size_t i = 0; i < inputsHandle->size(); ++i){
    inputs_.push_back(inputsHandle->ptrAt(i));
  }

  fjInputs_.reserve(inputs_.size());
  inputTowers();
  fjOriginalInputs_ = fjInputs_;

  calculatePedestal(fjInputs_);
  subtractPedestal(fjInputs_);

  fjJetDefinition_= JetDefPtr(new fastjet::JetDefinition(fastjet::antikt_algorithm, rParam_));
  fjClusterSeq_ = ClusterSequencePtr(new fastjet::ClusterSequence(fjInputs_, *fjJetDefinition_));
  fjJets_ = fastjet::sorted_by_pt(fjClusterSeq_->inclusive_jets(puPtMin_));

  etaEdgeLow_.clear();
  etaEdgeHi_.clear();
  etaEdges_.clear();
  rho_.clear();
  rhoMedian_.clear();
  rhoExtra_.clear();
  rhoM_.clear();
  nTow_.clear();
  towExcludePt_.clear();
  towExcludePhi_.clear();
  towExcludeEta_.clear();

  std::vector<fastjet::PseudoJet> orphanInput;
  calculateOrphanInput(orphanInput);
  calculatePedestal(orphanInput);
  packageRho();
  putRho(iEvent, iSetup);
}

void HiPuRhoProducer::inputTowers( )
{
  std::vector<edm::Ptr<reco::Candidate> >::const_iterator inBegin = inputs_.begin(),
    inEnd = inputs_.end(), i = inBegin;
  for(; i != inEnd; ++i){
    reco::CandidatePtr input = *i;
    
    if(edm::isNotFinite(input->pt())) continue;
    if(input->pt() < 100*std::numeric_limits<double>::epsilon()) continue;
    
    fjInputs_.push_back(fastjet::PseudoJet(input->px(),input->py(),input->pz(), input->energy()));
    fjInputs_.back().set_user_index(i - inBegin);
  }
}

void HiPuRhoProducer::setupGeometryMap(edm::Event& iEvent,const edm::EventSetup& iSetup)
{

  LogDebug("PileUpSubtractor")<<"The subtractor setting up geometry...\n";

  if(geo_ == 0) {
    edm::ESHandle<CaloGeometry> pG;
    iSetup.get<CaloGeometryRecord>().get(pG);
    geo_ = pG.product();
    std::vector<DetId> alldid =  geo_->getValidDetIds();

    int ietaold = -10000;
    ietamax_ = -10000;
    ietamin_ = 10000;
    for(std::vector<DetId>::const_iterator did=alldid.begin(); did != alldid.end(); did++){
      if((*did).det() == DetId::Hcal){
        HcalDetId hid = HcalDetId(*did);
        if((hid).depth() == 1){
          allgeomid_.push_back(*did);

          if((hid).ieta() != ietaold){
            ietaold = (hid).ieta();
            geomtowers_[(hid).ieta()] = 1;
            if((hid).ieta() > ietamax_) ietamax_ = (hid).ieta();
            if((hid).ieta() < ietamin_) ietamin_ = (hid).ieta();
          }
          else{
            geomtowers_[(hid).ieta()]++;
          }
        }
      }
    }
  }

  for (int i = ietamin_; i<ietamax_+1; i++) {
    ntowersWithJets_[i] = 0;
  }
}


void HiPuRhoProducer::calculatePedestal(std::vector<fastjet::PseudoJet> const & coll)
{
  LogDebug("PileUpSubtractor")<<"The subtractor calculating pedestals...\n";

  std::map<int,double> emean2;
  std::map<int,int> ntowers;

  int ietaold = -10000;
  int ieta0 = -100;
  // Initial values for emean_, emean2, esigma_, ntowers
  
  for(int vi = 0; vi < nEtaTow_; ++vi){
    int it = vi+1;
    if(it > nEtaTow_/2) it = vi - nEtaTow_;

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
    vrho1[vi] = -99;
    
    if((*(ntowersWithJets_.find(it))).second == 0){
      vmean0[vi] = -99;
      vrms0[vi] = -99;
      vrho0[vi] = -99;
    }
  }

  for(int i = ietamin_; i < ietamax_+1; i++){
    emean_[i] = 0.;
    emean2[i] = 0.;
    esigma_[i] = 0.;
    ntowers[i] = 0;

    eTop4_[i] = {0., 0., 0., 0.};
  }

  for(std::vector<fastjet::PseudoJet>::const_iterator input_object = coll.begin(),
	fjInputsEnd = coll.end();
      input_object != fjInputsEnd; ++input_object){
    
    const reco::CandidatePtr & originalTower= inputs_[ input_object->user_index()];
    ieta0 = ieta(originalTower);
    double Original_Et = originalTower->et();
    //    if(sumRecHits_) Original_Et = getEt(originalTower);

    if(Original_Et > eTop4_[ieta0][0]){
      eTop4_[ieta0][3] = eTop4_[ieta0][2];
      eTop4_[ieta0][2] = eTop4_[ieta0][1];
      eTop4_[ieta0][1] = eTop4_[ieta0][0];
      eTop4_[ieta0][0] = Original_Et;
    }
    else if(Original_Et > eTop4_[ieta0][1]){
      eTop4_[ieta0][3] = eTop4_[ieta0][2];
      eTop4_[ieta0][2] = eTop4_[ieta0][1];
      eTop4_[ieta0][1] = Original_Et;
    }
    else if(Original_Et > eTop4_[ieta0][2]){
      eTop4_[ieta0][3] = eTop4_[ieta0][2];
      eTop4_[ieta0][2] = Original_Et;
    }
    else if(Original_Et > eTop4_[ieta0][3]){
      eTop4_[ieta0][3] = Original_Et;
    }

    
    if(ieta0-ietaold != 0){
      emean_[ieta0] = emean_[ieta0]+Original_Et;
      emean2[ieta0] = emean2[ieta0]+Original_Et*Original_Et;
      ntowers[ieta0] = 1;
      ietaold = ieta0;
    }
    else{
      emean_[ieta0] = emean_[ieta0]+Original_Et;
      emean2[ieta0] = emean2[ieta0]+Original_Et*Original_Et;
      ntowers[ieta0]++;
    }
  }


  for(std::map<int,int>::const_iterator gt = geomtowers_.begin(); gt != geomtowers_.end(); gt++){
    int it = (*gt).first;
    
    int vi = it-1;

    if(it < 0) vi = nEtaTow_ + it;

    double e1 = (*(emean_.find(it))).second;
    double e2 = (*emean2.find(it)).second;
    int nt = (*gt).second - (*(ntowersWithJets_.find(it))).second;

    if(vi < nEtaTow_){
      vngeom[vi] = (*gt).second;
      vntow[vi] = nt;
    }

    LogDebug("PileUpSubtractor")<<" ieta : "<<it<<" number of towers : "<<nt<<" e1 : "<<e1<<" e2 : "<<e2<<"\n";
  
    if(nt > 0){
      if(postOrphan_){
	
	if(nt > (int)minimumTowersFraction_*((*gt).second)){
	  emean_[it] = e1/(double)nt;
	  double eee = e2/(double)nt - e1*e1/(double)(nt*nt);
	  if(eee<0.) eee = 0.;
	  esigma_[it] = nSigmaPU_*sqrt(eee);
	  
	  unsigned int numToCheck = std::min(int(eTop4_[it].size()), nt - (int)minimumTowersFraction_*((*gt).second));
	  //	  unsigned int numToCheck = std::max(0, nt - ((*gt).second) + 4);

	  for(unsigned int lI = 0; lI < numToCheck; ++lI){
	    if(eTop4_[it][lI] >= emean_[it] + towSigmaCut_*esigma_[it] && towSigmaCut_ > 0){
	      e1 -= eTop4_[it][lI];
	      nt -= 1;
	    }
	    else break;
	  }

	  if(e1 < .000000001) e1 = 0;
	}
      }
    
      emean_[it] = e1/(double)nt;
      double eee = e2/nt - e1*e1/(nt*nt);
      if(eee<0.) eee = 0.;
      esigma_[it] = nSigmaPU_*sqrt(eee);

      double etaWidth = etaedge[abs(it)] - etaedge[abs(it)-1];
      if(etaWidth < 0) etaWidth *= -1.;
    
      int sign = 1;
      if(it < 0){
	sign = -1;
      }
      
      if(double(sign)*etaedge[abs(it)] < double(sign)*etaedge[abs(it)-1]){
	etaEdgeLow_.push_back(double(sign)*etaedge[abs(it)]);
	etaEdgeHi_.push_back(double(sign)*etaedge[abs(it)-1]);
      }
      else{
	etaEdgeHi_.push_back(double(sign)*etaedge[abs(it)]);
	etaEdgeLow_.push_back(double(sign)*etaedge[abs(it)-1]);
      }

      if(vi < nEtaTow_){
	vmean1[vi] = emean_[it];
	//vrho1[vi] = emean_[it]/(etaWidth*(2.*3.14159265359/(double)nt));
	vrho1[vi] = emean_[it]/(etaWidth*(2.*3.14159265359/(double)vngeom[vi]));//THIS WAS A MISTAKE, OVERESTIMATE RHO ~15%
	rho_.push_back(vrho1[vi]);
	rhoMedian_.push_back(vrho1[vi]);
	rhoM_.push_back(0);
	vrms1[vi] = esigma_[it];
	if(vngeom[vi] == vntow[vi]){
	  vmean0[vi] = emean_[it];
	  vrho0[vi] = emean_[it]/(etaWidth*(2.*3.14159265359/(double)vngeom[vi]));//THIS WAS A MISTAKE, OVERESTIMATE RHO ~15%
	  //	  vrho0[vi] = emean_[it]/(etaWidth*(2.*3.14159265359/(double)nt));
	  //	  rho_.push_back(vrho0[vi]);
	  vrms0[vi] = esigma_[it];
	}
	rhoExtra_.push_back(vrho0[vi]);
	nTow_.push_back(vntow[vi]);
      }
    }
    else{
      emean_[it] = 0.;
      esigma_[it] = 0.;
    }
    LogDebug("PileUpSubtractor")<<" ieta : "<<it<<" Pedestals : "<<emean_[it]<<"  "<<esigma_[it]<<"\n";
  }

  postOrphan_ = false;
}


void HiPuRhoProducer::subtractPedestal(std::vector<fastjet::PseudoJet> & coll)
{

  LogDebug("PileUpSubtractor")<<"The subtractor subtracting pedestals...\n";
  int it = -100;
  std::vector<fastjet::PseudoJet> newcoll;

  for(std::vector<fastjet::PseudoJet>::iterator input_object = coll.begin(),
	fjInputsEnd = coll.end();
      input_object != fjInputsEnd; ++input_object){

    reco::CandidatePtr const & itow = inputs_[input_object->user_index()];

    it = ieta(itow);
    iphi(itow);

    double Original_Et = itow->et();
    //    if(sumRecHits_) Original_Et = getEt(itow);

    double etnew = Original_Et - (*(emean_.find(it))).second - (*(esigma_.find(it))).second;
    float mScale = etnew/input_object->Et();
    if(etnew < 0.) mScale = 0.;

    math::XYZTLorentzVectorD towP4(input_object->px()*mScale, input_object->py()*mScale,
				   input_object->pz()*mScale, input_object->e()*mScale);

    int index = input_object->user_index();
    input_object->reset_momentum(towP4.px(),
				 towP4.py(),
				 towP4.pz(),
				 towP4.energy());
    input_object->set_user_index(index);

    if(etnew > 0. && dropZeroTowers_) newcoll.push_back(*input_object);
  }

  if(dropZeroTowers_) coll = newcoll;
}


void HiPuRhoProducer::calculateOrphanInput(std::vector<fastjet::PseudoJet> & orphanInput)
{
  LogDebug("PileUpSubtractor")<<"The subtractor calculating orphan input...\n";
  
  fjInputs_ = fjOriginalInputs_;
  
  std::vector<int> jettowers; // vector of towers indexed by "user_index"                                                
  std::vector<std::pair<int,int> >  excludedTowers; // vector of excluded ieta, iphi values                                   

  std::vector<fastjet::PseudoJet>::iterator pseudojetTMP = fjJets_.begin(),
    fjJetsEnd = fjJets_.end();

  nref = 0;

  for(; pseudojetTMP != fjJetsEnd; ++pseudojetTMP){
    if(nref < nMaxJets_){
      jtexngeom[nref] = 0;
      jtexntow[nref] = 0;
      jtexpt[nref] = 0;
      jtpt[nref] = pseudojetTMP->perp();
      jteta[nref] = pseudojetTMP->eta();
      jtphi[nref] = pseudojetTMP->phi();
    }
    
    if(pseudojetTMP->perp() < puPtMin_) continue;

    for(std::vector<HcalDetId>::const_iterator im = allgeomid_.begin(); im != allgeomid_.end(); im++){
      double dr = reco::deltaR(geo_->getPosition((DetId)(*im)),(*pseudojetTMP));
      std::vector<std::pair<int,int> >::const_iterator exclude = find(excludedTowers.begin(),excludedTowers.end(),std::pair<int,int>(im->ieta(),im->iphi()));
      if(dr < radiusPU_ && exclude == excludedTowers.end() && (geomtowers_[(*im).ieta()] - ntowersWithJets_[(*im).ieta()]) > minimumTowersFraction_*(geomtowers_[(*im).ieta()])){
	ntowersWithJets_[(*im).ieta()]++;
	excludedTowers.push_back(std::pair<int,int>(im->ieta(),im->iphi()));

	

	if(nref < nMaxJets_) jtexngeom[nref]++;
      }
    }

    std::vector<fastjet::PseudoJet>::const_iterator it = fjInputs_.begin(),
      fjInputsEnd = fjInputs_.end();

    for(; it != fjInputsEnd; ++it){
      int index = it->user_index();
      int ie = ieta(inputs_[index]);
      int ip = iphi(inputs_[index]);
      std::vector<std::pair<int,int> >::const_iterator exclude = find(excludedTowers.begin(),excludedTowers.end(),std::pair<int,int>(ie,ip));
      if(exclude != excludedTowers.end()){
        jettowers.push_back(index);
      }
    }

    for(it = fjInputs_.begin(); it != fjInputsEnd; ++it){
      int index = it->user_index();
      const reco::CandidatePtr& originalTower = inputs_[index];
      double dr = reco::deltaR((*it),(*pseudojetTMP));

      if(dr < radiusPU_){
        if(nref < nMaxJets_){
          jtexntow[nref]++;
          jtexpt[nref] += originalTower->pt();
        }
      }      
    }



    if(nref < nMaxJets_) nref++;
  } // pseudojets    
  // Create a new collections from the towers not included in jets                                                  
  //                                                                                                                

  for(std::vector<fastjet::PseudoJet>::const_iterator it = fjInputs_.begin(),
        fjInputsEnd = fjInputs_.end(); it != fjInputsEnd; ++it){

    int index = it->user_index();
    std::vector<int>::const_iterator itjet = find(jettowers.begin(),jettowers.end(),index);
    if(itjet == jettowers.end()){
      const reco::CandidatePtr& originalTower = inputs_[index];
      fastjet::PseudoJet orphan(originalTower->px(),originalTower->py(),originalTower->pz(),originalTower->energy());
      orphan.set_user_index(index);
      orphanInput.push_back(orphan);
    }
    else{
      const reco::CandidatePtr& originalTower = inputs_[index];
      towExcludePt_.push_back(originalTower->pt());
      towExcludePhi_.push_back(originalTower->phi());
      towExcludeEta_.push_back(originalTower->eta());
    }
  }

  postOrphan_ = true;
}


void HiPuRhoProducer::packageRho()
{
  unsigned int etaPos = 0;
  while(etaPos < etaEdgeLow_.size()){
    bool isSwapDone = false;
    for(unsigned int etaIter = etaPos+1; etaIter < etaEdgeLow_.size(); ++etaIter){
      if(etaEdgeLow_.at(etaPos) > etaEdgeLow_.at(etaIter)){
	double tempEtaEdgeLow = etaEdgeLow_.at(etaPos);
	double tempEtaEdgeHi = etaEdgeHi_.at(etaPos);
	double tempRho = rho_.at(etaPos);
	double tempRhoMedian = rhoMedian_.at(etaPos);
	double tempRhoExtra = rhoExtra_.at(etaPos);
	double tempRhoM = rhoM_.at(etaPos);
	double tempNTow = nTow_.at(etaPos);

	etaEdgeLow_.at(etaPos) = etaEdgeLow_.at(etaIter);
	etaEdgeHi_.at(etaPos) = etaEdgeHi_.at(etaIter);
	rho_.at(etaPos) = rho_.at(etaIter);
	rhoMedian_.at(etaPos) = rhoMedian_.at(etaIter);
	rhoExtra_.at(etaPos) = rhoExtra_.at(etaIter);
	rhoM_.at(etaPos) = rhoM_.at(etaIter);
	nTow_.at(etaPos) = nTow_.at(etaIter);

	etaEdgeLow_.at(etaIter) = tempEtaEdgeLow;
        etaEdgeHi_.at(etaIter) = tempEtaEdgeHi;
        rho_.at(etaIter) = tempRho;
        rhoMedian_.at(etaIter) = tempRhoMedian;
        rhoExtra_.at(etaIter) = tempRhoExtra;
        rhoM_.at(etaIter) = tempRhoM;
        nTow_.at(etaIter) = tempNTow;

	isSwapDone = true;
      }
    }

    if(!isSwapDone) ++etaPos;
  }

  for(unsigned int etaIter = 0; etaIter < etaEdgeLow_.size(); ++etaIter){
    etaEdges_.push_back(etaEdgeLow_.at(etaIter));
  }
  etaEdges_.push_back(etaEdgeHi_.at(etaEdgeHi_.size()-1));

  for(unsigned int rhoIter = medianWindowWidth_; rhoIter < rho_.size()-medianWindowWidth_; ++rhoIter){
    std::vector<float> tempRhoMed;
    for(unsigned int rI = rhoIter - medianWindowWidth_; rI <= rhoIter+medianWindowWidth_; ++rI){tempRhoMed.push_back(rho_.at(rI));}
    std::sort(tempRhoMed.begin(), tempRhoMed.end());
    rhoMedian_.at(rhoIter) = tempRhoMed.at(tempRhoMed.size()/2);
  }
}


void HiPuRhoProducer::putRho(edm::Event& iEvent,const edm::EventSetup& iSetup)
{
  auto mapEtaRangesOut = std::make_unique<std::vector<double> >(83,-999.);
  auto mapToRhoOut = std::make_unique<std::vector<double> >(82,-999.);
  auto mapToRhoMedianOut = std::make_unique<std::vector<double> >(82,-999.);
  auto mapToRhoExtraOut = std::make_unique<std::vector<double> >(82,-999.);
  auto mapToRhoMOut = std::make_unique<std::vector<double> >(82,-999.);
  auto mapToNTowOut = std::make_unique<std::vector<int> >(82,-999.);
  auto mapToTowExcludePtOut = std::make_unique<std::vector<double> >(towExcludePt_.size(),-999.);
  auto mapToTowExcludePhiOut = std::make_unique<std::vector<double> >(towExcludePhi_.size(),-999.);
  auto mapToTowExcludeEtaOut = std::make_unique<std::vector<double> >(towExcludeEta_.size(),-999.);
  auto ptJetsOut = std::make_unique<std::vector<double> >(0,1e-6);
  auto areaJetsOut = std::make_unique<std::vector<double> >(0,1e-6);
  auto etaJetsOut = std::make_unique<std::vector<double> >(0,1e-6);

  for(unsigned int etaIter = 0; etaIter < etaEdges_.size(); ++etaIter){
    mapEtaRangesOut->at(etaIter) = etaEdges_.at(etaIter);
  }

  for(unsigned int rhoIter = 0; rhoIter < rho_.size(); ++rhoIter){
    mapToRhoOut->at(rhoIter) = rho_.at(rhoIter);
    mapToRhoMedianOut->at(rhoIter) = rhoMedian_.at(rhoIter);
    mapToRhoExtraOut->at(rhoIter) = rhoExtra_.at(rhoIter);
    mapToRhoMOut->at(rhoIter) = rhoM_.at(rhoIter);
    mapToNTowOut->at(rhoIter) = nTow_.at(rhoIter);
  }
  
  for(unsigned int excTowIter = 0; excTowIter < towExcludePt_.size(); ++excTowIter){
    mapToTowExcludePtOut->at(excTowIter) = towExcludePt_.at(excTowIter);
    mapToTowExcludePhiOut->at(excTowIter) = towExcludePhi_.at(excTowIter);
    mapToTowExcludeEtaOut->at(excTowIter) = towExcludeEta_.at(excTowIter);
  }

  iEvent.put(std::move(mapEtaRangesOut), "mapEtaEdges");
  iEvent.put(std::move(mapToRhoOut), "mapToRho");
  iEvent.put(std::move(mapToRhoMedianOut), "mapToRhoMedian");
  iEvent.put(std::move(mapToRhoExtraOut), "mapToRhoExtra");
  iEvent.put(std::move(mapToRhoMOut), "mapToRhoM");
  iEvent.put(std::move(mapToNTowOut), "mapToNTow");
  iEvent.put(std::move(mapToTowExcludePtOut), "mapToTowExcludePt");
  iEvent.put(std::move(mapToTowExcludePhiOut), "mapToTowExcludePhi");
  iEvent.put(std::move(mapToTowExcludeEtaOut), "mapToTowExcludeEta");
  iEvent.put(std::move(ptJetsOut), "ptJets");
  iEvent.put(std::move(areaJetsOut), "areaJets");
  iEvent.put(std::move(etaJetsOut), "etaJets");
}


// ------------ method called once each job just before starting event loop  ------------
void 
HiPuRhoProducer::beginJob()
{

}

// ------------ method called once each job just after ending the event loop  ------------
void 
HiPuRhoProducer::endJob() {
}
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void HiPuRhoProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


int HiPuRhoProducer::ieta(const reco::CandidatePtr & in) const {
  int it = 0;
  const CaloTower* ctc = dynamic_cast<const CaloTower*>(in.get());
  if(ctc){
    it = ctc->id().ieta();
  } else
    {
      throw cms::Exception("Invalid Constituent") << "CaloJet constituent is not of CaloTower type";
    }
  return it;
}

int HiPuRhoProducer::iphi(const reco::CandidatePtr & in) const {
  int it = 0;
  const CaloTower* ctc = dynamic_cast<const CaloTower*>(in.get());
  if(ctc){
    it = ctc->id().iphi();
  } else
    {
      throw cms::Exception("Invalid Constituent") << "CaloJet constituent is not of CaloTower type";
    }
  return it;
}



//define this as a plug-in
DEFINE_FWK_MODULE(HiPuRhoProducer);
