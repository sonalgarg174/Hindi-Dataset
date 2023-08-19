# -*- coding: utf-8 -*-
"""hindi mlclassifier_ifnd.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-HefKHzryLjhInpxdhHtPlSkN9yR4PiZ
"""



pip install torch==1.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

pip install inltk

from inltk.inltk import setup
setup('hi')

from inltk.inltk import tokenize

hindi_text = """प्राचीन काल में विक्रमादित्य नाम के एक आदर्श राजा हुआ करते थे।
अपने साहस, पराक्रम और शौर्य के लिए  राजा विक्रम मशहूर थे।
ऐसा भी कहा जाता है कि राजा विक्रम अपनी प्राजा के जीवन के दुख दर्द जानने के लिए रात्री के पहर में भेष बदल कर नगर में घूमते थे।"""

# tokenize(input text, language code)
tokenize(hindi_text, "hi")
from fastai.text import *
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
import sentencepiece as spm
import re
import pdb

df=pd.read_excel("/content/statement 13 july.xlsx")

df.head()

df=df.sample(frac=1).reset_index(drop=True)

x=df["Statement"]
y=df["Label"]

corpus = []
for i in range(0, len(x)):
    review = x[i]
    corpus.append(review)

corpus

from inltk.inltk import tokenize

str1 = ''.join(corpus)

tokenize(str1, "hi")

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_v=TfidfVectorizer(max_features=5000,ngram_range=(1,3))
X=tfidf_v.fit_transform(corpus).toarray()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

tfidf_v.get_feature_names()[:20]

# remove bag_of_words
import matplotlib.pyplot as plt
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    See full source and example:
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
from sklearn.naive_bayes import MultinomialNB
classifier=MultinomialNB()
from sklearn import metrics
import numpy as np
import itertools
classifier.fit(X_train, y_train)
pred = classifier.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print("accuracy:   %0.3f" % score)
cm = metrics.confusion_matrix(y_test, pred)
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'])

from sklearn.metrics import roc_curve, roc_auc_score, auc
# Function to get roc curve
def get_roc (y_test,pred):
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    fpr, tpr, _ = roc_curve(y_test, pred)
    roc_auc = auc(fpr, tpr)
    #Plot of a ROC curve
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="upper left")
    plt.show()
    return

from sklearn.metrics import  average_precision_score, precision_recall_curve


# Function to get Precision recall curve
def get_prec_recall (y_test,y_pred):
    average_precision = average_precision_score(y_test, y_pred)
    print('Average precision-recall score : {}'.format(average_precision))
    precision, recall, _ = precision_recall_curve(y_test, y_pred)
    plt.step(recall, precision, color='b', alpha=0.2, where='post')
    plt.fill_between(recall, precision, step='post', alpha=0.2,color='cyan')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
    return

#LOGISTIC REGRESSION

from sklearn.linear_model import LogisticRegression
logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)

predictions = logmodel.predict(X_test)

#Getting feature importances
print(logmodel.coef_)

from sklearn.metrics import classification_report
print(classification_report(y_test,predictions))

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = logmodel, X = X_train, y = y_train, cv = 10)
accuracies.mean()

from sklearn.metrics import confusion_matrix
#print(confusion_matrix(y_test,predictions))
cnf_matrix_logreg = metrics.confusion_matrix(y_test, predictions)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix_logreg), annot=True, cmap="YlGnBu" ,fmt='g')

plt.tight_layout()
plt.title('Confusion matrix for Logistic Regression', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
print("Model Accuracy for Logistic Regression:",metrics.accuracy_score(y_test, predictions))

#from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score
print ("Accuracy : ", accuracy_score(y_test,predictions)*100)

# Log Loss  - Should be close to 0 - Only for classification models
from sklearn.metrics import log_loss
log_loss(y_test,predictions)

# Get ROC curve for Logistic Regression
get_roc(y_test,predictions)

get_prec_recall(y_test,predictions)

from sklearn.model_selection import cross_validate

scoring = {'accuracy': 'accuracy', 'log_loss': 'neg_log_loss', 'auc': 'roc_auc'}

results = cross_validate(logmodel, X, y, cv=10, scoring=list(scoring.values()),
                         return_train_score=False)

print('K-fold cross-validation results:')
for sc in range(len(scoring)):
    print(logmodel.__class__.__name__+" average %s: %.3f (+/-%.3f)" % (list(scoring.keys())[sc], -results['test_%s' % list(scoring.values())[sc]].mean()
                               if list(scoring.values())[sc]=='neg_log_loss'
                               else results['test_%s' % list(scoring.values())[sc]].mean(),
                               results['test_%s' % list(scoring.values())[sc]].std()))

# GAUSSIAN-NB

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
accuracies.mean()

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
#print(confusion_matrix(y_test,predictions))
cnf_matrix_logreg = metrics.confusion_matrix(y_test, y_pred)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix_logreg), annot=True, cmap="YlGnBu" ,fmt='g')

plt.tight_layout()
plt.title('Confusion matrix for Naive Bayes', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
print("Model Accuracy for Naive Bayes:",metrics.accuracy_score(y_test, y_pred))

#from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score
print ("Accuracy : ", accuracy_score(y_test,y_pred)*100)

#MAE L1 loss function - Should be close to 0
from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,y_pred) #y_target, y_pred

#MAE L2 loss function - Should be close to 0
from sklearn.metrics import mean_squared_error
mean_squared_error(y_test,y_pred) #y_target, y_pred

# Log Loss  - Should be close to 0 - Only for classification models
from sklearn.metrics import log_loss
log_loss(y_test,y_pred)

# Get ROC curve for Naive Bayes

get_roc(y_test,y_pred)

get_prec_recall(y_test,y_pred)

# Applying k-Fold Cross Validation for test set
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = logmodel, X = X_test, y = y_test, cv = 10)
accuracies.mean()

scoring = {'accuracy': 'accuracy', 'log_loss': 'neg_log_loss', 'auc': 'roc_auc'}

results = cross_validate(classifier, X_train, y_train, cv=10, scoring=list(scoring.values()),
                         return_train_score=False)
print('K-fold cross-validation results:')
for sc in range(len(scoring)):
    print(classifier.__class__.__name__+" average %s: %.3f (+/-%.3f)" % (list(scoring.keys())[sc], -results['test_%s' % list(scoring.values())[sc]].mean()
                               if list(scoring.values())[sc]=='neg_log_loss'
                               else results['test_%s' % list(scoring.values())[sc]].mean(),
                               results['test_%s' % list(scoring.values())[sc]].std()))

#DECISION-TREE-CLASSIFIER

from sklearn import tree
decclassifier = tree.DecisionTreeClassifier(criterion ='entropy')
decclassifier.fit(X_train, y_train)

y_pred = decclassifier.predict(X_test)

#Validation
from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, y_pred)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = decclassifier, X = X_train, y = y_train, cv = 10)
accuracies.mean()

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
#print(confusion_matrix(y_test,predictions))
cnf_matrix_dectree = metrics.confusion_matrix(y_test, y_pred)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix_dectree), annot=True, cmap="YlGnBu" ,fmt='g')

plt.tight_layout()
plt.title('Confusion matrix for Decision Tree', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
print("Model Accuracy for Decision tree:",metrics.accuracy_score(y_test, y_pred))

#from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score
print ("Accuracy : ", accuracy_score(y_test,y_pred)*100)

#MAE L1 loss function - Should be close to 0
from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,y_pred) #y_target, y_pred

#MAE L2 loss function - Should be close to 0
from sklearn.metrics import mean_squared_error
mean_squared_error(y_test,y_pred) #y_target, y_pred

# Log Loss  - Should be close to 0 - Only for classification models
from sklearn.metrics import log_loss
log_loss(y_test,y_pred)

# Get ROC curve for Decision Tree

get_roc(y_test,y_pred)

get_prec_recall(y_test,y_pred)

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = decclassifier, X = X_train, y = y_train, cv = 10)
accuracies.mean()

from sklearn.model_selection import cross_validate

scoring = {'accuracy': 'accuracy', 'log_loss': 'neg_log_loss', 'auc': 'roc_auc'}

results = cross_validate(decclassifier, X_train, y_train, cv=10, scoring=list(scoring.values()),
                         return_train_score=False)
print('K-fold cross-validation results:')
for sc in range(len(scoring)):
    print(decclassifier.__class__.__name__+" average %s: %.3f (+/-%.3f)" % (list(scoring.keys())[sc], -results['test_%s' % list(scoring.values())[sc]].mean()
                               if list(scoring.values())[sc]=='neg_log_loss'
                               else results['test_%s' % list(scoring.values())[sc]].mean(),
                               results['test_%s' % list(scoring.values())[sc]].std()))

#RANDOM FOREST

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=1000)
rfc.fit(X_train, y_train)

rfc_pred = rfc.predict(X_test)

#'spam_score_fector','click_bait_score','toxicity_factor','src_url_polarity','sentiment_score','stance_factor_num'
rfc.feature_importances_

print(confusion_matrix(y_test,rfc_pred))

print(classification_report(y_test,rfc_pred))

#from sklearn.metrics import accuracy_score
print ("Accuracy : ", metrics.accuracy_score(y_test,rfc_pred)*100 )

#MAE L1 loss function - Should be close to 0
from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,rfc_pred) #y_target, y_pred

#MAE L2 loss function - Should be close to 0
from sklearn.metrics import mean_squared_error
mean_squared_error(y_test,rfc_pred) #y_target, y_pred

# Log Loss  - Should be close to 0 - Only for classification models
from sklearn.metrics import log_loss
log_loss(y_test,rfc_pred)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
#print(confusion_matrix(y_test,predictions))
cnf_matrix_rf = metrics.confusion_matrix(y_test, rfc_pred)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix_rf), annot=True, cmap="YlGnBu" ,fmt='g')

plt.tight_layout()
plt.title('Confusion matrix for Random Forest', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
print("Model Accuracy for Decision tree:",metrics.accuracy_score(y_test, y_pred)  * 100)

get_roc(y_test,rfc_pred)

get_prec_recall(y_test,rfc_pred)

from sklearn.model_selection import cross_validate

scoring = {'accuracy': 'accuracy', 'log_loss': 'neg_log_loss', 'auc': 'roc_auc'}

results = cross_validate(rfc, X_train, y_train, cv=10, scoring=list(scoring.values()),
                         return_train_score=False)
print('K-fold cross-validation results:')
for sc in range(len(scoring)):
    print(rfc.__class__.__name__+" average %s: %.3f (+/-%.3f)" % (list(scoring.keys())[sc], -results['test_%s' % list(scoring.values())[sc]].mean()
                               if list(scoring.values())[sc]=='neg_log_loss'
                               else results['test_%s' % list(scoring.values())[sc]].mean(),
                               results['test_%s' % list(scoring.values())[sc]].std()))

#SVM

# Fitting Kernel SVM to the Training set
from sklearn.svm import SVC
svcclassifier = SVC(kernel = 'rbf', random_state = 0, gamma=0.8, C=100, probability=True)
svcclassifier.fit(X_train, y_train)

svc_pred = svcclassifier.predict(X_test)

#print (svcclassifier.get_feature_names())
print(classification_report(y_test,svc_pred))

#from sklearn.metrics import accuracy_score
print ("Accuracy : ", accuracy_score(y_test,svc_pred)*100)

#MAE L1 loss function - Should be close to 0
from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,svc_pred) #y_target, y_pred

#MAE L2 loss function - Should be close to 0
from sklearn.metrics import mean_squared_error
mean_squared_error(y_test,svc_pred) #y_target, y_pred

# Log Loss  - Should be close to 0 - Only for classification models
from sklearn.metrics import log_loss
log_loss(y_test,svc_pred)

# Making the Confusion Matrix
cm = confusion_matrix(y_test, svc_pred)
#print(cm)
# create heatmap
sns.heatmap(pd.DataFrame(cm), annot=True, cmap="YlGnBu" ,fmt='g')

plt.tight_layout()
plt.title('Confusion matrix for SVM', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
print("Model Accuracy for SVM:",metrics.accuracy_score(y_test, svc_pred) * 100)
get_roc(y_test,svc_pred)

get_prec_recall(y_test,svc_pred)

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = svcclassifier, X = X_train, y = y_train, cv = 10)
accuracies.mean()

from sklearn.model_selection import cross_validate

scoring = {'accuracy': 'accuracy', 'log_loss': 'neg_log_loss', 'auc': 'roc_auc'}

results = cross_validate(svcclassifier, X_train, y_train, cv=10, scoring=list(scoring.values()),
                         return_train_score=False)
print('K-fold cross-validation results:')
for sc in range(len(scoring)):
    print(svcclassifier.__class__.__name__+" average %s: %.3f (+/-%.3f)" % (list(scoring.keys())[sc], -results['test_%s' % list(scoring.values())[sc]].mean()
                               if list(scoring.values())[sc]=='neg_log_loss'
                               else results['test_%s' % list(scoring.values())[sc]].mean(),
                               results['test_%s' % list(scoring.values())[sc]].std()))

#KNN

# Applying PCA
from sklearn.decomposition import PCA
pca = PCA(n_components = 5)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)
explained_variance = pca.explained_variance_ratio_

from sklearn.neighbors import KNeighborsClassifier
knnclassifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
knnclassifier.fit(X_train_pca, y_train)

# Predicting the Test set results
knn_pred = knnclassifier.predict(X_test_pca)

from sklearn.metrics import classification_report
print(classification_report(y_test,knn_pred))

#from sklearn.metrics import accuracy_score
print ("Accuracy : ", accuracy_score(y_test,knn_pred)*100)

#MAE L1 loss function - Should be close to 0
from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,knn_pred) #y_target, y_pred

#MAE L2 loss function - Should be close to 0
from sklearn.metrics import mean_squared_error
mean_squared_error(y_test,knn_pred) #y_target, y_pred

# Log Loss  - Should be close to 0 - Only for classification models
from sklearn.metrics import log_loss
log_loss(y_test,knn_pred)

# Making the Confusion Matrix
cm = confusion_matrix(y_test, knn_pred)
#print(cm)
# create heatmap
sns.heatmap(pd.DataFrame(cm), annot=True, cmap="YlGnBu" ,fmt='g')

plt.tight_layout()
plt.title('Confusion matrix for KNN', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
print("Model Accuracy for KNN:",metrics.accuracy_score(y_test, knn_pred) * 100)

get_roc(y_test,knn_pred)

get_prec_recall(y_test,knn_pred)

from sklearn.model_selection import cross_validate

scoring = {'accuracy': 'accuracy', 'log_loss': 'neg_log_loss', 'auc': 'roc_auc'}

results = cross_validate(knnclassifier, X_train, y_train, cv=10, scoring=list(scoring.values()),
                         return_train_score=False)
print('K-fold cross-validation results:')
for sc in range(len(scoring)):
    print(knnclassifier.__class__.__name__+" average %s: %.3f (+/-%.3f)" % (list(scoring.keys())[sc], -results['test_%s' % list(scoring.values())[sc]].mean()
                               if list(scoring.values())[sc]=='neg_log_loss'
                               else results['test_%s' % list(scoring.values())[sc]].mean(),
                               results['test_%s' % list(scoring.values())[sc]].std()))





