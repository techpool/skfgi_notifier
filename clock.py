import time
import requests
import threading

def scrap_call():
	while True:
		try:
			requests.post('http://skfginotifier.herokuapp.com/scrap', timeout=40)
		except requests.exceptions.ReadTimeout as e:
			print(e)
		finally:
			time.sleep(180)

t = threading.Thread(target=scrap_call)
t.daemon = True
t.start()