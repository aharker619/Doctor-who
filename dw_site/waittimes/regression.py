# Regression
#
# Tianchu Shu & Alyssa Harker
#
# kernel reg code gathered from 
#https://stats.stackexchange.com/questions/218514/how-to-decide-whether-a-kernel-density-estimate-is-good
#https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html
#https://www.kaggle.com/c/digit-recognizer/discussion/2299

import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import sklearn
from datetime import datetime
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.neighbors.kde import KernelDensity
from sklearn.ensemble import RandomForestClassifier

VAR = ['ARRTIME','AVGWAIT', 'MSA', 'PAINSCALE']
MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
WDAY = ['MON', 'TUE', 'WED', 'THUR', 'FRI','SAT', 'SUN']
indepv = WDAY + MONTHS + VAR

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
    df.drop(['HOSPCODE'], inplace=True, axis=1)
    df.drop(['YEAR'], inplace=True, axis=1)
    return df


def ols_reg(df):
    y = df["WAITTIME"]
    x = df[indepv]
    ols = linear_model.LinearRegression()
    ols_model = ols.fit(x, y)
    return ols_model


def rf(df):
    y = df["WAITTIME"]
    x = df[indepv]
    model = RandomForestClassifier(n_estimators=100)
    model.fit(x, y)
    return model


def user_time(df):
    '''
    get the realtime the user get put the zipcode and create the user input 
    for the random forest function
    '''
    inde = df[indepv]
    x = inde.loc[:4].copy()
    x = x.replace(x, 0) 
    user_time = datetime.now().timetuple()
    mon = user_time.tm_mon
    hour = user_time.tm_hour
    min_ = user_time.tm_min
    wday = user_time.tm_wday
    x["ARRTIME"] = hour * 60 + min_
    x[MONTHS[mon - 1]] = 1
    x[WDAY[wday]] = 1
    return x


###############################################################################
#The regressions we have tried...

def randomforest(df):
    y = df["WAITTIME"]
    x = df[indepv]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
    
    #create and train the random forest
    #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(x_train, y_train)
    predictions = rf.predict(x_test)
    # plot
    plt.scatter(y_test, predictions)
    plt.xlabel("True waittime")
    plt.ylabel("Predicted waittime")
    plt.axis()
    plt.show()

    print('RandomForest Score:', rf.score(x_test, y_test), rf.score(x_train, y_train))


def ols(dataset, indepv):
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

    # plot
    plt.scatter(y_test, predictions)
    plt.xlabel("True Values")
    plt.ylabel("Predictions")
    plt.axis()
    plt.show()

    print('OLS Score:', ols_model.score(x_test, y_test), ols_model.score(x_train, y_train))
    #return predictions, x_test, y_test


def logit(dataset, indepv):
    '''
    dataset: data frame of nhamcs data, cleaned
    '''
    y = dataset["WAITTIME"]
    x = dataset[indepv]

    # get train/test data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
    log = linear_model.LogisticRegression()
    log_model = log.fit(x_train, y_train)
    predictions = log_model.predict(x_test)

    # plot
    plt.scatter(y_test, predictions)
    plt.xlabel("True Values")
    plt.ylabel("Predictions")
    plt.axis()
    plt.show()

    print('Logit Score:', log_model.score(x_test, y_test), log_model.score(x_train, y_train))


def kernel_reg(df, bw=30, indepv="ARRTIME", kernel='gaussian'):
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
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

    train = pd.concat([x_train, y_train], axis=1)
    test = pd.concat([x_test, y_test], axis=1)
    #kernel density estimations

    # instantiate and fit the KDE model
    kde = KernelDensity(kernel=kernel, bandwidth=bw).fit(train)
    # score_samples returns the log of the probability density
    logprob = kde.score_samples(test)
    plt.scatter(y_test, logprob, label='%s, bw=%s' % (kernel, bw))
    plt.legend(loc=0)
    plt.show()
