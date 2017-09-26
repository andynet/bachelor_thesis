#!/usr/bin/python3

import sys
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.collections


def load_labels(labels_file):
    with open(labels_file) as f:
        lines = f.readlines()

    labels = []
    for line in lines:
        labels.append(int(line.strip()))

    return labels


# def onpick(event):      # type:matplotlib.backend_bases.
#
#     print('you pressed', event.button, event.xdata, event.ydata, event.artist, event.ind)


if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<distances_matrix> <labels>')
    exit()

data = pd.read_csv(sys.argv[1], sep='\t', header=None)
y = load_labels(sys.argv[2])
color_map = plt.cm.get_cmap('Set1')
# print(y)

fig = plt.figure(1, figsize=(8, 6))
# ax = Axes3D(fig, elev=-150, azim=110)
ax = plt
X_reduced = PCA(18).fit_transform(data)

pca = PCA(18)
pca.fit(data)
print(pca.explained_variance_ratio_)

ax.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap=color_map, edgecolor='k', s=100, picker=True)

### for 3D plot use this
# ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=y, cmap=color_map, edgecolor='k')
# ax.set_title("First three PCA directions")
# ax.set_xlabel("1st eigenvector")
# ax.w_xaxis.set_ticklabels([])
# ax.set_ylabel("2nd eigenvector")
# ax.w_yaxis.set_ticklabels([])
# ax.set_zlabel("3rd eigenvector")
# ax.w_zaxis.set_ticklabels([])

# fig.canvas.mpl_connect('pick_event', onpick)

# for label, x, y in zip(['phage']*len(X_reduced), X_reduced[:, 0], X_reduced[:, 1]):
#     ax.annotate(label, xy=(x, y), xytext=(x, y),
#                 # textcoords='offset points', ha='right', va='bottom',
#                 # bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
#                 # arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
#                 arrowprops=dict(arrowstyle='->')
#                 )


plt.show()
exit()
