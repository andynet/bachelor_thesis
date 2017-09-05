#!/usr/bin/python3

import sys
import multiprocessing


def get_phage_genes(phage, genes):

    result = []
    for gene in genes:
        gene_id = gene.split('\t')[0]
        phage_id = gene.split('\t')[1]

        if phage_id == phage:
            result.append(gene_id)

    return result


def load_gene_pairs(gene_pairs_file):

    with open(gene_pairs_file) as f:
        pairs = f.readlines()

    gene_pairs = set()

    for pair in pairs:
        gene1 = pair.split('\t')[0]
        gene2 = pair.split('\t')[1]

        gene_pairs.add((min(gene1, gene2), max(gene1, gene2)))

        if len(gene_pairs) % 1000 == 0:
            print(len(gene_pairs), 'gene pairs loaded successfully', end='\r')

    print('')
    return gene_pairs


def load_lines(file):

    with open(file) as f:
        lines = f.readlines()

    return lines


def get_comparison(phage_number):

    global gene_pairs
    global genes
    global phages

    phage1 = phages[phage_number].strip()
    phage1_genes = get_phage_genes(phage1, genes)
    out = open(phage1 + '.sim', 'w')

    header = 'name' + 'phage' * phage_number
    body = phage1 + '\t' * phage_number

    for i in range(phage_number, len(phages)):

        phage2 = phages[i].strip()
        phage2_genes = get_phage_genes(phage2, genes)

        intersection = 0
        for gene1 in phage1_genes:
            for gene2 in phage2_genes:

                if (min(gene1, gene2), max(gene1, gene2)) in gene_pairs:
                    intersection += 1
                    break

        union = len(phage1_genes) + len(phage2_genes) - intersection

        try:
            similarity = intersection/union
        except ZeroDivisionError:
            similarity = None

        # print(phage1, phage2, union, intersection, similarity)
        # header += '\t' + phage2
        body += '\t' + str(similarity)

    # out.write(header + '\n')
    out.write(body + '\n')
    out.close()


def init(gene_pairs_pointer, genes_pointer, phages_pointer):
    global gene_pairs
    global genes
    global phages

    gene_pairs = gene_pairs_pointer
    genes = genes_pointer
    phages = phages_pointer


# <editor-fold desc="start processes">
if len(sys.argv) != 6:
    print('Usage:', sys.argv[0], '<gene_pairs> <genes.conversion> <phages_list> <start> <end>')
    exit()

gene_pairs = load_gene_pairs(sys.argv[1])
genes = load_lines(sys.argv[2])
phages = load_lines(sys.argv[3])
start = int(sys.argv[4])
stop = min(int(sys.argv[5]), len(phages))

pool = multiprocessing.Pool(16, initializer=init, initargs=(gene_pairs, genes, phages))
pool.map(get_comparison, range(start, stop))
# </editor-fold>
