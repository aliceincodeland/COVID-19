'''
This code reads the currently available data on Covid-19 from github and plots the number of daily
confirmed cases and daily deaths in a given country or region.
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def mov_avg(some_vector, d):
    movingavg = []
    for j in range(d - 1, len(some_vector)):
        movingavg.append(round(some_vector[j - d + 1:j].sum() / d))

    return movingavg


def prepare_data_for_plot(topic, country, moving_avg_window):
    if topic == 'd':
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
              'csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    elif topic == 'c':
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
              'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

    dt = pd.read_csv(url, sep=',', header=None)  # , skiprows=0)
    arr = dt.values
    dates = arr[0][4::]
    month_beginning_indices = [i for i in range(len(dates)) if '/1/' in dates[i]]

    EU_list = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Republic of Cyprus', 'Czech Republic', 'Denmark',
               'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia',
               'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
               'Slovenia', 'Spain', 'Sweden']
    if country.casefold() == 'EU'.casefold():
        country = EU_list
    # Initialize the vector 'cumul_confirm_EU' where the total number of confirmed cases across all EU countries
    # will be calculated and stored.
    cumul_numbers = np.zeros(len(dates))
    for i in range(1, len(arr)):
        try:
            if arr[i][1].casefold() in country.casefold():
                int_arr = list(map(int, arr[i][4::]))  # Converting elements of arr to integer list
                cumul_numbers = np.add(cumul_numbers, int_arr)
        except AttributeError:
            #print('Proceeding for EU')
            if arr[i][1] in country:
                int_arr = list(map(int, arr[i][4::]))  # Converting elements of arr to integer list
                cumul_numbers = np.add(cumul_numbers, int_arr)

    # Convert the vector of the cumulative number of cases to an integer list
    cumul_numbers = list(map(int, cumul_numbers))
    total_cases = cumul_numbers[-1]
    # The number of confirmed cases on a daily basis would be the consecutive differences of the daily number of
    # cumulative cases.
    daily_numbers = np.diff(cumul_numbers)
    moving_avg = mov_avg(daily_numbers, moving_avg_window)

    return dates, moving_avg, month_beginning_indices, total_cases


# Specify the github url where the data in .csv format is located. Read the data as a pandas DataFrame
# object 'dt'. Convert it into a numpy array 'arr' for vectorized processing. The entries corresponding
# to all dates from 1/22/2020 till today are stored in a vector 'dates'

country = input('Enter the country name: ')
# topic = input('Enter d or c for data on deaths or confirmed cases respectively :')
# print(month_beginning_indices)
moving_avg_window = int(input('Enter the number of days over which the moving average is to be calculated: '))

dates, moving_avg_confirmed, month_beginning_indices, total_confirms = prepare_data_for_plot('c', country, moving_avg_window)
dd, moving_avg_deaths, mm, total_deaths = prepare_data_for_plot('d', country, moving_avg_window)
#print('Total Covid-19 deaths in EU from Feb till Sept 2020 = ', sum(moving_avg_deaths))

# Plot the time progression of daily confirmed cases
my_plot = plt.subplot(111)
my_plot.set_title('Covid-19 in ' + country)  # ('Covid-19 deaths in EU')
color = 'tab:red'
my_plot.set_ylabel('daily confirmed cases', color=color)
my_plot.spines['left'].set_color(color)
my_plot.tick_params(axis='y', colors=color)
my_plot.plot(dates[moving_avg_window - 1:moving_avg_window - 1 + len(moving_avg_confirmed)],
             moving_avg_confirmed, 'r-')

# Creating the second Y-axis for daily deaths on the same plot
my_plot2 = my_plot.twinx()  # instantiate a second axes that shares the same x-axis

color = 'k'
my_plot2.set_ylabel('daily deaths', color=color, fontsize=12)  # we already handled the x-label with ax1
my_plot2.plot(dates[moving_avg_window - 1:moving_avg_window - 1 + len(moving_avg_deaths)],
              moving_avg_deaths, color=color)
# my_plot.plot(dates[moving_avg_window-1:moving_avg_window-1+len(moving_avg_deaths)],
# moving_avg_deaths, 'k-')
my_plot.spines['left'].set_visible(False)
my_plot.spines['right'].set_visible(False)
my_plot.spines['top'].set_visible(False)
# my_plot.get_yaxis().set_visible(False)

my_plot.set_xticks(month_beginning_indices)
my_plot.set_xticklabels(['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept'])
my_plot.set_xlabel('Total Deaths: ' + str(total_deaths) + ',  Total Confirmed Cases: ' +
                   str(total_confirms) + ',   Ratio = ' + str(total_deaths/total_confirms))

plt.show()
