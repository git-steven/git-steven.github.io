---
title:  "Feature Selection with scikit-learn"
date:   2024-03-29 13:18:25 -0500
categories:
- scikit-learn
- feature-engineering
- python
- sklearn
- AI
- ML
author: steven
---

Identifying the Most Important Features in a Dataset Using [scikit-learn](https://scikit-learn.org/).

![](</assets/images/sklearn-features.png>)


## Introduction
In the field of medical research and machine learning, [feature selection](https://en.wikipedia.org/wiki/Feature_selection) is a crucial step in building accurate and efficient models. By identifying the most important attributes or features in a dataset, we can improve model performance, reduce overfitting, and gain insights into the underlying relationships between inputs and outputs.  In this article, we will explore how to use [scikit-learn](https://scikit-learn.org/)., a popular Python library for machine learning, to find the most important attributes in a dataset containing inputs and outputs.

## Correlation-based Feature Selection
One approach to identifying the most important attributes is by measuring their correlation with the output variable.  Correlation measures the strength and direction of the linear relationship between two variables. In scikit-learn, we can use the [f_regression](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.f_regression.html#sklearn.feature_selection.f_regression) function from the [feature_selection](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_selection) module to compute the correlation between each input feature and the output variable.  We will also use the powerful [RFE](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html#sklearn.feature_selection.RFE) (Recursive Feature Elimination) method.


## The Breast Cancer Dataset
The Breast Cancer [dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html#sklearn.datasets.load_breast_cancer) is a built-in dataset in scikit-learn. It contains information about breast cancer tumors, including various measurements and characteristics of the cell nuclei. The dataset consists of 30 input features and a target variable indicating whether the tumor is malignant (cancerous) or benign (non-cancerous). Our goal is to identify the features that have the most significant impact on predicting the tumor type.

### Feature Selection using f_regression:
The [f_regression](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.f_regression.html#sklearn.feature_selection.f_regression) function from scikit-learn's [feature_selection](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_selection) module is commonly used for feature selection in regression problems. Although the Breast Cancer dataset is a classification problem, we can still use `f_regression` to compute the correlation between each feature and the target variable. Higher F-values indicate stronger correlations.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.feature_selection import f_regression

# Load the Breast Cancer dataset
data = load_breast_cancer()
X, y = data.data, data.target

# Perform feature selection using f_regression
f_scores, p_values = f_regression(X, y)

# Get the feature importance scores
feature_importance = abs(f_scores)

# Sort the features by importance in descending order
sorted_indices = feature_importance.argsort()[::-1]

# Print the top 10 feature importance scores and names
for i in sorted_indices[:10]:
    print(f"{data.feature_names[i]}: {feature_importance[i]:.2f}")
```

In this example, we load the Breast Cancer dataset and use [f_regression](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.f_regression.html#sklearn.feature_selection.f_regression) to compute the F-values and p-values between each feature and the target variable. We then sort the features by their importance scores in descending order and print the top 10 features along with their importance scores. You can see and run this example in the jupyter [notebook](/notebook/sklearn-feature-engineering.ipynb).

The output looks like this:
```text
worst concave points: 964.39
worst perimeter: 897.94
mean concave points: 861.68
worst radius: 860.78
mean perimeter: 697.24
worst area: 661.60
mean radius: 646.98
mean area: 573.06
mean concavity: 533.79
worst concavity: 436.69
```

### RFE Feature Selection
[RFE](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html#sklearn.feature_selection.RFE) (Recursive Feature Elimination) is another powerful technique for feature selection. It recursively selects a subset of features by fitting a model, ranking the features based on their importance, and then removing the least important features. RFE can be used with various estimators, such as logistic regression or support vector machines.

#### `RFE` Example
```python
from sklearn.datasets import load_breast_cancer
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

# Load the Breast Cancer dataset
data = load_breast_cancer()
X, y = data.data, data.target

# Create a logistic regression estimator
estimator = LogisticRegression(max_iter=2000)

# Perform feature selection using RFE
selector = RFE(estimator, n_features_to_select=10, step=1)
selector = selector.fit(X, y)

# Get the selected feature indices
selected_feature_indices = selector.support_

# Print the selected feature names
selected_feature_names = [data.feature_names[i] for i in range(len(data.feature_names)) if selected_feature_indices[i]]
print("Selected features:", selected_feature_names)
```

In this example, we load the Breast Cancer dataset and create a logistic regression estimator. We then use RFE with the estimator to select the top 10 features. The `support_` attribute of the RFE object indicates the selected features. Finally, we print the names of the selected features.  You can see and run this example in the jupyter [notebook](/notebook/sklearn-feature-engineering.ipynb).

The output looks like this:
```text
Selected features: ['mean radius', 'mean compactness', 'mean concavity', 'texture error', 'worst radius', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry']
```

## Conclusion
Scikit-learn provides powerful feature selection techniques, such as `f_regression` and `RFE` (Recursive Feature Elimination), to identify the most important features in a dataset. By using these techniques on the Breast Cancer dataset, we can determine which features have the strongest correlation with the tumor type and are most informative for building diagnostic models. The `f_regression` function computes the correlation between each feature and the target variable, while RFE recursively selects a subset of features based on their importance. By focusing on the most relevant features, we can enhance the accuracy and interpretability of our models while gaining valuable insights into the underlying relationships in the data.
