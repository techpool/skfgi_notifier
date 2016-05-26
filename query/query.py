import sqlite3
import db.dbconnect as dbconnector
import json

def get_all_notice():
	connection = dbconnector.connect()
	cursor = connection.cursor()

	result = cursor.execute('SELECT * FROM notification')

	return result


def get_recent_notice():
	connection = dbconnector.connect()
	cursor = connection.cursor()

	result = cursor.execute('''SELECT * FROM notification ORDER BY updatetime DESC LIMIT 1''')

	return result

def get_n_recent_notice(limit=1):
	connection = dbconnector.connect()
	cursor = connection.cursor()

	result = cursor.execute('''SELECT * FROM notification ORDER BY updatetime DESC LIMIT ?''', (limit,))

	return result

