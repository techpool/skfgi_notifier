import sqlite3
import json
import db.dbconnect as dbconnector

def drop_table():
	conn = dbconnector.connect()
	cursor = conn.cursor()

	json_data = {}

	try:
		cursor.execute('''DROP TABLE notification''')
		json_data['status'] = "sucess"
	except sqlite3.OperationalError as e:
		json_data['status'] = "error"
		json_data['error'] = str(e)
	finally:
		conn.commit()

		json_data = json.dumps(json_data)
		return json_data

def create_table():
	conn = dbconnector.connect()
	cursor = conn.cursor()

	json_data = {}

	try:
		cursor.execute('''CREATE TABLE notification
	             (heading text, subheading text, url text, updatetime timestamp UNIQUE)''')
		json_data['status'] = "sucess"
	except sqlite3.OperationalError as e:
		json_data['status'] = "error"
		json_data['error'] = str(e)
	finally:
		conn.commit()

		json_data = json.dumps(json_data)
		return json_data