import sqlite3
def connections():

	conn=sqlite3.connect("websiteloginusers.db")
	c=conn.cursor()
	return c,conn
