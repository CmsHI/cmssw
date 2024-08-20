import FWCore.ParameterSet.Config as cms

def candidateBtaggingMiniAOD(process, isMC = True, jetPtMin = 15, jetCorrLevels = ['L2Relative', 'L3Absolute']):
    # DeepNtuple settings
    jetCorrectionsAK4 = ('AK4PFchs', jetCorrLevels, 'None')

    bTagInfos = [
        'pfDeepCSVTagInfos',
        'pfDeepFlavourTagInfos',
        'pfImpactParameterTagInfos',
        'pfInclusiveSecondaryVertexFinderTagInfos',
        'pfParticleTransformerAK4TagInfos',
        'pfUnifiedParticleTransformerAK4TagInfos'
    ]

    bTagDiscriminators = [
        'pfDeepCSVJetTags:probb',
        'pfDeepCSVJetTags:probbb',
        'pfDeepCSVJetTags:probc',
        'pfDeepCSVJetTags:probudsg',
        'pfDeepFlavourJetTags:probb',
        'pfDeepFlavourJetTags:probbb',
        'pfDeepFlavourJetTags:probc',
        'pfDeepFlavourJetTags:probg',
        'pfDeepFlavourJetTags:problepb',
        'pfDeepFlavourJetTags:probuds',
        'pfParticleTransformerAK4JetTags:probb',
        'pfParticleTransformerAK4JetTags:probbb',
        'pfParticleTransformerAK4JetTags:probc',
        'pfParticleTransformerAK4JetTags:probg',
        'pfParticleTransformerAK4JetTags:problepb',
        'pfParticleTransformerAK4JetTags:probuds',
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
    ]

    # Create gen-level information
    if isMC:
        from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import allPartons, cleanedPartons
        process.allPartons = allPartons.clone(
            src = 'prunedGenParticles'
        )
        process.cleanedPartons = cleanedPartons.clone()
        from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
        process.ak4GenJetsWithNu = ak4GenJets.clone(
            src = 'packedGenParticlesSignal'
        )
        process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector",
            src = cms.InputTag("packedGenParticlesSignal"),
            cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16")
        )
        process.ak4GenJetsRecluster = ak4GenJets.clone(
            src = 'packedGenParticlesForJetsNoNu'
        )
        process.genTask = cms.Task(process.allPartons, process.cleanedPartons, process.ak4GenJetsWithNu, process.packedGenParticlesForJetsNoNu, process.ak4GenJetsRecluster)

    # Remake secondary vertices
    from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import inclusiveCandidateVertexFinder, candidateVertexMerger, candidateVertexArbitrator, inclusiveCandidateSecondaryVertices
    process.inclusiveCandidateVertexFinder = inclusiveCandidateVertexFinder.clone(
        tracks = "packedPFCandidates",
        primaryVertices = "offlineSlimmedPrimaryVertices",
        minHits = 0,
        minPt = 0.8
    )
    process.candidateVertexMerger = candidateVertexMerger.clone()
    process.candidateVertexArbitrator = candidateVertexArbitrator.clone(
        tracks = "packedPFCandidates",
        primaryVertices = "offlineSlimmedPrimaryVertices"
    )
    process.inclusiveCandidateSecondaryVertices = inclusiveCandidateSecondaryVertices.clone()
    process.svTask = cms.Task(process.inclusiveCandidateVertexFinder, process.candidateVertexMerger, process.candidateVertexArbitrator, process.inclusiveCandidateSecondaryVertices)
    svSource = cms.InputTag("inclusiveCandidateSecondaryVertices")

    # Create unsubtracted reco jets
    from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
    addJetCollection(
        process,
        postfix            = "UnsubJets",
        labelName          = "AK4PF",
        jetSource          = cms.InputTag("ak4PFUnsubJets"),
        algo               = "ak", #name of algo must be in this format
        rParam             = 0.4,
        pvSource           = cms.InputTag("offlineSlimmedPrimaryVertices"),
        pfCandidates       = cms.InputTag("packedPFCandidates"),
        svSource           = svSource,
        muSource           = cms.InputTag("slimmedMuons"),
        elSource           = cms.InputTag("slimmedElectrons"),
        getJetMCFlavour    = isMC,
        genJetCollection   = cms.InputTag("slimmedGenJets" if isMC else ""),
        genParticles       = cms.InputTag("prunedGenParticles" if isMC else ""),
        jetCorrections     = ('AK4PF',) + jetCorrectionsAK4[1:],
    )
    process.patJetsAK4PFUnsubJets.useLegacyJetMCFlavour = False
    if isMC:
        process.patJetPartonMatchAK4PFUnsubJets = process.patJetPartonMatchAK4PFUnsubJets.clone(matched = "cleanedPartons")

    from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cff import ak4PFJets
    process.ak4PFUnsubJets = ak4PFJets.clone(
        src = 'packedPFCandidates',
        jetPtMin = jetPtMin
    )
    process.patAlgosToolsTask.add(process.ak4PFUnsubJets)

    # Create HIN subtracted reco jets
    from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
    addJetCollection(
        process,
        postfix            = "",
        labelName          = "AKCs4PF",
        jetSource          = cms.InputTag("akCs4PFJets"),
        algo               = "ak", #name of algo must be in this format
        rParam             = 0.4,
        pvSource           = cms.InputTag("offlineSlimmedPrimaryVertices"),
        pfCandidates       = cms.InputTag("packedPFCandidates"),
        svSource           = svSource,
        muSource           = cms.InputTag("slimmedMuons"),
        elSource           = cms.InputTag("slimmedElectrons"),
        getJetMCFlavour    = isMC,
        genJetCollection   = cms.InputTag("slimmedGenJets" if isMC else ""),
        genParticles       = cms.InputTag("prunedGenParticles" if isMC else ""),
        jetCorrections     = jetCorrectionsAK4,
    )
    process.patJetsAKCs4PF.embedPFCandidates = True
    if isMC:
        process.patJetPartonMatchAKCs4PF = process.patJetPartonMatchAKCs4PF.clone(matched = "cleanedPartons")

    if not isMC:
        for label in ["patJetsAK4PFUnsubJets", "patJetsAKCs4PF"]:
            getattr(process, label).addGenJetMatch = False
            getattr(process, label).addGenPartonMatch = False
            getattr(process, label).embedGenJetMatch = False
            getattr(process, label).embedGenPartonMatch = False
            getattr(process, label).genJetMatch = ""
            getattr(process, label).genPartonMatch = ""

    from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonJets_cff import PackedPFTowers, hiPuRho
    process.PackedPFTowers = PackedPFTowers.clone()
    process.hiPuRho = hiPuRho.clone(
        src = 'PackedPFTowers'
    )
    from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cff import akCs4PFJets
    process.akCs4PFJets = akCs4PFJets.clone(
        src = 'packedPFCandidates',
        jetPtMin = jetPtMin
    )
    for mod in ["PackedPFTowers", "hiPuRho", "akCs4PFJets"]:
        process.patAlgosToolsTask.add(getattr(process, mod))

    # Create b-tagging sequence ----------------
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    updateJetCollection(
        process,
        labelName = "DeepFlavour",
        jetSource = cms.InputTag('patJetsAKCs4PF'), # 'ak4Jets'
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
        matched = cms.InputTag("patJetsAK4PFUnsubJets")
    )
    process.patAlgosToolsTask.add(process.unsubUpdatedPatJetsDeepFlavour)

    process.pfUnifiedParticleTransformerAK4JetTagsDeepFlavour.model_path = 'HeavyIonsAnalysis/Configuration/data/UParTAK4_HIMG5132XADV.onnx'

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
        getattr(process, taginfo).unsubjet_map = "unsubUpdatedPatJetsDeepFlavour"
        getattr(process, taginfo).puppi_value_map = ""

    # Match with unsubtracted jets
    process.unsubJetMap = process.unsubUpdatedPatJetsDeepFlavour.clone(
        source = "selectedUpdatedPatJetsDeepFlavour"
    )
    process.patAlgosToolsTask.add(process.unsubJetMap)

    # Add extra b tagging algos
    from RecoBTag.ImpactParameter.pfJetProbabilityBJetTags_cfi import pfJetProbabilityBJetTags
    process.pfJetProbabilityBJetTagsDeepFlavour = pfJetProbabilityBJetTags.clone(tagInfos = ["pfImpactParameterTagInfosDeepFlavour"])
    process.patAlgosToolsTask.add(process.pfJetProbabilityBJetTagsDeepFlavour)

    # Associate to forest sequence
    if isMC:
        process.forest.associate(process.genTask)
    process.forest.associate(process.svTask)
    process.forest.associate(process.patAlgosToolsTask)
