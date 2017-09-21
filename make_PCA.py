#!/usr/bin/python3

import sys
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<distances_matrix>')
    exit()

data = pd.read_csv(sys.argv[1], sep='\t', header=None)
y = [[0]*len(data)]
# pca = PCA().fit(data)    # type: PCA
# pca_2d = pca.transform(data)
# print(pca.explained_variance_ratio_)
# print(pca_2d)

fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
X_reduced = PCA(n_components=3).fit_transform(data)
ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=y,
           cmap=plt.cm.Set1, edgecolor='k', s=40)
ax.set_title("First three PCA directions")
ax.set_xlabel("1st eigenvector")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("2nd eigenvector")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("3rd eigenvector")
ax.w_zaxis.set_ticklabels([])
plt.show()
exit()
