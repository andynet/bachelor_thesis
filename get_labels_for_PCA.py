#!/usr/bin/python3

import sys

if len(sys.argv) != 4:
    print('Usage:', sys.argv[0], '<phage_list.txt> <genomes.conversion> <marked_hosts>')
    exit()

with open(sys.argv[1]) as f:
    phages = f.readlines()

with open(sys.argv[2]) as f:
    lines = f.readlines()

with open(sys.argv[3]) as f:
    marked_hosts = f.readlines()

for phage in phages:
    phage = phage.strip()
    hosts = []

    for line in lines:
        record_phage = line.split('\t')[0].strip()
        if record_phage == phage:
            host1 = line.split('\t')[3].strip()
            host2 = line.split('\t')[4].strip()

            if host1 != 'NO_DATA':
                hosts.append(host1)
            if host2 != 'NO_DATA':
                hosts.append(host2)

    # print(phage)
    # print(list(set(hosts)))

    color = None
    for i in range(len(marked_hosts)):
        if marked_hosts[i].strip() in hosts:
            color = i

    if color is None:
        color = len(marked_hosts)

    print('{}\t{}'.format(phage, color))
