#!/usr/bin/env bash

./download_from_ncbi.py
./download_from_phagesdb.py
./download_from_viralzone.py

cat *.genomes.fasta > all.genomes.fasta
cat *.genomes.conversion > all.genomes.conversion
cat *.genes.fasta > all.genes.fasta
cat *.genes.conversion > all.genes.conversion

./deduplicate_genomes.py ./all.genomes.fasta ./all.genomes.conversion ./all.genes.conversion

prokka --force --kingdom Viruses ./deduplicated.genomes.fasta

./parse_prokka_output.py

# crocoblast
blastp  -query ./prokka_genes.fasta \
        -db ./prokka_genes.fasta    \
        -out ./prokka_genes.blast   \
        -outfmt "6 qseqid sseqid score pident ppos"     \
        -num_threads 16

./create_similarity_matrix.py ./prokka_genes.blast
./make_PCA.py