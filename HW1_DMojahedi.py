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
    relevant_rows = data_set[data_set[:, feature_location] == feature_value]
    return (1 - math.pow((np.count_nonzero(relevant_rows[:, 6] == 'acc') / relevant_rows.shape[0]), 2) - math.pow(
            (np.count_nonzero(relevant_rows[:, 6] == 'unacc') / relevant_rows.shape[0]), 2))


def row_finder(lab_finder, lab_row_value):
    for lab_iterator in range(0, len(lab_finder)):
        if lab_finder[lab_iterator]:
            lab_row_value.append(lab_iterator)
    return lab_row_value


def label_extractor(data_set, used_feature_values, used_column_location):
    dominant_label_values = []
    for used_feature_value in used_feature_values:
        acc_count = 0
        unacc_count = 0
        label_row_value = []
        label_finder = data_set[:, used_column_location] == [used_feature_value]
        label_row_value = row_finder(label_finder, label_row_value)

        for row in label_row_value:
            if data_set[row, 6] == "acc":
                acc_count += 1
            elif data_set[row, 6] == "unacc":
                unacc_count += 1

        if acc_count > unacc_count:
            dominant_label_values.append("acc")
        else:
            dominant_label_values.append("unacc")

    return dominant_label_values


def label_predictor(test_data_set, used_feature_values, test_column_location, predicted_set, predicted_label):
    test_label_values = []
    for used_feature_value in used_feature_values:
        label_finder = test_data_set[:, test_column_location] == [used_feature_value]
        test_label_values = row_finder(label_finder, test_label_values)
    for test_label_value in test_label_values:
        predicted_set[test_label_value] = predicted_label
    return predicted_set


def extract_used_features(data_set, used_feature_values, used_column_location):
    for used_feature_value in used_feature_values:
        data_set = data_set[data_set[:, used_column_location] != [used_feature_value]]
        return data_set

# def decision_array(left_branch, right_branch, used_feature_values, used_column_location, other_feature_values, label):
#     if len(left_branch) == 0:
#         for used_feature_value in used_feature_values:
#             left_branch.append([0, used_feature_value, used_column_location, label])
#     else:
#         for lb_feat_count in range(0, len(used_feature_values)):
#             for copy_ofv in range(1, len(other_feature_values[len(other_feature_values) - 1])):
#                 left_branch.append(other_feature_values[len(other_feature_values) - copy_ofv].copy())
#                 left_branch[len(left_branch) - 1].


def efficiency(predicted_labels, actual_labels):
    successes = 0

    for x in range(0, len(actual_labels)):
        if predicted_labels[x] == actual_labels[x]:
            successes += 1

    print("Success Rate:", successes/len(actual_labels) * 100, "%")

def tree_maker(node_value, column_number, relevant_features, remaining_features):
    # Combine relevant feature value into strings for node labeling.
    combined_relevant_features = []
    for rel_feat_x in range(0, len(relevant_features)):
        for rel_feat_y in range(0, len(remaining_features[rel_feat_x])):
            if rel_feat_y != len(relevant_features[rel_feat_x]) - 1:
                relevant_features[rel_feat_x][rel_feat_y] = relevant_features[rel_feat_x][rel_feat_y] + " / "
        combined_relevant_features.append(''.join(relevant_features[rel_feat_x]))

    # Combine combine features into strings for node labeling.
    combined_remaining_features = []
    for rem_feat_x in range(0, len(relevant_features)):
        for rem_feat_y in range(0, len(remaining_features[rem_feat_x])):
            if rem_feat_y != len(relevant_features[rem_feat_x]) - 1:
                relevant_features[rem_feat_x][rem_feat_y] = relevant_features[rem_feat_x][rem_feat_y] + " / "
        combined_remaining_features.append(''.join(relevant_features[rem_feat_x]))


# root_tuple = "Column ", str(column_number[0])
# root = Node(root_tuple)
# for x in range(0, len(remaining_features)):
#     if x % 2 == 0:
#
# root_tuple = "Column ", str(column_number[0])
# root = Node(root_tuple)
# for x in range(0, len(remaining_features)):
#     if x % 2 == 0:
#
#
#     for x in range(0, len(min_count_feature_values)):
#             parent_node_name.append(min_count_feature_values[x])
#             if x < len(min_count_feature_values) - 1:
#                 parent_node_name.append('/')
#         node_name = "Column", str(relevant_feature)
#         node_name = ''.join(node_name)
#         root_name = node_name
#         root = Node(node_name)
#         parent_node_name = ''.join(parent_node_name)
#     else:
#         if node_iterator % 2 == 0:
#             node["string{0}".format(node_iterator)] = Node([min_count_feature_values], parent=[parent_node_name])
#         else:
#             node["string{0}".format(node_iterator)] = Node([remaining_features], parent=[parent_node_name])
#
#     node_iterator += 1
#
# left_node = feature_values[relevant_feature]
# right_node = remaining_features
#
# print(RenderTree(root))


df = pd.read_csv('car.training.csv', header=None)
data = df.iloc[:, :].values


test_df = pd.read_csv('car.test.csv', header=None)
test_data = test_df.iloc[:, :].values


parent_node = 'null'  # Boolean value to determine if node is root.
node = {}  # Node array
node_iterator = -1  # A value for iterating node index values.

original_dataframe_rows = df.shape[0]
current_dataframe_rows = df.shape[0]

test_labels = [None] * test_df.shape[0]
actual_test_labels = test_data[:,6]

while current_dataframe_rows >= original_dataframe_rows / 10:  # Keep looping until 90% of data set covered.

    feature_values = []
    # The minimum gini coefficient observed in data set during each run of the analysis
    minimum_gini = 100
    # Counting the number of instances within one feature where the minimum gini coefficient is observed.
    min_count = [0] * (data.shape[1] - 1)
    min_count_feature_values = []  # The feature values (within the same column) with the lowest gini coefficient.
    relevant_feature = -1  # Feature in which the lowest gini coefficient is located.
    remaining_features = []  # Used to hold the features values within column with higher gini coefficient.

    for column_location in range(0, data.shape[1] - 1):
        feature_values.append(np.unique(data[:, column_location]))  # Getting unique values from each column.

        for x in range(0, len(feature_values[column_location])):
            # gini(data, column_location, feature_values[column_location][x])

            # Checking if feature value gini coefficient is lowest one in data set.
            if gini(data, column_location, feature_values[column_location][x]) < minimum_gini:
                min_count[column_location] = 1  # Counting number of feature values within column that share lowest gini coefficient.

                # If gini coefficient is the lowest one, the label as such for future comparisons.
                minimum_gini = gini(data, column_location, feature_values[column_location][x])
                min_count_feature_values.clear()  # Clear out any previous feature values that have been superseded.
                min_count_feature_values.append(feature_values[column_location][x])  # Add new feature value with lowest gini.

            # Checking if feature value's gini coefficient same as column's lowest gini coefficient.
            elif gini(data, column_location, feature_values[column_location][x]) == minimum_gini and min_count[column_location] > 0:
                min_count[column_location] += 1
                min_count_feature_values.append(feature_values[column_location][x])

            if min_count[column_location] > 0:
                relevant_feature = column_location  # Record feature index value where lowest gini coefficient is located.

    dominant_label_value = label_extractor(data, min_count_feature_values, relevant_feature)

    test_labels = label_predictor(test_data, min_count_feature_values, relevant_feature, test_labels, dominant_label_value)

    # Remove already used feature values from data set.
    data = extract_used_features(data, min_count_feature_values, relevant_feature)
    current_dataframe_rows = data.shape[0]


    remaining_features.append([z for z in feature_values[relevant_feature] if z not in min_count_feature_values])

    parent_node_name = []

for test_label in test_labels:
    if len(test_label) > 1:
        del test_label[0]

test_labels = np.array(test_labels)
actual_test_labels = np.array(actual_test_labels)

efficiency(test_labels, actual_test_labels)