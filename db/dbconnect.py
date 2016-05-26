import sqlite3


DB_NAME = 'skfgi.db'
connection = sqlite3.connect(DB_NAME)

def connect():
	return connection