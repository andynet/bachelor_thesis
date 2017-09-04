#!/usr/bin/python3

import sys
import time
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


def get_comparison(gene_pairs, genes, phages, phage1):

    phage1_genes = get_phage_genes(phage1, genes)
    out = open(phage1 + '.sim', 'w')

    header = 'name'
    body = phage1

    for i in range(len(phages)):

        phage2 = phages[i].strip()
        phage2_genes = get_phage_genes(phage2, genes)

        intersection = 0
        for gene1 in phage1_genes:
            for gene2 in phage2_genes:

                if (min(gene1, gene2), max(gene1, gene2)) in gene_pairs:
                    intersection += 1
                    break

        union = len(phage1_genes) + len(phage2_genes) - intersection
        similarity = intersection/union

        print(phage1, phage2, union, intersection, similarity)
        header += '\t' + phage2
        body += '\t' + str(similarity)

    out.write(header + '\n')
    out.write(body + '\n')
    out.close()


# <editor-fold desc="main">
if len(sys.argv) != 6:
    print('Usage:', sys.argv[0], '<gene_pairs> <genes.conversion> <phages_list> <start> <end>')
    exit()

gene_pairs = load_gene_pairs(sys.argv[1])
genes = load_lines(sys.argv[2])
phages = load_lines(sys.argv[3])
start = int(sys.argv[4])
end = int(sys.argv[5])

for i in range(start, end):

    phage = phages[i].strip()

    while multiprocessing.active_children() >= multiprocessing.cpu_count():
        time.sleep(10)

    process = multiprocessing.Process(target=get_comparison, args=(gene_pairs, genes, phages, phage))
    process.start()


# def f(x):
#     return x*x
#
# if __name__ == '__main__':
#     pool = multiprocessing.Pool()
#     result = pool.apply_async(f, [10])    # evaluate "f(10)" asynchronously
#     print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
#     print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"
# </editor-fold>
