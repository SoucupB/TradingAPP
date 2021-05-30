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
from tkinter import ttk
filepath = 'investing.csv'
root = tk.Tk()
root.geometry('1280x680+10+10')
root.title('Investing Startegies')
e1 = tk.Entry(root)
e1.pack(padx=550, pady=20)
variable = tk.StringVar(root)
variable.set("EV/Sales")
w = tk.OptionMenu(root, variable, "EV/Sales", "EV/EBITDA", "P/E")
w.pack()

class TestApp(tk.Frame):

  def jsonToCsv(self, data, csvName):
    parsedData = data
    with open(csvName, 'w', newline='') as file:
      writer = csv.writer(file)
      keys = []
      if isinstance(data, list):
        parsedData = data[0]
      for key, value in parsedData.items():
        keys.append(key)
      writer.writerow(keys)
      if isinstance(data, list):
        values = []
        for each in data:
          for _, value in parsedData.items():
            values.append(value)
          writer.writerow(values)
      else:
        values = []
        for _, value in parsedData.items():
          values.append(value)
        writer.writerow(values)
        writer.writerow([""] * len(keys))
  def readJson(self, jsonData):
    result = {}
    with open(jsonData, 'r+', newline='') as file:
      result = json.loads(file.read().replace("\n", " "))
    return result
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
    self.lastUsedVariable = None
  def searchCompany(self):
    self.procIndiv = subprocess.Popen(f'python dbUpdater.py company {e1.get()} investing.json')
    self.pollIndividual = self.procIndiv.poll()
    self.timerIndividual()
    self.lastUsedVariable = e1.get()
  def searchBatch(self, stre):
    self.procMulti = subprocess.Popen(f'python dbUpdater.py companies {stre} troliu.json')
    self.pollMulti = self.procMulti.poll()
  def getRandomInterval(self, lastNumber, threshhold):
    newValue = lastNumber + random.randint(5, 25)
    if newValue < threshhold:
      return newValue
    return lastNumber
  def timerMulti(self, batch):
    if self.pollMulti != None:
      self.searchBatch(batch)
      self.table.importCSV(filepath)
      self.table.update()
      return
    else:
      self.pollMulti = self.procMulti.poll()
      self.after(1000, self.timerMulti)
  def timerIndividual(self):
    if self.pollIndividual != None:
      self.progress['value'] = 100
      self.update_idletasks()
      time.sleep(1.0)
      jsonReponse = self.readJson("investing.json")
      self.jsonToCsv(jsonReponse, "investing.csv")
      self.table.importCSV(filepath)
      self.table.update()
      self.progress['value'] = 0
      self.update_idletasks()
      self.timerMulti(jsonReponse["sector"].replace(" ", "%20"))
    else:
      self.progress['value'] = self.getRandomInterval(self.progress['value'], 95)
      self.update_idletasks()
      self.pollIndividual = self.procIndiv.poll()
      self.after(random.randint(200, 800), self.timerIndividual)

app = TestApp(root, filepath)
app.pack(fill=tk.BOTH, expand=1)
root.mainloop()



