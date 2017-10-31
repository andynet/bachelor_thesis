#!/usr/bin/python3

import os
import sys
import math
import subprocess
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

if len(sys.argv) != 4:
    print('Usage:', sys.argv[0], '<complete_assembled_output.blast> <genes.fasta> <tmp_dir>')
    print('Example:', sys.argv[0], '/data/projects/kimona/data/CrocoBLAST_2/complete_assembled_output '
                                   '/data/projects/kimona/data/03-annotation/PROKKA_2017-08-31.genes.fasta '
                                   '/data/projects/kimona/data/global_alignment')
    exit()

script_dir = '/'.join(sys.argv[0].split('/')[0:-1])
blast_output = sys.argv[1]
original_fasta = sys.argv[2]
tmp_dir = sys.argv[3]

split_fastas = '{}/split_fastas'.format(tmp_dir)

if not os.path.isdir(split_fastas):

    os.mkdir(split_fastas)
    fa_list = list(SeqIO.parse(original_fasta, 'fasta'))

    for fasta in fa_list:

        fasta = fasta   # type: SeqRecord

        file = '{}/{}.fa'.format(split_fastas, fasta.id)
        ID = '>{}\n'.format(fasta.id)
        seq = '{}\n'.format(str(fasta.seq))

        fasta_file = open(file, 'w')
        fasta_file.write(ID)
        fasta_file.write(seq)
        fasta_file.close()
        # print('Fasta file {} completed.'.format(fasta_file.name))

    print('Fasta files correctly prepared.')

with open(blast_output) as f:
    lines = f.readlines()

lines_num = len(lines)
files_num = 80000       # this number was established artificially based on number of threads on our cluster
records_per_file = math.ceil(lines_num/files_num)

head_of_script = '#!/bin/bash\n\n'
tail_of_script = 'cat {} > {:0>5}.abc.gz; rm {};'

script = head_of_script
created_files = ''

for i, line in enumerate(lines):

    if i % records_per_file == 0:

        number = int(i/records_per_file)

        if number != 0:

            script += tail_of_script.format(created_files, number, created_files)
            script_name = 'tmp_script_{}.sh'.format(number)

            script_out = open(script_name, 'w')
            script_out.write(script)
            script_out.close()

            qsub_command = 'echo "bash {0}; rm {0}" | qsub -l thr=1 -cwd -N {0}'.format(script_name)
            # print(qsub_command)
            subprocess.call(qsub_command, shell=True)

            script = head_of_script
            created_files = ''

    seq1 = line.split('\t')[0].strip()
    seq2 = line.split('\t')[1].strip()

    seq1_file = '{}/{}.fa'.format(split_fastas, seq1)
    seq2_file = '{}/{}.fa'.format(split_fastas, seq2)

    needle_out = '{}/{}_to_{}.needle'.format(tmp_dir, seq1, seq2)
    needle_tsv_out = '{}/{}_to_{}.needle.tsv'.format(tmp_dir, seq1, seq2)

    needle_command = 'needle -asequence {} ' \
                     '       -bsequence {} ' \
                     '       -outfile {}   ' \
                     '       -gapopen 10.0 ' \
                     '       -gapextend 0.5' \
                     '       -endweight Y  ' \
                     '       -endopen 10.0 ' \
                     '       -endextend 0.5' \
                     '       -aformat score'.format(seq1_file, seq2_file, needle_out)

    parse_needle_command = '{}/parse_needle.py {} {}'.format(script_dir, needle_out, needle_tsv_out)
    save_space_command = 'gzip {}; rm {}'.format(needle_tsv_out, needle_out)

    script += '{}; {}; {};\n'.format(needle_command, parse_needle_command, save_space_command)
    created_files += '{}.gz '.format(needle_tsv_out)




