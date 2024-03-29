from calendar import c
from re import A
from shlex import shlex
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn import metrics
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix,roc_curve,roc_auc_score,accuracy_score, plot_confusion_matrix,classification_report
# data collection and prpcessing
# loading the dataset to pandas Dataframe

loan_dataset = pd.read_csv(r'D:\My programs\loan_data.csv')

# print(loan_dataset.head())

# Print the number of rows and columns
loan_dataset.shape

# Some statitical measuers
loan_dataset.describe()

# number of missing valuse in each column
loan_dataset.isnull().sum()

# dropping all the missing values
loan_dataset = loan_dataset.dropna()

# --------------------data encoding------------------#
loan_dataset.replace({"Loan_Status": {'N': 0, 'Y': 1}}, inplace=True)
loan_dataset.replace({"Credit_History": {'0': 0, '1': 1}}, inplace=True)
loan_dataset.replace({"Gender": {'Male': 0, 'Female': 1}}, inplace=True)
loan_dataset.replace({"Married": {'Yes': 1, 'No': 0}}, inplace=True)
loan_dataset.replace({"Education": {'Graduate': 1, 'Not Graduate': 0}}, inplace=True)
loan_dataset.replace({"Self_Employed": {'Yes': 1, 'No': 0}}, inplace=True)
loan_dataset.replace({"Property_Area": {'Rural': 0, 'Semiurban': 1, 'Urban': 2}}, inplace=True)
loan_dataset.replace({"Dependents": {'3+': 1, '2': 1 }}, inplace=True)
#loan_dataset.replace({"Dependents": {'3+': 4 }}, inplace=True)
# Replacing the value of +3
#loand_dataset = loan_dataset.replace(to_replace='3+', value=4)
#print(loand_dataset)
# --------------------data Visualization-------------------#

# education and the loan Status
sns.countplot(x='Education', hue='Loan_Status', data=loan_dataset)

# matital status & loan status
sns.countplot(x='Married', hue='Loan_Status', data=loan_dataset)
# -----------------------------------------------------------#

# seperating the data and lable
X = loan_dataset.drop(columns=['Loan_ID', 'Loan_Status'], axis=1)
Y = loan_dataset['Loan_Status']

#________________________________________________
#split the data for trining set and test set
from sklearn.model_selection import train_test_split

xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size = 0.35,shuffle=True, random_state = 10)
#####################################################
#Scaling
scalar =StandardScaler()
scalar.fit(xtrain)
xtrain_scaled=scalar.transform(xtrain)
xtest_scaled=scalar.transform(xtest)
######################################################
#data frame
xtrain_scaled=pd.DataFrame(xtrain_scaled,columns=xtrain.columns)

############################################################
#linear
poly_features = PolynomialFeatures(degree=1)

# transforms the existing features to higher degree features.
X_train_poly = poly_features.fit_transform(xtrain)

# fit the transformed features to Linear Regression
poly_model = linear_model.LinearRegression()
poly_model.fit(X_train_poly, ytrain)

# predicting on training data-set
y_train_predicted = poly_model.predict(X_train_poly)

# predicting on test data-set
prediction = poly_model.predict(poly_features.fit_transform(xtest))

#r2_score = poly_model.score(xtest,ytest)
print("accuracy ", metrics.r2_score(ytest,prediction))

print('Co-efficient of linear regression',poly_model.coef_)
print('Intercept of linear regression model',poly_model.intercept_)
print('Mean Square Error', metrics.mean_squared_error(ytest, prediction))

###########################################
#logistic
model = LogisticRegression(C=100.0, random_state=1, solver='lbfgs' , multi_class='ovr')
model.fit(xtrain_scaled, ytrain)
ypredict=model.predict(xtest_scaled)
#train_acc = model.score(xtrain_scaled, ytrain)
print("The Accuracy of logistic is %.3f"%metrics.accuracy_score(ytest,ypredict))
print ("------------------------------------------------------------------------------------------")
##########################################
#svm
from sklearn.model_selection import GridSearchCV

####################################
#deciion treee

from sklearn.tree import DecisionTreeClassifier
clf_model = DecisionTreeClassifier(criterion="gini", random_state=42,max_depth=3, min_samples_leaf=5)
clf_model.fit(xtrain,ytrain)
DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=42)
y_predict1 = clf_model.predict(xtest)
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
print(accuracy_score(ytest,y_predict1))

#another #decision tree

DTClassifier= DecisionTreeClassifier(criterion= 'entropy' , random_state=0)
DTClassifier.fit(xtrain, ytrain)
y_predict= DTClassifier.predict(xtest)
#y_predict
print("accuracy of decision tree is: ",metrics.accuracy_score(y_predict,ytest)*100)
print("_____________________________________")
############################################################{}%".format(train_acc*100)
#SVM
model = svm.SVC(kernel='linear')
model.fit(xtrain, ytrain)
predictions = model.predict(xtest)
print('SVM Accuracy : ', accuracy_score(ytest, predictions)*100)
print("_____________________________________")

#######################
#KNN
model2 = KNeighborsClassifier(n_neighbors=5)
model2.fit(xtrain, ytrain)
pred = model2.predict(xtest)
print(' KNN Accuracy : ', accuracy_score(ytest, pred)*100)
print("_____________________________________")
###############.format(train_acc*100)
#navin
model2 = GaussianNB()
model2.fit(xtrain, ytrain)
ypred = model2.predict(xtest)
print(' NAVIEN Accuracy : ', accuracy_score(ytest, ypred)*100)