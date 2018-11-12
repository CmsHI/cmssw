# ZDC RecHit Producer for 2018 CMS PbPb Run

## ZDC Detector

1. Zero Degree Calorimeter (ZDC) is located 140m from the CMS IP, in side the LHC tunnel.
2. Major change this year is that it is digitized in the tunnel and then send optical signals to USC.
3. Since the cable length is only 12m long from the detector, it reduces the long frequency noise significantly.
4. New front end electronics, QIE10, are used for digitizing, identical to HF.
5. QIE10 has large dynamic range, more than 10x, comparing to old QIE8.

## ZDC Calibration

1. Currently, only DIGIs are saved in AOD. DIGIs cannot be used directly.
2. DIGIs can be converted to charges collected by capacitors.
3. DIGI to charge conversion needs calibration constants for each QIE card. This is done by averaging all QIE constants used by HF to get average calibration constants.
4. Charges are then inter-calibrated according to 2010 PbPb data to match the gain of EM and HAD sections.
5. If gain matching is correct, we should be able to see neutron peaks as a function of charge.
6. The first neutron peak is then located at the beam energy, i.e. 2.51 TeV. This gives us the calibration from charge to energy.

## Software

1. This EDProducer produces the ZDC RecHit collection used by various down stream EDAnalyzer, such as HiForest.
2. The calibration constants are loaded as python modules.
3. The current calibration is very rough. The pedestal is not subtracted. The Plus side and Minus side do not have the same spectrum shape.
4. Example to run the code:
```
cd CMSSW_10_3_1/src
cmsenv
mkdir QWAna
cd QWAna
git clone git@github.com:BetterWang/QWZDC2018RecHit.git
cd QWZDC2018RecHit
scram b
cd test
cmsRun recHitRAW_cfg.py runNumber=326480 runInputDir=/eos/cms/store/hidata/HIRun2018A/HIMinimumBias2/RAW/v1/000/ source=PoolSource rawTag='rawDataRepacker' outputTag=_MB2RecHit hlt=HLT_HIMinimumBias_part2_v`
```

# Again, VERY PRELIMINARY

## Works from LHC Fill 7433, CMS Run 326476
