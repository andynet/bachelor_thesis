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

DATA_DIR=${1}
STAGE_DIR=${DATA_DIR}/stages

mkdir -p ${DATA_DIR}
mkdir -p ${STAGE_DIR}

###############################################################################
##### Initialization complete, start execution ################################
###############################################################################

if [ -f ${STAGE_DIR}/001_downloading ]; then
    echo "Data already downloaded. Skipping..."
else
    ${SCRIPT_DIR}/001_download_from_ncbi.py ${DATA_DIR}
    ${SCRIPT_DIR}/001_download_from_phagesdb.py ${DATA_DIR}
    ${SCRIPT_DIR}/001_download_from_viralzone.py ${DATA_DIR}

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
    ${SCRIPT_DIR}/003_deduplicate_genomes.py ${DATA_DIR}/002_all.genomes.fasta      \
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
    ${SCRIPT_DIR}/005_extract_prokka_genes.py ${DATA_DIR}/004_PROKKA/genomes.gbk \
                                              ${DATA_DIR}

    touch ${STAGE_DIR}/005_extracting
fi

###############################################################################
#
#   ../scripts/bachelor_thesis/scripts/006_split_train_test_other.py
#       005_annotated.genes.conversion 005_annotated.genes.fasta
#       003_deduplicated.genomes.conversion 003_deduplicated.genomes.fasta
#       101_hosts
#       mycobac,strepto,escheri,gordoni,pseudom,arthrob,lactoco,staphyl
#       0.8
#
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

    mv ${DATA_DIR}/CrocoBLAST_1 ${DATA_DIR}/006_crocoblast_output
fi

###############################################################################

if [ -f ${STAGE_DIR}/007_global_aligning ]; then
    echo "Global aligning already done. Skipping..."
else
    GLOBAL_ALIGNMENT_DIR=${DATA_DIR}/007_global_alignment
    rm -rf ${GLOBAL_ALIGNMENT_DIR}
    mkdir  ${GLOBAL_ALIGNMENT_DIR}

    ${SCRIPT_DIR}/007_parallelize_global_alignment_from_blast.py                      \
                    ${DATA_DIR}/006_crocoblast_output/complete_assembled_output       \
                    ${DATA_DIR}/005_annotated.genes.fasta                             \
                    ${GLOBAL_ALIGNMENT_DIR}

    while [ ! -f ${GLOBAL_ALIGNMENT_DIR}/qsub_completed ]; do
        sleep 20m
    done

    for i in $(seq 0 1 9); do
        cat ${GLOBAL_ALIGNMENT_DIR}/tmp/${i}*.abc > ${GLOBAL_ALIGNMENT_DIR}/tmp/${i}.final.abc  \
            && echo "${GLOBAL_ALIGNMENT_DIR}/tmp/${i}.final.abc created."                       \
            || echo "There are no files to merge into ${i}.final.abc."
    done;

    cat ${GLOBAL_ALIGNMENT_DIR}/tmp/*.final.abc > ${DATA_DIR}/007_complete_global_alignment.abc

    touch ${STAGE_DIR}/007_global_aligning
fi

###############################################################################
#
#   ../scripts/bachelor_thesis/scripts/008_get_train_and_test_sets.py
#       ./007_complete_global_alignment.abc
#       ./005_annotated.genes.conversion
#       ./101_hosts
#       mycobac,strepto,escheri,gordoni,pseudom,arthrob,lactoco,staphyl
#       0.8
#
###############################################################################

if [ -f ${STAGE_DIR}/008_mcl ]; then
    echo "Creating clusters with markov cluster algorithm done. Skipping..."
else
    mcl ${DATA_DIR}/007_complete_global_alignment.abc --abc -o ${DATA_DIR}/008_genes.clstr -I 1.2

    touch ${STAGE_DIR}/008_mcl
fi

###############################################################################

if [ -f ${STAGE_DIR}/009_matrix_creation ]; then
    echo "Matrix already created. Skipping..."
else
    less ${DATA_DIR}/003_deduplicated.genomes.conversion | cut -f1 | sort | uniq > ${DATA_DIR}/genomes.list

    ${SCRIPT_DIR}/009_parallelize_matrix_creation_from_mcl.py ${DATA_DIR}/005_annotated.genes.conversion    \
                                                              ${DATA_DIR}/008_genes.clstr                   \
                                                              ${DATA_DIR}/genomes.list

    while [ $(ls ${DATA_DIR}/matrix.part* | wc -l) -ne 11 ]; do
        sleep 1m
    done

    sleep 1m
    cat ${DATA_DIR}/matrix.part* > ${DATA_DIR}/009_matrix.tsv
    rm ${DATA_DIR}/matrix.part*
    rm ${DATA_DIR}/genomes.list

    touch ${STAGE_DIR}/009_matrix_creation
fi

###############################################################################

if [ -f ${STAGE_DIR}/010_cluster_annotation ]; then
    echo "Clusters already annotated. Skipping..."
else
    CLUSTER_ANNOTATION_DIR=${DATA_DIR}/010_cluster_annotation
    rm -rf ${CLUSTER_ANNOTATION_DIR}
    mkdir  ${CLUSTER_ANNOTATION_DIR}

    for i in $(seq 0 $(less ${DATA_DIR}/008_genes.clstr | wc -l));
    do
        echo "Annotating Cluster_${i}"

        ${SCRIPT_DIR}/101_prepare_cluster_for_interpro.py ${DATA_DIR}/005_annotated.genes.fasta                 \
                                                          ${DATA_DIR}/008_genes.clstr                           \
                                                          ${i}                                                  \
                                                          > ${CLUSTER_ANNOTATION_DIR}/Cluster_${i}.genes.fasta

        cd-hit -i ${CLUSTER_ANNOTATION_DIR}/Cluster_${i}.genes.fasta                \
               -o ${CLUSTER_ANNOTATION_DIR}/Cluster_${i}.genes.fasta.cd-hit         \
               -c 1 -d 0 -T 16

        interproscan -i ${CLUSTER_ANNOTATION_DIR}/Cluster_${i}.genes.fasta.cd-hit       \
                     -o ${CLUSTER_ANNOTATION_DIR}/Cluster_${i}.genes.fasta.cd-hit.tsv   \
                     -f tsv -goterms -cpu 16

        less ${CLUSTER_ANNOTATION_DIR}/Cluster_${i}.genes.fasta.cd-hit.tsv | cut -f 12,13 | sort | uniq -c | sort -nr   \
             > ${CLUSTER_ANNOTATION_DIR}/Cluster_${i}.result

    done

    touch ${STAGE_DIR}/010_cluster_annotation
fi

###############################################################################
echo "Program finished successfully."
echo "You can find final matrix in ${DATA_DIR}/009_matrix.tsv"
