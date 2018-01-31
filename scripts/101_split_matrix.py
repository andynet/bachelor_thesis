#!/usr/bin/python3

import pandas as pd
import sys
import os

if len(sys.argv) != 4:
    print('Usage', sys.argv[0], '<HOST_STRING> <QUERY> <MATRIX>')
    exit()

query = str(sys.argv[2]).lower().replace(' ', '_')
data_dir = os.path.dirname(os.path.abspath(sys.argv[3]))
query_wdir = '{}/{}'.format(data_dir, query)

if not os.path.isdir(query_wdir):
    os.mkdir(query_wdir)

with open(sys.argv[1]) as f:
    hosts_lines = f.readlines()

matrix = pd.read_csv(sys.argv[3], sep='\t', header=0, index_col=0)

print('Hosts lines: ', len(hosts_lines))
print('Matrix shape: ', matrix.shape)

has_not_host = []
has_host = []

hosts_out = open('{}/hosts.out'.format(query_wdir), 'w')
no_hosts_out = open('{}/no_hosts.out'.format(query_wdir), 'w')

for record in hosts_lines:
    phage = record.split('\t')[0]
    hosts_string = record.split('\t')[1].strip()

    if query in hosts_string:
        has_host.append(phage)
        hosts_out.write('{}\t{}\n'.format(phage, hosts_string))
    else:
        has_not_host.append(phage)
        no_hosts_out.write('{}\t{}\n'.format(phage, hosts_string))

hosts_out.close()
no_hosts_out.close()

matrix_has_host = matrix.drop(has_not_host)             # type: pd.DataFrame
matrix_has_host.to_csv('{}/matrix_host.tsv'.format(query_wdir), sep='\t')

matrix_has_not_host = matrix.drop(has_host)             # type: pd.DataFrame
matrix_has_not_host.to_csv('{}/matrix_no_host.tsv'.format(query_wdir), sep='\t')
