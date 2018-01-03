from sklearn.feature_selection import mutual_info_classif
import numpy as np
import matplotlib.pyplot as plt

def my_scoring_function(X, y) :
    """Creates a mutual_info_classif scoring with fixed random state."""
    return mutual_info_classif(X, y, random_state=2)

def create_exportable_dataset(name_list, feature_matrix, feature_names, labels) :
    """Converts features given in ndarray into dictionary"""
    my_dataset = {}
    
    for i in range(len(name_list)) :
        name = name_list[i]
        current_dict = {}
        for j in range(len(feature_names)) :
    
            current_dict[feature_names[j]] = feature_matrix[i, j]
            
        current_dict['poi'] = labels[i]
        my_dataset[name] = current_dict
        
    return my_dataset

def set_feature_to_zero(names_to_set, name_array, feature_array) :
    """Sets given features in given rows to zero."""
    for (name, f_index) in names_to_set :
        set_index = np.where(name_array == name)[0][0]
        feature_array[set_index, f_index] = 0
        
    return feature_array

def remove_by_names(names_to_remove, name_array, feature_array, labels) :
    """Removes lines belonging to given names."""
    
    for ii in range(len(names_to_remove)) :
        remove_index = np.where(name_array == names_to_remove[ii])[0][0]
        name_array = np.delete(name_array, remove_index)
        feature_array = np.delete(feature_array, remove_index, axis=0)
        labels = np.delete(labels, remove_index)
        
    return (name_array, feature_array, labels)

def plot_given_feature(feature_matrix, feature_index, feature_list) : 
    """Plots a given feature on scatterplot."""
    current_feature = feature_matrix[:, feature_index]
    current_fname = feature_list[feature_index + 1] #0 index for POI label
    
    plt.figure()
    plt.scatter(current_feature, np.ones(current_feature.shape))
    plt.title(current_fname)

def find_outliers_name(name_array, feature_array, feature_index, threshold) :
    """Find names who are considered as outlier according to the given threshold."""
    current_feature = feature_array[:, feature_index]
    outlier_flag = (current_feature > threshold)
    print(name_array[outlier_flag])