#!/usr/bin/python3

import sys
import argparse
import subprocess
from Bio import SeqIO

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<genes.fasta> <tmp_dir>')
    exit()

original_fasta = sys.argv[1]
tmp_dir = sys.argv[2]

fa_list = list(SeqIO.parse(original_fasta, 'fasta'))
max_records = 10    # len(fa_list)  # TODO: is it possible to run at once?
step = 25

for record_num in range(0, max_records):

    gene_out = '{}/gene_{}.fasta'.format(tmp_dir, record_num)

    if record_num % step == 0:
        genes_out = '{}/genes_{}-{}.fasta'.format(tmp_dir, record_num, max_records-1)

        command1 = 'less {} | tail -n {} > {}'.format(original_fasta, (max_records-record_num)*2, genes_out)
        subprocess.call(command1, shell=True)
        print(command1)

    command2 = 'less {} | head -n {} | tail -n 2 > {}'.format(genes_out, (record_num % step + 1)*2, gene_out)
    subprocess.call(command2, shell=True)
    print(command2)

    needle_out = '{}/{}_to_{}-{}.needle'.format(tmp_dir, record_num, record_num - (record_num % step), max_records-1)
    needle_tsv_out = '{}/{}_to_{}-{}.needle.tsv'.format(tmp_dir, record_num, record_num - (record_num % step), max_records-1)

    needle_command = 'needle -asequence {} ' \
                     '       -bsequence {} ' \
                     '       -outfile {}   ' \
                     '       -gapopen 10.0 ' \
                     '       -gapextend 0.5'.format(gene_out, genes_out, needle_out)

    parse_needle_command = './parse_needle.py {} {}'.format(needle_out, needle_tsv_out)

    save_space_command = 'gzip {}; rm {}; rm {}; touch {}/completed_{}'.format(needle_tsv_out, needle_out,
                                                                               gene_out, tmp_dir, record_num)

    qsub_command = 'echo "{}; {}; {};" | qsub -l thr=1 -cwd -N glal{}'.format(needle_command, parse_needle_command,
                                                                              save_space_command, record_num)
    subprocess.call(qsub_command, shell=True)
    print(qsub_command)



