// -*- C++ -*-
//
// Package:    RpPbAnalysis/ppPileupFilter
// Class:      ppPileupFilter
// 
/**\class ppPileupFilter ppPileupFilter.cc RpPbAnalysis/ppPileupFilter/plugins/ppPileupFilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Hong Ni
//         Created:  Thu, 10 Dec 2015 10:01:29 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//
// class declaration
//
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class ppPileupFilter : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit ppPileupFilter(const edm::ParameterSet&);
      ~ppPileupFilter();
      static bool vtxSort(const reco::Vertex & a, const reco::Vertex & b); 
      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      void initHistos(const edm::Service<TFileService> & fs);
      bool passesTrackCuts(const reco::Track & track, const reco::Vertex & vertex);

      // ----------member data ---------------------------
      TH1F *hNtrkOffline;  
      TH1F *htrkDz_notrkcut;
      TH1F *htrkDz_wtrkcut;    

      std::map<std::string, TH1F*> evtPerf_;
      std::map<std::string, TH1F*> trkPerf_;
      std::map<std::string, TH1F*> vtxPerf_;
      std::map<std::string, TH2F*> vtxPerf2D_;
 
      std::vector<double> ptBins_;    
  
      edm::EDGetTokenT<edm::View<reco::Track> > trackSrc_;
      edm::EDGetTokenT<reco::VertexCollection> vertexSrc_;
      
      double vertexZMax_;

      std::string qualityString_;
      double dzSigMax_;
      double dxySigMax_;
      double ptErrOverptMax_; 
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
ppPileupFilter::ppPileupFilter(const edm::ParameterSet& iConfig)
{
  //now do what ever initialization is needed

  trackSrc_ = consumes<edm::View<reco::Track> >(iConfig.getParameter<edm::InputTag>("trackSrc"));
  vertexSrc_ = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexSrc"));

  ptBins_ = iConfig.getParameter<std::vector<double> >("ptBins");
  vertexZMax_ = iConfig.getParameter<double>("vertexZMax"); 

  qualityString_ = iConfig.getParameter<std::string>("qualityString");
  dzSigMax_ = iConfig.getParameter<double>("dzSigMax");
  dxySigMax_ = iConfig.getParameter<double>("dxySigMax");
  ptErrOverptMax_ = iConfig.getParameter<double>("ptErrOverptMax");

  edm::Service<TFileService> fs;
  initHistos(fs);
}


ppPileupFilter::~ppPileupFilter()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
ppPileupFilter::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   Handle<edm::View<reco::Track>> tcol;
   iEvent.getByToken(trackSrc_, tcol);
   
   Handle<std::vector<reco::Vertex>> vertex;
   iEvent.getByToken(vertexSrc_, vertex);

   std::vector<reco::Vertex> vsorted = *vertex;
   std::sort(vsorted.begin(), vsorted.end(), vtxSort);

   if(vsorted.size() == 0) return;
   if(vsorted[0].tracksSize() < 2) return;
   if(fabs(vsorted[0].z()) > vertexZMax_) return;
   // int bx=iEvent.eventAuxiliary().bunchCrossing();
   // if( bx < 150 ) return;

   //find Ntrkoffline and get trkDCAz distribution
   math::XYZPoint pvPoint(0.,0.,0.);
   pvPoint = vsorted[0].position(); 

   int count = 0;
   for(auto &track : *tcol)
   {
       double trkdz = track.dz(pvPoint);
       htrkDz_notrkcut->Fill(trkdz);          
 
       if(!passesTrackCuts(track, vsorted[0])) continue;
       htrkDz_wtrkcut->Fill(trkdz);

       trkPerf_["Nhit"]->Fill(track.numberOfValidHits());
       trkPerf_["pt"]->Fill(track.pt());      
       trkPerf_["eta"]->Fill(track.eta());
       trkPerf_["phi"]->Fill(track.phi());
       trkPerf_["chi2"]->Fill(track.normalizedChi2());

       if ( fabs(track.eta()) > 2.4 || track.pt() < 0.4  ) continue;
       
       count++;   
   }

   hNtrkOffline->Fill(count);

   //fill evt perf histos
   int lumi = iEvent.getLuminosityBlock().luminosityBlock();
   evtPerf_["evtRaw"]->Fill(0.5);
   evtPerf_["Nvtx"]->Fill(vsorted.size());
   evtPerf_["Ntrk"]->Fill(tcol->size());
   evtPerf_["Lumi"]->Fill(lumi);

   //fill vtx perf histos
   int vcount = 0;
   for(auto & vi : vsorted)
   {
       vtxPerf_["Ntrk"]->Fill(vi.tracksSize());
       vtxPerf_["x"]->Fill(vi.x());
       vtxPerf_["y"]->Fill(vi.y());
       vtxPerf_["z"]->Fill(vi.z());
       vtxPerf2D_["Ntrk2D"]->Fill(vcount, vi.tracksSize());
       vcount++;
   }

   //comparison between PV and additional vtx
   for(unsigned int i = 1; i<vsorted.size(); i++)
   {
       double dx = fabs(vsorted[i].x() - vsorted[0].x());
       double dy = fabs(vsorted[i].y() - vsorted[0].y());
       double dz = fabs(vsorted[i].z() - vsorted[0].z());
       double dxy = sqrt(dx*dx + dy*dy);

       vtxPerf_["assocVtxDz"]->Fill(dz);
       vtxPerf_["assocVtxDxy"]->Fill(dxy);
       vtxPerf2D_["assocVtxDxyNtrk"]->Fill(dxy,vsorted[i].tracksSize());
       vtxPerf2D_["assocVtxDzNtrk"]->Fill(dz,vsorted[i].tracksSize());
       vtxPerf2D_["assocVtxDzNtrk_ratio"]->Fill(dz, double(vsorted[i].tracksSize() )/double(vsorted[0].tracksSize()) );
       vtxPerf2D_["assocVtxDxyDz"]->Fill(dxy,dz);
   }
  
}

bool
ppPileupFilter::passesTrackCuts(const reco::Track & track, const reco::Vertex & vertex)
{   
    math::XYZPoint vtxPoint(0.,0.,0.);
    double vzErr = 0., vxErr = 0., vyErr = 0.;
    vtxPoint = vertex.position();
    vzErr = vertex.zError();
    vxErr = vertex.xError();
    vyErr = vertex.yError();
    
    double dxy = 0., dz = 0., dxysigma = 0., dzsigma = 0.;
    dxy = track.dxy(vtxPoint);
    dz = track.dz(vtxPoint);
    dxysigma = sqrt(track.d0Error()*track.d0Error()+vxErr*vyErr);
    dzsigma = sqrt(track.dzError()*track.dzError()+vzErr*vzErr);
    
    if(track.quality(reco::TrackBase::qualityByName(qualityString_)) != 1)
        return false;
    if(fabs(dxy/dxysigma) > dxySigMax_) return false;
    if(fabs(dz/dzsigma) > dzSigMax_) return false;
    if(track.ptError() / track.pt() > ptErrOverptMax_) return false;
    
    return true;
}

void
ppPileupFilter::initHistos(const edm::Service<TFileService> & fs)
{
    hNtrkOffline = fs->make<TH1F>("hNtrkOffline","N_{trk}^{offline}",300,0,300);
    htrkDz_notrkcut = fs->make<TH1F>("htrkDz_notrkcut","track DCA to PV at z",100,-5,5);
    htrkDz_wtrkcut = fs->make<TH1F>("htrkDz_wtrkcut","track DCA to PV at z",100,-5,5);

    evtPerf_["evtRaw"] = fs->make<TH1F>("evtRaw","Raw number of events",1,0,1);
    evtPerf_["Nvtx"] = fs->make<TH1F>("evtNvtx","Primary Vertices per event",10,0,10);
    evtPerf_["Ntrk"] = fs->make<TH1F>("evtNtrk","Tracks per event",100,0,400);
    evtPerf_["Lumi"] = fs->make<TH1F>("evtLumi","Events by Lumi",200,0,2000);
    vtxPerf_["Ntrk"] = fs->make<TH1F>("vtxNtrk","Tracks Per Vertex",50,0,200);
    vtxPerf_["x"] = fs->make<TH1F>("vtxX","Vertex x position",1000,-1,1);
    vtxPerf_["y"] = fs->make<TH1F>("vtxY","Vertex y position",1000,-1,1);
    vtxPerf_["z"] = fs->make<TH1F>("vtxZ","Vertex z position",100,-30,30);    vtxPerf_["assocVtxDz"] = fs->make<TH1F>("assocVtxDz","Z Distance from first PV; dz (cm)",200,0,50);
    vtxPerf_["assocVtxDxy"] = fs->make<TH1F>("assocVtxDxy","Rho Distance from first PV; dxy (cm)",200,0,4);
    vtxPerf2D_["Ntrk2D"] = fs->make<TH2F>("vtxNtrk2D","Tracks per vertex;vertex (sorted by Ntrk);Ntrk",10,0,10,200,0,200);
    vtxPerf2D_["assocVtxDzNtrk"] = fs->make<TH2F>("assocVtxDzNtrk","Z Distance from first PV vs Ntrk of assoc; dz (cm); Ntrk",200,0,20,100,0,100);
    vtxPerf2D_["assocVtxDzNtrk_ratio"] = fs->make<TH2F>("assocVtxDzNtrk_ratio","Z Distance from first PV vs Ntrk/Ntrk1 of assoc; dz (cm); Ntrk",200,0,20,1000,0,1);
    vtxPerf2D_["assocVtxDxyNtrk"] = fs->make<TH2F>("assocVtxDxyNtrk","Rho Distance from first PV vs Ntrk of assoc; dxy (cm); Ntrk",200,0,2,100,0,100);
    vtxPerf2D_["assocVtxDxyDz"] = fs->make<TH2F>("assocVtxDxyDz","Rho Distance from frist PV vs Rho Distance from assoc;dxy(cm); dz",200,0,2,200,0,20);
    trkPerf_["Nhit"] = fs->make<TH1F>("trkNhit","Tracks by Number of Valid Hits;N hits",35,0,35);
    trkPerf_["pt"] = fs->make<TH1F>("trkPt", "Track p_{T} Distribution;p_{T} [GeV/c]",ptBins_.size()-1,&ptBins_[0]);
    trkPerf_["eta"] = fs->make<TH1F>("trkEta", "Track Pseudorapidity Distribution;#eta",50,-2.5,2.5);
    trkPerf_["phi"] = fs->make<TH1F>("trkPhi", "Track Azimuthal Distribution;#phi",100,-3.15,3.15);
    trkPerf_["chi2"] = fs->make<TH1F>("trkChi2", "Track Normalized #chi^{2};#chi^{2}/n.d.o.f",60,0,6);
     
           
}

bool
ppPileupFilter::vtxSort(const reco::Vertex & a, const reco::Vertex & b)
{
    if(a.tracksSize() != b.tracksSize())
        return a.tracksSize() > b.tracksSize() ? true : false;
    else
        return a.chi2() < b.chi2() ? true : false;
}

// ------------ method called once each job just before starting event loop  ------------
void 
ppPileupFilter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ppPileupFilter::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
ppPileupFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(ppPileupFilter);
