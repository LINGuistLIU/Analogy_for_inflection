#!/bin/bash

LANGUAGE=$1
TYPE=$2
DIRNOW=$3

python3 $DIRNOW/src/makedata_$TYPE/prepareTrain.py $LANGUAGE $DIRNOW
python3 $DIRNOW/src/makedata_$TYPE/prepareDev.py $LANGUAGE $DIRNOW
python3 $DIRNOW/src/makedata_$TYPE/prepareTest.py $LANGUAGE $DIRNOW


fairseq-preprocess \
    --source-lang="${LANGUAGE}.input" \
    --target-lang="${LANGUAGE}.output" \
    --trainpref=$DIRNOW/train \
    --validpref=$DIRNOW/dev \
    --testpref=$DIRNOW/test \
    --tokenizer=space \
    --thresholdsrc=1 \
    --thresholdtgt=1 \
    --destdir="${DIRNOW}/data-bin/${LANGUAGE}/"

#rm *.input *.output

DATADIR="${DIRNOW}/data_${TYPE}/${LANGUAGE}"

mkdir -p $DATADIR

mv $DIRNOW/*".${LANGUAGE}."* $DATADIR
