#!/bin/bash

for system in PbPb pp
do
    for reco in HI pp
    do
        [ $reco == "HI" ] && [ $system == "pp" ] && continue

        for sample in data jec mc mb
        do
            [ $sample == "mb" ] && [ $system == "pp" ] && continue

            for algo in ak
            do
                for object in PF Calo
                do
                    for sub in Pu Cs FlowPuCs NONE
                    do
                        [ $object == "Calo" ] && ( [ $sub == "Cs" ] || [ $sub == "FlowPuCs" ] ) && continue

                        for groom in SoftDrop SoftDropZ05B15 NONE
                        do
                            [ $object == "Calo" ] && [ $groom != "NONE" ] && continue

                            for radius in 1 2 3 4 5 6
                            do
                                [ $sub == "NONE" ] && subt="" || subt=$sub
                                [ $groom == "NONE" ] && groomt="" || groomt=$groom
                                [ $system == "pp" ] && systemt="" || systemt="Hi"

                                if [ $system == "PbPb" ]; then
                                    if [ $sample == "mb" ]; then
                                        genjets="HiGenJets"
                                        matchGenjets="HiCleanedGenJets"
                                        partons="cleanedPartons"
                                        matchpartons="myPartons"
                                    else
                                        genjets="HiSignalGenJets"
                                        matchGenjets="HiSignalGenJets"
                                        partons="hiSignalGenParticles"
                                        matchpartons="signalPartons"
                                    fi
                                else
                                    genjets="GenJets"
                                    matchGenjets="GenJets"
                                    partons="genParticles"
                                    matchpartons="myPartons"
                                fi

                                if [ $sub == "Cs" ]; then
                                    resolveByDist="True"
                                elif [ $sub == "FlowPuCs" ]; then
                                    resolveByDist="True"
                                else
                                    resolveByDist="False"
                                fi

                                ismc="False"
                                doSubJets="False"
                                doGenSubJets="False"
                                doGenSym="False"
                                doGenTaus="False"
                                domatch="False"
                                match=""
                                eventinfotag="generator"
                                jetcorrlevels="\'L2Relative\'"
                                corrlabel="_offline"

                                if [ $reco == "HI" ]; then
                                    vertex="offlinePrimaryVertices"
                                    tracks="hiGeneralTracks"
                                    pflow="particleFlowTmp"
                                    doTower="True"
                                else
                                    vertex="offlinePrimaryVertices"
                                    tracks="generalTracks"
                                    pflow="particleFlow"
                                    genparticles="genParticles"
                                    doTower="False"
                                fi

                                if ([ $system == "pp" ] || [ $system == "PbPb" ]) \
                                    && [ $object == "PF" ]; then
                                    if [ $sample = "data" ]; then
                                        jetcorrlevels="\'L2Relative\',\'L2L3Residual\'"
                                    else
                                        jetcorrlevels="\'L2Relative\'"
                                    fi
                                fi

                                if [ $sample != "data" ]; then
                                    ismc="True"
                                    if [ $object == "PF" ] \
                                        && ( [ $sub == "Cs" ] || [ $sub == "FlowPuCs" ] || [ $system == "pp" ] ) \
                                        && [ $sample != "mb" ]; then
                                        doGenTaus="True"
                                    fi
                                fi

                                if [ $reco == "HI" ] && [ $sub == "Pu" ]; then
                                    corrname=$(echo ${algo} | sed 's/\(.*\)/\U\1/')${sub}${radius}${object}${corrlabel}
				# to be updated with new JECs
				elif [ $object == "Calo" ]; then
				    corrname="AK4PF"
				else
				    corrname="AK${radius}${object}"
                                fi

                                if [ $groom != "NONE" ]; then
                                    doSubJets="True"
                                    doGenTaus="False"
                                    if [ $sample == "mc" ]; then
                                        doGenSubJets="True"
                                        doGenSym="True"
                                    fi
                                fi

                                fulltag=${algo}${subt}${groomt}${radius}${object}
                                jetseqfile=${fulltag}JetSequence_${reco}on${system}_${sample}_cff.py

				if [ $sub == "Cs" ] || [ $sub == "FlowPuCs" ] || [ $sub == "Pu" ]; then
                                    cat templateSequence_bTag_LegacyFlavor_cff.py.txt | sed \
					-e "s/ALGO_/$algo/g" \
					-e "s/SUB_/$subt/g" \
					-e "s/GROOM_/$groomt/g" \
					-e "s/RADIUS_/$radius/g" \
					-e "s/OBJECT_/$object/g" \
					-e "s/SAMPLE_/$sample/g" \
					-e "s/CORRNAME_/$corrname/g" \
					-e "s/MATCHED_/$match/g" \
					-e "s/ISMC/$ismc/g" \
					-e "s/MATCHGENJETS/$matchGenjets/g" \
					-e "s/GENJETS/$genjets/g" \
					-e "s/GENPARTICLES/$genparticles/g" \
					-e "s/PARTONS/$partons/g" \
					-e "s/MATCHPS/$matchpartons/g" \
					-e "s/TRACKS/$tracks/g" \
					-e "s/VERTEX/$vertex/g" \
					-e "s/PARTICLEFLOW/$pflow/g" \
					-e "s/DOMATCH/$domatch/g" \
					-e "s/EVENTINFOTAG/$eventinfotag/g" \
					-e "s/JETCORRECTIONLEVELS/$jetcorrlevels/g" \
					-e "s/DOTOWERS_/$doTower/g" \
					-e "s/DOSUBJETS_/$doSubJets/g" \
					-e "s/DOGENTAUS_/$doGenTaus/g" \
					-e "s/DOGENSUBJETS_/$doGenSubJets/g" \
					-e "s/DOGENSYM_/$doGenSym/g" \
					-e "s/RESOLVEBYDIST_/$resolveByDist/g" \
					-e "s/SYSTEM_/$systemt/g" \
					> $jetseqfile
				    
                                else
                                    cat templateSequence_bTag_cff.py.txt | sed \
					-e "s/ALGO_/$algo/g" \
					-e "s/SUB_/$subt/g" \
					-e "s/GROOM_/$groomt/g" \
					-e "s/RADIUS_/$radius/g" \
					-e "s/OBJECT_/$object/g" \
					-e "s/SAMPLE_/$sample/g" \
					-e "s/CORRNAME_/$corrname/g" \
					-e "s/MATCHED_/$match/g" \
					-e "s/ISMC/$ismc/g" \
					-e "s/MATCHGENJETS/$matchGenjets/g" \
					-e "s/GENJETS/$genjets/g" \
					-e "s/GENPARTICLES/$genparticles/g" \
					-e "s/PARTONS/$partons/g" \
					-e "s/MATCHPS/$matchpartons/g" \
					-e "s/TRACKS/$tracks/g" \
					-e "s/VERTEX/$vertex/g" \
					-e "s/PARTICLEFLOW/$pflow/g" \
					-e "s/DOMATCH/$domatch/g" \
					-e "s/EVENTINFOTAG/$eventinfotag/g" \
					-e "s/JETCORRECTIONLEVELS/$jetcorrlevels/g" \
					-e "s/DOTOWERS_/$doTower/g" \
					-e "s/DOSUBJETS_/$doSubJets/g" \
					-e "s/DOGENTAUS_/$doGenTaus/g" \
					-e "s/DOGENSUBJETS_/$doGenSubJets/g" \
					-e "s/DOGENSYM_/$doGenSym/g" \
					-e "s/RESOLVEBYDIST_/$resolveByDist/g" \
					-e "s/SYSTEM_/$systemt/g" \
					> $jetseqfile
                                fi


                                if [ $sample == "jec" ]; then
                                    echo "${fulltag}JetAnalyzer.genPtMin = cms.untracked.double(1)" >> $jetseqfile
                                    echo "${fulltag}JetAnalyzer.jetPtMin = cms.double(1)" >> $jetseqfile
                                fi

                                if [[ $groom =~ "SoftDrop" ]]; then
                                    echo "${fulltag}patJetsWithBtagging.userData.userFloats.src += ['${fulltag}Jets:sym']" >> $jetseqfile
                                    echo "${fulltag}patJetsWithBtagging.userData.userInts.src += ['${fulltag}Jets:droppedBranches']" >> $jetseqfile
                                fi

                                if [[ $sub =~ "Cs" ]] || [[ $sub =~ "FlowPuCs" ]] && [ $sample == "mc" ] && [ $reco == "pp" ]; then
				    echo -e "\n" >> $jetseqfile
                                    echo "${fulltag}JetAnalyzer.matchJets = cms.untracked.bool(True)" >> $jetseqfile				    
                                    echo "${fulltag}JetAnalyzer.matchTag = cms.untracked.InputTag(\"ak"${radius}$"PFpatJetsWithBtagging\")" >> $jetseqfile
                                fi
                            done
                        done
                    done
                done
            done
        done
    done
done
