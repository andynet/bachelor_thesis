#!/usr/bin/python3

import sys
import datetime
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


def safe_get_qualifier(feature, key, default_value='NO_DATA'):
    try:
        return ';'.join(feature.qualifiers[key])
    except KeyError:
        return default_value


genes_output_file = 'PROKKA_' + str(datetime.date.today()) + '.genes.fasta'
genes_conversion_file = 'PROKKA_' + str(datetime.date.today()) + '.genes.conversion'
genes_output = open(genes_output_file, 'w')
genes_conversion = open(genes_conversion_file, 'w')

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<gbk_file>')
    exit()

gb_list = list(SeqIO.parse(sys.argv[1], 'genbank'))
gene_num = 30000000

for gb in gb_list:      # type: SeqRecord

    fasta_id = gb.id

    for feature in gb.features:
        if feature.type == 'CDS':
            gene_id = 'gene{:0>8}'.format(gene_num)
            gene_num += 1

            gene_seq = safe_get_qualifier(feature, 'translation')

            genes_output.write('>' + gene_id + '\n')
            genes_output.write(gene_seq + '\n')

            protein_id = safe_get_qualifier(feature, 'protein_id')
            product = safe_get_qualifier(feature, 'product')
            note = safe_get_qualifier(feature, 'note')

            genes_conversion.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(gene_id, fasta_id, protein_id,
                                                                     feature.location, product, note))

genes_output.close()
genes_conversion.close()
