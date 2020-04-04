from __future__ import print_function
import pandas as pd
import pymysql
from datetime import date, datetime, timedelta

user = 'root'
password = 'yourdbpassword'
host = 'localhost'
database = 'covid19'

###### Step 1 #######
# download a timeseries of daily deaths per country
glob_death = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
deaths = pd.read_csv(glob_death)

###### Step 2 ######
# convert the table to appropriate format


def convert_df(df):
    df = df.drop(['Long', 'Lat'], axis=1)
    df = df.melt(id_vars=['Province/State', 'Country/Region'],
                 var_name='date', value_name='total')
    df.date = pd.to_datetime(df.date)
    df['Province/State'].fillna('all', inplace=True)
    df.total.fillna(0, inplace=True)
    df.columns = ['prov_state', 'country_region', 'date', 'total']

    return df


# convert the table so that each country and each day is a separate row
deaths = convert_df(deaths)
dates = deaths['date'].dt.floor('D')
dates = deaths['date'].dt.date

newDeath = deaths.drop(['prov_state'], axis=1)
newDeath = newDeath.groupby(['country_region', dates]).sum().reset_index()

###### Step 3 ######
# query to create deaths_total table
create_deathTotal = """CREATE TABLE IF NOT EXISTS `deaths_total` 
                        (`CountryRegion` varchar(16) NOT NULL, 
                        `CalDate` date NOT NULL, 
                        `Total` int(11) NOT NULL, 
                        PRIMARY KEY (`CountryRegion`, `CalDate`))"""
# insert query
insert_deathTotal = """INSERT IGNORE INTO `deaths_total` (`CountryRegion`, `CalDate`, `Total`) 
                        VALUES (%s, %s, %s)"""
# select deaths_total
select_deathTotal = "SELECT * FROM `deaths_total`"

# connect to database
conn = pymysql.connect(user=user, password=password,
                       host=host, database=database)
try:
    cursor = conn.cursor()

    # create deaths_total table
    cursor.execute(create_deathTotal)

    print("Inserting data to database")
    for i, row in newDeath.iterrows():
        cursor.execute(insert_deathTotal,
                       (row[0], row[1].strftime("%Y-%m-%d"), int(row[2])))
        conn.commit()
    print("Finish loading data to database")
finally:
    conn.close()

###### Step 4 ######
change = []
countries = newDeath.country_region.unique()

# calculate death change of each country
for country in countries:
    country_change = list(
        newDeath[newDeath['country_region'] == country].total.diff(periods=1))
    change += country_change

newDeath['daily_change'] = change
newDeath['daily_change'].fillna(0, inplace=True)

###### Step 5 ######
# query to create deathsChange table
create_deathChange = """CREATE TABLE IF NOT EXISTS `deaths_change_python` 
                        (`CountryRegion` varchar(16) NOT NULL,
                        `CalDate` date NOT NULL,
                        `Total` int(11) NOT NULL,
                        `DailyChange` int(11) NOT NULL,
                        PRIMARY KEY (`CountryRegion`, `CalDate`))"""
# insert query
insert_deathChange = """INSERT IGNORE INTO `deaths_change_python` 
                        (`CountryRegion`, `CalDate`, `Total`, `DailyChange`) 
                        VALUES (%s, %s, %s, %s)"""
# select deathChange query
select_deathChange = "SELECT * FROM `deaths_change_python`"

# connect to the database
conn = pymysql.connect(user=user, password=password,
                       host=host, database=database)
# load data to database
try:
    cursor = conn.cursor()

    # create deaths_change_python table
    cursor.execute(create_deathChange)

    print("Inserting data to database")
    for i, row in newDeath.iterrows():
        cursor.execute(insert_deathChange, (row[0], row[1].strftime(
            "%Y-%m-%d"), int(row[2]), int(row[3])))

        conn.commit()
    print("Finish loading data to database")
finally:
    conn.close()
