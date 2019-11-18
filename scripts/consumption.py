import pandas as pd
import matplotlib.pyplot as plt

# TODO: visualize the daily consumption
# TODO: add stats analysis using scipy
# (https://docs.scipy.org/doc/scipy/reference/stats.html)


def visualize(data, x, y, king='line'):
    ax = data.plot(kind='line', x=x, y=y)
    # Set the x-axis label
    ax.set_xlabel("Date")
    # Set the y-axis label
    ax.set_ylabel("Consumption (MW)")
    plt.show()


def getDailyData(data):
    # TODO: get daily values per hour
    res = {}
    print(data.groupby(['Date']).mean())
    for value in data.groupby(['Date']).mean().itertuples():
        pass  # print(value)
    # for row in data.groupby(['Date']).mean():

        # res[''] =
        # pass


def getExtremums(data, key):
    print(type(data))
    return (min(data[key]), max(data[key]))


def getData(filepath, delimiter=';'):
    return pd.read_csv(filepath, delimiter=delimiter)


def main():
    fp = '../Datasets/ProdConso/eco2mix-regional-tr.csv'
    data = getData(fp)

    print(getExtremums(data, 'Consommation (MW)'))

    getDailyData(data)

    visualize(data, 'Date', 'Consommation (MW)')

if __name__ == '__main__':
    main()
