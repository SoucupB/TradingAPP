import tkinter as tk
from pandastable import Table, TableModel
import time
import csv
import requests
import json
import aiohttp
import asyncio
import subprocess

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
  def __init__(self, parent, filepath):
    super().__init__(parent)
    self.index = 0
    self.table = Table(self, showtoolbar = False, showstatusbar = False)
    self.table.importCSV(filepath)
    self.table.show()
    self.poll = True
    self.stre = "Consumer%20Defensive%20Sector"
    self.B = tk.Button(parent, text ="Hello", command = self.daa)
    self.B.pack()
  def daa(self):
    print("DFSFDSFS", e1.get())
  def startQuery(self, stre):
    if self.poll == True:
      self.proc = subprocess.Popen(f'python dbUpdater.py companies {stre}')
      self.poll = self.proc.poll()
    return
  def timer(self):
    if self.poll != None:
      self.table.importCSV(filepath)
      self.table.update()
      self.poll = True
      self.startQuery(self.stre)
    self.poll = self.proc.poll()
    self.after(3000, self.timer)

app = TestApp(root, filepath)
#root.after(1000, app.timer)
app.pack(fill=tk.BOTH, expand=1)
root.mainloop()



