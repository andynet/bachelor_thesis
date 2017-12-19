#!/usr/bin/python3

import sys

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<complete_assembled_output> <weights.abc>')
    exit()

with open(sys.argv[1]) as f:
    lines = f.readlines()

out = open(sys.argv[2], 'w')

for line in lines:
    split_line = line.split('\t')

    gene1 = split_line[0]
    gene2 = split_line[1]

    if gene1 == gene2:
        continue

    if split_line[10] == '0.0':
        number = float('2.225074e-308')
    else:
        number = float(split_line[10])

    weight = 1/number

    out.write('{}\t{}\t{}\n'.format(gene1, gene2, weight))

out.close()
