#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "fastjet/contrib/SoftKiller.hh"
#include "correction.h"
#include "TMVA/RBDT.hxx"
#include "TMVA/RInferenceUtils.hxx"

namespace pat {

  class HIElectronInfoProducer : public edm::global::EDProducer<> {
  public:
    explicit HIElectronInfoProducer(const edm::ParameterSet& iConfig)
        : electronToken_(consumes<pat::ElectronCollection>(iConfig.getParameter<edm::InputTag>("electrons"))),
          pfCandidateToken_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("pfCandidates"))),
          centralityToken_(consumes<int>(iConfig.getParameter<edm::InputTag>("centrality"))),
          etaToken_(consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>("etaMap"))),
          rhoToken_(consumes<std::vector<double>>(iConfig.getParameter<edm::InputTag>("rhoMap"))),
          patElectronPutToken_(produces<pat::ElectronCollection>()),
          pfMaxEta_(iConfig.getParameter<double>("pf_maxAbsEta")),
          skRadius_(iConfig.getParameter<double>("sk_radius")),
          electronMinPt_(iConfig.getParameter<double>("electron_minPt")),
          rVeto_(iConfig.getParameter<double>("iso_rVeto")),
          rCone_(iConfig.getParameter<double>("iso_rCone")),
          era_(iConfig.getParameter<std::string>("era")),
          isoCorr_(getCorrection(iConfig, "iso_rho_correction")),
          hoeCorr_(getCorrection(iConfig, "hoecorrector")),
          isoModel_(getModel(iConfig, "file_isoModel", "eleiso_BDT")),
          idModel_(getModel(iConfig, "file_idModel", "eleid_BDT")) {}
    ~HIElectronInfoProducer() override{};

    void produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const override;

    static void fillDescriptions(edm::ConfigurationDescriptions&);

  private:
    const edm::EDGetTokenT<pat::ElectronCollection> electronToken_;
    const edm::EDGetTokenT<reco::CandidateView> pfCandidateToken_;
    const edm::EDGetTokenT<int> centralityToken_;
    const edm::EDGetTokenT<std::vector<double>> etaToken_;
    const edm::EDGetTokenT<std::vector<double>> rhoToken_;
    const edm::EDPutTokenT<pat::ElectronCollection> patElectronPutToken_;

    const reco::PFCandidate convert_;
    const double pfMaxEta_, skRadius_, electronMinPt_, rVeto_, rCone_;
    const std::string era_;
    const std::shared_ptr<const correction::Correction> isoCorr_, hoeCorr_;
    const std::unique_ptr<TMVA::Experimental::RBDT<>> isoModel_, idModel_;

    std::shared_ptr<const correction::Correction> getCorrection(const edm::ParameterSet& iConfig,
                                                                const std::string& label) {
      const auto& csetIsoRhoCorrections =
          correction::CorrectionSet::from_file(iConfig.getParameter<edm::FileInPath>("file_corr").fullPath());
      return csetIsoRhoCorrections->at(label);
    }

    TMVA::Experimental::RBDT<>* getModel(const edm::ParameterSet& iConfig, const std::string& f, const std::string& l) {
      return new TMVA::Experimental::RBDT<>(l, iConfig.getParameter<edm::FileInPath>(f).fullPath());
    }

    enum WP { WP95 = 0, WP90 = 1, WP85 = 4, WP80 = 2, WP70 = 3 };
    bool passMVAIso(const double&, const double&, const bool&, const WP& wp) const;
    bool passMVAId(const double&, const double&, const bool&, const WP& wp) const;
    bool passCutID(const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const double&,
                   const bool&,
                   const WP&) const;
  };

}  // namespace pat

bool pat::HIElectronInfoProducer::passMVAIso(const double& mva,
                                             const double& cent,
                                             const bool& isEB,
                                             const WP& wp) const {
  double cut(10.);
  const auto cen = cent > 90. ? 90. : cent;
  const auto cen2 = cen * cen;
  const auto cen3 = cen * cen * cen;
  if (era_ == "Run3_2023_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = 6.050705656931276e-07 * cen3 + -8.675509363314822e-05 * cen2 + 0.002218485908134624 * cen +
              0.8117784878911797;
      else
        cut = -1.8611301873048183e-07 * cen3 + 1.1749047227407727e-05 * cen2 + -0.0004589054908512365 * cen +
              0.9243796918741759;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = 1.0706528567114571e-06 * cen3 + -0.00017034263298702041 * cen2 + 0.004158428420930109 * cen +
              0.6678062332568974;
      else
        cut = -3.748291770902249e-07 * cen3 + 1.2264518183783658e-05 * cen2 + -0.0004954559134085261 * cen +
              0.8648468182914509;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = 1.2228391411360716e-06 * cen3 + -0.0001816689395238405 * cen2 + 0.0035566414371282634 * cen +
              0.5514679545748985;
      else
        cut = -2.400909102332375e-07 * cen3 + -1.0779177540489446e-05 * cen2 + -0.0003609382150404037 * cen +
              0.8110586630738115;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = 1.1480925637812821e-06 * cen3 + -0.00016356985855249789 * cen2 + 0.0025657545636278297 * cen +
              0.45146896982940105;
      else
        cut = -1.8601466730793873e-08 * cen3 + -4.0565692662267314e-05 * cen2 + 0.00020063921014607203 * cen +
              0.745984624998374;
    }
  } else if (era_ == "Run3_2024_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = 7.109642951957174e-07 * cen3 + -8.872806476059474e-05 * cen2 + 0.002028107140882347 * cen +
              0.8084472802958512;
      else
        cut = 2.2444480569042535e-07 * cen3 + -4.0312657816409935e-05 * cen2 + 0.0017399548982262318 * cen +
              0.8944826095832374;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = 1.0832974048376298e-06 * cen3 + -0.00015826155906626017 * cen2 + 0.0036083128567260254 * cen +
              0.6603427035366111;
      else
        cut = 6.17753744613321e-08 * cen3 + -3.439725427500278e-05 * cen2 + 0.00151151895502841 * cen +
              0.8303951838511106;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = 1.063943232309302e-06 * cen3 + -0.00015177221779582225 * cen2 + 0.0024999629652588274 * cen +
              0.5413676552774369;
      else
        cut = 1.2154591258860994e-07 * cen3 + -4.946728408749522e-05 * cen2 + 0.001717484272457839 * cen +
              0.7663510371295376;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = 9.465688589264508e-07 * cen3 + -0.00013124331249976786 * cen2 + 0.0015089832226412346 * cen +
              0.4368616774414533;
      else
        cut = 2.0264667376111144e-07 * cen3 + -6.254410466971262e-05 * cen2 + 0.0018466814015436922 * cen +
              0.6976133751479653;
    }
  } else if (era_ == "Run3_2025_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = 7.153984680058798e-07 * cen3 + -7.594550190459527e-05 * cen2 + 0.0007531760133602444 * cen +
              0.8688789278109084;
      else
        cut = 1.6455067065625354e-07 * cen3 + -2.117704810366124e-05 * cen2 + 2.9481308041491354e-05 * cen +
              0.9358478795494535;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = 1.055757464167042e-06 * cen3 + -0.00013275589872070547 * cen2 + 0.0011361236298112357 * cen +
              0.7569376744997602;
      else
        cut = -1.2737118642305232e-07 * cen3 + 3.4953499748282335e-06 * cen2 + -0.0016549808349599238 * cen +
              0.9025720919104148;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = 1.1496036725645927e-06 * cen3 + -0.00013792017828673488 * cen2 + -0.00023902495205989894 * cen +
              0.6574063371068777;
      else
        cut = -7.357694325905743e-08 * cen3 + -9.593356492086259e-06 * cen2 + -0.0021724237423018378 * cen +
              0.8595927923198561;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = 9.30281194149958e-07 * cen3 + -9.91527250478951e-05 * cen2 + -0.0023188791553027865 * cen +
              0.5658947268153894;
      else
        cut = 5.6593910044829465e-08 * cen3 + -2.3736390766574776e-05 * cen2 + -0.002767179269256407 * cen +
              0.815602834542731;
    }
  } else if (era_ == "Run3_2026_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = 7.217787467296688e-07 * cen3 + -7.64487924676041e-05 * cen2 + 0.0007540923015873242 * cen +
              0.8689745134058919;
      else
        cut = 1.5170125896940316e-07 * cen3 + -1.9774011810217074e-05 * cen2 + -2.54942703206216e-06 * cen +
              0.9358629504686591;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = 1.0644994458381363e-06 * cen3 + -0.00013389877077818013 * cen2 + 0.0011649054767034984 * cen +
              0.7569645253248685;
      else
        cut = -1.0608406609427081e-07 * cen3 + 3.8848617911052485e-07 * cen2 + -0.0015413347643396232 * cen +
              0.9018901108491791;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = 1.1636492280071092e-06 * cen3 + -0.00013951668297582974 * cen2 + -0.00019435312810817763 * cen +
              0.6572287463717116;
      else
        cut = -6.506886642688687e-08 * cen3 + -1.0610580199024548e-05 * cen2 + -0.0021532003621548795 * cen +
              0.8594102222955649;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = 9.325682645017744e-07 * cen3 + -9.953909663611066e-05 * cen2 + -0.0023016036081423747 * cen +
              0.56578911759451;
      else
        cut = 3.878237278184764e-08 * cen3 + -2.166453069424242e-05 * cen2 + -0.0028272691691731706 * cen +
              0.8161189593712405;
    }
  } else
    throw std::logic_error("[ERROR] Wrong era for HIElectronInfoProducer");
  return mva < cut;
}

bool pat::HIElectronInfoProducer::passMVAId(const double& mva, const double& cen, const bool& isEB, const WP& wp) const {
  double cut(10.);
  const auto cen2 = cen * cen;
  const auto cen3 = cen * cen * cen;
  if (era_ == "Run3_2023_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = -1.5240230468578694e-06 * cen3 + 0.0002423784162638523 * cen2 + -0.01331529410784093 * cen +
              0.5418680077670319;
      else
        cut = -1.294660595473618e-06 * cen3 + 0.00021554060597753889 * cen2 + -0.014278841680646814 * cen +
              0.8854193584785804;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = -6.396975957346326e-07 * cen3 + 0.00010828855098015914 * cen2 + -0.006423750716195923 * cen +
              0.2405424125484589;
      else
        cut = -1.7981901242892499e-06 * cen3 + 0.00029886869533678824 * cen2 + -0.017975261462461374 * cen +
              0.7166095818301947;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = -3.439056749932262e-07 * cen3 + 5.7946444409353315e-05 * cen2 + -0.003334025188592283 * cen +
              0.11900357131088288;
      else
        cut = -1.184263124123819e-06 * cen3 + 0.0002046266340841097 * cen2 + -0.013146379531433829 * cen +
              0.5180183882619553;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = -1.6118542418468373e-07 * cen3 + 2.7232687402092295e-05 * cen2 + -0.001589681449002205 * cen +
              0.06374074252135704;
      else
        cut = -7.777733099289559e-07 * cen3 + 0.0001398756083096567 * cen2 + -0.009560014392973095 * cen +
              0.37951347202856184;
    }
  } else if (era_ == "Run3_2024_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = -1.297095217577941e-06 * cen3 + 0.0002120174570633429 * cen2 + -0.012397915335399025 * cen +
              0.5426323794735601;
      else
        cut = -1.2757640348667187e-06 * cen3 + 0.00020678457465295516 * cen2 + -0.013300802612760298 * cen +
              0.833232587490345;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = -5.350792129539487e-07 * cen3 + 9.439527400459571e-05 * cen2 + -0.0060705860524204 * cen +
              0.2425709435740952;
      else
        cut = -1.4408134003617199e-06 * cen3 + 0.0002404548628670886 * cen2 + -0.015025878791121038 * cen +
              0.6458629577292293;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = -2.839047394143468e-07 * cen3 + 5.080521341738257e-05 * cen2 + -0.0032480658785239104 * cen +
              0.12244430934832529;
      else
        cut = -1.0077249048545508e-06 * cen3 + 0.0001767124348500872 * cen2 + -0.011750994486350573 * cen +
              0.4746829057041775;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = -1.4624001978640575e-07 * cen3 + 2.613936769160016e-05 * cen2 + -0.0016751594216330035 * cen +
              0.06586320501219185;
      else
        cut = -7.24468729787579e-07 * cen3 + 0.0001317304649291509 * cen2 + -0.008970938384534681 * cen +
              0.3458153561788365;
    }
  } else if (era_ == "Run3_2025_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = -1.6359888690453566e-06 * cen3 + 0.0002722503475537796 * cen2 + -0.015819728049471557 * cen +
              0.5883378474351182;
      else
        cut = -6.481224406650867e-07 * cen3 + 0.0001379795297293089 * cen2 + -0.013417441044108105 * cen +
              0.8474018210818155;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = -9.397768059150222e-07 * cen3 + 0.0001583013928916616 * cen2 + -0.00907711703755352 * cen +
              0.2741949453695386;
      else
        cut = -1.4336118975399723e-06 * cen3 + 0.0002757239036878914 * cen2 + -0.019604263892456775 * cen +
              0.7037150500058229;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = -4.866617489631336e-07 * cen3 + 8.309333971327067e-05 * cen2 + -0.004782152592841904 * cen +
              0.13666422067853343;
      else
        cut = -1.6580292058765154e-06 * cen3 + 0.00030309935163314527 * cen2 + -0.019320339885359594 * cen +
              0.5580259314610615;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = -2.656449145120441e-07 * cen3 + 4.5212383612225475e-05 * cen2 + -0.002571255417385907 * cen +
              0.07262545446269467;
      else
        cut = -1.5244532963683015e-06 * cen3 + 0.00027251388537854695 * cen2 + -0.016550840870570332 * cen +
              0.4302351175940266;
    }
  } else if (era_ == "Run3_2026_PbPb") {
    //Working point: WP95
    if (wp == WP95) {
      if (isEB)
        cut = -1.6333777687033803e-06 * cen3 + 0.00027216199023910397 * cen2 + -0.01583104313604055 * cen +
              0.5886781724010374;
      else
        cut = -6.439965866049528e-07 * cen3 + 0.00013689936686016728 * cen2 + -0.013346543155890444 * cen +
              0.8469315518791294;
    }
    //Working point: WP90
    else if (wp == WP90) {
      if (isEB)
        cut = -9.391612052997617e-07 * cen3 + 0.00015833278223756779 * cen2 + -0.009085696153703538 * cen +
              0.2744020692132599;
      else
        cut = -1.4555878762884259e-06 * cen3 + 0.00027826089029688814 * cen2 + -0.019678611608093678 * cen +
              0.7044204374001843;
    }
    //Working point: WP85
    else if (wp == WP85) {
      if (isEB)
        cut = -4.864549249542749e-07 * cen3 + 8.311921059168683e-05 * cen2 + -0.004787461117523357 * cen +
              0.13679680359664048;
      else
        cut = -1.6517069188557994e-06 * cen3 + 0.00030210207821817093 * cen2 + -0.01928114753088982 * cen +
              0.5579889534239683;
    }
    //Working point: WP80
    else if (wp == WP80) {
      if (isEB)
        cut = -2.6572346465729227e-07 * cen3 + 4.523495480219165e-05 * cen2 + -0.0025732357082070226 * cen +
              0.07266411633969566;
      else
        cut = -1.5259871203653157e-06 * cen3 + 0.00027255781900584734 * cen2 + -0.01654844526831775 * cen +
              0.43038915633448804;
    }
  } else
    throw std::logic_error("[ERROR] Wrong era for HIElectronInfoProducer");
  return mva < cut;
}

bool pat::HIElectronInfoProducer::passCutID(const double& sInIn,
                                            const double& adEta,
                                            const double& adPhi,
                                            const double& hOverE,
                                            const double& eOverP,
                                            const double& aD0,
                                            const double& aDz,
                                            const double& missH,
                                            const double& cen,
                                            const bool& isEB,
                                            const WP& wp) const {
  std::array<double, 4> max_sInIn{{0.}}, max_adEta{{0.}}, max_adPhi{{0.}}, max_hOverE{{0.}}, max_eOverP{{0.}},
      max_aD0{{0.}}, max_aDz{{0.}}, max_missH{{0}};
  if (isEB) {
    if (cen < 30.) {
      //            WP95     WP90     WP80     WP70
      max_sInIn = {{0.0131, 0.0125, 0.0106, 0.0106}};
      max_adEta = {{0.00389, 0.00365, 0.00343, 0.00342}};
      max_adPhi = {{0.0963, 0.0314, 0.0238, 0.0195}};
      max_hOverE = {{0.156, 0.155, 0.153, 0.124}};
      max_eOverP = {{0.421, 0.0547, 0.0285, 0.00837}};
      max_missH = {{2, 1, 1, 1}};
      max_aD0 = {{0.05, 0.05, 0.05, 0.05}};
      max_aDz = {{0.10, 0.10, 0.10, 0.10}};
    } else {
      max_sInIn = {{0.0105, 0.0103, 0.0101, 0.0101}};
      max_adEta = {{0.00457, 0.00377, 0.00322, 0.00305}};
      max_adPhi = {{0.0634, 0.0554, 0.0262, 0.0185}};
      max_hOverE = {{0.107, 0.0762, 0.0555, 0.0401}};
      max_eOverP = {{0.137, 0.0513, 0.0477, 0.0327}};
      max_missH = {{2, 1, 1, 1}};
      max_aD0 = {{0.05, 0.05, 0.05, 0.05}};
      max_aDz = {{0.10, 0.10, 0.10, 0.10}};
    }
  } else {
    if (cen < 30.) {
      max_sInIn = {{0.0382, 0.0329, 0.029, 0.0283}};
      max_adEta = {{0.00881, 0.00682, 0.00576, 0.00489}};
      max_adPhi = {{0.264, 0.19, 0.071, 0.024}};
      max_hOverE = {{0.178, 0.174, 0.172, 0.156}};
      max_eOverP = {{0.146, 0.133, 0.0585, 0.0174}};
      max_missH = {{3, 1, 1, 1}};
      max_aD0 = {{0.10, 0.10, 0.10, 0.10}};
      max_aDz = {{0.20, 0.20, 0.20, 0.20}};
    } else {
      max_sInIn = {{0.028, 0.0277, 0.0271, 0.0271}};
      max_adEta = {{0.0074, 0.00731, 0.00629, 0.0059}};
      max_adPhi = {{0.253, 0.0794, 0.0300, 0.0242}};
      max_hOverE = {{0.107, 0.075, 0.0639, 0.0338}};
      max_eOverP = {{0.142, 0.0462, 0.0144, 0.0122}};
      max_missH = {{3, 1, 1, 1}};
      max_aD0 = {{0.10, 0.10, 0.10, 0.10}};
      max_aDz = {{0.20, 0.20, 0.20, 0.20}};
    }
  }
  return (sInIn < max_sInIn[wp]) && (adEta < max_adEta[wp]) && (adPhi < max_adPhi[wp]) && (hOverE < max_hOverE[wp]) &&
         (eOverP < max_eOverP[wp]) && (missH <= max_missH[wp]) && (aD0 < max_aD0[wp]) && (aDz < max_aDz[wp]);
}

void pat::HIElectronInfoProducer::produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  // extract input information
  const auto& electrons = iEvent.get(electronToken_);
  const auto& pfCandidates = iEvent.get(pfCandidateToken_);
  const auto& etaMap = iEvent.get(etaToken_);
  const auto& rhoMap = iEvent.get(rhoToken_);
  const double cent = iEvent.get(centralityToken_) / 2.0;

  // select PF candidates
  std::vector<std::tuple<double, double, double, int, int, double>> selPFCands;
  if (etaMap.size() > 1) {
    selPFCands.reserve(pfCandidates.size());
    std::vector<std::vector<fastjet::PseudoJet>> particlesForSK(etaMap.size() - 1);
    for (const auto& pf : pfCandidates) {
      // determine eta category
      int ieta(-1);
      for (size_t i = 1; i < etaMap.size(); i++)
        if (pf.eta() >= etaMap[i - 1] && pf.eta() < etaMap[i]) {
          ieta = i - 1;
          break;
        }
      if (ieta < 0)
        continue;
      // fill particles for soft killer
      particlesForSK[ieta].emplace_back(pf.px(), pf.py(), pf.pz(), pf.energy());
      // fill selected PF candidates
      const auto& id = convert_.translatePdgIdToType(pf.pdgId());
      if (id > 0 && id <= 5 && std::abs(pf.eta()) <= pfMaxEta_)
        selPFCands.emplace_back(pf.pt(), pf.eta(), pf.phi(), id, ieta, 0.0);
    }

    // compute soft killer thresholds
    std::vector<double> skThrs(etaMap.size() - 1);
    for (size_t i = 0; i < particlesForSK.size(); i++) {
      const auto& particles = particlesForSK[i];
      if (not particles.empty()) {
        fastjet::contrib::SoftKiller soft_killer(etaMap[i], etaMap[i + 1], skRadius_, skRadius_);
        std::vector<fastjet::PseudoJet> soft_killed_event;
        soft_killer.apply(particles, soft_killed_event, skThrs[i]);
      }
    }

    // add soft killer thresholds to selected PF candidates
    for (auto& cand : selPFCands)
      std::get<5>(cand) = skThrs[std::get<4>(cand)];
  }

  // initialize output electron collection
  pat::ElectronCollection output(electrons);

  // loop over output electrons
  for (auto& electron : output) {
    if (electron.pt() < electronMinPt_)
      continue;

    // associate rho value
    double rho(-1.);
    for (size_t i = 1; i < etaMap.size(); i++)
      if (electron.eta() >= etaMap[i - 1] && electron.eta() < etaMap[i]) {
        rho = rhoMap[i - 1];
        break;
      }
    if (rho < 0)
      continue;

    const auto absEta = std::abs(electron.eta());
    const bool isEB(absEta < 1.45);

    // compute the identification from MVA
    const auto& sigmaIetaIeta = electron.sigmaIetaIeta();
    const auto& dEtaSeedAtVtx = electron.deltaEtaSeedClusterTrackAtVtx();
    const auto& dPhiAtVtx = electron.deltaPhiSuperClusterTrackAtVtx();
    const auto& track = electron.gsfTrack();
    const auto& d0 = electron.dB(pat::Electron::PV2D);
    const auto& dz = electron.dB(pat::Electron::PVDZ);
    const double& missHits = electron.gsfTrack()->numberOfLostHits();
    const auto& ecalEnergy =
        electron.hasUserFloat("rawEcalEnergy") ? electron.userFloat("rawEcalEnergy") : electron.ecalEnergy();
    const auto& eOverPInv = 1. / ecalEnergy - 1. / electron.trackMomentumAtVtx().R();
    const auto& corHoverEBc = electron.hcalOverEcalBc() - hoeCorr_->evaluate({{rho}});
    const std::vector<double> inputsID(
        {absEta, electron.phi(), rho, sigmaIetaIeta, dEtaSeedAtVtx, dPhiAtVtx, d0, dz, missHits, eOverPInv, corHoverEBc});
    const std::vector<float> featuresID(inputsID.begin(), inputsID.end());
    const auto idValue = 1. - idModel_->Compute(featuresID)[0];
    electron.addUserFloat("hiMVAId", idValue);
    electron.addUserInt("hiMVAIdWP95", passMVAId(idValue, cent, isEB, WP95));
    electron.addUserInt("hiMVAIdWP90", passMVAId(idValue, cent, isEB, WP90));
    electron.addUserInt("hiMVAIdWP85", passMVAId(idValue, cent, isEB, WP85));
    electron.addUserInt("hiMVAIdWP80", passMVAId(idValue, cent, isEB, WP80));

    // compute IP3D significance
    const auto ip3DSig = std::abs(electron.dB(pat::Electron::PV3D)) / electron.edB(pat::Electron::PV3D);

    // compute PF and soft killer isolations
    double pfChIso(0.), pfNeuIso(0.), pfPhoIso(0.);
    double skPFChIso(0.), skPFNeuIso(0.), skPFPhoIso(0.);
    for (const auto& cand : selPFCands) {
      const auto& [pt, eta, phi, id, ieta, skThr] = cand;
      const auto dR2 = reco::deltaR2(electron.eta(), electron.phi(), eta, phi);
      if (dR2 >= rVeto_ * rVeto_ && dR2 <= rCone_ * rCone_) {
        (id == 5 ? pfNeuIso : (id == 4 ? pfPhoIso : pfChIso)) += pt;
        (id == 5 ? skPFNeuIso : (id == 4 ? skPFPhoIso : skPFChIso)) += pt * (pt > skThr);
      }
    }
    const auto& pfIso = pfChIso + pfNeuIso + pfPhoIso;
    const auto& skPFIso = skPFChIso + skPFNeuIso + skPFPhoIso;

    // correct the PF isolation variables
    const auto& pfRelIso = (pfIso - isoCorr_->evaluate({{"PFIso", "ele", rho}})) / electron.pt();
    const auto& pfChRelIso = (pfChIso - isoCorr_->evaluate({{"PFChIso", "ele", rho}})) / electron.pt();
    const auto& skPFRelIso = (skPFIso - isoCorr_->evaluate({{"skPFIso", "ele", rho}})) / electron.pt();
    const auto& skPFChRelIso = (skPFChIso - isoCorr_->evaluate({{"skPFChIso", "ele", rho}})) / electron.pt();

    // compute the isolation from MVA
    const std::vector<double> inputsISO(
        {absEta, electron.phi(), rho, ip3DSig, pfRelIso, pfChRelIso, skPFRelIso, skPFChRelIso, idValue});
    const std::vector<float> featuresISO(inputsISO.begin(), inputsISO.end());
    const auto isoValue = 1. - isoModel_->Compute(featuresISO)[0];
    electron.addUserFloat("hiMVAIso", isoValue);
    electron.addUserInt("hiMVAIsoWP95", passMVAIso(isoValue, cent, isEB, WP95));
    electron.addUserInt("hiMVAIsoWP90", passMVAIso(isoValue, cent, isEB, WP90));
    electron.addUserInt("hiMVAIsoWP85", passMVAIso(isoValue, cent, isEB, WP85));
    electron.addUserInt("hiMVAIsoWP80", passMVAIso(isoValue, cent, isEB, WP80));

    // compute the cut-based identification
    const auto& sInIn = electron.full5x5_sigmaIetaIeta();
    const auto& dEtaSeed = (electron.superCluster().isNonnull() && electron.superCluster()->seed().isNonnull())
                               ? (electron.deltaEtaSuperClusterTrackAtVtx() - electron.superCluster()->eta() +
                                  electron.superCluster()->seed()->eta())
                               : std::numeric_limits<float>::max();
    const auto adEta = std::abs(dEtaSeed);
    const auto adPhi = std::abs(dPhiAtVtx);
    const auto& hOverE = electron.full5x5_hcalOverEcalBc();
    const auto& ooEmooP = (1.0 - electron.eSuperClusterOverP()) / electron.ecalEnergy();
    const auto eOverP = (electron.ecalEnergy() > 0 && std::isfinite(electron.ecalEnergy())) ? std::abs(ooEmooP) : 1.e30;
    const auto aD0 = std::abs(d0);
    const auto aDz = std::abs(dz);
    electron.addUserInt("hiCutIdWP95",
                        passCutID(sInIn, adEta, adPhi, hOverE, eOverP, aD0, aDz, missHits, cent, isEB, WP95));
    electron.addUserInt("hiCutIdWP90",
                        passCutID(sInIn, adEta, adPhi, hOverE, eOverP, aD0, aDz, missHits, cent, isEB, WP90));
    electron.addUserInt("hiCutIdWP80",
                        passCutID(sInIn, adEta, adPhi, hOverE, eOverP, aD0, aDz, missHits, cent, isEB, WP80));
    electron.addUserInt("hiCutIdWP70",
                        passCutID(sInIn, adEta, adPhi, hOverE, eOverP, aD0, aDz, missHits, cent, isEB, WP70));
  }

  iEvent.emplace(patElectronPutToken_, std::move(output));
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void pat::HIElectronInfoProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("electrons", edm::InputTag("slimmedElectrons"))->setComment("electron input collection");
  desc.add<edm::InputTag>("pfCandidates", edm::InputTag("packedPFCandidates"))
      ->setComment("PF candidate input collection");
  desc.add<edm::InputTag>("centrality", edm::InputTag("centralityBin:HFtowers"))->setComment("centrality");
  desc.add<edm::InputTag>("etaMap", edm::InputTag("hiFJRhoProducerFinerBins:mapEtaEdges"))
      ->setComment("eta ranges for rho and soft killer");
  desc.add<edm::InputTag>("rhoMap", edm::InputTag("hiFJRhoProducerFinerBins:mapToRho"))->setComment("rho");
  desc.add<double>("pf_maxAbsEta", 2.8)->setComment("Maximum absolute eta for PF candidates");
  desc.add<double>("sk_radius", 0.4)->setComment("Radius for soft killer threshold");
  desc.add<double>("electron_minPt", 0.0)->setComment("Electron minimum pt");
  desc.add<double>("iso_rVeto", 0.026)->setComment("Isolation veto radius");
  desc.add<double>("iso_rCone", 0.3)->setComment("Isolation cone radius");
  desc.add<std::string>("era", "")->setComment("Era");
  desc.add<edm::FileInPath>("file_idModel", {})->setComment("Path to identification model");
  desc.add<edm::FileInPath>("file_isoModel", {})->setComment("Path to isolation model");
  desc.add<edm::FileInPath>("file_corr", {})->setComment("Path to rho correction");
  descriptions.add("hiElectrons", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(HIElectronInfoProducer);
