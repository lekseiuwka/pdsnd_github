import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months=['January', 'February', 'March', 'April', 'May', 'June','All']
days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']

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
    city=input('What city do you want to analyze? We have data for Chicago, New York City and Washington\n').lower()
    while (city not in CITY_DATA.keys()):
        city=input('Sorry, we don\'t have this city. Please choose hicago, New York City or Washington\n').lower()
    else:
        print('Ok, let\'s go with', city)

    # get user input for month (all, january, february, ... , june)
    month=input('Now let\'s choose the month for our data. We have data for January, February, March, April, May, June. Please choose the month, or type \'All\'\n').title()
    while (month not in months):
        month=input('Sorry, that\'s not an option. Please choose from January, February, March, April, May, June or type \'All\'\n').title()
    else:
        print('Ok, let\'s go with', month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Lastly let\'s choose the day of the week for our data. Please choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or type \'All\'\n').title()
    while (day not in days):
        day=input('Sorry, that\'s not an option. Please choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or type \'All\'\n').title()
    else:
        print('Ok, let\'s go with %s days' % day)

    print('-'*40)
    print('Thanks! Your filters are:',city,',',month,',',day)
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
    #loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    months=['January', 'February', 'March', 'April', 'May', 'June','All']
    days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #creating new columns month and day of the week from Start Time column
    df['month']=df['Start Time'].dt.month
    df['day']=df['Start Time'].dt.dayofweek
    df['hour']=df['Start Time'].dt.hour
    df['id']=df['Unnamed: 0']


    #filter by month
    if month != 'All':
        #using index from months list to get the corresponding int
        month=months.index(month)+1
        df=df[df['month']==month]
    else:
        df=df
    if day != 'All':
        day=days.index(day)+1
        df=df[df['day']==day]
    else:
        df=df

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months=['January', 'February', 'March', 'April', 'May', 'June']
    days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    # display the most common month
    most_popular_month=df['month'].mode()[0]
    print('The most popular month was', months[most_popular_month-1])

    # display the most common day of week
    most_popular_weekday=df['day'].mode()[0]
    print('The most popular day was', days[most_popular_weekday-1])

    # display the most common start hour
    most_popular_start_hour=df['hour'].mode()[0]
    print('The most common start hour was ', most_popular_start_hour)

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station=df['Start Station'].mode()[0]
    print('%s was the most common start station' % start_station.title())

    # display most commonly used end station
    end_station=df['End Station'].mode()[0]
    print('%s was the most common end station\n\n' % end_station.title())

    # display most frequent combination of start station and end station trip
    df['combination']='Start: '+df['Start Station']+' - End: '+df['End Station']
    combination=df['combination']
    print('The most common combination of stations was\n', combination.mode()[0], sep='')

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print ('Total trip duration is:', round((total_travel_time/60/60/24/365),2), 'years')

    # display mean travel time
    avg_travel_time=df['Trip Duration'].mean()
    print ('Avg trip duration is:', round((avg_travel_time/60),2), 'hours')

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    if  'Birth Year' in df:

        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_types=df['User Type'].value_counts().to_frame()
        print('\nHere is the user type distribution:\n\n',user_types.to_string(header=False),sep='')

        # Display counts of gender
        gender_types=df['Gender'].value_counts().to_frame()
        print('\nHere is the gender type distribution:\n\n',gender_types.to_string(header=False),sep='')

        # Display earliest, most recent, and most common year of birth
        common_y_b=int(df['Birth Year'].mode()[0])
        oldest=int(df['Birth Year'].min())
        yongest=int(df['Birth Year'].max())
        print('\nPlease find the data about birth years below:\n%s is the most common year of birth' % common_y_b)
        print('The oldest user was born in', oldest)
        print('And %s was the yongest' % yongest)

        print("\nThis took %s seconds." % round((time.time() - start_time),4))
        print('-'*40)
    else:
        print('Sorry, we don\'t have user data for this city')


def raw_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data=='yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input('Do you wish to continue? (yes/no):').lower()
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
