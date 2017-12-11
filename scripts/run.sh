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

    touch ${STAGE_DIR}/003_deduplicating
fi

###############################################################################

if [ -f ${STAGE_DIR}/004_annotating ]; then
    echo "Data already annotated. Skipping..."
else
    /usr/local/tools/prokka-1.12.0/bin/prokka --force                                      \
                                              --kingdom Viruses                            \
                                              --outdir ${DATA_DIR}/004_PROKKA              \
                                              --prefix genomes                             \
                                              ${DATA_DIR}/003_deduplicated.genomes.fasta

    touch ${STAGE_DIR}/004_annotating
fi

###############################################################################

if [ -f ${STAGE_DIR}/005_extracting ]; then
    echo "Prokka genes already extracted. Skipping..."
else
    ${SCRIPT_DIR}/extract_prokka_genes.py ${DATA_DIR}/004_PROKKA/genomes.gbk \
                                          ${DATA_DIR}

    touch ${STAGE_DIR}/005_extracting
fi

###############################################################################

if [ -f ${STAGE_DIR}/006_local_aligning ]; then
    echo "Local aligning already done. Skipping..."
else
    rm -rf ${DATA_DIR}/006_crocoblast/ ${DATA_DIR}/006_crocoblast_database/
    cp -r  ${SCRIPT_DIR}/crocoblast/ ${DATA_DIR}/006_crocoblast/
    mkdir  ${DATA_DIR}/006_crocoblast_database

    ${DATA_DIR}/006_crocoblast/crocoblast -add_database                                 \
                                              --sequence_file                           \
                                                  protein                               \
                                                  ${DATA_DIR}/005_annotated.genes.fasta \
                                                  005_annotated.genes.fasta             \
                                                  ${DATA_DIR}/006_crocoblast_database

    ${DATA_DIR}/006_crocoblast/crocoblast -add_to_queue                             \
                                              blastp                                \
                                              005_annotated.genes.fasta             \
                                              ${DATA_DIR}/005_annotated.genes.fasta \
                                              ${DATA_DIR}                           \
                                              --blast_options                       \
                                                  -outfmt 6                         \
                                                  -max_target_seqs 1000000          \
                                                  -max_hsps 1

    echo "${DATA_DIR}/006_crocoblast/crocoblast -run > /dev/null; touch ${STAGE_DIR}/006_local_aligning" \
    | qsub -l thr=16 -cwd -N crocoblast

    while [ ! -f ${STAGE_DIR}/006_local_aligning ]; do
        sleep 20m
    done
fi

###############################################################################
exit
# until now everything LGTM
# TODO refactor python scripts

if [ -f ${STAGE_DIR}/007_global_aligning ]; then
    echo "Global aligning already done. Skipping..."
else
    ${SCRIPT_DIR}/parallelize_global_alignment_from_blast.py    \
                    ${DATA_DIR}/complete_assembled_output       \
                    ${DATA_DIR}/005_annotated.genes.fasta       \
                    ${DATA_DIR}/007_global_alignment

    cat ${DATA_DIR}/007_global_alignment/*.tsv.gz > ${DATA_DIR}/all.tsv.gz
    gunzip ${DATA_DIR}/all.tsv.gz

    touch ${STAGE_DIR}/007_global_aligning
fi

###############################################################################

if [ -f ${STAGE_DIR}/008_mcl ]; then
    echo "Creating clusters with markov cluster algorithm done. Skipping..."
else
    mcl --abc ${DATA_DIR}/all.tsv -o ${DATA_DIR}/clusters.clstr -I 1.2

    touch ${STAGE_DIR}/008_mcl
fi

###############################################################################

if [ -f ${STAGE_DIR}/009_matrix_creation ]; then
    echo "Matrix already created. Skipping..."
else
    less ${DATA_DIR}/003_deduplicated.genomes.conversion | cut -f1 | sort | uniq > ${DATA_DIR}/deduplicated.genomes.list

    ${SCRIPT_DIR}/create_matrix_from_mcl.py ${DATA_DIR}/005_annotated.genes.conversion  \
                                            ${DATA_DIR}/clusters.clstr                  \
                                            ${DATA_DIR}/deduplicated.genomes.list
    touch ${STAGE_DIR}/009_matrix_creation
fi

###############################################################################
echo "Program finished successfully."
echo "You can find final matrix in ${DATA_DIR}/"
exit