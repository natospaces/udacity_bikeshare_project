import sqlite3

db_connection = sqlite3.connect('udabikeshare.db')

db_cursor = db_connection.cursor()

db_cursor.execute("""CREATE TABLE t_trip_cities(
	id               integer primary key,
	city_id          integer,
	city             text,
	[Start Time]     text,
	[End Time]       text,
	[Duration]       integer,
	[Start Station]  text,
	[End Station]    text,
	[User Type]      text,
	[Gender]         text,
	[Birth Year]     text)

""")

db_connection.commit()

db_connection.close()