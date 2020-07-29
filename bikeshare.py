import time
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)

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
    city = ''
    month = ''
    day = ''
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
    while city not in ['chicago', 'washington', 'new york city']:
        city = input('Which city would you like to explore? (Chicago, Washington or New York City)\n').lower()
        if city not in ['chicago', 'washington', 'new york city']:
            print('\nInvalid entry! Please choose one of the three cities.')

    # Get user input for month (all, january, february, ... , june)
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Would you like to explore a certain month from Jan-Jun? Type \'all\' for all months\n').lower()
        if month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print('\nInvalid entry! Please choose a month between January and June or type \'all\'.')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        day = input('Would you like to explore a certain weekday? Type \'all\' for all days\n').title()
        if day not in ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            print('\nInvalid entry! Please choose a valid weekday or type \'all\'.')

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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
        
    # Start Time column is converted to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
        
    # Month and day of week from Start Time are extracted to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # Monthly filter is applied
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 
        df = df[(df['month']) == month] 
    
    # Daily filter is applied
    if day != 'All': # Capital A important as input -> .title()
        df = df[df['day_of_week'] == day]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the most common times of travel...\n')
    start_time = time.time()

    # The most common month is identified
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month_number = int(df['Start Time'].dt.month.mode())
    most_common_month = months[month_number - 1]
    print('The most common...\n...month is {}.'.format(most_common_month))

    # The most common weekday is identified
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_number = int(df['Start Time'].dt.dayofweek.mode())
    most_common_day = days[day_number]
    print('...weekday is {}.'.format(most_common_day))

    # The most common start hour is identified
    most_common_hour = int(df['Start Time'].dt.hour.mode())
    print('...hour is {}'.format(most_common_hour) + ' o\'clock.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most common stations and trip...\n')
    start_time = time.time()

    # The most common start station is identified
    most_common_start = str(df['Start Station'].mode()[0])
    print('The most common...\n...start station is {}.'.format(most_common_start))

    # The most common end station is identified
    most_common_end = str(df['End Station'].mode()[0])
    print('...end station is {}.'.format(most_common_end))

    # The most common combination of start and end station is identified
    #df['start_end'] = df['Start Station'] + df ['End Station']
    #print(df)
    most_common_trip = str((df['Start Station'] + ' to ' + df ['End Station']).mode()[0])
    print('...trip is from {}.'.format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating total and mean trip duration...\n')
    start_time = time.time()

    # The total travel time is calculated
    total_duration = int(df['Trip Duration'].sum())
    m, s = divmod(total_duration, 60)
    h, m = divmod(m, 60)
    print('The total trip duration is {:d} hours, {:02d} minutes and {:02d} seconds.'.format(h, m, s))
    
    # The mean travel time is calculated
    mean_duration = int(df['Trip Duration'].mean())
    m, s = divmod(mean_duration, 60)
    h, m = divmod(m, 60)
    print('The mean trip duration is {:d} hours, {:02d} minutes and {:02d} seconds.'.format(h, m, s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def user_type_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user stats...\n')
    start_time = time.time()

    # User type counter
    user_types = df['User Type'].value_counts()
    print ('The split between subscribers and customers is:\n\n' + user_types.to_string(header=None, index=1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def user_gender_year_stats(df):

    start_time = time.time()
    
    # Male/Female counter seperately as Washington has no gender and birth data
    gender = df['Gender'].value_counts()
    print ('\nThe split between females and males is:\n\n' + gender.to_string(header=None, index=1))

    # Earliest, most recent, and most common year of birth are identified
    min_year = int(np.nanmin(df['Birth Year'])) # nanmin to exclude NaN
    print('\nThe earliest year of birth is {}'.format(min_year))
    
    min_year = int(np.nanmax(df['Birth Year'])) # nanmin to exclude NaN
    print('\nThe most recent year of birth is {}'.format(min_year))
    
    common_year = int(df['Birth Year'].mode())
    print('\nThe most common year of birth is {}'.format(common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Display of 5 lines of raw data until user says 'no'
    """
    df = df.drop(['month', 'day_of_week'], axis = 1) # removing columns which were added earlier
    start = 0
    end = 5
    choice = ''
    while choice.lower() not in ['yes', 'no']:
        choice = input('Do you want to see 5 lines of raw data? Enter yes or no.\n')
        if choice.lower() not in ['yes', 'no']:
            print('\nInvalid input, please try again')
        elif choice.lower() == "yes":
            print(df.iloc[start:end])
            while True:
                sec_choice = input('Do you want to see 5 more lines of raw data? Enter yes or no.\n')
                if sec_choice.lower() not in ['yes', 'no']:
                    print('\nInvalid input, please try again')
                elif sec_choice.lower() == "yes":
                    start += 5
                    end += 5
                    print(df.iloc[start:end])
                elif sec_choice == "no":
                    break
        elif choice.lower() == "no":
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_type_stats(df)
        if city.title() == 'New York City' or city.title() == 'Chicago':
            user_gender_year_stats(df)
        else: print('\nNo birth and gender statistics available for Washington!')
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()