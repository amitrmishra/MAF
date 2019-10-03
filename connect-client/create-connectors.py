import requests
import sys
import time

list_json_files = sys.argv[1:]

for filename in list_json_files:
	for attempt in range(0, 10):
		try:
			data = open(filename, 'r').read()
			response = requests.post('http://connect:8083/connectors', 
				headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, 
				data=data)
			if not response.ok:
				raise Exception(response.text)
			else:
				print('Created connector corresponding to ', filename)
				break
		except Exception as e:
			print('Got exception while creating connector ', filename, e)
			print('Going to wait')
			time.sleep(10)
