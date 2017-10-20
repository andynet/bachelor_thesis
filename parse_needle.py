#!/usr/bin/python3

import sys
import math

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<needle_out> <needle_tsv_out>')
    exit()

out = open(sys.argv[2], 'w')

with open(sys.argv[1]) as f:
    lines = f.readlines()

for line in lines:

    if line == '\n':
        break

    first_ID = line.split()[0]
    second_ID = line.split()[1]
    score = line.split()[3].strip().strip('()')

    if float(score) > 0.0:        # use -math.inf to record all
        record = '{}\t{}\t{}\n'.format(first_ID, second_ID, score)
        out.write(record)

out.close()
