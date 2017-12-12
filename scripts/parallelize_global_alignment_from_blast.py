#!/usr/bin/python3

from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import subprocess
import math
import sys
import os
import re


def create_fasta_dir(directory, fasta):

    os.mkdir(directory)
    fa_list = list(SeqIO.parse(fasta, 'fasta'))

    for record in fa_list:      # type: SeqRecord

        file = '{}/{}.fa'.format(directory, record.id)
        seq_id = '>{}\n'.format(record.id)
        seq = '{0!s}\n'.format(record.seq)

        out = open(file, 'w')
        out.write(seq_id)
        out.write(seq)
        out.close()


if len(sys.argv) != 4:
    print('Usage:', sys.argv[0], '<blast_output> <genes.fasta> <tmp_dir>')
    exit()

script_dir = sys.path[0]
blast_output = sys.argv[1]
original_fasta = sys.argv[2]
tmp_dir = sys.argv[3]

split_fastas = '{}/split_fastas'.format(tmp_dir)

if not os.path.isdir(split_fastas):
    create_fasta_dir(split_fastas, original_fasta)
    print('Fasta files correctly prepared.')

with open(blast_output) as f:
    lines = f.readlines()

lines_num = len(lines)
files_num = 80000       # this number was established artificially based on number of threads on our cluster
records_per_file = math.ceil(lines_num/files_num)

script_template = '#!/bin/bash\n'                                                                   \
                  '\n{body}\n'                                                                      \
                  '\ncat {list_of_tsv} > {fileno:0>5}.abc; rm {list_of_tsv}; rm {list_of_needle}\n'

created_needle_files = []
created_needle_tsv_files = []
commands = []

for i, line in enumerate(lines):

    seq1 = line.split('\t')[0].strip()
    seq2 = line.split('\t')[1].strip()

    seq1_file = '{}/{}.fa'.format(split_fastas, seq1)
    seq2_file = '{}/{}.fa'.format(split_fastas, seq2)

    needle_out = '{}/{}_to_{}.needle'.format(tmp_dir, seq1, seq2)
    needle_tsv_out = '{}/{}_to_{}.needle.tsv'.format(tmp_dir, seq1, seq2)

    created_needle_files.append(needle_out)
    created_needle_tsv_files.append(needle_tsv_out)

    needle_command = 'needle -asequence {} ' \
                     '       -bsequence {} ' \
                     '       -outfile {}   ' \
                     '       -gapopen 10.0 ' \
                     '       -gapextend 0.5' \
                     '       -endweight Y  ' \
                     '       -endopen 10.0 ' \
                     '       -endextend 0.5' \
                     '       -aformat score'.format(seq1_file, seq2_file, needle_out)

    parse_needle_command = '{}/parse_needle.py {}' \
                           '                   {}'.format(script_dir, needle_out, needle_tsv_out)

    commands.append(re.sub(' +', ' ', needle_command))
    commands.append(re.sub(' +', ' ', parse_needle_command))

    if i % records_per_file == 0:

        number = int(i/records_per_file)

        if number == 0:
            continue

        script = script_template.format(body='\n'.join(commands), list_of_tsv=' '.join(created_needle_tsv_files),
                                        fileno=number, list_of_needle=' '.join(created_needle_files))
        script_name = '{}/tmp_script_{}.sh'.format(tmp_dir, number)

        script_out = open(script_name, 'w')
        script_out.write(script)
        script_out.close()

        created_needle_files = []
        created_needle_tsv_files = []
        commands = []

        qsub_command = 'echo "bash {0}; rm {0}" | qsub -l thr=1 -cwd -N glal_{1}'.format(script_name, number)
        # print(qsub_command)
        subprocess.call(qsub_command, shell=True)




