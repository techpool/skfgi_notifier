import time
import requests
import threading

def scrap_call():
	while True:
		try:
			a = requests.post('http://localhost:8000/scrap', timeout=40)
			print(a.json())
		except requests.exceptions.ReadTimeout as e:
			print(e)
		finally:
			time.sleep(180)

t = threading.Thread(target=scrap_call)
t.daemon = True
t.start()