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

matrix = pd.read_csv(sys.argv[2])   # type: pd.DataFrame

print(len(labels_lines))
print(matrix.shape)

#
# data = np.array([[1, 2], [3, 4]])
# observed = pd.DataFrame(data=data)
# observed.columns = ["in_cluster", "not_in_cluster"]
# observed.index = ["has_host", "without_host"]
#
# print(observed)
# print()
# print(stats.chi2_contingency(observed=observed))
