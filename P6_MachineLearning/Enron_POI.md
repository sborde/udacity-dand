# Identify Fraud from Enron Dataset

## Project summary
The goal of the project was to train a machine learning model to identify key persons in the Enron Fraud.
### Overall description
I got many features of the Enron employees like salary, bonus, stock options, etc. Besides that, I got some other features like the connection between employees through e-mail. There was one more feature, the so-called POI label. It designates that a person has a significant role in the fraud.
### Benefit of ML  on this project
This dataset is suitable for supervised learning algorithms because it serves as a labeled dataset.

If we could build a good model maybe we could prevent frauds at other companies, e.g., we create a model which can predict possible fraud based on money transfer.
### Outlier identification and handling
First, I decided to retain all of the financial and e-mail features, then I will select from them using some algorithm. Because of this, I needed to check all of the features for outliers.

First, I found the TOTAL as outlier (as we saw in the videos).

Next, I found two people who appeared to be outlier in at least two features. These two person were LAY KENNETH L. and MARK FREVERT. However, their measurements were real and they were really involved in the fraud, I decided to remove them from the list, because I wanted to build a generalized model and any outlier can distort the result.

There were three more persons who appeared as outlier only in one feature (BHATNAGAR SANJAY (restricted_stock_deferred), PICKERING MARK R (load_advances), MARTIN AMANDA K (long_term_incentive)), so I retained them in the dataset and set their value to 0.

After removing these people, I realized that feature called loan_advances became completely zero, so I decided to remove that feature entirely from the feature matrix. But then, I got some idea...

## Feature creation and selection

When I saw that only outliers had any loan_advances, I converted it to a binary feature called 'has_loan_advance'. 

## Selection of algorithm

## Parameter tuning

## Validation

## Evaluation
