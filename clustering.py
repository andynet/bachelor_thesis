#!/usr/bin/python3
# this file is not planned to be used in final work

import sys
import nltk
import random
from Bio import SeqIO

bases = ('A', 'C', 'T', 'G')
size = 100
seq_old = ''

for j in range(10):
    seq = ''
    for i in range(size):
        seq += random.choice(bases)

    dist = nltk.edit_distance(seq, seq_old)
    print(seq, seq_old, dist, dist/size, sep='\n')
    seq_old = seq


txt1 = 'AAA'
txt2 = 'ATT'
