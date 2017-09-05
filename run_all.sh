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

less ../../data/deduplicated.genomes.conversion | cut -f1 | sort | uniq > ../../data/deduplicated.genomes.list

./parallelize_matrix_creation.py ../../data/CrocoBLAST_2/complete_assembled_output \
                                 ../../data/PROKKA_2017-08-31.genes.conversion \
                                 ../../data/deduplicated.genomes.list

# TODO: merge_sim_files.py
# TODO: make_PCA.py