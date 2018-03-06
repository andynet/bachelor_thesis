#!/usr/bin/python3

import sys
import random

if len(sys.argv) != 8:
    print('Usage:', sys.argv[0], '005_annotated.genes.conversion 005_annotated.genes.fasta',
                                 '003_deduplicated.genomes.conversion 003_deduplicated.genomes.fasta',
                                 '101_hosts',
                                 'mycobac,strepto,escheri,gordoni,pseudom,arthrob,lactoco,staphyl',
                                 '0.8')
    exit()

train_set = set()
other_set = set()

with open(sys.argv[5]) as f:
    lines = f.readlines()

selected_hosts = sys.argv[6].split(',')
train_ratio = float(sys.argv[7])

for line in lines:
    phage, host_string = line.split()

    select = False
    for host in selected_hosts:
        if host in host_string:
            select = True

    if select:
        train_set.add(phage)
    else:
        other_set.add(phage)

train_set_count = int(len(train_set) * train_ratio)

train_list = list(train_set)
random.shuffle(train_list)

train_set = set(train_list[:train_set_count])
test_set = set(train_list[train_set_count:])

print('Train set: {}, Test set: {}, Other set: {}'.format(len(train_set), len(test_set), len(other_set)))
