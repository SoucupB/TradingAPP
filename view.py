# from tkinter import *


# class Table:

#     def __init__(self, lst):
#       self.root = Tk()
#       self.lst = lst
#       self.y = len(lst)
#       self.x = len(lst[0])
#       self.mapEntries = [[0] * self.x] * self.y
#       for i in range(self.y):
#         for j in range(self.x):
#           self.e = Entry(self.root, width=20, fg='blue',
#                           font=('Arial',16,'bold'))
#           self.mapEntries[i][j] = self.e
#           self.e.grid(row=i, column=j)
#           self.e.insert(END, self.lst[i][j])

#     def update(self):
#       print("DADADADA")
#       #self.mapEntries[0][2].configure(text="ANA")
#       self.mapEntries[0][0].insert(END, "DADADADA")
#       self.root.after(1000, self.update)

#     def createMainLoop(self):
#       self.update()
#       self.root.mainloop()
# lst = [(1,'Raj','Mumbai',19, 5),
#        (2,'Aaryan','Pune',18, 6),
#        (3,'Vaishnavi','Mumbai',20, 7),
#        (4,'Rachna','Mumbai',21, 7),
#        (5,'Shubham','Delhi',21, 9)]

# t = Table(lst)
# t.createMainLoop()

# import tkinter as tk
# from tk_html_widgets import HTMLLabel

# root = tk.Tk()
# html_label = HTMLLabel(root, html="""
#   <div style="display: flex; height: 400px; width: 400px;">
#     <div style="color: green;">Ana are mere</div>
#     <div style="color: green;">Ana are mere</div>
#     <div style="color: green;">Ana are mere</div>
#     <div style="color: green;">Ana are mere</div>
#   </div>
# """)
# html_label.pack(fill="both", expand=True)
# html_label.fit_height()
# root.mainloop()

import tkinter as tk
from pandastable import Table, TableModel
import time

filepath = 'investing.csv'

root = tk.Tk()
root.geometry('1280x680+10+10')
root.title('Investing Startegies')

class TestApp(tk.Frame):
    def __init__(self, parent, filepath):
      super().__init__(parent)
      self.table = Table(self, showtoolbar=False, showstatusbar=False)
      self.table.importCSV(filepath)
      self.table.show()

    def timer(self):
      self.table.importCSV(filepath)
      self.table.update()
      self.after(3000, self.timer)

app = TestApp(root, filepath)
app.timer()
app.pack(fill=tk.BOTH, expand=1)

root.mainloop()