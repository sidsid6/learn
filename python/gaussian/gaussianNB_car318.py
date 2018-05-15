#-*- coding: utf-8 -*-
from sklearn import datasets
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np

def Gaussian(dataset):

    #X = dataset[['spd','rpm', 'accel', 'stop']]
    X = dataset[['spd','rpm','accel','stop']]
    Xarray = X.as_matrix(columns=None)

    Y = dataset[['fuel']]
    Yarray = Y.stack().values

    model = GaussianNB()
    model.fit(Xarray, Yarray)

    expected = np.array(Yarray)
    temp = np.array(Xarray)

    predicted = model.predict(temp)

    print(metrics.classification_report(expected, predicted))


if __name__ == '__main__':

    _dataset = pd.read_csv('C:\Users\Kim Seung Il\Desktop\\analysis\multiprocessing\\318car.csv')
    n = np.around(_dataset['fuel']*1000).astype(int)
    _dataset['fuel']=n

    fulldata= _dataset
    spdunder50= _dataset[(_dataset.spd<=50)]
    spd50to100 = _dataset[(_dataset.spd > 50) & (_dataset.spd <= 100)]
    spd100to150 = _dataset[(_dataset.spd > 100) & (_dataset.spd <= 150)]

    Gaussian(fulldata)
    Gaussian(spdunder50)
    Gaussian(spd50to100)
    Gaussian(spd100to150)




