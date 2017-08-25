#!/usr/bin/python3

import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


def merge(ids):

    accessions = set()
    hosts = set()
    names = set()

    for data in ids:
        splited_data = data.split('|')

        accessions.add(splited_data[0])
        hosts.add(splited_data[1])
        names.add(splited_data[2])

    accession = '|'.join(accessions)
    host = '|'.join(hosts)
    name = '|'.join(names)

    new_id = '>{}||{}||{}'.format(accession, host, name)

    return new_id


if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<fasta>')
    exit()

fastas = list(SeqIO.parse(sys.argv[1], 'fasta'))
fastas.sort(key=lambda fasta: fasta.seq)

current_seq = ''
same_seqs = []

for i in range(len(fastas)):
    if fastas[i].seq == current_seq:
        seq = fastas[i]                     # type: SeqRecord
        same_seqs.append(seq.description)
    else:
        new_id = merge(same_seqs)
        print(new_id)
        print(current_seq)

        current_seq = fastas[i].seq
        same_seqs = [fastas[i].id]
