#!/usr/bin/env bash

SEARCH=$1

./get_labels_for_PCA.py ./phage_list.txt ../../data/deduplicated.genomes.conversion "$SEARCH" > labels.txt
./make_PCA.py ../../data/matrix_170921_tabs.tsv ./labels.txt