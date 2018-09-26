import random
import grequests
import itertools
import json
import re

payload = {'section': 'Scout Troop', 'weekdays[]': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']}
sections = ['Beaver Colony', 'Cub Pack', 'Scout Troop', 'Venturer Company', 'Rover Crew']
digit = '0123456789'
postal_letter = 'ABCEGHJKLMNPRSTVWXYZ'
postal_start = 'ABCEGHJKLMNPRSTVXY'
url = "https://www.myscouts.ca/ca/netforum_locator/search"
postal_codes = list(map(''.join, itertools.product(postal_start, digit, postal_letter, digit, postal_letter, digit)))
data = set()

rs = (grequests.post(url, data=dict(payload, **{'zip': pc})) for pc in random.sample(postal_codes, 100))
for response in grequests.map(rs):
  data.update(re.findall("\"latitude\": \"(-?[0-9]*\.[0-9]*)\"\, \"longitude\": \"(-?[0-9]*\.[0-9]*)\"", response.text))


print(data)
print(len(data))  
