import random
import grequests
import atexit
import itertools
import json
import re

payload = {'section': 'Scout Troop', 'weekdays[]': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']}
sections = ['Beaver Colony', 'Cub Pack', 'Scout Troop', 'Venturer Company', 'Rover Crew']
url = "https://www.myscouts.ca/ca/netforum_locator/search"
data = set()
f  = open('uniq_postal_codes.txt')
postal_codes = f.readlines()
f.close()
err = open('err.txt', 'a')

def exit_handler():
  f = open('canada_groups.txt', 'a')
  for i in data:
    f.write(i + '\n')
  
atexit.register(exit_handler)

for i in range(710625, len(postal_codes), 75):
  rs = (grequests.post(url, data=dict(payload, **{'zip': pc})) for pc in postal_codes[i:i+75])
  for idx, response in enumerate(grequests.map(rs)):
    if not response:
      print("Error: no response: " + postal_codes[i+idx])
      err.write(postal_codes[i+idx] + '\n')
    else:
      print(i)
      data.update(re.findall("\"latitude\": \"-?[0-9]*\.[0-9]*\"\, \"longitude\": \"-?[0-9]*\.[0-9]*\"[^}]*}", response.text))
      data.update(re.findall("<br\/>[^<]*<br\/>Meeting Day: [a-zA-Z]*<br\/>Meeting Time: [0-9]+:[0-9][0-9] [AP]M<br\/>Meeting Location: [^<]*<br\/>Registration Fee: \$[0-9]*<br \/>(?:<img src=\"\/sites\/all\/themes\/scouts\/images\/sunshine10x10\.png\" style=\"vertical-align:-15\%\">Program runs throughout the summer\.)?<", response.text))
      response.close()

