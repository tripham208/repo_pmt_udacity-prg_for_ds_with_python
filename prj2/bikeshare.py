import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH = ['january', 'february', 'march', 'april', 'may', 'june']
DAY = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
CHOICE = ['yes', 'no']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter the city you want (chicago, new york city, washington): ')
    city = city.lower()
    while city not in CITY_DATA:
        city = input('Invalid city name. Try Again: ')
        city = city.lower()

    # get user input for month (all, january, february, ... , june)

    month = input('Enter the month (all, january, february, ... , june) : ')
    month = month.lower()
    while month not in MONTH and month != 'all':
        month = input('Invalid month name. Try Again: ')
        month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter the day from Monday to Sunday OR Enter "all" for no day filter : ')
    day = day.lower()
    while day not in DAY and day != 'all':
        day = input('Invalid day name. Try Again: ')
        day = day.lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # Filtering by month if applicable
    if month != 'all':
        df = df[df['month'] == MONTH.index(month) + 1]
    if day != 'all':
        df = df[df['day_of_week'] == DAY.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].mode()[0]

    print("most_month", most_month)

    print('Most Popular Month:', MONTH[most_month - 1])
    # display the most common day of week

    most_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular day of the week:', DAY[most_day_of_week])
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('most commonly used start station: ', df['Start Station'].mode()[0])

    # display most commonly used end station

    print('Most commonly used end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('most frequent combination of start station and end station trip:\n',
          df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user types:', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('counts of user types:', df['Gender'].value_counts())
    else:
        print('no gender column in data')

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        print('Earliest year of Birth:', int(df['Birth Year'].min()))
        print('Most recent year of Birth:', int(df['Birth Year'].max()))
        print('Most common year of Birth:', int(df['Birth Year'].mode()[0]))
    else:
        print('no Birth Year column in data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw = input('\nWould you like to show raw? Enter yes or no.\n')
        while show_raw not in CHOICE:
            show_raw = input('Invalid. Try Again: ')
            show_raw = show_raw.lower()

        if show_raw.lower() == 'yes':
            n = 0
            while True:
                if show_raw.lower() == 'yes':
                    print(df.iloc[n: n + 5])
                    n += 5
                    show_raw = input('\nWould you like to see more data? (Type:Yes/No): ')
                    while show_raw.lower() not in CHOICE:
                        show_raw = input('Please Enter Yes or No:')
                        show_raw = show_raw.lower()
                else:
                    break

        restart = input('\nWould you like to restart? Enter yes to restart or any to out: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
