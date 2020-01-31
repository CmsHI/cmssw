#ifndef __MultipleAlgoIterator_h_
#define __MultipleAlgoIterator_h_

#include "RecoJets/JetProducers/interface/PileUpSubtractor.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

class MultipleAlgoIterator : public PileUpSubtractor {
 public:
 MultipleAlgoIterator(const edm::ParameterSet& iConfig, edm::ConsumesCollector && iC);
    virtual void offsetCorrectJets();
    void rescaleRMS(double s);
    double getEt(const reco::CandidatePtr & in) const;
    double getEta(const reco::CandidatePtr & in) const;
    virtual void calculatePedestal(std::vector<fastjet::PseudoJet> const & coll);
    virtual void subtractPedestal(std::vector<fastjet::PseudoJet> & coll);
    virtual void calculateOrphanInput(std::vector<fastjet::PseudoJet> & orphanInput);

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

		double minimumTowersFraction_;

    bool sumRecHits_;
    bool dropZeroTowers_;
    ~MultipleAlgoIterator() override{;}
    
};


#endif
