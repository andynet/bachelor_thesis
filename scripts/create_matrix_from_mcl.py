#!/usr/bin/python3
# TODO: parallelize for 160 cores
#

import sys
import multiprocessing


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


def get_vector(phage_number):

    global genes_conv
    global genes_to_clusters
    global phage_list
    global number_of_clusters
    global out

    phage = phage_list[phage_number].strip()
    genes = get_phage_genes(phage, genes_conv)

    active_clusters = set()
    for gene in genes:
        try:
            active_clusters.add(genes_to_clusters[gene])
        except KeyError:
            print('Gene', gene, 'has no cluster.')

    vector = []
    for i in range(0, number_of_clusters):
        if 'cluster{}'.format(i) in active_clusters:
            vector.append('1')
        else:
            vector.append('0')

    out.write('{}\t{}\n'.format(phage, '\t'.join(vector)))


def init(genes_conv_pointer, genes_to_cluster_pointer, phage_list_pointer, number_of_clusters_pointer, out_pointer):
    global genes_conv
    global genes_to_clusters
    global phage_list
    global number_of_clusters
    global out

    genes_conv = genes_conv_pointer
    genes_to_clusters = genes_to_cluster_pointer
    phage_list = phage_list_pointer
    number_of_clusters = number_of_clusters_pointer
    out = out_pointer

# <editor-fold desc="start processes">
if len(sys.argv) != 7:
    print('Usage:', sys.argv[0], '<genes.conversion> <complete_output.clstr> <phages_list> <start> <end> <out>')
    print('Example:', sys.argv[0], '/data/projects/kimona/data/03-annotation/PROKKA_2017-08-31.genes.conversion ',
                                   '/data/projects/kimona/data/mcl/complete_records.abc.clstr ',
                                   '/data/projects/kimona/data/phage_list.txt ',
                                   '0 ',
                                   '10000 ',
                                   '/data/projects/kimona/data/matrix_from_mcl.tsv')
    exit()

with open(sys.argv[1]) as f:
    genes_conv = f.readlines()

with open(sys.argv[2]) as f:
    lines = f.readlines()
    number_of_clusters = len(lines)
    genes_to_clusters = get_genes_to_clusters(lines)

with open(sys.argv[3]) as f:
    phage_list = f.readlines()

start = int(sys.argv[4])
stop = min(int(sys.argv[5]), len(phage_list))
out = open(sys.argv[6], 'w')

pool = multiprocessing.Pool(32, initializer=init, initargs=(genes_conv, genes_to_clusters, phage_list,
                                                            number_of_clusters, out))
pool.map(get_vector, range(start, stop))

out.close()
# </editor-fold>