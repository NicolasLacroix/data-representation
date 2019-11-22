import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
# TODO: visualize the daily consumption
# TODO: add stats analysis using scipy
# (https://docs.scipy.org/doc/scipy/reference/stats.html)


def visualize(data, x, y, kind='line'):
    ax = data.plot(subplots=True, kind=kind, x=x, y=y)
    plt.show()


def getDailyData(data):
    # TODO: get daily values per hour
    res = {}
    for date, values in data.groupby(['Date']):
        # day_values = values[['Date - Heure', 'Consommation (MW)']]
        res[date] = values[['Date - Heure', 'Consommation (MW)']]
    return res


def getExtremums(data, key):
    print(type(data))
    return (min(data[key]), max(data[key]))


def getData(filepath, delimiter=';'):
    return pd.read_csv(filepath, delimiter=delimiter)


def normalize(data):
    data = data.values
    uni_train_mean = data.mean()
    uni_train_std = data.std()
    data = (data - uni_train_mean) / uni_train_std


def main():
    fp = '../Datasets/ProdConso/eco2mix-regional-tr.csv'
    data = getData(fp)

    print(getExtremums(data, 'Consommation (MW)'))

    dailyData = getDailyData(data)

    print(dailyData)
    visualize(dailyData['2019-10-01'], 'Date - Heure',
              'Consommation (MW)')

if __name__ == '__main__':
    main()
