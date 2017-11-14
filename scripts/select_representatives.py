#!/usr/bin/python3
# TODO: finish
# NOT USED IN MAIN PIPELINE

import sys
import subprocess
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


def get_gene_cluster(lines):

    result = dict()

    for i, line in enumerate(lines):
        genes = line.split()
        for gene in genes:
            result[gene] = 'cluster{:0>7}'.format(i)

    return result


if len(sys.argv) != 5:
    print('Usage:', sys.argv[0], '<clusters> <abc_file> <genes.fasta> <out.fasta>')
    exit()

with open(sys.argv[1]) as f:
    lines = f.readlines()
    gene_cluster = get_gene_cluster(lines)

gene_score = dict()

with open(sys.argv[2]) as f:
    lines = f.readlines()

for i, line in enumerate(lines):

    gene1 = line.split()[0]
    gene2 = line.split()[1]
    score = float(line.split()[2])

    if gene1 not in gene_score:
        gene_score[gene1] = 0

    if gene2 not in gene_score:
        gene_score[gene2] = 0

    if gene_cluster[gene1] == gene_cluster[gene2] and gene1 != gene2:
        gene_score[gene1] += score
        gene_score[gene2] += score

    if i % 1000000 == 0:
        print('{} lines from abc file processed'.format(i))

print('Abc file processed completely.')
best_results = dict()

for gene, cluster in gene_cluster.items():

    if cluster not in best_results:
        best_results[cluster] = (gene, gene_score[gene])
    else:
        if best_results[cluster][1] < gene_score[gene]:
            best_results[cluster] = (gene, gene_score[gene])

genes_fa = list(SeqIO.parse(sys.argv[3], 'fasta'))
switched_dict = dict((value[0], (cluster, value[1])) for cluster, value in best_results.items())
tmp_out_file = '{}_tmp'.format(sys.argv[4])
out = open(tmp_out_file, 'w')

for record in genes_fa:     # type: SeqRecord

    if record.id in switched_dict:

        data = switched_dict[record.id]

        if data[1] != 0:
            out.write('>{}_{}_{}:'.format(data[0], record.id, data[1]))
            out.write('{}\n'.format(record.seq))

out.close()

subprocess.call("less {} | sort  | tr ':' '\n' > {}; rm {}".format(tmp_out_file, sys.argv[4], tmp_out_file), shell=True)
