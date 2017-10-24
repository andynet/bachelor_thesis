#!/usr/bin/python3

import sys
import subprocess
from Bio import SeqIO

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<genes.fasta> <tmp_dir>')
    exit()

script_dir = '/'.join(sys.argv[0].split('/')[0:-1])
original_fasta = sys.argv[1]
tmp_dir = sys.argv[2]

fa_list = list(SeqIO.parse(original_fasta, 'fasta'))
max_records = len(fa_list)

for record_num in range(18010, max_records):     # with range(0, max_records) needs around 2TB data on disk

    gene_out = '{}/gene_{}.fasta'.format(tmp_dir, record_num)
    genes_out = '{}/genes_{}-{}.fasta'.format(tmp_dir, record_num, max_records-1)

    command1 = 'less {} | tail -n {} > {}'.format(original_fasta, (max_records-record_num)*2, genes_out)
    command2 = 'less {} | head -n {} > {}'.format(genes_out, 2, gene_out)

    needle_out = '{}/{:0>6}_to_{}-{}.needle'.format(tmp_dir, record_num, record_num, max_records-1)
    needle_tsv_out = '{}/{:0>6}_to_{}-{}.needle.tsv'.format(tmp_dir, record_num, record_num, max_records-1)

    needle_command = 'needle -asequence {} ' \
                     '       -bsequence {} ' \
                     '       -outfile {}   ' \
                     '       -gapopen 10.0 ' \
                     '       -gapextend 0.5' \
                     '       -endweight Y  ' \
                     '       -endopen 10.0 ' \
                     '       -endextend 0.5' \
                     '       -aformat score'.format(gene_out, genes_out, needle_out)

    parse_needle_command = '{}/parse_needle.py {} {}'.format(script_dir, needle_out, needle_tsv_out)
    save_space_command = 'gzip {}; rm {} {} {}'.format(needle_tsv_out, gene_out, genes_out, needle_out)

    qsub_command = 'echo "{}; {}; {}; {}; {};" ' \
                   '| qsub -l thr=1 -cwd -N ga{}'.format(command1, command2, needle_command, parse_needle_command,
                                                              save_space_command, record_num)
    subprocess.call(qsub_command, shell=True)



