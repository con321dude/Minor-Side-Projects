import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle

'''
linear regression: algorithm that attempts to find a best fit line to a set of data points
(attempts to find LINEAR patterns amongst data to predict future values)
this algorithm is good for basic linear data, but for more complex datasets, linear regression might not be best
'''

data = pd.read_csv("student-mat.csv", sep=";") #import the dataset(.csv = comma separated values)

#print(data.head()) #prints first 5 students, and all their input/output

'''
inputs only the integer values of the dataset: three grade inputs, the study time, their failures, and absences; 
The final correct grade 
'''
data = data[["G1","G2","G3","studytime","failures","absences"]]

#print(data.head())

predict = "G3"  #value in the dataset that is trying to be predicted

X = np.array(data.drop([predict], 1)) #
Y = np.array(data[predict]) #labels

''' taking all attributes and labels we are trying to predict, then splits them up into 4 arrays... 
x_train is a segment of X, y_train is a segment of Y... test data is used to test the accuracy of our algorithm
test_size = percentage of the data becomes test samples'''
x_train, x_test, y_train, y_test =  sklearn.model_selection.train_test_split(X,Y,test_size=0.1)

linear = linear_model.LinearRegression()

linear.fit(x_train, y_train) #fits the data to find a best fitting line using the x and y training set data into linear

acc = linear.score(x_test, y_test) #accuracy of our line using the set of chosen training data
print ("\n\nAccuracy for this chosen training set is", acc)
print("Coefficients: " , linear.coef_) #m coefficients (in a 5 dimensional space, so its not just a single coefficient slope)
print("Intercept: " , linear.intercept_,"\n \n") #y-intercept (b in y=mx+b)

predictions = linear.predict(x_test) #predict the testing set values, so we can compare it to the real value


for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x]) #prints our prediction, followed by the inputs, and then the real output

