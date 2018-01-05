#!/usr/bin/python3
# NOT USED IN MAIN PIPELINE

import sys
import matplotlib.pyplot as plt
from collections import Counter

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<mcl.clstr>')
    exit()

with open(sys.argv[1]) as f:
    lines = f.readlines()

counts = []
densities = []

for line in lines:
    counts.append(len(line.split()))

c = Counter(counts)
print(c)

x_axes = range(1, max(counts)+1)

for i in x_axes:
    densities.append(c[i])

width = 1
plt.bar(x_axes, densities, width)
plt.show()

