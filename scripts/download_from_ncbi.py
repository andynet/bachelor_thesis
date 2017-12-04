#!/usr/bin/python3

from http.client import IncompleteRead
from Bio.SeqRecord import SeqRecord
from Bio import Entrez
from Bio import SeqIO
import time
import sys


def safe_get_qualifier(feature, key, default_value='NO_DATA'):
    try:
        return ';'.join(feature.qualifiers[key])
    except KeyError:
        return default_value


if len(sys.argv) != 2:
    print('Usage:', sys.argv, '<dir>')
    exit()

genomes_output_file = '{}/001_ncbi.genomes.fasta'.format(sys.argv[1])
genomes_conversion_file = '{}/001_ncbi.genomes.conversion'.format(sys.argv[1])
genomes_output = open(genomes_output_file, 'w')
genomes_conversion = open(genomes_conversion_file, 'w')

genes_output_file = '{}/001_ncbi.genes.fasta'.format(sys.argv[1])
genes_conversion_file = '{}/001_ncbi.genes.conversion'.format(sys.argv[1])
genes_output = open(genes_output_file, 'w')
genes_conversion = open(genes_conversion_file, 'w')

query = 'phage[Title] AND (complete genome[Title] OR complete sequence[Title]) AND (viruses[filter] ' \
        'AND biomol_genomic[PROP] AND ("10000"[SLEN] : "100000000"[SLEN]))'

Entrez.email = 'andrejbalaz001@gmail.com'

handle = Entrez.esearch(db="nucleotide", term=query, idtype='acc', retmax=100000, usehistory='y')
record = Entrez.read(handle)
handle.close()

webenv = record["WebEnv"]
query_key = record["QueryKey"]
batch = 200
genome_num = 0
gene_num = 0

i = 0
while i < len(record['IdList']):

    print('Downloaded', i, 'sequences.')

    fa_handle = None
    gb_handle = None

    while fa_handle is None or gb_handle is None:
        fa_handle = Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text", idtype="acc",
                                  retstart=i, retmax=batch, webenv=webenv, query_key=query_key)
        gb_handle = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text",
                                  retstart=i, retmax=batch, webenv=webenv, query_key=query_key)

    try:
        fa_list = list(SeqIO.parse(fa_handle, 'fasta'))
        gb_list = list(SeqIO.parse(gb_handle, 'genbank'))
    except IncompleteRead:
        print('Incomplete read. Trying again...')
        time.sleep(10)
        continue

    fa_handle.close()
    gb_handle.close()

    for j in range(0, len(fa_list)):

        fa = fa_list[j]                 # type: SeqRecord
        gb = gb_list[j]                 # type: SeqRecord

        fasta_id = 'phage{:0>7}'.format(genome_num)
        genome_num += 1

        fasta_seq = str(fa.seq)

        genomes_output.write('>' + fasta_id + '\n')
        genomes_output.write(fasta_seq + '\n')

        for feature in gb.features:
            if feature.type == 'source':

                organism = safe_get_qualifier(feature, 'organism')
                host = safe_get_qualifier(feature, 'host')
                lab_host = safe_get_qualifier(feature, 'lab_host')

                genomes_conversion.write('{}\t{}\t{}\t{}\t{}\n'.format(fasta_id, gb.id, organism, host, lab_host))

            if feature.type == 'CDS':

                gene_id = 'gene{:0>8}'.format(gene_num)
                gene_num += 1

                gene_seq = safe_get_qualifier(feature, 'translation')

                genes_output.write('>' + gene_id + '\n')
                genes_output.write(gene_seq + '\n')

                protein_id = safe_get_qualifier(feature, 'protein_id')
                product = safe_get_qualifier(feature, 'product')
                note = safe_get_qualifier(feature, 'note')

                genes_conversion.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(gene_id, fasta_id, protein_id,
                                                                         feature.location, product, note))

    i += batch

genomes_output.close()
genomes_conversion.close()
genes_output.close()
genes_conversion.close()
