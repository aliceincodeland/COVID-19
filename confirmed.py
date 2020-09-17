"""
This code reads the currently available data on Covid-19 from github and plots the time series of the number of
daily confirmed cases in a country or a region of interest.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def mov_avg(some_vector, d):
    movingavg = []
    for j in range(d - 1, len(some_vector)):
        movingavg.append(round(some_vector[j - d + 1:j].sum() / d))

    return movingavg

# Specify the github url where the data in .csv format is located. Read the data as a pandas DataFrame
# object 'dt'. Convert it to a numpy array 'arr' for vectorized processing. The entries corresponding
# to all dates from 1/22/2020 till today are stored in a vector 'dates'
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
      'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
dt = pd.read_csv(url, sep=',', header=None)
arr = dt.values
dates = arr[0][4:]

month_beginning_indices = [i for i in range(len(dates)) if '/1/' in dates[i]]  # Indices for the first day of each month
# to be used for labelling the ticks on the X-axis

EU_list = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Republic of Cyprus', 'Czech Republic', 'Denmark',
           'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia',
           'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
           'Slovenia', 'Spain', 'Sweden']

# Initialize the vector 'cumul_confirm_EU' where the total number of confirmed cases across all EU countries
cumul_confirm_EU = np.zeros(len(dates))
for i in range(1, len(arr)):
    if arr[i][1] in EU_list:
        int_arr = list(map(int, arr[i][4:]))
        cumul_confirm_EU = np.add(cumul_confirm_EU, int_arr)

# Convert the vector of the cumulative number of cases to an integer list
cumul_confirm_EU = list(map(int, cumul_confirm_EU))

# The number of confirmed cases on a daily basis would be the consecutive differences of the daily number of
# cumulative cases.
daily_confirms_EU = np.diff(cumul_confirm_EU)

# Calculate the moving average over number_of_days to make the plot look smoother
number_of_days = 7
moving_avg = mov_avg(daily_confirms_EU, number_of_days)

# Plot the time progression of daily confirmed cases
my_plot = plt.subplot(111)
my_plot.plot(dates[6:6+len(moving_avg)], moving_avg, 'r-')
my_plot.spines['left'].set_visible(False)
my_plot.spines['right'].set_visible(False)
my_plot.spines['top'].set_visible(False)
my_plot.spines['bottom'].set_position(('data', 0.0))
my_plot.get_yaxis().set_visible(False)

my_plot.set_xticks(month_beginning_indices)
my_plot.set_xticklabels(['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept'])
my_plot.set_xlabel('EU', fontsize=13)
my_plot.set_title('Total Cases: ' + str(cumul_confirm_EU[-1]) + '\n' + '  Recent/New Day: '
                  + str(daily_confirms_EU[-1]), {'fontsize': 10}, y=-0.2)
plt.tight_layout(h_pad=1.0)
# cursor(hover=True) # Can be switched ON for reading data interactively from the plot.
plt.show()
