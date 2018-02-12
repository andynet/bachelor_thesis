#!/usr/bin/python3

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import pandas as pd
import sys
import os


def get_hosts(file):

    with open(file) as f:
        lines = f.readlines()

    hosts = dict()
    for line in lines:
        phage = line.split()[0]
        host = line.split()[1]

        hosts[phage] = host

    return hosts


def on_pick(event):

    global matrices
    global groups
    global hosts

    print('--------------------------------------------------------------------------------')
    gind = groups.index(event.artist)

    for eind in event.ind:
        phage = matrices[gind].index[eind]
        print('{}\t{}'.format(phage, hosts[phage]))


if len(sys.argv) < 4 or len(sys.argv) % 2 != 0:
    print('Usage:', sys.argv[0], '<hosts> <label> <matrix> <label> <matrix>...')
    exit()

data_dir = os.path.dirname(os.path.abspath(sys.argv[1]))

labels = [0]
matrices = []
number_of_records = []

for i in range(0, len(sys.argv)//2 - 1):
    with open(sys.argv[i*2+2]) as f:
        labels.append(labels[-1]+len(f.readlines()))

    matrix = pd.read_csv(sys.argv[i*2+3], sep='\t', header=0, index_col=0)
    matrices.append(matrix)

features = pd.concat(matrices)
hosts = get_hosts(sys.argv[1])

pca_comps = PCA(8)
pca_comps.fit(features)
print(pca_comps.explained_variance_ratio_)
pca = pca_comps.transform(features)

cmap = plt.get_cmap('jet')
norm = Normalize(vmin=0, vmax=len(labels))

fig = plt.figure()

groups = []
for i in range(1, len(labels)):
    group = plt.scatter(pca[labels[i-1]:labels[i], 5], pca[labels[i-1]:labels[i], 7],
                        c=[cmap(norm(i))]*(labels[i]-labels[i-1]), edgecolor='k', s=50, picker=True, alpha=0.3,
                        label=sys.argv[i*2])
    groups.append(group)

cid = fig.canvas.mpl_connect('pick_event', on_pick)
plt.legend(loc='best', fontsize='x-small')
plt.show()

# generate all graphs
# for j in range(8):
#     for k in range(8):
#
#         fig = plt.figure()
#         groups = []
#
#         for i in range(1, len(labels)):
#             group = plt.scatter(pca[labels[i-1]:labels[i], j], pca[labels[i-1]:labels[i], k],
#                                 c=[cmap(norm(i))]*(labels[i]-labels[i-1]), edgecolor='k', s=50, picker=True,
#                                 alpha=0.3, label=sys.argv[i*2])
#             groups.append(group)
#
#         plt.legend(loc='best', fontsize='x-small')
#         fig.savefig('104_PC{}_PC{}.png'.format(j, k), dpi=300)
#         plt.close(fig)

# plt.figure()
# plt.plot(pca_comps.components_[0], '.')
# plt.show()
