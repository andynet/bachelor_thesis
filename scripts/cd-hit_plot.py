#!/usr/bin/python3

import os
import sys
import subprocess
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<fasta>')
    exit()

counts = []
percentages = []
fasta = sys.argv[1]

for i in range(100, 50, -1):

    perc = i/100
    command = 'cd-hit -c {} -d 0 -g 1 -i {} -o {}_{}.fa -T 10'.format(perc, fasta, os.path.basename(fasta), perc)

    try:
        print(command)
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print('Finished at', perc, '%')
        break

    with open('{}_{}.fa'.format(os.path.basename(fasta), perc)) as f:
        lines = f.readlines()
        count = len(lines)/2
        print(count)

        counts.append(count)
        percentages.append(perc)

plt.figure()
plt.plot(percentages, counts)
plt.show()
plt.savefig(os.path.basename(fasta) + '.figure.png')


