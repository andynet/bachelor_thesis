#!/usr/bin/python3

import sys
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib as mpl


def load_labels(labels_file):

    with open(labels_file) as f:
        lines = f.readlines()

    labels = []
    y = []

    for line in lines:
        labels.append(line.strip())
        y.append(int(line.split('\t')[1].strip()))

    return labels, y


def on_pick(event):

    global labels

    print('you pressed', event.ind)

    for ind in event.ind:
        print(labels[ind])


if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<distances_matrix> <labels>')
    exit()

data = pd.read_csv(sys.argv[1], sep='\t', header=None)
labels, y = load_labels(sys.argv[2])
color_map = mpl.colors.ListedColormap([[0.5, 0.5, 0.5], [0.95, 0.95, 0.95], [1.0, 0.0, 0.0]])

fig = plt.figure()
X_reduced = PCA(18).fit_transform(data)

pca = PCA(18)
pca.fit(data)
print(pca.explained_variance_ratio_)

plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap=color_map, edgecolor='k', s=100, picker=True)
cid = fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()
exit()
