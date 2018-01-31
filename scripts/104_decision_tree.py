#!/usr/bin/python3

from sklearn.feature_selection import VarianceThreshold
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import pandas as pd
import graphviz
import sys
import os

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

# print(features)
# print(len(labels), features.shape)

selection = VarianceThreshold(threshold=(.95 * (1 - .95)))
mask = selection.fit(features).get_support(indices=True)
selected_features = features[mask]

# print(selected_features.shape)
# print(selected_features)

# labels are natural numbers - 0 for first #line of label, 1 for second #line of labels, 2 for

clf = DecisionTreeClassifier()
clf.fit(selected_features, labels)

# visualizing of tree
dot_data = tree.export_graphviz(clf, out_file=None, feature_names=selected_features.columns)
graph = graphviz.Source(dot_data)
graph.format = 'pdf'
graph.render('{}/tree'.format(data_dir))
