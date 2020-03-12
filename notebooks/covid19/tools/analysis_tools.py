from pandas.plotting import register_matplotlib_converters

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from datetime import datetime

register_matplotlib_converters()

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
        country_data = d_data.groupby("Country/Region", as_index=False).agg(sum)
        country_data = country_data.loc[country_data['Country/Region'] == country]
        for column in country_data.columns[4:]:
            countryDict[d_name][datetime.strptime(column, '%m/%d/%y')] = country_data[column].values[0]
    return countryDict

def showCountryData(countries, dicts):
    fig = plt.figure(figsize=(10, 10))
    fig.suptitle('Covid19 evolution', fontsize=20)
    spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)

    axs = []
    axs.append(fig.add_subplot(spec[0, 0]))
    axs.append(fig.add_subplot(spec[0, 1], sharey=axs[-1]))
    axs.append(fig.add_subplot(spec[1, 0], sharex=axs[-1]))
    axs.append(fig.add_subplot(spec[1, 1], sharex=axs[-1]))

    for d, ax, c in zip(dicts, axs, countries):
        ax.plot(list(d['confirmed'].keys()), list(d['confirmed'].values()), color='b')
        ax.plot(list(d['death'].keys()), list(d['death'].values()), color='k')
        ax.plot(list(d['recovered'].keys()), list(d['recovered'].values()), color='g')
        #x_length = len(list(d['confirmed'].values()))
        #ax.plot(list(d['confirmed'].keys()), [math.exp(x) for x in range(x_length)], label='exponential', color='r')

        ax.set_title(c)
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of confirmed cases')
        ax.grid(True)
    return fig, axs
