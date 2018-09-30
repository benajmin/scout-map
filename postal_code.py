import grequests
import itertools
import random
import re

digit = '0123456789'
postal_letter = 'ABCEGHJKLMNPRSTVWXYZ'
postal_start = 'ABCEGHJKLMNPRSTVXY'
postal_prefixes = sorted(re.findall("\t([A-Z][0-9][A-Z])\t", open("CA.txt").read()))
postal_codes = list(map(''.join, itertools.product(postal_prefixes, digit, postal_letter, digit)))
real_pcs = []
f = open('postalCodes.txt', 'a')
err = open('err.txt', 'a')


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

