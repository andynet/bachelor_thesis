#!/usr/bin/env bash

SEARCH=$1

./get_labels_for_PCA.py ../../data/phage_list.txt ../../data/deduplicated.genomes.conversion "$SEARCH" > ../../data/labels.txt
./make_PCA.py ../../data/matrix_170921_tabs.tsv ../../data/labels.txt