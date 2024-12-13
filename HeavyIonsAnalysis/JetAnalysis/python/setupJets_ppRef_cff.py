import FWCore.ParameterSet.Config as cms

def candidateBtaggingMiniAOD(process, isMC = True, jetPtMin = 15, jetCorrLevels = ['L2Relative', 'L3Absolute'], doBtagging = False, labelR = "0"):
    # DeepNtuple settings
    jetR = 0.1*int(labelR)
    if labelR == "0": jetR = 0.4

    jetCorrectionsAK4 = ('AK4PFchs' if labelR == "0" else 'AK'+labelR+'PFchs', jetCorrLevels, 'None')


    if doBtagging:
        bTagInfos = [
            'pfDeepCSVTagInfos',
            'pfDeepFlavourTagInfos',
            'pfImpactParameterTagInfos',
            'pfInclusiveSecondaryVertexFinderTagInfos',
            'pfParticleTransformerAK4TagInfos',
            'pfUnifiedParticleTransformerAK4TagInfos'
        ]

        bTagDiscriminators = [
            'pfUnifiedParticleTransformerAK4JetTags:probb',
            'pfUnifiedParticleTransformerAK4JetTags:probbb',
            'pfUnifiedParticleTransformerAK4JetTags:probc',
            'pfUnifiedParticleTransformerAK4JetTags:probg',
            'pfUnifiedParticleTransformerAK4JetTags:problepb',
            'pfUnifiedParticleTransformerAK4JetTags:probu',
            'pfUnifiedParticleTransformerAK4JetTags:probd',
            'pfUnifiedParticleTransformerAK4JetTags:probs',
            'pfUnifiedParticleTransformerAK4JetTags:probtaup1h0p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaup1h1p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaup1h2p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaup3h0p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaup3h1p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaum1h0p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaum1h1p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaum1h2p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaum3h0p',
            'pfUnifiedParticleTransformerAK4JetTags:probtaum3h1p',
            'pfUnifiedParticleTransformerAK4JetTags:probele',
            'pfUnifiedParticleTransformerAK4JetTags:probmu',
            'pfUnifiedParticleTransformerAK4JetTags:ptcorr',
            'pfUnifiedParticleTransformerAK4JetTags:ptnu',
        ]
    else: 
        bTagInfos = ['None']
        bTagDiscriminators = ['None']

    # Create gen-level information
    if isMC:
        from RecoHI.HiJetAlgos.hiSignalParticleProducer_cfi import hiSignalParticleProducer as hiSignalGenParticles
        process.hiSignalGenParticles = hiSignalGenParticles.clone(
            src = "prunedGenParticles"
        )
        from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import allPartons
        process.allPartons = allPartons.clone(
            src = 'hiSignalGenParticles'
        )
        from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
        setattr(process,"ak"+labelR+"GenJetsWithNu",
                ak4GenJets.clone(
                    src = 'packedGenParticles',
                    rParam = jetR
                )
        )
        process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector",
            src = cms.InputTag("packedGenParticles"),
            cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16")
        )
        setattr(process,"ak"+labelR+"GenJetsRecluster",
                ak4GenJets.clone(
                    src = 'packedGenParticlesForJetsNoNu'
                )
        )
        process.genTask = cms.Task(process.hiSignalGenParticles, process.allPartons, getattr(process,"ak"+labelR+"GenJetsWithNu"), process.packedGenParticlesForJetsNoNu, getattr(process,"ak"+labelR+"GenJetsRecluster"))


    # Create unsubtracted reco jets

    from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cff import ak4PFJets
    setattr(process, "ak"+labelR+"PFUnsubJets", 
            ak4PFJets.clone(
                src = 'packedPFCandidates',
                jetPtMin = 5.,  # set lower than subtracted version
                rParam = jetR
            )
    )
    

    if isMC:
        from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
        from PhysicsTools.JetMCAlgos.AK4PFJetsMCFlavourInfos_cfi import ak4JetFlavourInfos
        process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone(particles = "prunedGenParticles")
        setattr(process,"ak"+labelR+"PFFlavourInfos",
                ak4JetFlavourInfos.clone(
                    jets = "ak"+labelR+"PFJetsCHS",
                    partons = "selectedHadronsAndPartons:algorithmicPartons",
                    hadronFlavourHasPriority = True,
                    rParam = jetR
                )
        )
        process.genTask.add(process.selectedHadronsAndPartons)
        process.genTask.add(getattr(process,"ak"+labelR+"PFFlavourInfos"))

    matchedGenJets = ""
    if isMC:
        if labelR == "0": matchedGenJets = "slimmedGenJets"
        else: matchedGenJets  = "ak"+labelR+"GenJetsWithNu"


    svSource = cms.InputTag("slimmedSecondaryVertices")

    from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
    addJetCollection(
        process,
        postfix            = "UnsubJets",
        labelName          = str("AK"+labelR+"PF"),
        jetSource          = cms.InputTag("ak"+labelR+"PFUnsubJets"),
        algo               = "ak", #name of algo must be in this format
        rParam             = jetR,
        pvSource           = cms.InputTag("offlineSlimmedPrimaryVertices"),
        pfCandidates       = cms.InputTag("packedPFCandidates"),
        svSource           = svSource,
        muSource           = cms.InputTag("slimmedMuons"),
        elSource           = cms.InputTag("slimmedElectrons"),
        getJetMCFlavour    = isMC,
        genJetCollection   = cms.InputTag(matchedGenJets),
        genParticles       = cms.InputTag("hiSignalGenParticles" if isMC else ""),
        jetCorrections     = ('AK4PFchs' if labelR=='0' else 'AK'+labelR+'PFchs',) + jetCorrectionsAK4[1:],
    )

    getattr(process,"patJetsAK"+labelR+"PFUnsubJets").useLegacyJetMCFlavour = False

    process.patAlgosToolsTask.add(getattr(process,"ak"+labelR+"PFUnsubJets"))

    # Create CHS subtracted reco jets
    from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
    addJetCollection(
        process,
        postfix            = "",
        labelName          = "AK"+labelR+"PFCHS",
        jetSource          = cms.InputTag("ak"+labelR+"PFJetsCHS"),
        algo               = "ak", #name of algo must be in this format
        rParam             = jetR,
        pvSource           = cms.InputTag("offlineSlimmedPrimaryVertices"),
        pfCandidates       = cms.InputTag("packedPFCandidates"),
        svSource           = svSource,
        muSource           = cms.InputTag("slimmedMuons"),
        elSource           = cms.InputTag("slimmedElectrons"),
        getJetMCFlavour    = isMC,
        genJetCollection   = cms.InputTag(matchedGenJets),
        genParticles       = cms.InputTag("hiSignalGenParticles" if isMC else ""),
        jetCorrections     = jetCorrectionsAK4,
    )
    if labelR == "0": getattr(process,"patJetsAK"+labelR+"PFCHS").embedPFCandidates = True # not working with CHS jet reclustering

    if not isMC:
        for label in ["patJetsAK"+labelR+"PFUnsubJets", "patJetsAK"+labelR+"PFCHS"]:
            getattr(process, label).addGenJetMatch = False
            getattr(process, label).addGenPartonMatch = False
            getattr(process, label).embedGenJetMatch = False
            getattr(process, label).embedGenPartonMatch = False
            getattr(process, label).genJetMatch = ""
            getattr(process, label).genPartonMatch = ""

    # left here for reference in case we want to move reclustering here
    from CommonTools.ParticleFlow.pfCHS_cff import pfCHS
    process.pfCHS = pfCHS.clone()
    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsCHS
    setattr(process,"ak"+labelR+"PFJetsCHS",
            ak4PFJetsCHS.clone(
                src = "pfCHS",
                jetPtMin = jetPtMin,
                rParam = jetR
            )
    )
    for mod in ["pfCHS","ak"+labelR+"PFJetsCHS"]:
        process.patAlgosToolsTask.add(getattr(process, mod))

    # Create b-tagging sequence ----------------
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    updateJetCollection(
        process,
        labelName = "DeepFlavour",
        jetSource = cms.InputTag("slimmedJets" if labelR == "0" else "patJetsAK"+labelR+"PFCHS"), 
        jetCorrections = jetCorrectionsAK4,
        pfCandidates = cms.InputTag('packedPFCandidates'),
        pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
        svSource = svSource,
        muSource = cms.InputTag('slimmedMuons'),
        elSource = cms.InputTag('slimmedElectrons'),
        btagInfos = bTagInfos,
        btagDiscriminators = bTagDiscriminators,
        explicitJTA = False
    )

    process.unsubUpdatedPatJetsDeepFlavour = cms.EDProducer("JetMatcherDR",
                                                            source = cms.InputTag("updatedPatJetsDeepFlavour"),
                                                            matched = cms.InputTag("patJetsAK"+labelR+"PFUnsubJets")
    )
    process.patAlgosToolsTask.add(process.unsubUpdatedPatJetsDeepFlavour)

    if doBtagging:

        process.pfUnifiedParticleTransformerAK4JetTagsDeepFlavour.model_path = 'RecoBTag/Combined/data/UParTAK4/HIN/V00/UParTAK4_PbPb_2023.onnx'
        process.pfUnifiedParticleTransformerAK4TagInfosDeepFlavour.sort_cand_by_pt = True

        if hasattr(process,'updatedPatJetsTransientCorrectedDeepFlavour'):
            process.updatedPatJetsTransientCorrectedDeepFlavour.addTagInfos = True
            process.updatedPatJetsTransientCorrectedDeepFlavour.addBTagInfo = True
        else:
            raise ValueError('I could not find updatedPatJetsTransientCorrectedDeepFlavour to embed the tagInfos, please check the cfg')

            # Remove PUPPI
        process.patAlgosToolsTask.remove(process.packedpuppi)
        process.patAlgosToolsTask.remove(process.packedpuppiNoLep)
        process.pfInclusiveSecondaryVertexFinderTagInfosDeepFlavour.weights = ""
        for taginfo in ["pfDeepFlavourTagInfosDeepFlavour", "pfParticleTransformerAK4TagInfosDeepFlavour", "pfUnifiedParticleTransformerAK4TagInfosDeepFlavour"]:
            getattr(process, taginfo).fallback_puppi_weight = True
            getattr(process, taginfo).fallback_vertex_association = True
            getattr(process, taginfo).puppi_value_map = ""

    # Match with unsubtracted jets
    process.unsubJetMap = process.unsubUpdatedPatJetsDeepFlavour.clone(
        source = "selectedUpdatedPatJetsDeepFlavour"
    )
    process.patAlgosToolsTask.add(process.unsubJetMap)

    # Add extra b tagging algos
    from RecoBTag.ImpactParameter.pfJetProbabilityBJetTags_cfi import pfJetProbabilityBJetTags
    process.pfJetProbabilityBJetTagsDeepFlavour = pfJetProbabilityBJetTags.clone(tagInfos = ["pfImpactParameterTagInfosDeepFlavour"])
    if doBtagging:
        process.patAlgosToolsTask.add(process.pfJetProbabilityBJetTagsDeepFlavour)

    # Associate to forest sequence
    if isMC:
        process.forest.associate(process.genTask)
    process.forest.associate(process.patAlgosToolsTask)
