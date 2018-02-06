# Alyssa Harker
# 2/3/18
# own code unless specified

# references: pa5 from CS122, 
# https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6

import nhamcs
import numpy as np
import pandas as pandas
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt


def clean_data(dataset):
	'''
	clean nhamcs data
	'''
	'''
	# clean IMMEDR
	# -9 blank, -8 unknown, 0 and 7 no triage, 1-5
	dataset['IMMEDR'] = dataset['IMMEDR'].replace([-9, -8, 7, 0], np.nan)

	# PAINSCALE -9 blank, -8 unknown, 1-10
	# -9 blank, -8 unknown, 1 yes 2 no others
	dataset[['PAINSCALE', 'AMBDIV', 'PHYSPRACTRIA', 'FASTTRAK']] = dataset[
		['PAINSCALE', 'AMBDIV', 'PHYSPRACTRIA', 'FASTTRAK']].replace(
		[-9, -8], np.nan)
	# -9 blank, -8 unknown, -7 Not applicable, 5 not available. 2-4
	dataset['TOTHRDIVR'] = dataset['TOTHRDIVR'].replace([-9, -8, -7, 5], np.nan)
	'''
	# remove data that doesn't have wait time recorded
	# -9 is blank, -7 not applicable
	values = dataset[dataset['WAITTIME'] >= 0].copy()
	values.loc[:,'AVGWAIT'] = values.loc[:,'WAITTIME'].groupby(values.loc[:,'HOSPCODE']).transform('mean')

	clean_data = values
	target = values['WAITTIME']

	return clean_data, target


def split_data(dataset, parameters, target):
	'''
	dataset: data frame of nhamcs data, cleaned
	'''
	df = dataset[parameters]
	# set target variable
	y = dataset[target]

	# get train/test data
	x_train, x_test, y_train, y_test = train_test_split(df, y, test_size = 0.3)

	# fit a model
	lm = linear_model.LinearRegression()
	model = lm.fit(x_train, y_train)
	predictions = lm.predict(x_test)

	#print('predictions', predictions)

	# plot
	plt.scatter(y_test, predictions)
	plt.xlabel("True Values")
	plt.ylabel("Predictions")
	plt.axis([0, 200, 0, 200])
	plt.show()

	print('Score:', model.score(x_test, y_test), model.score(x_train, y_train))
	#return predictions, x_test, y_test


def explore_data(data, group, x, y):
	'''
	Plot to see potential relationships
	'''
	fig, ax = plt.subplots()

	for key, grp in data.groupby(group):
		ax = grp.plot(ax = ax, kind = 'line', x = x, y = y, label = key)

	plt.legend(loc = 'best')
	plt.show()
