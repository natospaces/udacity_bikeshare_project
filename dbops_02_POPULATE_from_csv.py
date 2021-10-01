import csv
import sqlite3
# with open("new_york_city.csv",'r') as city:
#     reader = csv.reader(city)
#     for index, row in enumerate(reader):
#         irow =  '{} | {} | {} | {} | {} | {} | {} | {} | {}'.format(str(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
#         print(irow)
#         if index > 3:
#             break

con = sqlite3.connect("udabikeshare2.db")
cur = con.cursor()

CITY_DATA = { 'chicago': '3',
              'new_york_city': '1',
              'washington': '2' }

def insert_city(name):

    a_file = open(name+".csv")
    rows = csv.reader(a_file)
    next(rows)
    cur.executemany("""INSERT INTO t_trip_cities (city_id
    ,city
    ,[Start Time]
    ,[End Time]
    ,Duration
    ,[Start Station]
    ,[End Station]
    ,[User Type]
    ,Gender
    ,[Birth Year])  VALUES(?,?,?, ?,?, ?,?, ?,?,?) 
    """, rows)

for key in CITY_DATA:
    insert_city(key)
cur.execute("SELECT DiSTINCT city FROM t_trip_cities")


con.commit()
con.close()