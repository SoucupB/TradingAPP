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

  def jsonToCsv(self, data):
    with open('investing.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      keys = []
      values = []
      for key, value in data.items():
        keys.append(key)
        values.append(value)
      writer.writerow(keys)
      writer.writerow(values)

  def readJson(self):
    result = {}
    with open('investing.json', 'r+', newline='') as file:
      result = json.loads(file.read().replace("\n", " "))
      self.jsonToCsv(result)
      print("Donzo")

  def __init__(self, parent, filepath):
    super().__init__(parent)
    self.index = 0
    self.table = Table(self, showtoolbar = False, showstatusbar = False)
    self.table.importCSV(filepath)
    self.table.show()
    self.poll = True
    self.stre = "Consumer%20Defensive%20Sector"
    self.B = tk.Button(parent, text ="Hello", command = self.searchCompany)
    self.B.pack()
    self.progress = ttk.Progressbar(parent, orient = tk.HORIZONTAL,
              length = 100, mode = 'determinate')
    self.progress.pack(pady = 10)
    self.lastUsedVariable = None
  def searchCompany(self):
    self.proc = subprocess.Popen(f'python dbUpdater.py company {e1.get()}')
    self.poll = self.proc.poll()
    self.timer()
    self.lastUsedVariable = e1.get()
  def startQuery(self, stre):
    if self.poll == True:
      self.proc = subprocess.Popen(f'python dbUpdater.py companies {stre}')
      self.poll = self.proc.poll()
    return
  def getRandomInterval(self, lastNumber, threshhold):
    newValue = lastNumber + random.randint(5, 25)
    if newValue < threshhold:
      return newValue
    return lastNumber
  def timer(self):
    if self.poll != None:
      self.progress['value'] = 100
      self.update_idletasks()
      time.sleep(1.0)
      self.readJson()
      self.table.importCSV(filepath)
      self.table.update()
      self.progress['value'] = 0
      self.update_idletasks()
      #self.poll = True
      #self.startQuery(self.stre)
    else:
      self.progress['value'] = self.getRandomInterval(self.progress['value'], 95)
      self.update_idletasks()
      self.poll = self.proc.poll()
      self.after(random.randint(200, 800), self.timer)

app = TestApp(root, filepath)
#root.after(1000, app.timer)
app.pack(fill=tk.BOTH, expand=1)
root.mainloop()



