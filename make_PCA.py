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
    y = []
    for line in lines:
        labels.append(line.strip())
        y.append(int(line.split('\t')[1].strip()))

    return labels, y


labels, y = load_labels(sys.argv[2])


def on_pick(event):      # type:matplotlib.backend_bases.
    global labels
    print('you pressed', event.ind)
    for ind in event.ind:
        print(labels[ind])



if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<distances_matrix> <labels>')
    exit()

data = pd.read_csv(sys.argv[1], sep='\t', header=None)
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

### toto funguje
# #!/usr/bin/python3
# """
# compute the mean and stddev of 100 data sets and plot mean vs stddev.
# When you click on one of the mu, sigma points, plot the raw data from
# the dataset that generated the mean and stddev
# """
# import numpy as np
# import matplotlib.pyplot as plt
#
# xs = [1,2,3,4,5]
# ys = [1,2,3,4,5]
# label = ['a', 'b', 'c', 'd', 'e']
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_title('click on point to plot time series')
# line, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance
#
# def on_pick(event):
#     global label
#     thisline = event.artist
#     xdata, ydata = thisline.get_data()
#     ind = event.ind
#     print('on pick line:', label[ind[0]])
#
cid = fig.canvas.mpl_connect('pick_event', on_pick)
#
# plt.show()

plt.show()
exit()
