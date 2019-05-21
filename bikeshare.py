import time
import numpy as np
import pandas as pd
import calendar as cal

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data.')
    # get user input for city (chicago, new york city, washington).
    city = input("Which city's bikeshare data do you want to explore (chicago, new york city or washington)?: ")
    city = city.lower().strip()

    while city not in ('chicago', 'new york city', 'washington'):
        city = input("Invalid input, please enter one of the following (chicago, new york city or washington): ")
        city = city.lower().strip()

    # get user input for month (all, january, february, ... , june)
    month = input("Month that you want to explore the data for ('all', 'january', 'february', 'march', 'april', 'may', 'june')?: ")
    month = month.lower().strip()

    while month.lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input("Invalid input, enter one of the following ('all', 'january', 'february', 'march', 'april', 'may', 'june'): ")
        month = month.lower().strip()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Day of the week that you want to explore the data for ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')?: ")
    day = day.lower().strip()

    while day.lower() not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input("Invalid input, enter one of the following ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'): ")
        day = day.lower().strip()
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for a specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if necessary
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if necessary
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df, month, day):
    """Displays statistics for the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if(month.lower() == 'all'):
        # display most common month
        df['month_num'] = df['Start Time'].dt.month
        df['month_name'] = df['month_num'].apply(lambda x: cal.month_abbr[x])
        popular_month = df['month_name'].value_counts().idxmax()
        print("Most popular month is: {}".format(popular_month))

        # display most common day of week
        df['day'] = df['Start Time'].dt.weekday_name
        common_day = df['day'].value_counts().idxmax()
        print("Most common day is: {}".format(common_day))

        # display most common start hour
        df['hour'] = df['Start Time'].dt.hour
        common_start_hour = df['hour'].value_counts().idxmax()
        print("Most common start hour is: {}".format(common_start_hour))
    else:
        # display most common start hour
        df['hour'] = df['Start Time'].dt.hour
        common_start_hour = df['hour'].value_counts().idxmax()
        print("Most common start hour for {} in the month {} is: {}".format(day.title(), month.title(), common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics for the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    #print(df['Start Station'].value_counts())
    print("Most commonly used start station is: \n  {}".format(common_start_station))
    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    #print(df['End Station'].value_counts())
    print("Most commonly used end station is: \n  {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    #print(("From: " + df['Start Station'] + " To: " + df['End Station']).value_counts())
    freq_start_end_station = ("\n  Start Station: " + df['Start Station'] + "\n  End Station: " + df['End Station']).value_counts().idxmax()
    print("Most frequent combination of start and end station is: {}".format(freq_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics for the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Duration: ",total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Average Duration: ",mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays the statistics for bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print("Count of user types:\n{}".format(count_user_types))

    if set(['Birth Year', 'Gender']).issubset(df.columns):
        # Display counts of gender
        count_gender = df['Gender'].value_counts()
        print("Gender count:\n{}".format(count_gender))

        # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].min()
        print("Youngest rider (Earliest year of birth): {}".format(earliest_year_of_birth))
        recent_year_of_birth = df['Birth Year'].max()
        print("Oldest rider (Most recent year of birth: {}".format(recent_year_of_birth))

        common_year_of_birth = df['Birth Year'].value_counts().idxmax()
        print("Most popular year of birth: {}".format(common_year_of_birth))
    else:
        print("No Birth Year and Gender information for {}".format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_data(df):

    user_input = user_input_trip_data()
    if user_input == 'no':
        return

    trip_data = df.to_dict('record')

    i, n = 0, 5
    for element in trip_data:
        print("Individual trip data, traveler {}\n".format(i+1))
        for key, value in element.items():
            print(str(key)+":"+str(value))
        print("\n")
        i += 1
        if i == n:
            user_input = user_input_trip_data()
            if user_input == 'yes':
                n = n + 5
                continue
            elif user_input == 'no':
                break

def user_input_trip_data():
    user_input = input("Would you like to see individual trip data? Type 'yes' or 'no': \n")
    user_input = user_input.lower().strip()

    while user_input not in ('yes', 'no'):
        user_input = input("Invalid input, please type 'yes' or 'no': \n")
        user_input = user_input.lower().strip()

    return user_input

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        individual_trip_data(df)

        restart = input('\nDo you want to restart? Enter yes or no.\n')
        if restart.lower().strip() != 'yes':
            break

if __name__ == "__main__":
	main()
