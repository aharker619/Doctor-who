# Regression
#
# Tianchu Shu & Alyssa Harker
#
# kernel reg code gathered from 
#https://stats.stackexchange.com/questions/218514/how-to-decide-whether-a-kernel-density-estimate-is-good

import numpy as np
import matplotlib.pylab as plt
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors.kde import KernelDensity
from sklearn import svm

VAR = ['ARRTIME', 'AVGWAIT', 'MSA', 'PAINSCALE']
MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
WDAY = ['MON', 'TUE', 'WED', 'THUR', 'FRI','SAT', 'SUN']
ALLVAR = VAR + MONTHS + WDAY

def clean_data(FILENAME):
    '''
    Input: 
         a string of the csvfile name
    Output:
         a clean panda dataframe
    '''
    df = pd.read_csv(FILENAME, index_col=0)
    #drop all the negatvie value
    df = df[(df > 0).all(1)]
    #conver the arrival time to real min
    df['ARRTIME'] = df['ARRTIME'].apply(lambda x: 60*(x//100) + x%100) 
    #make MSA a dummy var
    df['MSA'] = df['MSA'].apply(lambda x: x-1) 
    df = df[df['PAINSCALE'] >= 0]
    #generate avg waittime for every hosiptal
    df.loc[:,'AVGWAIT'] = df.loc[:,'WAITTIME'].groupby(df.loc[:,'HOSPCODE']).transform('mean')

    #generate dummy var for month and day of the week
    dummies = pd.get_dummies(df['VMONTH']).rename(columns=lambda x: 'MONTH' + str(x))
    dummies.columns = MONTHS
    df = pd.concat([df, dummies], axis=1)
    df.drop(['VMONTH'], inplace=True, axis=1)

    dummies = pd.get_dummies(df['VDAYR']).rename(columns=lambda x: 'DAY' + str(x))
    dummies.columns = WDAY
    df = pd.concat([df, dummies], axis=1)
    df.drop(['VDAYR'], inplace=True, axis=1)
    return df


def split_data(dataset, indepv=ALLVAR):
    '''
    dataset: data frame of nhamcs data, cleaned
    '''
    y = dataset["WAITTIME"]
    x = dataset[indepv]

    # get train/test data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)


    # fit a OLS model
    ols = linear_model.LinearRegression()
    ols_model = ols.fit(x_train, y_train)
    predictions = ols.predict(x_test)

    #print('predictions', predictions)

    # plot
    plt.scatter(y_test, predictions)
    plt.xlabel("True Values")
    plt.ylabel("Predictions")
    plt.axis()
    plt.show()

    print('OLS Score:', ols_model.score(x_test, y_test), ols_model.score(x_train, y_train))
    #return predictions, x_test, y_test


def kernel_reg(df, indepv=VAR, bw=5):
    '''
    Make various KDEs that using 3 different kernels and bandwidths 
    
    Inputs:
        df: pandas dataframe
        indepv: (a list) of strings of the indepedent variable names
        bw: (float) bandwidth
        
    Returns: the plot graph
    '''
    y = df["WAITTIME"]
    x = df[indepv]
    x_train, x, y_train, y = train_test_split(x, y, test_size = 0.3)

    # kernel density estimations
    kernel='epanechnikov'
    kde = KernelDensity(kernel=kernel, bandwidth=bw).fit(x)
    plt.plot(y, np.exp(kde.score_samples(x)), label='%s, bw=%s' % (kernel, bw))
    plt.legend(loc=0)

    kernel='gaussian'
    kde = KernelDensity(kernel=kernel, bandwidth=bw).fit(x)
    plt.plot(y, np.exp(kde.score_samples(x)), label='%s, bw=%s' % (kernel, bw))
    plt.legend(loc=0)

    kernel='tophat'
    kde = KernelDensity(kernel=kernel, bandwidth=bw).fit(x)
    plt.plot(y, np.exp(kde.score_samples(x)), label='%s, bw=%s' % (kernel, bw))
    plt.legend(loc=0)

    plt.show()