import datetime
import matplotlib.pyplot as plt, pandas as pd, os, matplotlib.dates as mdates

def create_plot(date: str) -> None:
    """
    Create plot from daily solar data.

    Args:
        date (str): Date of the day on which the plot is to be created.
    """

    path = os.path.join(os.getcwd(), 'data', date)
    df_path = os.path.join(path, f'{date}.pickle')

    data = pd.read_pickle(df_path)

    plt.figure(figsize=(16,9), dpi=150)
    plt.plot(data['Time'], data['PAC(W)'], color='skyblue')
    plt.title(f"Production and heater usage over the hours {date}")
    plt.xlabel('Hour')
    plt.ylabel('Wattage')
    plt.ylim([min(data['PAC(W)']), max(data['PAC(W)']) + 100])
    # plt.xlim(data['Time'][len(data)-1], data['Time'][0])
    plt.fill_between(data['Time'],
                     data['PAC(W)'],
                     color='skyblue',
                     label='Production')
    plt.fill_between(data['Time'],
                     y1=0,
                     y2=2000,
                     color='orange',
                     where=data['PAC(W)'] > 2000,
                     label='Heater usage')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz='UTC+2'))
    plt.savefig(os.path.join(path, f'{date}.png'))


if __name__ == '__main__':
    create_plot(str(datetime.date.date()))