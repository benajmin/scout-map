import re
import json

source = open('canada_groups.txt').read()
groups = []

for i in re.findall(r'^<.*$', source, re.MULTILINE):
  group = dict()
  group['Name'] = re.search(r'^<br/>([^<+]*) (12\+ year-olds )?(Troop|Scouts)?', i).group(1)
  group['Sections'] = ['Troop']
  group['Meeting Day'] = re.search(r'Meeting Day: ([^<]*)', i).group(1)
  group['Meeting Time'] = re.search(r'Meeting Time: ([^<]*)', i).group(1)
  group['Meeting Location'] = re.search(r'Meeting Location: ([^<]*)', i).group(1)
  group['Registration Fee'] = re.search(r'Registration Fee: ([^<]*)', i).group(1)
  if re.search(r'Program runs throughout the summer', i):
    group['Summer Program'] = True
  else:
    group['Summer Program'] = False
  pattern = r'^".*' + group['Name'].replace("'", "\\\\'").replace("(", "\\(").replace(")", "\\)")
  line2 = re.search(pattern, source, re.MULTILINE)
  if (line2):
    line2 = line2.group(0)
    group['Latitude'] = re.search(r'"latitude": "([^"]*)', line2).group(1)
    group['Longitude'] = re.search(r'"longitude": "([^"]*)', line2).group(1)
    groups.append(group)
  else:
    print(i)
    print(pattern)

open('canada.json', 'w').write(json.dumps(groups))
