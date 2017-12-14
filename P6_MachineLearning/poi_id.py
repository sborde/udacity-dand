#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
import matplotlib.pyplot as plt
import numpy as np

def set_to_zero_by_name(name_to_set, name_array, feature_array, feature_index) :
    set_index = np.where(name_array == name_to_set)[0][0]
    feature_array[set_index, feature_index] = 0
    return feature_array

def remove_by_name(name_to_remove, name_array, feature_array) :
    remove_index = np.where(name_array == name_to_remove)[0][0]
    name_array = np.delete(name_array, remove_index)
    feature_array = np.delete(feature_array, remove_index, axis=0)
    return (name_array, feature_array)

def plot_given_feature(feature_matrix, feature_index, feature_list) : 
    current_feature = feature_matrix[:, feature_index]
    current_fname = feature_list[feature_index + 1] #0 index for POI label
    
    plt.figure()
    plt.scatter(current_feature, np.ones(current_feature.shape))
    plt.title(current_fname)

def find_outlier_name(name_array, feature_array, feature_index, threshold) :
    current_feature = feature_array[:, feature_index]
    outlier_flag = (current_feature > threshold)
    print(name_array[outlier_flag])

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi'] # You will need to use more features
financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']
email_num_features = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

features_list += financial_features
features_list += email_num_features

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# Convert everything to numpy datatypes
feature_matrix = np.asarray(features)
name_matrix = np.asanyarray(sorted(list(data_dict.keys())))
name_matrix = np.delete(name_matrix, np.where(name_matrix=='LOCKHART EUGENE E')[0][0])

(name_matrix, feature_matrix) = remove_by_name('TOTAL', name_matrix, feature_matrix)

### Task 3: Create new feature(s)
features_list += ['has_loan_advance']
new_feature = (feature_matrix[:, 3]>0)
new_feature = np.ones((feature_matrix.shape[0],)) * new_feature
feature_matrix = np.column_stack((feature_matrix, new_feature))

### Task 2: Remove outliers
(name_matrix, feature_matrix) = remove_by_name('LAY KENNETH L', name_matrix, feature_matrix)
(name_matrix, feature_matrix) = remove_by_name('FREVERT MARK A', name_matrix, feature_matrix)

feature_matrix = set_to_zero_by_name('PICKERING MARK R', name_matrix, feature_matrix, 3)
feature_matrix = set_to_zero_by_name('BHATNAGAR SANJAY', name_matrix, feature_matrix, 5)
feature_matrix = set_to_zero_by_name('MARTIN AMANDA K', name_matrix, feature_matrix, 11)

feature_matrix = np.delete(feature_matrix, 3, axis=1)
del features_list[4]

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)