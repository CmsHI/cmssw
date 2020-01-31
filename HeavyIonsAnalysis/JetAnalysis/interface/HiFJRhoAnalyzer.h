#ifndef HiJetBackground_HiFJRhoAnalyzer_h
#define HiJetBackground_HiFJRhoAnalyzer_h

// system include files
#include <memory>
#include <sstream>
#include <string>
#include <vector>

//root
#include "TTree.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

//
// class declaration
//

class HiFJRhoAnalyzer : public edm::EDAnalyzer {
   public:
      explicit HiFJRhoAnalyzer(const edm::ParameterSet&);
      ~HiFJRhoAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      //input
      edm::EDGetTokenT<std::vector<double>>                  etaToken_;
      edm::EDGetTokenT<std::vector<double>>                  rhoToken_;
      edm::EDGetTokenT<std::vector<double>>                  rhomToken_;
      edm::EDGetTokenT<std::vector<double>>                  rhoCorrToken_;
      edm::EDGetTokenT<std::vector<double>>                  rhomCorrToken_;
      edm::EDGetTokenT<std::vector<double>>                  rhoCorr1BinToken_;
      edm::EDGetTokenT<std::vector<double>>                  rhomCorr1BinToken_;
	  
      edm::EDGetTokenT<std::vector<double>>                  rhoGridToken_;
      edm::EDGetTokenT<std::vector<double>>                  meanRhoGridToken_;
      edm::EDGetTokenT<std::vector<double>>                  etaMinRhoGridToken_;
      edm::EDGetTokenT<std::vector<double>>                  etaMaxRhoGridToken_;
      
      edm::EDGetTokenT<std::vector<double>>                  ptJetsToken_;
      edm::EDGetTokenT<std::vector<double>>                  areaJetsToken_;
      edm::EDGetTokenT<std::vector<double>>                  etaJetsToken_;

      //output
      TTree *tree_;
      edm::Service<TFileService> fs_;

      struct RHO {
        std::vector<double> etaMin;
        std::vector<double> etaMax;
        std::vector<double> rho;
        std::vector<double> rhom;
        std::vector<double> rhoCorr;
        std::vector<double> rhomCorr;
        std::vector<double> rhoCorr1Bin;
        std::vector<double> rhomCorr1Bin;
		
        std::vector<double> rhoGrid;
        std::vector<double> meanRhoGrid;
        std::vector<double> etaMinRhoGrid;
        std::vector<double> etaMaxRhoGrid;
		
        std::vector<double>ptJets;
        std::vector<double>areaJets;
        std::vector<double>etaJets;
      };
      
      RHO rhoObj_;
};

#endif
