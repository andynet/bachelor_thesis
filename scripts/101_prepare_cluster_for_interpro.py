#!/usr/bin/python3

import sys
from Bio import SeqIO

if len(sys.argv) != 4:
    print('Usage:', sys.argv[0], '<genes.fasta> <clusters> <cluster_id>')
    exit()

with open(sys.argv[2]) as f:
    clusters = f.readlines()

genes = list(SeqIO.parse(sys.argv[1], 'fasta'))
cluster_of_interest = sorted(clusters[int(sys.argv[3])].split())

# print(len(cluster_of_interest))
# print(cluster_of_interest[:10])

for gene in cluster_of_interest:
    index = int(gene[5:])
    # print(index)
    # print(genes[index])
    print('>{}'.format(genes[index].description))
    print('{}'.format(genes[index].seq))
