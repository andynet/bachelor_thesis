#!/usr/bin/python3

# TODO:
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sys
import os


def on_pick(event):

    global labels

    print('you pressed', event.ind)

    for ind in event.ind:
        print(labels[ind])


if len(sys.argv) < 5 or len(sys.argv) % 2 != 1:
    print('Usage:', sys.argv[0], '<label> <matrix> <label> <matrix>...')
    exit()

data_dir = os.path.dirname(os.path.abspath(sys.argv[1]))

labels = []
matrices = []

for i in range(len(sys.argv)//2):
    with open(sys.argv[i*2+1]) as f:
        labels += [i]*len(f.readlines())

    matrices.append(pd.read_csv(sys.argv[i*2+2], sep='\t', header=0, index_col=0))

# print('Labels:', labels)
# print('Matrices:', matrices)

# merge matrices
features = pd.concat(matrices)

color_map = mpl.colors.ListedColormap([[0.5, 0.5, 0.5], [0.95, 0.95, 0.95], [1.0, 0.0, 0.0]])

fig = plt.figure()
X_reduced = PCA(18).fit_transform(features)

pca = PCA(18)
pca.fit(features)
print(pca.explained_variance_ratio_)

plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=labels, cmap=color_map, edgecolor='k', s=100, picker=True)
cid = fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()