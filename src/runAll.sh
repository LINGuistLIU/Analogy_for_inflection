#!/bin/bash

set -euo pipefail

TYPE=1src2crosstable
DIRNOW=./
SNT=10

RESULTDIR=$DIRNOW/results_$TYPE
mkdir -p $RESULTDIR

convertsecs() {
 ((h=${1}/3600))
 ((m=(${1}%3600)/60))
 ((s=${1}%60))
 printf "%02d:%02d:%02d\n" $h $m $s
}

# 15 languages
for LANGUAGE in tgk dje mao lin xno lud zul sot vro ceb mlg gmh kon gaa izh; do
# 11 languages
#for LANGUAGE in mwf zpv kjh hil gml tel vot czn ood mlt gsw; do
# 8 languages
#for LANGUAGE in tgl xty syc ctp dak liv nya bod; do

    echo $LANGUAGE

    OUTFILE=$RESULTDIR/$LANGUAGE.txt
    
    echo "----start time----" >> $OUTFILE

    date >> $OUTFILE
	
    STARTLANG=$(date +%s)
    echo "... preprocessing data ..."
    $DIRNOW/src/preprocess.sh $LANGUAGE $TYPE $DIRNOW

    count=0
    accpre=0
    for MXU in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do

        ((MXU=MXU*1000))
	
	STARTTIME=$(date +%s)
        echo "... training models MXU: ${MXU}, count: ${count}, previous accuracy: ${accpre} ..." >> $OUTFILE
        $DIRNOW/src/train.sh $LANGUAGE $MXU $DIRNOW $SNT
	
	ENDTIME=$(date +%s)
	((t=ENDTIME-STARTTIME))
	echo "Training for MXU=${MXU} takes $(convertsecs $t)" >> $OUTFILE


	STARTTIME=$(date +%s)
        echo "... generating and evaluating for dev set ..."
        $DIRNOW/src/generate.sh $LANGUAGE dev $OUTFILE $DIRNOW
	
	ENDTIME=$(date +%s)
	((t=ENDTIME-STARTTIME))


        accnow=$( tail -n 1 $OUTFILE )
        if [ $accnow == $accpre ]; then
          ((count=count+1))
        else
	  count=0
	fi
        

	accpre=$accnow
        echo $accnow $count
	echo $accnow $count >> $OUTFILE
	echo "Dev generating for MXU=${MXU} takes $(convertsecs $t)" >> $OUTFILE
	
        if [ $count -eq 5 ]; then
          break
        fi

    done


    # generate for test data
    echo "... generating and evaluating for test set ..."
    $DIRNOW/src/generate.sh $LANGUAGE test $OUTFILE $DIRNOW

    mkdir -p "${DIRNOW}/checkpoints-${TYPE}/"
    mkdir -p "${DIRNOW}/data-bin-${TYPE}/"

    mv "${DIRNOW}/checkpoints/${LANGUAGE}"* "${DIRNOW}/checkpoints-${TYPE}/"
    mv "${DIRNOW}/data-bin/${LANGUAGE}"* "${DIRNOW}/data-bin-${TYPE}/"

    echo "----end time----" >> $OUTFILE
    
    date >> $OUTFILE

    ENDLANG=$(date +%s)
    ((t=ENDLANG-STARTLANG))
    echo "${LANGUAGE} takes $(convertsecs $t)" >> $OUTFILE

done

