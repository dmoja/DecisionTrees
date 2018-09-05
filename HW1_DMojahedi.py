from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from graphviz import Digraph
import graphviz


# Determining gini coefficient.
def gini(data_set, feature_location, feature_value):
    conditional_boolean = data_set[:, feature_location] == feature_value
    relevant_rows = data_set[conditional_boolean, :]
    print(1 - math.pow((np.count_nonzero(relevant_rows[:, 6] == 'acc') / relevant_rows.shape[0]), 2) - math.pow(
        (np.count_nonzero(relevant_rows[:, 6] == 'unacc') / relevant_rows.shape[0]), 2))


df = pd.read_csv('car.training.csv', header=None)
data = df.iloc[:, :].values



parent_node = 'null'  # Boolean value to determine if node is root.
node = {}  # Node array
node_iterator = 0  # A value for iterating node index values.


# while True:  # Keep looping until lowest gini coefficient reaches a certain value.
#
feature_values = [0] * (data.shape[1] - 1)
#     # The minimum gini coefficient observed in data set during each run of the analysis
#     minimum_gini = 100
#     # Counting the number of instances within one feature where the minimum gini coefficient is observed.
#     min_count = [0] * (data.shape[1] - 1)
#     min_count_feature_values = [None]  # The feature values (within the same column) with the lowest gini coefficient.
#     min_count_feature_values.clear()
#     relevant_feature = -1  # Feature in which the lowest gini coefficient is located.
#     remaining_features = [None]  # Used to hold the features values within column with higher gini coefficient.
#     remaining_features.clear()
#
for column_location in range(0, data.shape[1] - 1):
    feature_values[column_location] = np.unique(data[:, column_location])  # Getting unique values from each column.
    for featured_value in feature_values:
        gini(data, column_location, featured_value)
#             # Checking if feature value gini coefficient is lowest one in data set.
#             if gini(data, column_location, featured_value) < minimum_gini:
#                 min_count[column_location] = 1  # Counting number of feature values within column that share lowest gini coefficient.
#                 # If gini coefficient is the lowest one, the label as such for future comparisons.
#                 minimum_gini = gini(data, column_location, featured_value)
#                 min_count_feature_values.clear()  # Clear out any previous feature values that have been superseded.
#                 min_count_feature_values.append(featured_value)  # Add new feature value with lowest gini.
#             # Checking if feature value's gini coefficient same as column's lowest gini coefficient.
#             elif gini(data, column_location, featured_value) == minimum_gini and min_count[column_location] > 0:
#                 min_count[column_location] += 1
#                 min_count_feature_values.append(featured_value)
#
#             if min_count[column_location] > 0:
#                 relevant_feature = column_location  # Record feature index value where lowest gini coefficient is located.
#
#         # This breaks the loop if the gini coefficient exceeds the given value in order to avoid overfitting.
#         if minimum_gini > 0.35:
#             break
#
#         print(minimum_gini)
#
#     # remaining_features = [z for z in feature_values[relevant_feature] if z not in min_count_feature_values]
#     #
#     # if parent_node == 'null':
#     #     node_name = "Column", relevant_feature
#     #     root = Node(node_name)
#     #     parent_node = min_count_feature_values
#     # else:
#     #     if (node_iterator % 2 == 0):
#     #         node["string{0}".format(node_iterator)] = Node(min_count_feature_values, parent=parent_node)
#     #     else:
#     #         node["string{0}".format(node_iterator)] = Node(remaining_features, parent=parent_node)
#     #     node_iterator += 1
#
#     data = pd.DataFrame(data)  # Convert numpy array to pandas Dataframe to more easily remove rows.
#
#     for mean_count_feature_value in min_count_feature_values:  # Remove rows which have been added to decision tree.
#         data = data.drop(index=mean_count_feature_value)
#
#
#     # print(gini_min_count, min_count_feature_values, relevant_feature)
#     minimum_gini = 100
# print(RenderTree(root, style=DoubleStyle))
