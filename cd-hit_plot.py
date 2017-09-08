#!/usr/bin/python3

import os
import sys
import subprocess
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<fasta>')
    exit()


def get_matrix_density_from_clstr(clstr):

    highest_clstr_num = 0
    density = 0

    for line in clstr:

        if line[0] == '>':
            density += highest_clstr_num * highest_clstr_num
            highest_clstr_num = 0
        else:
            clstr_num = int(line.split('\t')[0])
            highest_clstr_num = max(highest_clstr_num, clstr_num+1)

    return density


densities = []
percentages = []
fasta = sys.argv[1]

# with open(fasta) as f:
#     lines = f.readlines()
#     matrix_size = len(lines/2) * len(lines/2)

for i in range(100, 50, -1):

    perc = i/100
    command = 'cd-hit -c {} -d 0 -g 1 -i {} -o {}_{} -T 10'.format(perc, fasta, os.path.basename(fasta), perc)

    try:
        print(command)
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print('Finished at', perc, '%')
        break

    with open('{}_{}.clstr'.format(os.path.basename(fasta), perc)) as f:
        lines = f.readlines()
        density = get_matrix_density_from_clstr(lines)
        densities.append(density)
        percentages.append(perc)

plt.figure()
plt.plot(percentages, densities)
plt.show()
plt.savefig(os.path.basename(fasta) + '.figure.png')


