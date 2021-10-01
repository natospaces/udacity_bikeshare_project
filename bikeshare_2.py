import time
import pandas as pd
import numpy as np
from itertools import chain, repeat
import csv
import sqlite3
import json
from datetime import datetime

CITY_DATA = { 'chicago': '3',
              'new york': '1',
              'washington': '2' }

is_yes_no_dict = {'1':'Yes','2':'No'}
month_filter = {'-1':'None','0':'All','1':'January','2':'February','3':'March', '4':'April','5':'May','6':'June'}
day_filter = {'-1':'None','0':'All','1':'Sunday','2':'Monday','3':'Tuesday','4':'Wednesday','5':'Thursday',\
              '6':'Friday','7':'Saturday'}
selected_city = []

def get_input_with_validation(input_prompt_message,options):
    """
    Takes a message to be used as in input prompt in the command line
    and dictionary which will be used to validate the user input
    
    if user enters an incorrect option it loops till they enter a correct one

    Returns:
        (str) correct_response - selection that matches of the dictionary keys
    """

    input_error = "Incorrect Selection"
    prompt = chain([input_prompt_message], repeat(' '.join([input_error, input_prompt_message])))
    replies = map(input, prompt)
    correct_response = next(filter(lambda x: False if options.get(str(x).lower()) == None else True, replies))
    return correct_response.lower()
    

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Hiya Let's explore US bikeshare data
    # Select city Chicago,NY or Wash
    input_city_greeting = "Please type the city name for analysis : Chicago, \
New York or Washington \n"
    city = get_input_with_validation(input_city_greeting,CITY_DATA)
    
    # get user input for month (all, january, february, ... , june)
    input_is_month_message = "Would you like to filter by month? Type number next \
to your choice (1=Yes,2=No)\n"
    is_month = get_input_with_validation(input_is_month_message,is_yes_no_dict)
    
    if is_month == '1':
        input_month_message = """To select by all months type 0\n or for a particular \
month type appropriate integer(1=Jan,2=Feb,3=Mar,4=Apr,5=May,6=Jun)\n"""
        month = get_input_with_validation(input_month_message,month_filter)
    else:
        month = '-1'

    # get user input for day of week (all, monday, tuesday, ... sunday)

    input_is_day_message = "Would you like to filter by day? Type number next to \
your choice (1=Yes,2=No)\n"
    is_day = get_input_with_validation(input_is_day_message,is_yes_no_dict)
    
    if is_day == '1':
        input_day_message = """To select by all day type 0\nor for a particular day \
type appropriate integer(1=Sun,2=Mon,3=Tue,4=Wed,5=Thu,6=Fri,7=Sat)\n"""
        day = get_input_with_validation(input_day_message,day_filter)
    else:
        day = '-1'
        

    print("-"*40)
    selected_city.append(city.lower())
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
    sqlcon = sqlite3.connect("udabikeshare.db")
    
    main_select = """ SELECT   c.[Start Time]
                              ,c.[End Time]
                              ,c.[Duration]
                              ,c.[Start Station]
                              ,c.[End Station]
                              ,c.[User Type]
                              ,c.[Gender]
                              ,c.[Birth Year]
                      FROM    t_trip_cities c
                """
    
    city_filter = " where city_id = " + str(CITY_DATA.get(city.lower()))
        
    if month == '-1' or month == '0':
        month_filter = ""
    else:
        month_filter = " and substr([Start Time],4,2) = '0" + month + "'"
        
    if day == '-1' or day == '0':
        day_filter = ""
    else:
        day_filter = " and strftime('%w',(substr([Start Time],7,4) || '-'\
|| substr([Start Time],4,2) || '-' || substr([Start Time],1,2)\
|| case when substr([Start Time],12,1) in ('1','2') then substr([Start Time],11) else ' 0'\
|| substr([Start Time],12)  end)) = '" + str((int(day)) - 1) + "' ;"
    
    #print statement below shows the generated sql query
    #print(main_select + city_filter + month_filter + day_filter)
        
    df = pd.read_sql_query(main_select + city_filter + month_filter + day_filter, sqlcon)
    df['Start Time'] = pd.to_datetime(df['Start Time']).dt.strftime("%m/%d/%Y %H:%M")
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Start Year Month Name'] = df['Start Time'].dt.month_name()
    df['Start Year Week Day Name'] = df['Start Time'].dt.day_name()
    df['Start Year Hour'] = df['Start Time'].dt.hour
    
    df['Start Time'] = pd.to_datetime(df['Start Time']).dt.strftime("%m/%d/%Y %H:%M")
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['Birth Year'] = pd.to_numeric(df['Birth Year'], downcast ='integer',errors='coerce')
    if df['Birth Year'].isnull().values.all(axis=0):
        df = df.drop('Birth Year', 1)

    if df.loc[(df.Gender != "null")].size == 0:
        df = df.drop('Gender', 1)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCALCULATING ::  TIMES OF TRAVEL FREQUENCY")
    print("--"*21)
    start_time = time.time()

    # display the most common month
    print("\n Most Frequent Month : {month_name}".format(month_name=df['Start Year Month Name'].mode()[0]))

    # display the most common day of week
    print("\n Most Frequent Day   : {day_name}".format(day_name=df['Start Year Week Day Name'].mode()[0]))

    # display the most common start hour
    print("\n Most Frequent Hour  : {hour}".format(hour=df['Start Year Hour'].mode()[0]))
 
    print("\n"+("-"*40)+("*"*20))
    print("\nFrequency Stats Operations took %s seconds to execute." % (time.time() - start_time))
    print("-"*85)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCALCULATING ::  TOP STATIONS AND TRIPS")
    print("--"*19)
    start_time = time.time()

    # display most commonly used start station
    print("\n Top Start Station              : {top_start}\
".format(top_start=df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("\n Top End Station                : {top_end}\
".format(top_end=df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("\n Top Trip Combination Stations  : {top_combination}\
".format(top_combination=df['Start Station'].str.cat(df['End Station'], sep=' to ').mode()[0]))
    

    print("\n"+("-"*40)+("*"*20))
    print("\nThe Top Stations and Trips Operations took %s seconds to execute." % (time.time() - start_time))
    print("-"*85)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCALCULATING :: TRIP DURATION SUM AND MEAN")
    print("--"*21)
    start_time = time.time()

    # display total travel time
    print("\nTotal Trip Duration  : {hours} hours, {mins} minutes and {secs} \
seconds. ".format(hours=divmod(divmod(df['Duration'].sum(),60)[0],60)[0],\
                  mins = divmod(df['Duration'].sum(),60)[0],secs=divmod(df['Duration'].sum(),60)[1]))
    # display mean travel time
    print("Mean Trip Duration   : {mins} minutes and {secs} \
seconds. ".format(mins=divmod(df['Duration'].mean(), 60)[0],secs=divmod(df['Duration'].mean(), 60)[1]) \
          if divmod(df['Duration'].mean(), 60)[0]<60 else "Mean Trip Duration  : {hours} hours, {mins} \
minutes and {secs} seconds. ".format(hours=divmod(divmod(df['Duration'].mean(), 60)[0], 60)[0],\
                                     mins=divmod(divmod(df['Duration'].mean(), 60)[1], 60)[1],\
                                     secs=divmod(df['Duration'].mean(), 60)[0]))

    print("\n"+("-"*40)+("*"*20))
    print("\nTrip Duration Operations took %s seconds to execute." % (time.time() - start_time))
    print("-"*85)
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCALCULATING :: USER STATS")
    print("--"*13)
    start_time = time.time()

    # Display counts of user types
    print("\nUSER TYPE Counts - if User Type Column is empty that indicates null \
or empty values\n\n{user_type}\
".format(user_type=df['User Type'].value_counts().rename_axis('User Type').to_frame('Total')))

 
    # Display earliest, most recent, and most common year of birth
    if 'Gender' in df.columns:
        # Display counts of gender
        print("\n")
        #setting the dropna parameter to False ensures null value counts are displayed
        print("GENDER Counts - if Gender Column is empty that indicates null or empty values \n\n{gender_type}\
".format(gender_type=df['Gender'].value_counts(dropna=False).rename_axis('Gender').to_frame('Total')))
    else:
        print("\nUnfortunately {selected_city} has no Gender Stats".format(selected_city=selected_city[0].capitalize()))

        
    if 'Birth Year' in df.columns:
        print('BYear')
#         print("\nCALCULATING :: Birth Year Stats: Earliest Year -> " + str(int(df['Birth Year'].min())) + \
#           " , Most Recent Year -> " + str(int(df['Birth Year'].max())) + " , \
# Most Common Year -> " + str(int(df['Birth Year'].mode()[0])))
    else:    
        print("\nUnfortunately {selected_city} has no Birth Year Stats".format(selected_city=selected_city[0].capitalize()))
    print("\n"+("-"*40)+("*"*20))
    print("\nUser and Birth Year Stats Operations took %s seconds to execute." % (time.time() - start_time))
    print("-"*85)


def individual_rows_stats(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param (df): Filtered data frame.
    """
    input_row_by_row_message = "Would you like to view 5 rows of individual trip data?  Select 1 or 2  (1=Yes,2=No)\n"
    is_row = get_input_with_validation(input_row_by_row_message,is_yes_no_dict)
    print("\nPrinting the first 5 rows of the filtered data")
    
    if is_row == '1':
        total_rows = len(df.index)
        index = 0
        increment = 5
        while index < total_rows:
            print(df.iloc[index:index+increment,])
            is_row = get_input_with_validation("Do you wish to continue viewing the data? Select 1 or 2 (1=Yes,2=No)\n",is_yes_no_dict)
            if is_row == '2':
                break
            index = index + increment
    else:
        print("not paging")

    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_rows_stats(df)
        selected_city.clear()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':       
            break

if __name__ == "__main__":
	main()
