#!/usr/bin/env bash

echo "Script started at "$(date)
set -e                  # exit immediately after return of non-zero status
set -u                  # treat unset variables as an error

SCRIPT=$(readlink -f ${0})
SCRIPT_DIR=$(dirname ${SCRIPT})

if [ $# -ne 1 ]; then
    echo "Usage: ${SCRIPT} <DATA_DIR>"
    exit 1
fi

DATA_DIR=${1}           # Example: /data/projects/kimona/data_17-11-28
STAGE_DIR=${DATA_DIR}/stages

mkdir -p ${DATA_DIR}
mkdir -p ${STAGE_DIR}

###############################################################################
##### Initialization complete, start execution ################################
###############################################################################

if [ -f ${STAGE_DIR}/001_downloading ]; then
    echo "Data already downloaded. Skipping..."
else
    #${SCRIPT_DIR}/download_from_ncbi.py ${DATA_DIR}
    ${SCRIPT_DIR}/download_from_phagesdb.py ${DATA_DIR}
    ${SCRIPT_DIR}/download_from_viralzone.py ${DATA_DIR}

    touch ${STAGE_DIR}/001_downloading
fi

###############################################################################

if [ -f ${STAGE_DIR}/002_merging ]; then
    echo "Data already merged. Skipping..."
else
    cat ${DATA_DIR}/001_*.genomes.fasta         > ${DATA_DIR}/002_all.genomes.fasta
    cat ${DATA_DIR}/001_*.genomes.conversion    > ${DATA_DIR}/002_all.genomes.conversion
    cat ${DATA_DIR}/001_*.genes.fasta           > ${DATA_DIR}/002_all.genes.fasta
    cat ${DATA_DIR}/001_*.genes.conversion      > ${DATA_DIR}/002_all.genes.conversion

    touch ${STAGE_DIR}/002_merging
fi

###############################################################################

if [ -f ${STAGE_DIR}/003_deduplicating ]; then
    echo "Data already deduplicated. Skipping..."
else
    ${SCRIPT_DIR}/deduplicate_genomes.py ${DATA_DIR}/002_all.genomes.fasta      \
                                         ${DATA_DIR}/002_all.genomes.conversion \
                                         ${DATA_DIR}/002_all.genes.conversion   \
                                         ${DATA_DIR}
fi

###############################################################################
exit

prokka --force                                      \
       --kingdom Viruses                            \
       --outdir ${DATA_DIR}/PROKKA                  \
       --prefix deduplicated.genomes                \
       ${DATA_DIR}/003_deduplicated.genomes.fasta

${SCRIPT_DIR}/extract_prokka_genes.py ${DATA_DIR}/PROKKA/003_deduplicated.genomes.gbk ${DATA_DIR}   # TODO

crocoblast -add_database \
                --sequence_file \
                    protein \
                    ${DATA_DIR}/PROKKA_2017-08-31.genes.fasta \
                    PROKKA_2017-08-31.genes.fasta \
                    /data/projects/kimona/crocoblast/

crocoblast -add_to_queue \
                blastp \
                PROKKA_2017-08-31.genes.fasta \
                ${DATA_DIR}/PROKKA_2017-08-31.genes.fasta \
                /data/projects/kimona/data/ \
                --blast_options \
                    -outfmt 6 \
                    -max_target_seqs 1000000 \
                    -max_hsps 1

crocoblast -run


