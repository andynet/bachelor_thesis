#!/usr/bin/python3

import sys


def get_genes_to_clusters(lines):

    result = dict()
    for i, line in enumerate(lines):
        records = line.split()
        for record in records:
            result[record] = 'cluster{}'.format(i)

    return result


def get_phage_genes(phage, genes):

    result = []
    for gene in genes:
        gene_id = gene.split('\t')[0]
        phage_id = gene.split('\t')[1]

        if phage_id == phage:
            result.append(gene_id)

    return result



if len(sys.argv) != 4:
    print('Usage', sys.argv[0], '<PROKKA.genes.conversion> <complete_output.clstr> <phage_list>')
    exit()

with open(sys.argv[1]) as f:
    genes_conv = f.readlines()

with open(sys.argv[2]) as f:
    lines = f.readlines()
    genes_to_clusters = get_genes_to_clusters(lines)

with open(sys.argv[3]) as f:
    phage_list = f.readlines()

for phage in phage_list:

    phage = phage.strip()
    genes = get_phage_genes(phage, genes_conv)

    active_clusters = set()
    for gene in genes:
        active_clusters.add(genes_to_clusters[gene])

    vector = []
    for cluster in range(0, 25000):
        if cluster in active_clusters:
            vector.append(1)
        else:
            vector.append(0)

    print('{}\t{}\n'.format(phage, '\t'.join(vector)))
    exit()
