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

./extract_prokka_genes.py ./deduplicated.prokka

# crocoblast
blastp  -query ./prokka_genes.fasta \
        -db ./prokka_genes.fasta    \
        -out ./prokka_genes.blast   \
        -outfmt "6 qseqid sseqid score pident ppos"     \
        -num_threads 16

./create_similarity_matrix.py CrocoBlast/final_result PROKKA.genes.conversion deduplicated.genomes.list 0 1000

./make_PCA.py