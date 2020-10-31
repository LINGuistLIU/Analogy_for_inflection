#!/bin/bash

set -euo pipefail

LANGUAGE=$1
TYPE=$2
OUTFILE=$3
DIRNOW=$4

DATABIN=$DIRNOW/data-bin
CKPTS=$DIRNOW/checkpoints

echo $LANGUAGE $TYPE

CHECKPOINT_DIR="${CKPTS}/${LANGUAGE}-models"
PRED="${CKPTS}/${LANGUAGE}-predictions/test"

mkdir -p "${CKPTS}/${LANGUAGE}-predictions"

if [[ "${TYPE}" == "dev" ]]; then
    TYPE=valid
    PRED="${CKPTS}/${LANGUAGE}-predictions/dev"
fi

for MODEL in $(ls "${CHECKPOINT_DIR}"); do
  echo "... generating with model ${MODEL} ..."

  fairseq-generate \
      "${DATABIN}/${LANGUAGE}" \
      --gen-subset "${TYPE}" \
      --source-lang "${LANGUAGE}.input" \
      --target-lang "${LANGUAGE}.output" \
      --path "${CHECKPOINT_DIR}/${MODEL}" \
      --beam 5 \
      > "${PRED}-${MODEL}.txt"

done

# keep only the first 5 best models on dev and the best and last models, delete others
if [[ "${TYPE}" == "valid" ]]; then
    TYPE=dev
    python $DIRNOW/src/best_model_on_dev.py $LANGUAGE $DIRNOW >> $OUTFILE
fi


