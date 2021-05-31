import tkinter as tk
from pandastable import Table, TableModel
import time
import csv
import requests
import json
import aiohttp
import asyncio
import subprocess
import random
import copy
from tkinter import ttk
filepath = 'temp/investing.csv'
root = tk.Tk()
root.geometry('1280x680+10+10')
root.title('Investing Startegies')
e1 = tk.Entry(root)
e1.pack(padx=550, pady=20)
variable = tk.StringVar(root)
variable.set("EV/Sales")
w = tk.OptionMenu(root, variable, "EV/Sales", "EV/EBITDA", "P/E")
w.pack()

rowNames = {
  "name": "Company Name",
  "volume": "Volume",
  "marketCap": "Market Cap",
  "totalRevenue": "Total Revenue",
  "dept": "Net Dept",
  "totalRevenue": "Total Revenue",
  "netIncomeForCommonStakeholder": "Net Income Common Stockholders",
  "evSales": "EV/Sales",
  "vEBITBA": "V/EBITBA",
  "pe": "P/E",
  "price": "Prvious Close",
  "companyValue": "Company Value"
}

class TestApp(tk.Frame):
  def jsonToCsv(self, data, csvName):
    parsedData = data
    with open(csvName, 'w', newline='') as file:
      writer = csv.writer(file)
      keys = []
      if isinstance(data, list):
        parsedData = data[0]
      for key, value in parsedData.items():
        if key in rowNames:
          keys.append(rowNames[key])
      writer.writerow(keys)
      if isinstance(data, list):
        for each in data:
          values = []
          for key, value in each.items():
            if key in rowNames:
              values.append(value)
          writer.writerow(values)
      else:
        values = []
        for key, value in parsedData.items():
          if key in rowNames:
            values.append(value)
        writer.writerow(values)
        writer.writerow([""] * len(keys))
        writer.writerow([""] * len(keys))
        writer.writerow([""] * len(keys))
  def readJson(self, jsonData):
    result = {}
    with open(jsonData, 'r+', newline='') as file:
      result = json.loads(file.read().replace("\n", " "))
    return result
  def combine_files(self, first, second, target):
    nmd = ""
    with open(first, 'r+', newline='') as file:
      nmd += file.read()
    with open(second, 'r+', newline='') as file:
      nmd += file.read()
    with open(target, 'w+', newline='') as file:
      file.write(nmd)
  def __init__(self, parent, filepath):
    super().__init__(parent)
    self.index = 0
    self.table = Table(self, showtoolbar = False, showstatusbar = False)
    self.table.importCSV(filepath)
    self.table.show()
    self.pollIndividual = True
    self.pollMulti = True
    self.stre = "Consumer%20Defensive%20Sector"
    self.check = tk.Button(parent, text ="Search", command = self.searchCompany)
    self.check.pack()
    self.progress = ttk.Progressbar(parent, orient = tk.HORIZONTAL,
              length = 100, mode = 'determinate')
    self.progress.pack(pady = 10)
    self.progressMulti = ttk.Progressbar(parent, orient = tk.HORIZONTAL,
              length = 100, mode = 'determinate')
    self.progressMulti.pack(pady = 10)
    self.lastUsedVariable = None
  def searchCompany(self):
    self.procIndiv = subprocess.Popen(f'python dbUpdater.py company {e1.get()} temp/investing.json')
    self.pollIndividual = self.procIndiv.poll()
    self.timerIndividual()
    self.lastUsedVariable = e1.get()
  def searchBatch(self, stre):
    self.procMulti = subprocess.Popen(f'python dbUpdater.py companies {stre} temp/multiData.json')
    self.pollMulti = self.procMulti.poll()
  def getMedianBy(self, companies, by, currentCompany):
    records = []
    for i in range(len(companies)):
      records.append(companies[i][by])
    records.sort()
    currentCompanyCopy = copy.deepcopy(currentCompany)
    currentCompanyCopy[by] = records[len(records) // 2]
    return currentCompanyCopy
  def getRandomInterval(self, lastNumber, threshhold, left, right):
    newValue = lastNumber + random.randint(left, right)
    if newValue < threshhold:
      return newValue
    return lastNumber
  def timerMulti(self):
    if self.pollMulti != None:
      self.progressMulti['value'] = 100
      self.update_idletasks()
      time.sleep(1.0)
      jsonReponse = self.readJson("temp/multiData.json")
      print(self.getMedianBy(jsonReponse, "pe", self.singleton))
      self.jsonToCsv(jsonReponse, "temp/cmps.csv")
      self.progressMulti['value'] = 0
      self.update_idletasks()
      self.combine_files("temp/investing.csv", "temp/cmps.csv", "temp/res.csv")
      self.table.importCSV("temp/res.csv")
      self.table.update()
      return
    else:
      self.pollMulti = self.procMulti.poll()
      self.progressMulti['value'] = self.getRandomInterval(self.progressMulti['value'], 95, 1, 5)
      self.after(random.randint(200, 800), self.timerMulti)
  def timerIndividual(self):
    if self.pollIndividual != None:
      self.progress['value'] = 100
      self.update_idletasks()
      time.sleep(1.0)
      jsonReponse = self.readJson("temp/investing.json")
      self.singleton = jsonReponse
      self.jsonToCsv(jsonReponse, "temp/investing.csv")
      self.table.importCSV(filepath)
      self.table.update()
      self.progress['value'] = 0
      self.update_idletasks()
      self.searchBatch(jsonReponse["sector"].replace(" ", "%20"))
      self.timerMulti()
    else:
      self.progress['value'] = self.getRandomInterval(self.progress['value'], 95, 5, 25)
      self.update_idletasks()
      self.pollIndividual = self.procIndiv.poll()
      self.after(random.randint(200, 800), self.timerIndividual)

app = TestApp(root, filepath)
app.pack(fill=tk.BOTH, expand=1)
root.mainloop()



