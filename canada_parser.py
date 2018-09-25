import requests
import json
import re

payload = {'zip': 'K1G0H3', 'section': 'Beaver Colony', 'weekdays[]': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']}
r = requests.post("https://www.myscouts.ca/ca/netforum_locator/search", data = payload)

data = re.findall("\"latitude\": \"(-?[0-9]*\.[0-9]*)\"\, \"longitude\": \"(-?[0-9]*\.[0-9]*)\"", r.text)

print(data)


