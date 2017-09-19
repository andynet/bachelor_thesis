#!/usr/bin/python3

import sys
import numpy as np

merged = []
for sim_file in sys.argv[1:]:
    sim = open(sim_file)
    merged.append(sim.readlines()[0])
    sim.close()

matrix = np.zeros((len(merged), len(merged)))
no_genes = set()
for i in range(len(merged)):
    data = merged[i].split('\t')[1:]
    for j in range(i, len(data)):
        value = data[j]
        if value == 'None':
            value = np.nan
            no_genes.add(i)
            matrix[i][j] = value
            matrix[j][i] = value
        else:
            matrix[i][j] = 1.0 - float(value)
            matrix[j][i] = 1.0 - float(value)

no_genes = sorted(list(no_genes))
for i, no_gene in enumerate(no_genes):
    matrix = np.delete(matrix, no_gene-i, axis=0)
    matrix = np.delete(matrix, no_gene-i, axis=1)

np.savetxt('matrix.tsv', matrix)
