#!/usr/bin/python3

import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<genomes.fasta> <tag.predict>')
    exit()

fasta = list(SeqIO.parse(sys.argv[1], 'fasta'))

with open(sys.argv[2]) as f:
    lines = f.readlines()

current_fasta = None
i = 0

for line in lines:
    if line[0] == '>':
        current_fasta = fasta[i]        # type: SeqRecord
        i += 1
        print('Current fasta is', current_fasta.description)
    else:
        split_line = line.split()

        print(split_line)

        name = split_line[0]
        start = int(split_line[1])
        stop = int(split_line[2])

        gene_description = current_fasta.description + '|{}|{}|{}|{}'.format(name, start, stop, '')

        if start < stop:
            gene = current_fasta.seq[start:stop]
        else:
            gene = current_fasta.seq[start:stop:-1]

        print(gene_description)
        print(gene)



