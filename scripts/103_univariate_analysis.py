#!/usr/bin/python3

import sys
import numpy as np
import pandas as pd
import scipy.stats as stats

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<labels> <matrix>')
    exit()

with open(sys.argv[1]) as f:
    labels_lines = f.readlines()

matrix = pd.read_csv(sys.argv[2], sep='\t', header=None)   # type: pd.DataFrame
# matrix = pd.read_csv(sys.argv[2], sep='\t', header=0, index_col=0)

# print(len(labels_lines))
# print(matrix.shape)

for j in range(matrix.shape[1]):                 # matrix.shape[1]):

    contingency_table_00 = 0
    contingency_table_01 = 0
    contingency_table_10 = 0
    contingency_table_11 = 0

    for i in range(matrix.shape[0]):

        if labels_lines[i].split()[1] == 1:
            continue

        attacking_bacteria = int(labels_lines[i].split()[1]) == 2
        has_gene_in_cluster = int(matrix.iloc[i, j]) == 1

        if not attacking_bacteria and not has_gene_in_cluster:
            contingency_table_00 += 1

        if not attacking_bacteria and has_gene_in_cluster:
            contingency_table_01 += 1

        if attacking_bacteria and not has_gene_in_cluster:
            contingency_table_10 += 1

        if attacking_bacteria and has_gene_in_cluster:
            contingency_table_11 += 1

    data = np.array([[contingency_table_00, contingency_table_01],
                     [contingency_table_10, contingency_table_11]])

    observed = pd.DataFrame(data=data)
    observed.columns = ["has not gene from cluster", "has gene from cluster"]
    observed.index = ["does not infect", "infect"]
    # print(observed)

    chi2, p, dof, expected = stats.chi2_contingency(observed=observed)
    # print('\nCluster{} has p-value {} and expected table:'.format(j, p))

    expected = pd.DataFrame(data=expected)
    expected.columns = ["has not gene from cluster", "has gene from cluster"]
    expected.index = ["does not infect", "infect"]
    # print(expected)
    # print('--------------------------------------------------\n')

    obs = (observed.iloc[0, 0], observed.iloc[0, 1], observed.iloc[1, 0], observed.iloc[1, 1])
    exp = (expected.iloc[0, 0], expected.iloc[0, 1], expected.iloc[1, 0], expected.iloc[1, 1])
    print('Cluster{}\t{}\t{}\t{}'.format(j, p, obs, exp))


# matrix.drop(matrix.index[droplist], inplace=True)
# print(observed)
# print()
# print(stats.chi2_contingency(observed=observed))
