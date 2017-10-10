#!/usr/bin/python3

import sys

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<needle_out> <needle_tsv_out>')
    exit()

out = open(sys.argv[2], 'w')
needle = open(sys.argv[1])
for line in needle:

    if line[0:5] == '# 1: ':
        first_ID = line[5:].strip()

    if line[0:5] == '# 2: ':
        second_ID = line[5:].strip()

    if line[0:10] == '# Length: ':
        length = line[10:].strip()

    if line[0:12] == '# Identity: ':
        identity = line[12:].strip()

    if line[0:14] == '# Similarity: ':
        similarity = line[14:].strip()

    if line[0:8] == '# Gaps: ':
        gaps = line[8:].strip()

    if line[0:9] == '# Score: ':
        score = line[9:].strip()
        record = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{:.4f}\n'.format(first_ID, second_ID, length, identity,
                                                               similarity, gaps, score, float(score)/float(length))
        out.write(record)

needle.close()
out.close()
