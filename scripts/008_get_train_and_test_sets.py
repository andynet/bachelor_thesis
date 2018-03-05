#!/usr/bin/python3

import sys
import random


def create_genes_dict(genes_conv):

    genes_dict = dict()
    with open(genes_conv) as f:
        lines = f.readlines()

    for line in lines:
        gene, phage = line.split()[0:2]
        if phage not in genes_dict:
            genes_dict[phage] = [gene]
        else:
            genes_dict[phage].append(gene)

    return genes_dict


if len(sys.argv) != 6:
    print('Usage:', sys.argv[0], '<abc_file> <annotated_genes_conversion> <hosts> <our_selection> <train_perc>')
    print('Example:', sys.argv[0], './007_complete_global_alignment.abc ./005_annotated.genes.conversion ./101_hosts'
                                   'mycobac,strepto,escheri,gordoni,pseudom,arthrob,lactoco,staphyl 0.8')
    exit()

with open(sys.argv[1]) as f:
    abc_lines = f.readlines()

phage_to_genes = create_genes_dict(sys.argv[2])

with open(sys.argv[3]) as f:
    hosts_lines = f.readlines()

selected_hosts = sys.argv[4].split(',')
train_perc = float(sys.argv[5])


host_dict = dict()

for host in selected_hosts:
    host_dict[host] = []

for line in hosts_lines:

    phage = line.split()[0]

    for host in selected_hosts:
        if host in line:
            host_dict[host].append(phage)
            break

train_set = set()
test_set = set()

for host in host_dict:

    phage_list = host_dict[host]
    random.shuffle(phage_list)
    train_num = int(len(phage_list)*train_perc)
    print(host, train_num, len(phage_list))

    train_set = train_set | set(phage_list[:train_num])
    test_set = test_set | set(phage_list[train_num:])

# create sets of genes
train_set_genes = set()
test_set_genes = set()

for phage in train_set:
    try:
        genes = phage_to_genes[phage]
        train_set_genes = train_set_genes | set(genes)
    except KeyError:
        print('Phage {} has no genes in dictionary.'.format(phage))


for line in abc_lines:
    gene1, gene2 = line.split()[0:2]
    if gene1 in train_set_genes and gene2 in train_set_genes:
        print(line, end='')

# TODO 