#!/usr/bin/env bash

cd /data/projects/kimona/scripts/bachelor_thesis
./download_from_ncbi.py
./download_from_phagesdb.py
./download_from_viralzone.py

mv *.genomes.fasta /data/projects/kimona/data/
mv *.genomes.conversion /data/projects/kimona/data/
mv *.genes.fasta /data/projects/kimona/data/
mv *.genes.conversion /data/projects/kimona/data/

cat *.genomes.fasta > all.genomes.fasta
cat *.genomes.conversion > all.genomes.conversion
cat *.genes.fasta > all.genes.fasta
cat *.genes.conversion > all.genes.conversion

./deduplicate_genomes.py ../../data/all.genomes.fasta \
                         ../../data/all.genomes.conversion \
                         ../../data/all.genes.conversion

mv ./deduplicated.genomes.fasta /data/projects/kimona/data/
mv ./deduplicated.genomes.conversion /data/projects/kimona/data/
mv ./deduplicated.genes.conversion /data/projects/kimona/data/

prokka --force --kingdom Viruses ../../data/deduplicated.genomes.fasta

mv ./PROKKA_08302017/ /data/projects/kimona/data/

./extract_prokka_genes.py ../../data/PROKKA_08302017/PROKKA_08302017.gbk

mv ./PROKKA_2017-08-31.genes.fasta ../../data/
mv ./PROKKA_2017-08-31.genes.conversion ../../data/

# for NUM in $(seq 1 -0.01 0.6); do
#     cd-hit -c ${NUM} -d 0 -g 1 -i ../PROKKA_2017-08-31.genes.fasta -o genes_${NUM} -T 10;
# done;

# ./parallelize_global_alignment.py ../../data/cd-hit/genes_1.00 ../../data/global_alignment_tmp

crocoblast -add_database \
                --sequence_file \
                    protein \
                    ../../data/PROKKA_2017-08-31.genes.fasta \
                    PROKKA_2017-08-31.genes.fasta \
                    /data/projects/kimona/crocoblast/

crocoblast -add_to_queue \
                blastp \
                PROKKA_2017-08-31.genes.fasta \
                ../../data/PROKKA_2017-08-31.genes.fasta \
                /data/projects/kimona/data/ \
                --blast_options \
                    -outfmt 6 \
                    -max_target_seqs 1000000 \
                    -max_hsps 1

crocoblast -run

cd ../../data/global_alignment

# next step around 11 hours on 160 cores
../../scripts/bachelor_thesis/scripts/parallelize_global_alignment_from_blast.py \
                    ../data/CrocoBLAST_2/complete_assembled_output \
                    ../data/03-annotation/PROKKA_2017-08-31.genes.fasta \
                    ../data/global_alignment


# ./prepare_data_for_mcl.py ../../data/CrocoBLAST_2/complete_assembled_output
# Example: mcl 00001.abc --abc -o 00001.abc.clstr -I 1.2
# mcl ../../data/weights.abc --abc -o ../../data/clusters.clstr -I 1.2     # -I should be from 1.2 (biggest clusters) to 5.0
# ./create_pairs_from_mcl_output.py ../../data/clusters.clstr ../../data/pairs.txt

cat ../../data/global_alignment_tmp/*.tsv.gz > all.tsv.gz
gunzip all.tsv.gz
mcl --abc all.tsv -o ../../data/clusters.clstr -I 1.2

# ./expand_clusters ../../data/clusters.clstr ../../data/cd-hit/genes_1.00.clstr > ../../data/complete_clusters
# ./create_pairs_from_clusters ../../data/complete_clusters > ../../data/pairs

less ../../data/deduplicated.genomes.conversion | cut -f1 | sort | uniq > ../../data/deduplicated.genomes.list

# ./parallelize_matrix_creation.py ../../data/CrocoBLAST_2/complete_assembled_output \
#                                  ../../data/PROKKA_2017-08-31.genes.conversion \
#                                  ../../data/deduplicated.genomes.list

# this is for the first iteration
# ./parallelize_matrix_creation.py ../../data/pairs \
#                                  ../../data/PROKKA_2017-08-31.genes.conversion \
#                                  ../../deduplicated.genomes.list

./create_matrix_from_mcl.py ../../data/03-annotation/PROKKA_2017-08-31.genes.conversion \
                            ../../data/mcl/complete_records.abc.clstr \
                            ../../data/phage_list.txt        # ../../data/deduplicated.genomes.list

# first iteration
# mkdir ../../data/similarities/
# mv *.sim ../../data/similarities/
# marge_sim_files.py ../../data/similarities/*.sim

mv matrix.tsv ../../data/matrix_170919.tsv

./create_plot.sh "Escherichia"    # use string in which you are interested
