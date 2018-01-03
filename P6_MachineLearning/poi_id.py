#!/usr/bin/python


import warnings
warnings.filterwarnings('ignore')

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from poi_id_helper import create_exportable_dataset, my_scoring_function
from poi_id_helper import remove_by_names, set_feature_to_zero
import matplotlib.pyplot as plt
import numpy as np



### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi',
        'salary', 'deferral_payments', 
        'total_payments', 'loan_advances', 
        'bonus', 'restricted_stock_deferred', 
        'deferred_income', 'total_stock_value', 
        'expenses', 'exercised_stock_options', 
        'other', 'long_term_incentive', 
        'restricted_stock', 'director_fees',
        'to_messages', 'from_poi_to_this_person',
        'from_messages', 'from_this_person_to_poi',
        'shared_receipt_with_poi']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

### Extract features and labels from dataset for local testing
data = featureFormat(data_dict, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# Convert everything to numpy datatypes
feature_matrix = np.asarray(features)
name_matrix = np.asanyarray(sorted(list(data_dict.keys())))
name_matrix = np.delete(name_matrix, np.where(name_matrix=='LOCKHART EUGENE E')[0][0])

### Task 2: Remove outliers
names_to_remove = ['TOTAL', 'LAY KENNETH L', 'FREVERT MARK A']
names_to_set_zero = [('PICKERING MARK R', 3) , ('BHATNAGAR SANJAY', 5), ('MARTIN AMANDA K', 11)]

(name_matrix, feature_matrix, labels) = remove_by_names(names_to_remove, name_matrix, feature_matrix, labels)
feature_matrix = set_feature_to_zero(names_to_set_zero, name_matrix, feature_matrix)

### Remove fourth feature, because it is all zero 
feature_matrix = np.delete(feature_matrix, 3, axis=1)
del features_list[4]

### Task 3: Create new feature(s)
restricted_stock = feature_matrix[:, features_list.index('restricted_stock')-1]
total_stock = feature_matrix[:, features_list.index('total_stock_value')-1]
new_feature = np.zeros(restricted_stock.shape)
has_stock = total_stock > 0
new_feature[has_stock] = restricted_stock[has_stock] / total_stock[has_stock]

### Add new feature and its name to the others
feature_matrix = np.column_stack((feature_matrix, new_feature))
features_list += ['restricted_stock_ratio']

### Scale features to [0,1] interval
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(feature_matrix)
feature_matrix = scaler.transform(feature_matrix)

from sklearn.feature_selection import SelectKBest, mutual_info_classif

### Switch this variable to True for parameter tuning. Else, 
### preset algorithm with preset parameters will run.
tuning = False

if tuning :
    
    algorithm = 'svm'
    #algorithm = 'dct'
    #algorithm = 'gnb'
    
    result_list = []
    
    ### Automatic feature selection using mutual information
    for no_feat in range(1, feature_matrix.shape[1]) :
    
        selector = SelectKBest(my_scoring_function, k=no_feat)
        selector.fit(feature_matrix, labels)
        best_feature_matrix = selector.fit_transform(feature_matrix, labels)
        
        
        ### Task 4: Try a varity of classifiers
        ### Please name your classifier clf for easy export below.
        ### Note that if you want to do PCA or other multi-stage operations,
        ### you'll need to use Pipelines. For more info:
        ### http://scikit-learn.org/stable/modules/pipeline.html
        if algorithm == 'svm' :
            from sklearn.svm import SVC
            clf = SVC()   
            parameters = {
                    'C':[1, 10, 100, 1000, 10000],
                    'gamma':[0.0001, 0.001, 0.01, 0.1, 0.5]
                    }
        elif algorithm == 'dct' :
            
            if no_feat < 5 :
                continue
            
            from sklearn.tree import DecisionTreeClassifier
            clf = DecisionTreeClassifier()
            parameters = {
                    'criterion':['gini', 'entropy'],
                    'max_features':[i for i in range(4, min(no_feat, 10))],
                    'min_samples_split': [0.1, 0.3, 0.5],
                    'splitter':['best','random'] 
                    }
        elif algorithm == 'gnb' :
            from sklearn.naive_bayes import GaussianNB
            clf = GaussianNB()
            
        
        ### Task 5: Tune your classifier to achieve better than .3 precision and recall 
        ### using our testing script. Check the tester.py script in the final project
        ### folder for details on the evaluation method, especially the test_classifier
        ### function. Because of the small size of the dataset, the script uses
        ### stratified shuffle split cross validation. For more info: 
        ### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
        if algorithm == 'svm' or algorithm == 'dct' :
                from sklearn.model_selection import GridSearchCV    
                selector = GridSearchCV(clf, parameters, scoring='f1', cv=3);
                selector.fit(best_feature_matrix, labels)    
                clf = selector.best_estimator_
        
        ### Task 6: Dump your classifier, dataset, and features_list so anyone can
        ### check your results. You do not need to change anything below, but make sure
        ### that the version of poi_id.py that you submit can be run on its own and
        ### generates the necessary .pkl files for validating your results.
        my_features = ['poi'] + ['feature_' + str(i+1) for i in range(best_feature_matrix.shape[1])]
        my_dataset = create_exportable_dataset(name_matrix, best_feature_matrix, my_features[1:], labels)
        
        ### Validate with real tester
        dump_classifier_and_data(clf, my_dataset, my_features)
        import tester
        result = tester.main()
        if result :
            result_list.append(list(result))
        else :
            result_list.append([0, 0, 0, 0])
        
        
        print('Number of features: {}'.format(no_feat))
        
    result_arr = np.asarray(result_list)
    
    plt.figure()
    plt.hold(True)
    x_value = range(1, result_arr.shape[0]+1)
    plt.plot(x_value, result_arr[:, 0])
    plt.plot(x_value, result_arr[:, 1])
    plt.plot(x_value, result_arr[:, 2])
    plt.plot(x_value, result_arr[:, 3])
    plt.legend(['accuracy', 'precision', 'recall', 'f1'], loc=7)
    plt.xticks(x_value)
    plt.hold(False)
    
else :
    from sklearn.svm import SVC
    clf = SVC(C=10000, kernel='rbf', gamma=0.5)
    
    micl = mutual_info_classif(feature_matrix, labels, random_state=2)
    
    plt.figure()
    plt.hold()
    mibars = plt.bar(range(1, len(micl)+1), micl)
    mibars[-1].set_color('r')
    
    feature_selection_order = np.argsort(-micl)
    print('Best 7 MI scores of features (in descending order):')
    for ii in range(0, 7) :
        print('{0}: {1:.3f}'.format(features_list[feature_selection_order[ii]+1], micl[feature_selection_order[ii]]))
    
    
    selector = SelectKBest(my_scoring_function, k=7)
    selector.fit(feature_matrix, labels)
    best_feature_matrix = selector.fit_transform(feature_matrix, labels)
    
    my_features = ['poi'] + ['feature_' + str(i+1) for i in range(best_feature_matrix.shape[1])]
    my_dataset = create_exportable_dataset(name_matrix, best_feature_matrix, my_features[1:], labels)
        
    dump_classifier_and_data(clf, my_dataset, my_features)
    import tester
    result = tester.main()
            
    