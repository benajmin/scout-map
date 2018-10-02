# Script for determining all valid canadian postal codes
import grequests
import itertools
import re

digit = '0123456789'
postal_letter = 'ABCEGHJKLMNPRSTVWXYZ'
# Download list of postal prefixes from http://download.geonames.org/export/dump/
postal_prefixes = sorted(re.findall("\t([A-Z][0-9][A-Z])\t", open("CA.txt").read()))
postal_codes = list(map(''.join, itertools.product(postal_prefixes, digit, postal_letter, digit)))
f = open('postalCodes.txt', 'a')
err = open('err.txt', 'a')


# Use prefixes to generate all possible postal codes and check if their correct
# Sometimes errors are returned. It just saves them to be rerun later (see below)
# Sometimes will freeze and stop printing, just end the program and restart with
# start set to last printed value

def run(start):
  for i in range(postal_codes.index(start), len(postal_codes), 75):
    rs = (grequests.get("http://www.canada411.ca/search/?stype=pc&pc="+code, stream=False) for code in postal_codes[i:i+75])
    for response in grequests.map(rs):
      if not response:
        print("Error: no response: " + str(i))
        err.write(str(i) + '\n')
      if response and "We didn't find any result for" not in response.text:
        real_pcs.append(response.url[-6:])
        print(response.url[-6:])
        f.write(response.url[-6:] + '\n')
      if response:
        response.close()
    
# Reruns all postal codes that returned errors
# Use uniq err.txt > uniq_error.txt to remove duplicate error codes
# May have to do this multiple times

def run_err():
  for i in open('uniq_err.txt', 'r'):
    rs = (grequests.get("http://www.canada411.ca/search/?stype=pc&pc="+code, stream=False) for code in postal_codes[int(i):int(i)+75])
    for response in grequests.map(rs):
      if not response:
        print("Error: no response: " + str(i))
        err.write(str(i) + '\n')
      if response and "We didn't find any result for" not in response.text:
        real_pcs.append(response.url[-6:])
        print(response.url[-6:])
        f.write(response.url[-6:] + '\n')
      if response:
        response.close()

run('A0A0A0')

