#ifndef __PuWithNtuple_h_
#define __PuWithNtuple_h_

#include "RecoJets/JetProducers/interface/PileUpSubtractor.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include <TTree.h>

class PuWithNtuple : public PileUpSubtractor {
 public:
  PuWithNtuple(const edm::ParameterSet& iConfig, edm::ConsumesCollector && iC);
    virtual void offsetCorrectJets();
    void rescaleRMS(double s);
    double getEt(const reco::CandidatePtr & in) const;
    double getEta(const reco::CandidatePtr & in) const;
    virtual void calculatePedestal(std::vector<fastjet::PseudoJet> const & coll);
    virtual void subtractPedestal(std::vector<fastjet::PseudoJet> & coll);
    virtual void calculateOrphanInput(std::vector<fastjet::PseudoJet> & orphanInput);

    bool sumRecHits_;
    bool dropZeroTowers_;
    bool isOrphanInputRun_;

    double minimumTowersFraction_;

    ~PuWithNtuple(){;}

    edm::Service<TFileService> fs_;
    TTree* tree_;

    int Neta_;

    int nref;
    float jteta[200],jtphi[200],jtpt[200],jtpu[200],jtexpt[200];
    int jtexngeom[200], jtexntow[200];

    int vngeom[82],vntow[82],vieta[82];
    float veta[82],vmean0[82],vrms0[82],vmean1[82],vrms1[82];

    double etaedge[42];
    
};


#endif
