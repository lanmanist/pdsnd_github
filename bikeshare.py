import time 
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    cities = ['chicago', 'new york city', 'washington']
    city = input('Would you like to see the data for Chicago, New York City, or Washington: \n').lower()
    while city not in cities:
        city = input('Invalid city. Please enter city again: ').lower()

    # ask if users want to filter the data by month, day, or both
    answer = input("Would you like to filter the data by month, day, both, or not at all. Type month, day, both or none: \n").lower()
    valid_answers = ['month', 'day', 'both', 'none']
    while answer not in valid_answers:
        answer = input("Invalid input. Please choose again the filter by month, day, both, or none: ").lower()

    if answer == 'month':
    # get user input for month (all, january, february, ... , june)
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input('Enter month: ').lower()
        while month not in months:
            month = input('Invalid month. Please enter again: ').lower()
        day = 'all'
    elif answer == 'day':
    # get user input for day of week (all, monday, tuesday, ... sunday)
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        day = input('Enter day of week: ').lower()
        while day not in days:
            day = input('Invalid day. Please enter again: ').lower()
        month = 'all'
    elif answer == 'both':
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input('Enter month: ').lower()
        while month not in months:
            month = input('Invalid month. Please enter again: ').lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        day = input('Enter day of week: ').lower()
        while day not in days:
            day = input('Invalid day. Please enter again: ').lower()
    elif answer == 'none':
        month = 'all'
        day = 'all'

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city]) # Load data file into dataframe
    df['Start Time'] = pd.to_datetime(df['Start Time']) # Convert the Start Time column to datetime
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month] # Filter by input month

    if day != 'all':
        df = df[df['day_of_week'] == day.title()] # Filter by day of week

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f'The most common month: {most_common_month}')

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f'The most common day: {most_common_day}')

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print(f'The most common start hour: {most_common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f'The most common start station: {most_common_start_station}')

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f'The most common end station: {most_common_start_station}')

    # display most frequent combination of start station and end station trip
    df['start_and_end_stations'] = 'From ' + df['Start Station'] + ' to ' + df['End Station']
    most_common_combo = df['start_and_end_stations'].mode()[0]
    print(f'The most frequent combination of start and end station strip: {most_common_combo}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    travel_time_fixed = time.gmtime(travel_time)
    travel_time_final = time.strftime("%H:%M:%S", travel_time_fixed)
    print(f'Total travel time: {travel_time_final}')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_fixed = time.gmtime(mean_travel_time)
    mean_travel_time_final = time.strftime("%H:%M:%S", mean_travel_time_fixed)
    print(f'Mean travel time: {mean_travel_time_final}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(user_type_count)
    print("\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
        print("\n")
    else:
        print('Gender data doesn\'t exist')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        print(f'Earliest year of birth: {earliest}')

        latest = df['Birth Year'].max()
        print(f'Latest year of birth: {latest}')

        most_common_year = df['Birth Year'].mode()[0]
        print(f'Most common year of birth {most_common_year}')
    else:
        print('Birth data doesn\'t exists')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_data(df):
    # ask if user wants to see 5 rows of raw data
    view_data = input('Do you want to see 5 rows of data? (Answer yes / no): \n').lower()
    valid_answers = ['yes', 'no']

    while view_data not in valid_answers:
        view_data = input('Do you want to see 5 rows of data? (Answer yes / no): \n').lower()

    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:(start_loc + 5)])
        start_loc += 5
        view_data = input('Do you wish to see the next 5 rows? (Answer yes / no) \n').lower()
        if view_data == 'no':
            break
        else:
            view_data = 'yes'

    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
