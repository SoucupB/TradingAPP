import tkinter as tk
from pandastable import Table, TableModel
import time
import csv

filepath = 'investing.csv'
root = tk.Tk()
root.geometry('1280x680+10+10')
root.title('Investing Startegies')

def mue():
  print("DFSFDSFS")

B = tk.Button(root, text ="Hello", command = mue)

def writeToCsv(data):
  with open('investing.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name", "Volume", "Market Cap", "Net Dept", "Company Value", "Total Revenue", "EBITDA", "Net Income Common Stockholders", "EV/Sales", "V/EBITBA", "P/E"])
    for elements in data:
      writer.writerow([elements["name"], elements["volume"], elements["marketCap"], elements["dept"], elements["companyValue"],
                       elements["totalRevenue"], elements["EBITDA"], elements["netIncomeForCommonStakeholder"], elements['evSales'], elements['vEBITBA'], elements['pe']])

class TestApp(tk.Frame):
    def __init__(self, parent, filepath):
      super().__init__(parent)
      self.index = 0
      self.table = Table(self, showtoolbar=False, showstatusbar=False)
      self.table.importCSV(filepath)
      self.table.show()

    def timer(self):
      self.table.importCSV(filepath)
      self.table.update()
      self.index += 1
      self.after(3000, self.timer)

app = TestApp(root, filepath)
app.timer()
app.pack(fill=tk.BOTH, expand=1)
B.pack()
root.mainloop()