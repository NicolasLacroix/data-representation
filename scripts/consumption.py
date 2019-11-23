import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import dateutil.parser
from datetime import datetime

# TODO: add min/max visualization
# TODO: make a pie chart
# TODO: add stats analysis using scipy
# (https://docs.scipy.org/doc/scipy/reference/stats.html)


def visualize(data, x, y=None, subplots=False, kind='line'):
    if not y:
        ax = data.plot(subplots=subplots, kind=kind, x=x)
    else:
        ax = data.plot(subplots=subplots, kind=kind, x=x, y=y)
    plt.show()


def getDailyData(data, *args):
    if len(args) == 0:
        raise ValueError('args must be non-empty')
    param = []
    for elem in args:
        if type(elem) is list:
            param += elem
        else:
            param.append(elem)
    res = {}
    for date, values in data.groupby(['Date']):
        res[date.strftime('%Y-%m-%d')] = values[param]
    return res


def getExtremums(data, key):
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
    data['Date'] = pd.to_datetime(data['Date'])
    data['Heure'] = pd.to_datetime(data['Heure'], format='%H:%M')
    data[
        'Date - Heure'] = pd.to_datetime(data['Date - Heure'], format='%Y-%m-%dT%H:%M:%S')

    volumeLabels = list(data.columns.values)[7:14]
    percentLabels = list(data.columns.values)[15:-1]

    print(getExtremums(data, 'Consommation (MW)'))

    dailyData = getDailyData(data, 'Date - Heure', volumeLabels)
    print(dailyData['2019-10-01']['Date - Heure'])

    visualize(dailyData['2019-10-02'], 'Date - Heure',
              subplots=False, kind='line')

if __name__ == '__main__':
    main()
