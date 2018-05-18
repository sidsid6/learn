#-*- coding: utf-8 -*-
from sklearn import datasets
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np


def Gaussian(dataset):

    X=[]
    X.append(dataset[['spd']])
    X.append(dataset[['spd','rpm']])
    X.append(dataset[['spd','rpm','accel']])
    X.append(dataset[['spd','rpm','stop']])
    X.append(dataset[['spd','accel','stop']])
    X.append(dataset[['spd','rpm','accel','stop']])

    for i in range(0,len(X)):

        X1=X[i]
        X1array = X1.as_matrix(columns=None)

        Y = dataset[['fuel']]
        Yarray = Y.stack().values

        model = GaussianNB()
        model.fit(X1array, Yarray)

        expected = np.array(Yarray)
        temp = np.array(X1array)

        predicted = model.predict(temp)

        print(metrics.classification_report(expected, predicted))

if __name__ == '__main__':

    _dataset = pd.read_csv('C:\Users\Kim Seung Il\Desktop\\analysis\multiprocessing\\283car.csv')
    n = np.around(_dataset['fuel']*1000).astype(int)
    _dataset['fuel']=n

    fulldata= _dataset

    Gaussian(fulldata)



