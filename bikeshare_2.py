import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
list_months = ("january","february","march","april","may","june","all")
list_days = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday","all")

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
    city = input('From which of following cities do you whish to know more: Chicago, New York or Washington: ').lower()

    while city not in CITY_DATA:
        city = input ("I am sorry, I do not recognize that city. Please make sure that you write it down correctly: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to select: January, February, March, April, May, June or all: ').lower()
    while month not in list_months:
        month = input("I am sorry, I do not recognize that month. Please make sure that you write it down correctly: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please let us know which spefic day you are looking for: ').lower()
    while day not in list_days:
        day = input("I am sorry, I do not recognize that day. Please make sure that you write it down correctly: ").lower()

    check = input("you entered the name the following: \nCity: {} \nMonth: {} \nDay: {} \n Is this correct?(Enter yes or no):".format(city, month, day)).lower()
    if check == "no":
        city = "abort"
        month = "abort"
        day = "abort"

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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # the option to see some raw data
    raw_data = input("Do you wish to see the raw data?(Enter yes or no): ").lower()
    while raw_data == "yes":
        print(df.sample(5))
        raw_data = input("Do you wish to see more data?(Enter yes or no): ").lower()

     # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = {1:"January", 2:"Februay", 3:"March", 4:"April", 5:"May",6:"June"}

    # display the most common month
    df["month"] = df["Start Time"].dt.month
    common_month = months[df["month"].mode()[0]]

    print("The most common month is,",common_month)

    # display the most common day of week
    df["day"] = df["Start Time"].dt.weekday_name
    common_day = df["day"].mode()[0]
    print("The most common day is,",common_day)

    # display the most common start hour
    df["start_hour"] = df["Start Time"].dt.hour
    common_hour = df["start_hour"].mode()[0]
    print("The most commom start hour is,", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df["Start Station"].mode()[0]

    # display most commonly used end station
    common_end = df["End Station"].mode()[0]

    # display most frequent combination of start station and end station trip
    df["both"] = df["Start Station"].str.cat(df[["End Station"]],sep= " & ")
    common_both = df["both"].mode()[0]


    print("The most commonly used start station is:",common_start)
    print("The most commonly used end station is:",common_end)
    print("The most frequent combination of the two is:",common_both)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df["Trip Duration"].sum()

    # display mean travel time
    mean_duration = df["Trip Duration"].mean()

    print("The total travel time was:",total_duration)
    print("The mean travel time was:",mean_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats_gender(df):
    """Displays statistics on bikeshare users, including gender and age."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df["User Type"].value_counts()

    # Display counts of gender
    gender_count = df["Gender"].value_counts()

    # Display earliest, most recent, and most common year of birth
    common_year = int(df["Birth Year"].mode()[0])
    earliest_year = int(df["Birth Year"].min())
    newest_year = int(df["Birth Year"].max())



    print("The number of users was:\n",user_count)
    print("The gender distribution was:\n",gender_count)
    print("The oldest user was born in:",earliest_year)
    print("The youngest user was born in:", newest_year)
    print("The most common year of birth is:",common_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats_nogender(df):
    """Displays statistics on bikeshare users, excluding gender and age."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df["User Type"].value_counts()

    print("The number of users was:\n",user_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        #checks if the user wants to abort
        if city == "abort":
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        else:

        #if not aborted, the program continues
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)

            #the washington file lacks the gender and age column.
            #if washington was selected a different this makes sure that the progrma doesn't crash

            if city != "washington":
                user_stats_gender(df)
            else:
                user_stats_nogender(df)
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
	main()
