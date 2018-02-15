#!/usr/bin/env bash

set -e                  # exit immediately after return of non-zero status
set -u                  # treat unset variables as an error

SCRIPT=$(readlink -f ${0})
SCRIPT_DIR=$(dirname ${SCRIPT})

if [ $# -ne 2 ]; then
    echo "Usage: ${SCRIPT} <QUERY> <009_matrix.tsv>"
    exit 1
fi

QUERY=${1}
INPUT=${2}
DATA_DIR=$(dirname $(readlink -f ${2}))

MATRIX=${INPUT%%.tsv}.noid.tsv
LIST=${INPUT%%.tsv}.list

less ${INPUT} | cut -f 2- > ${MATRIX}
less ${INPUT} | cut -f 1  > ${LIST}

LABELS=${INPUT%%.tsv}.${QUERY}.labels

# ../scripts/bachelor_thesis/scripts/101_create_host_string.py 003_deduplicated.genomes.conversion > 101_hosts
# ${SCRIPT_DIR}/101_create_host_string.py ${DATA_DIR}/003_deduplicated.genomes.conversion > ${HOST_STRINGS}
# ${SCRIPT_DIR}/101_split_matrix.py ${HOST_STRINGS} ${QUERY} ${MATRIX}
${SCRIPT_DIR}/101_create_labels_for_PCA.py ${LIST} ${DATA_DIR}/003_deduplicated.genomes.conversion ${QUERY} > ${LABELS}
${SCRIPT_DIR}/102_PCA.py ${MATRIX} ${LABELS}

# interproscan -i /data/tools/interproscan-5.27.66/test_proteins.fasta -f tsv -dp -goterms

# chi square - which gene clusters are interesting?

# PCA
# ../scripts/bachelor_thesis/scripts/103_PCA.py ./101_hosts
                                            # ./mycobac/hosts.out ./mycobac/matrix_host.tsv
                                            # ./strepto/hosts.out ./strepto/matrix_host.tsv
                                            # ./escheri/hosts.out ./escheri/matrix_host.tsv
                                            # ./gordoni/hosts.out ./gordoni/matrix_host.tsv
                                            # ./pseudom/hosts.out ./pseudom/matrix_host.tsv
                                            # ./arthrob/hosts.out ./arthrob/matrix_host.tsv
                                            # ./lactoco/hosts.out ./lactoco/matrix_host.tsv
                                            # ./staphyl/hosts.out ./staphyl/matrix_host.tsv

# decision tree
# ../scripts/bachelor_thesis/scripts/104_decision_tree.py
                                                        # ./mycobac/hosts.out ./mycobac/matrix_host.tsv
                                                        # ./strepto/hosts.out ./strepto/matrix_host.tsv
                                                        # ./escheri/hosts.out ./escheri/matrix_host.tsv
                                                        # ./gordoni/hosts.out ./gordoni/matrix_host.tsv
                                                        # ./pseudom/hosts.out ./pseudom/matrix_host.tsv
                                                        # ./arthrob/hosts.out ./arthrob/matrix_host.tsv
                                                        # ./lactoco/hosts.out ./lactoco/matrix_host.tsv
                                                        # ./staphyl/hosts.out ./staphyl/matrix_host.tsv

