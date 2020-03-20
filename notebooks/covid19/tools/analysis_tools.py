from pandas.plotting import register_matplotlib_converters

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy as np

from datetime import datetime

import math

register_matplotlib_converters()

def getCountryGroupedData(country, dataset):
    country_data = dataset.groupby("Country/Region", as_index=False).agg(sum)
    return country_data.loc[country_data['Country/Region'] == country]
    
def getDataFromDayZero(country, datasets, threshold=0):
    """
    Structure of return : 
    
    countryDict = {
        'confirmed' = {
            n: nb1,
            ...
        },
        'death' = {
            n: nb1,
            ...
        },
        'recovered' = {
            n: nb1,
            ...
        },
    }
    where n is the day number (from day zero)
    """
    dayZeroPos = -1
    countryDict = {}
    for d_name, d_data in datasets.items():
        countryDict[d_name] = {}
        country_data = getCountryGroupedData(country, d_data)
        if (dayZeroPos == -1):
            dayZeroPos = 4
            if (country_data.iloc[:, -1].values[0] < threshold):
                day_zeroPos = country_data.size
            else:
                while (country_data.iloc[:, dayZeroPos].values[0] < threshold):
                    dayZeroPos += 1
        day = 0
        for column in country_data.columns[dayZeroPos:]:
            countryDict[d_name][day] = country_data[column].values[0]
            day += 1
    return countryDict

def getCountryData(country, datasets):
    """
    Structure of return : 
    
    countryDict = {
        'confirmed' = {
            datetime(...): nb1,
            datatime(...): nb2
        },
        'death' = {
            datetime(...): nb1,
            datatime(...): nb2
        },
        'recovered' = {
            datetime(...): nb1,
            datatime(...): nb2
        },
    }
    """
    countryDict = {}
    for d_name, d_data in datasets.items():
        countryDict[d_name] = {}
        country_data = getCountryGroupedData(country, d_data)
        for column in country_data.columns[4:]:
            countryDict[d_name][datetime.strptime(column, '%m/%d/%y')] = country_data[column].values[0]
    return countryDict

def getPlotDimensions(labels):
    """
    returns the best (x,y) dimensions for plotting
    the data with given labels
    """
    size = len(labels)
    if (size == 1):
        return 1, 1
    n = 4
    while (math.ceil(size/n) == 1):
        n -= 1
    y = math.ceil(size/n)
    x = size-y
    return x, y

def showCountryData(dicts, day_zero=False):
    """
    returns the figure (fig) with its axis (axs)
    plotting dicts' data
    """
    countries = list(dicts.keys())
    nbCols, nbRows = getPlotDimensions(countries)
    fig = plt.figure(figsize=(10, 10))
    fig.suptitle('Covid19 evolution', fontsize=20)
    spec = gridspec.GridSpec(ncols=nbCols, nrows=nbRows, figure=fig)

    axs = []
    for x in range(nbRows):
        for y in range(nbCols):
            if (x == 0 and y == 0):
                axs.append(fig.add_subplot(spec[0, 0]))
            elif (not day_zero):
                axs.append(fig.add_subplot(spec[x, y], sharey=axs[x]))
            else:
                axs.append(fig.add_subplot(spec[x, y], sharex=axs[x], sharey=axs[x]))

    for d, ax, c in zip(dicts.values(), axs, countries):
        ax.plot(list(d['confirmed'].keys()), list(d['confirmed'].values()), color='b')
        ax.plot(list(d['death'].keys()), list(d['death'].values()), color='k')
        ax.plot(list(d['recovered'].keys()), list(d['recovered'].values()), color='g')

        ax.set_title(c)
        if (day_zero):
            ax.set_xlabel('Day')
        else:
            ax.set_xlabel('Date')
        ax.set_ylabel('Number of cases')
        ax.grid(True)
    return fig, axs
