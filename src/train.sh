#!/bin/bash

set -euo pipefail

LANGUAGE=$1
# Max-update
MXU=$2
#MXU=30000
#MXU=20000
#MXU=1000
DIRNOW=$3

# save-interval
#SNT=50
#SNT=10
#SNT=1
SNT=$4

SEED=3124
#SEED=111
#SEED=312
##SEED=112
##SEED=64
##SEED=212
##SEED=1000
DATABIN=$DIRNOW/data-bin
CKPTS=$DIRNOW/checkpoints

# Encoder embedding dim.
EED=256
# Encoder hidden layer size.
EHS=1024
# Encoder number of layers.
ENL=4
# Encoder number of attention heads.
EAH=4
# Decoder embedding dim.
DED=256
# Decoder hidden layer size.
DHS=1024
# Decoder number of layers.
DNL=4
# Decoder number of attention heads.
DAH=4
# Dropout
DRP=0.3

# Batch size
BTS=400
# Warmup update
WMU=4000
# Learning rate
LRT=0.001
# Label smoothing
LST=0.1
# clip-norm
CNM=1.0

# Max-epoch
#MPC=10000



fairseq-train "${DATABIN}/${LANGUAGE}" \
    --task=translation \
    --source-lang="${LANGUAGE}.input" \
    --target-lang="${LANGUAGE}.output" \
    --save-dir="${CKPTS}/${LANGUAGE}-models" \
    --dropout="${DRP}" \
    --attention-dropout="${DRP}" \
    --activation-dropout="${DRP}" \
    --arch=transformer \
    --activation-fn=relu \
    --encoder-embed-dim="${EED}" \
    --encoder-ffn-embed-dim="${EHS}" \
    --encoder-layers="${ENL}" \
    --encoder-attention-heads="${EAH}" \
    --encoder-normalize-before \
    --decoder-embed-dim="${DED}" \
    --decoder-ffn-embed-dim="${DHS}" \
    --decoder-layers="${DNL}" \
    --decoder-attention-heads="${DAH}" \
    --decoder-normalize-before \
    --share-decoder-input-output-embed \
    --optimizer=adam \
    --adam-betas='(0.9, 0.98)' \
    --clip-norm="${CNM}" \
    --lr="${LRT}" \
    --lr-scheduler=inverse_sqrt \
    --warmup-updates="${WMU}" \
    --criterion=label_smoothed_cross_entropy \
    --label-smoothing="${LST}" \
    --batch-size="${BTS}" \
    --max-update="${MXU}" \
    --save-interval="${SNT}" \
    --distributed-world-size=1 \
    --device-id=0 \
    --seed="${SEED}"


