#!/bin/sh

for system in pp
do
    for sample in data jec mc
    do
        for algo in ak
        do
	    for groom in SoftDrop Filter NONE
	    do
		for radius in 1 2 3 4 5 6
		do
		    for object in PF Calo
		    do
			subt=""
			groomt=$groom
			if [ $groom == "NONE" ]; then
			    groomt=""
			fi
			partons="genParticles"
			genjets="GenJets"
			matchGenjets="GenJets"
			resolveByDist="False"
			ispp="True"
			ismc="False"
			corrlabel="_offline"
			domatch="True"
			tracks="generalTracks"
			pflow="particleFlow"
			domatch="False"
			doTower="False"
			doSubJets="False"
			doGenSubJets="False"
			match=""
			eventinfotag="generator"
			jetcorrectionlevels="\'L2Relative\'"
			genparticles="genParticles"

			if [ $sample == "data" ]; then
			    jetcorrectionlevels="\'L2Relative\',\'L2L3Residual\'"
			fi

			if [ $sample == "mc" ] || [ $sample == "jec" ]; then
			    ismc="True"
			fi

			if [ $object == "PF" ]; then
			    corrname="AK${radius}${object}"
			else
			    corrname="AK4PF"
			fi
			if [ $groom == "SoftDrop" ] || [ $groom == "Filter" ]; then
			    doSubJets="True"
			    if [ $sample == "mc" ] && [ $groom == "SoftDrop" ]; then
				doGenSubJets="True"
			    fi
			fi

			fulltag=${algo}${subt}${groomt}${radius}${object}
			jetseqfile=${fulltag}JetSequence_${system}_${sample}_cff.py

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
			    -e "s/ISPP/$ispp/g" \
			    -e "s/MATCHGENJETS/$matchGenjets/g" \
			    -e "s/GENJETS/$genjets/g" \
			    -e "s/GENPARTICLES/$genparticles/g" \
			    -e "s/PARTONS/$partons/g" \
			    -e "s/TRACKS/$tracks/g" \
			    -e "s/PARTICLEFLOW/$pflow/g" \
			    -e "s/DOMATCH/$domatch/g" \
			    -e "s/EVENTINFOTAG/$eventinfotag/g" \
			    -e "s/JETCORRECTIONLEVELS/$jetcorrectionlevels/g" \
			    -e "s/DOTOWERS_/$doTower/g" \
			    -e "s/DOSUBJETS_/$doSubJets/g" \
			    -e "s/DOGENSUBJETS_/$doGenSubJets/g" \
			    -e "s/RESOLVEBYDIST_/$resolveByDist/g" \
			    > $jetseqfile

			if [ $doSubJets == "True" ]; then
			    sed -i 's/\#SUBJETDUMMY_//g' $jetseqfile
			fi

                        if [ $object != "Calo" ]; then
                            sed -i 's/\#DISABLE_PPCALO_//g' $jetseqfile
			else
			    sed -i 's/\#ENABLE_PPCALO_//g' $jetseqfile
                        fi
			# skip no sub
			if [ $sample == "jec" ]; then
			    echo "${fulltag}JetAnalyzer.genPtMin = cms.untracked.double(1)" >> $jetseqfile
			    echo "${fulltag}JetAnalyzer.jetPtMin = cms.double(1)" >> $jetseqfile
			    echo "${fulltag}JetAnalyzer.doSubEvent = True" >> $jetseqfile
			fi
		    done
		done
	    done
	done
    done
done
