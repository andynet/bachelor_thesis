#!/usr/bin/python3

import sys
import math

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<needle_out> <needle_tsv_out>')
    exit()

out = open(sys.argv[2], 'w')
needle = open(sys.argv[1])

first_ID = None
second_ID = None

for line in needle:

    if line[0:5] == '# 1: ':
        first_ID = line[5:].strip()

    if line[0:5] == '# 2: ':
        second_ID = line[5:].strip()

    if line[0:9] == '# Score: ':
        score = line[9:].strip()

        assert first_ID is not None, "First_ID is None"
        assert second_ID is not None, "Second_ID is None"

        if float(score) > 0.0:        # use -math.inf to record all
            record = '{}\t{}\t{}\n'.format(first_ID, second_ID, score)
            out.write(record)
            second_ID = None
            first_ID = None

needle.close()
out.close()
