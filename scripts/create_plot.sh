#!/usr/bin/env bash

SEARCH=$1
FILE=$2
MATRIX=${FILE%%.tsv}.sorted.cutted.tsv
LIST=${FILE%%.tsv}.list
LABELS=${FILE%%.tsv}.labels

less ${FILE} | sort -k 1 | cut -f 2- > ${MATRIX}
less ${FILE} | sort -k 1 | cut -f 1 > ${LIST}

echo "${MATRIX}"
echo "${LIST}"

./get_labels_for_PCA.py ${LIST} ../../../data/deduplicated.genomes.conversion "$SEARCH" > ${LABELS}
./make_PCA.py ${MATRIX} ${LABELS}