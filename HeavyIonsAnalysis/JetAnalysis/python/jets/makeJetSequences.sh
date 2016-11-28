#!/bin/sh

for system in PbPb pp pPb
do
    for sample in data jec mc mb
    do
	if [ $system == "pp" ] && [ $sample == "mb" ]; then
	    continue
	fi	
        for algo in ak
        do
            for sub in Vs Pu Cs NONE
            do
                for groom in SoftDrop Filter NONE
                do
                    for radius in 1 2 3 4 5 6
                    do
                        for object in PF Calo
                        do
			    # no Cs Calo or pp jets
			    
                            if( [ $system == "pPb" ] ) && ( [ $radius -ne 4 ] || [ $sample != "jec" ] || [ $sub != "NONE" ] || [ $groom != "NONE" ] ) ; then 
                                continue
                            fi
                            if ( [ $object == "Calo" ] || [ $system == "pp" ] ) && ( [ $sub == "Cs" ] ) ; then
			        continue
			    fi
                            subt=$sub
                            if [ $sub == "NONE" ]; then
                                subt=""
                            fi
                            groomt=$groom
                            if [ $groom == "NONE" ]; then
                                groomt=""
                            fi
			    if [ $sample == "mb" ]; then
                                matchGenjets="HiCleanedGenJets"
			        partons="selectedPartons"
			    else
			        matchGenjets="HiSignalGenJets"
			        partons="hiSignalGenParticles"
			    fi
			    if ( [ $sub == "Vs" ] || [ $sub == "Cs" ] ) ; then
			        resolveByDist="True"
			    else 
			        resolveByDist="False"
			    fi
			    genjets="HiGenJets"
                            ismc="False"
                            corrlabel="_offline"
                            domatch="True"
                            tracks="hiGeneralTracks"
			    vertex="offlinePrimaryVertices"
                            pflow="particleFlowTmp"
                            domatch="False"
			    doTower="True"
			    doSubJets="False"
                            doGenSubJets="False"
                            match=""
                            eventinfotag="generator"
			    jetcorrectionlevels="\'L2Relative\',\'L3Absolute\'"
                            #echo "" > $algo$subt$radius${object}JetSequence_${system}_${sample}_cff.py
                            
                            if [ $system == "pp" ] || [ $system == "pPb" ]; then
                                #corrlabel="_generalTracks"
                                tracks="generalTracks"
			        vertex="offlinePrimaryVertices"
                                genparticles="genParticles"
                                partons="genParticles"
                                pflow="particleFlow"
			        if [ $sample == "data" ] && [ $sub == "NONE" ] && [ $radius == 4 ] && [ $object == "PF" ]; then
				    jetcorrectionlevels="\'L2Relative\',\'L3Absolute\',\'L2L3Residual\'"
			        fi
                            fi

                            if [ $sample == "mc" ] || [ $sample == "jec" ] || [ $sample == "mb" ]; then
                                ismc="True"
                            fi

                            if [ $system == "pp" ] || [ $system == "pPb" ]; then
                                genjets="GenJets"
                                matchGenjets="GenJets"
                            fi
                            if [ $system == "pp" ]; then
                                doTower="False"
                            fi
                            if [ $system == "pPb" ]; then 
                                corrlabel=""
                            fi
			    if [ $sub == "Pu" ]; then
			        corrname=`echo ${algo} | sed 's/\(.*\)/\U\1/'`${sub}${radius}${object}${corrlabel}
			    else 
			        corrname=`echo ${algo} | sed 's/\(.*\)/\U\1/'`${radius}${object}${corrlabel}
			    fi
                            
			    if [ $groom == "SoftDrop" ] || [ $groom == "Filter" ]; then
			        doSubJets="True"
                                if [ $sample == "mc" ] && [ $groom == "SoftDrop" ]; then
                                    doGenSubJets="True"
                                fi
			    fi

                            cat templateSequence_bTag_cff.py.txt \
                                | sed -e "s/ALGO_/$algo/g" \
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
                                      -e "s/TRACKS/$tracks/g" \
                                      -e "s/VERTEX/$vertex/g" \
                                      -e "s/PARTICLEFLOW/$pflow/g" \
                                      -e "s/DOMATCH/$domatch/g" \
                                      -e "s/EVENTINFOTAG/$eventinfotag/g" \
			              -e "s/JETCORRECTIONLEVELS/$jetcorrectionlevels/g" \
			              -e "s/DOTOWERS_/$doTower/g" \
			              -e "s/DOSUBJETS_/$doSubJets/g" \
                                      -e "s/DOGENSUBJETS_/$doGenSubJets/g" \
			              -e "s/RESOLVEBYDIST_/$resolveByDist/g" \
				      > $algo$subt$groomt$radius${object}JetSequence_${system}_${sample}_cff.py

			    # skip no sub
			    if [ $sample == "jec" ]; then
                                echo "${algo}${subt}${groomt}${radius}${object}JetAnalyzer.genPtMin = cms.untracked.double(1)" >> $algo$subt$groomt$radius${object}JetSequence_${system}_${sample}_cff.py
			        echo "${algo}${subt}${groomt}${radius}${object}JetAnalyzer.jetPtMin = cms.double(1)" >> $algo$subt$groomt$radius${object}JetSequence_${system}_${sample}_cff.py
                            fi
                        done
                    done
                done
            done
        done
    done
done
