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
  "companyValue": "Company Value",
  "targetPrice": "Pret tinta"
}

rowTargetCompany = {
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
  "companyValue": "Company Value",
  "targetPrice": "Pret tinta"
}

averageMedian = {
  "Median": "Median",
  "Average": "Average",
  "Types": "Types"
}

headerStructure = {
  "Types": "Types",
  "Values": "Values",
  "Randament": "Randament"
}

class TestApp(tk.Frame):
  def jsonToCsv(self, data, csvName, maxRows, rowNames, spaces):
    parsedData = data
    with open(csvName, 'w', newline='') as file:
      writer = csv.writer(file)
      keys = []
      if isinstance(data, list):
        parsedData = data[0]
      for key, value in parsedData.items():
        if key in rowNames:
          keys.append(rowNames[key])
      fxy = len(keys)
      for index in range(fxy, self.maxRows):
        keys.append(" ")
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
      for i in range(spaces):
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
    if second != None:
      with open(second, 'r+', newline='') as file:
        nmd += file.read()
    with open(target, 'w+', newline='') as file:
      file.write(nmd)
  def __init__(self, parent, filepath):
    super().__init__(parent)
    self.index = 0
    self.table = Table(self, showtoolbar = False, showstatusbar = False)
    try:
      self.table.importCSV(filepath)
    except:
      print("No rew table is present!")
    self.table.show()
    self.pollIndividual = True
    self.pollMulti = True
    self.maxRows = 15
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
  def getApplicationHeader(self, priceCategory, company, allCompanies):
    response = []
    if priceCategory == "P/E":
      newCompany = self.changeRules("pe", allCompanies, company)
      response.append({
        "Types": "Previous Close",
        "Values": newCompany["price"],
        "Randament": newCompany["targetPrice"] / newCompany["price"] - 1
      })
      response.append({
        "Types": "Pret Tinta",
        "Values": newCompany["targetPrice"],
        "Randament": " "
      })
      response.append({
        "Types": "Recomandare",
        "Values": "SELL",
        "Randament": " "
      })
      self.jsonToCsv(response, "temp/Corn.csv", self.maxRows, headerStructure, 2)
    return response
  def getMedianValue(self, companies, by):
    records = []
    for i in range(len(companies)):
      records.append(companies[i][by])
    records.sort()
    return records[len(records) // 2]
  def getAverageValue(self, companies, by):
    total = 0
    for i in range(len(companies)):
      total += companies[i][by]
    return total / len(companies)
  def getMedianBy(self, companies, by, currentCompany):
    medianValue = self.getMedianValue(companies, by)
    currentCompanyCopy = copy.deepcopy(currentCompany)
    currentCompanyCopy[by] = medianValue
    return currentCompanyCopy
  def changeRules(self, by, allCompanies, company):
    cCompany = None
    if by == "pe":
      cCompany = self.getMedianBy(allCompanies, by, company)
      cCompany["companyValue"] = cCompany["totalRevenue"] * cCompany[by]
      cCompany["marketCap"] = cCompany["marketCap"] - cCompany["dept"]
      cCompany["targetPrice"] = cCompany["volume"] / cCompany["marketCap"]
    if by == "vEBITBA":
      cCompany = self.getMedianBy(allCompanies, by, company)
      cCompany["companyValue"] = cCompany["EBITDA"] * cCompany[by]
      cCompany["marketCap"] = cCompany["marketCap"] - cCompany["dept"]
      cCompany["targetPrice"] = cCompany["volume"] / cCompany["marketCap"]
    if by == "evSales":
      cCompany = self.getMedianBy(allCompanies, by, company)
      cCompany["companyValue"] = cCompany["EBITDA"] * cCompany[by]
      cCompany["marketCap"] = cCompany["marketCap"] - cCompany["dept"]
      cCompany["targetPrice"] = cCompany["volume"] / cCompany["marketCap"]
    return cCompany

  def createTargetCompany(self, allCompanies, company):
    response = []
    response.append(self.changeRules("pe", allCompanies, company))
    response.append(self.changeRules("vEBITBA", allCompanies, company))
    response.append(self.changeRules("evSales", allCompanies, company))
    self.jsonToCsv(response, "temp/targetCompany.csv", self.maxRows, rowTargetCompany, 2)

  def combineDataIntoOnetable(self, tables):
    self.combine_files(tables[0], None, "temp/res.csv")
    for i in range(1, len(tables)):
      self.combine_files("temp/res.csv", tables[i], "temp/res.csv")

  def createMedianAndAverageTable(self, allCompanies):
    response = []
    response.append({
      "Types": "EV/Sales",
      "Median": self.getMedianValue(allCompanies, "pe"),
      "Average": self.getAverageValue(allCompanies, "pe")
    })
    response.append({
      "Types": "V/EBITBA",
      "Median": self.getMedianValue(allCompanies, "vEBITBA"),
      "Average": self.getAverageValue(allCompanies, "vEBITBA")
    })
    response.append({
      "Types": "P/E",
      "Median": self.getMedianValue(allCompanies, "evSales"),
      "Average": self.getAverageValue(allCompanies, "evSales")
    })
    self.jsonToCsv(response, "temp/medianObj.csv", self.maxRows, averageMedian, 2)

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
      self.createTargetCompany(jsonReponse, self.singleton)
      self.jsonToCsv(jsonReponse, "temp/cmps.csv", self.maxRows, rowNames, 2)
      self.createMedianAndAverageTable(jsonReponse)
      self.getApplicationHeader("P/E", self.singleton, jsonReponse)

      self.progressMulti['value'] = 0
      self.update_idletasks()
      self.combineDataIntoOnetable(["temp/Corn.csv", "temp/cmps.csv", "temp/medianObj.csv", "temp/targetCompany.csv"])
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
      self.jsonToCsv(jsonReponse, "temp/investing.csv", self.maxRows, rowNames, 2)
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



