import tkinter as tk
from pandastable import Table, TableModel
import time
import csv
import requests
import json
from datetime import datetime
import sys
def writeToCsv(data):
  with open('investing.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name", "Volume", "Market Cap", "Net Dept", "Company Value", "Total Revenue", "EBITDA", "Net Income Common Stockholders", "EV/Sales", "V/EBITBA", "P/E"])
    for elements in data:
      writer.writerow([elements["name"], elements["volume"], elements["marketCap"], elements["dept"], elements["companyValue"],
                       elements["totalRevenue"], elements["EBITDA"], elements["netIncomeForCommonStakeholder"], elements['evSales'], elements['vEBITBA'], elements['pe']])
    for index in range(3):
      writer.writerow([])

def getSectors():
  testsite_array = []
  with open('config.dbe', 'r', newline='') as file:
    for line in file:
      testsite_array.append(line)
  return testsite_array[len(testsite_array) - 1].replace('\n', '').replace('\r', '').replace('\t', '')

argument_lists = sys.argv
print(argument_lists)
if argument_lists[1] == "companies":
  r = requests.get(f'http://localhost:8080/companies/{argument_lists[2]}')
  print("New request at", r.url, datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  writeToCsv(json.loads(r.text))

if argument_lists[1] == "company":
  r = requests.get(f'http://localhost:8080/company/{argument_lists[2]}')
  print("New request at", r.url, datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  writeToCsv(json.loads(r.text))

