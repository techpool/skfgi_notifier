import requests
import sqlite3
import datetime
import json
import db.dbconnect as dbconnector

from bs4 import BeautifulSoup

def scrap():

	new_notice = 0
	new_notice_list = []

	# Creating the database connection
	conn = dbconnector.connect()

	# Creating the cursor object
	c = conn.cursor()

	# The root link for the notice page where er get the irritating marquee
	notice_root_link = 'http://www.skf.edu.in/notice/'

	# Finak endpoint for the notice page
	notice_link_endpoint = notice_root_link + 'notice.aspx'

	# Response object after making a GET request to the endpoint
	response_object = requests.get(notice_link_endpoint)

	# Parsing the complete html out of the response object
	notice_html = response_object.text

	# Creating soup object for parsing the HTML later
	soup = BeautifulSoup(notice_html, 'html.parser')

	# Selector for notice anchor tags
	notice_list = soup.select('#divSkill a')

	# Sl no. is only for printing, they are not saved in the DB
	sl_no = 1
	for notice in notice_list:
		print(str(sl_no), end=': ')

		# Selecting the previous sibling which gives the text withing the ugly 
		# background coloured text, which is saved as heading
		notice_heading_object = notice.previous_sibling.previous_sibling
		notice_heading = notice_heading_object.b.span.text

		# escaping some html escape sequence
		notice_heading = notice_heading.replace(u'\xa0', u' ')

		print(notice_heading, end=': ')

		# Taking the notice subheading text
		notice_sub_heading = notice.b.text
		print(notice_sub_heading)

		# Taking the URL for each of the notices
		notice_link = notice_root_link + notice['href']
		print('URL: ' + notice_link)

		# Sending a HEAD request to the above got URL in order to get the
		# LAST MODIFIED header information which will act as a primary key 
		# in the database
		notice_request = requests.head(notice_link)
		last_modified = notice_request.headers['Last-Modified']
		print('Last Modified: ' + last_modified)

		# Parsing the datatime in the format recognizable for the SQLite
		time = datetime.datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")

		# Try inserting the data in the table

		# TO_DO: If the insertion takes place then it will shout out the data to a
		# WebHook for messenger which will send off the data to all the subscribers
		# of the page
		try:
			values = (notice_heading, notice_sub_heading, notice_link, time)
			c.execute("INSERT INTO notification VALUES(?, ?, ?, ?)", values)
			new_notice = new_notice + 1
			notice_details = {
				"heading": values[0],
				"sub_heading": values[1],
				"url": values[2],
				"update_time": str(values[3])
			}
			new_notice_list.append(notice_details)
		except sqlite3.IntegrityError as e:
			print('Record Already Exists')

		sl_no += 1

	# Commiting the changes in the database so that the change is persistent
	# in the database
	conn.commit()

	json_data = {
		"status": "success",
		"new_items": len(new_notice_list),
		"data": new_notice_list
	}

	json_data = json.dumps(json_data)

	return json_data

if __name__ == '__main__':
	scrap()