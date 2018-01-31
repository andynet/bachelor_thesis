#!/usr/bin/python3

import sys

if len(sys.argv) != 4:
    print('Usage:', sys.argv[0], '<phage_list.txt> <genomes.conversion> <searched>')
    exit()

with open(sys.argv[1]) as f:
    phages = f.readlines()

with open(sys.argv[2]) as f:
    lines = f.readlines()

searched_term = sys.argv[3]

for phage in phages:
    phage = phage.strip()
    hosts = []

    for line in lines:
        record_phage = line.split('\t')[0].strip()
        if record_phage == phage:
            host1 = line.split('\t')[3].strip().strip('\'')
            host2 = line.split('\t')[4].strip().strip('\'')

            if host1 != 'NO_DATA':
                hosts.append(host1)
            if host2 != 'NO_DATA':
                hosts.append(host2)

    if len(hosts) != 0:
        host_line = ';'.join(list(set(hosts)))
    else:
        host_line = 'NO_HOST'

    color = 0
    if host_line == 'NO_HOST':
        color = 1
    if searched_term in host_line:
        color = 2

    print('{}\t{}\t{}'.format(phage, color, host_line))
