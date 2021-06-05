import yfinance as yf
from get_all_tickers import get_tickers as gt
import time
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re, requests
import io
import random
import json
from urllib.request import urlopen as uReq

def current_milli_time():
    return round(time.time() * 1000)

UNDEF_VALUE = -1

class DataPath():
  def __init__(self):
    self.yfinance = None
    self.yFinanceExtend = None
    self.timeStamp = 70000 # 5 secunde
    self.callUnixTime = {}
    self.sectors = None
    self.allCompaniesInSector = None
    self.sectorsMap = {}
  def fetchFinanceData(self, name=None, sym=None, sector=None):
    if name == "yfinance":
      if (name + sym not in self.callUnixTime) or (name + sym in self.callUnixTime and current_milli_time() - self.callUnixTime[name + sym] >= self.timeStamp):
        self.yfinance = yf.Ticker(sym)
        self.callUnixTime[name + sym] = current_milli_time()
    if name == "yExtendFinance":
      url = f"https://finance.yahoo.com/quote/{sym}/financials?ltr=1"
      if (name + sym not in self.callUnixTime) or (name + sym in self.callUnixTime and current_milli_time() - self.callUnixTime[name + sym] >= self.timeStamp):
        time.sleep(0.3)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.yFinanceExtend = soup
        self.callUnixTime[name + sym] = current_milli_time()
    if name == "getSectors":
      url = 'https://www.stockmonitor.com/sectors/'
      if self.sectors == None or (name in self.callUnixTime and current_milli_time() - self.callUnixTime[name] >= self.timeStamp):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.sectors = soup
        self.callUnixTime[name] = current_milli_time()
    if name == "getCompaniesBySector":
      url = f'https://www.stockmonitor.com{self.sectorsMap[sector]}'
      if (name + sector not in self.callUnixTime) or (name + sector in self.callUnixTime and current_milli_time() - self.callUnixTime[name + sector] >= self.timeStamp):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.allCompaniesInSector = soup
        self.callUnixTime[name + sector] = current_milli_time()
    if name == "wsj":
      url = f'https://www.wsj.com/market-data/quotes/{sym}/financials'
      if (name + sym not in self.callUnixTime) or (name + sym in self.callUnixTime and current_milli_time() - self.callUnixTime[name + sym] >= self.timeStamp):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.resp = soup
        self.callUnixTime[name + sym] = current_milli_time()
    if name == 'rapid':
      url = f'https://api.polygon.io/v2/reference/financials/{sym}?limit=1&apiKey=sMCn6GfWpIJkhAyw2utieD11XxA5ctwy'
      if (name + sym not in self.callUnixTime) or (name + sym in self.callUnixTime and current_milli_time() - self.callUnixTime[name + sym] >= self.timeStamp):
        response = json.loads(requests.get(url).text)
        self.response = response
        self.callUnixTime[name + sym] = current_milli_time()

  def valueByName(self, name):
    if self.yFinanceExtend == None or not len(self.yFinanceExtend):
      return None
    spanName = self.yFinanceExtend.find_all("span", {"class": "Va(m)"}, text=re.compile(name))
    if not len(spanName):
      return None
    c_ID = int(float(spanName[0]["data-reactid"]))
    spanValue = self.yFinanceExtend.find_all("span", {"data-reactid": str(c_ID + 3)})
    if not len(spanValue):
      return None
    return int(float(spanValue[0].string.replace(",", "")))
  def getAllSectors(self):
    allSectors = []
    self.fetchFinanceData("getSectors")
    localSectors = self.sectors.find_all("td", {"class": "text-left", "style": "width: auto;"})
    for sector in localSectors:
      hrefName = sector.find_all("a", {})
      if hrefName != None and len(hrefName) > 0:
        allSectors.append(hrefName[0].string)
        self.sectorsMap[hrefName[0].string] = hrefName[0]["href"]
    return allSectors

  def tableDataText(self, table):
    def rowgetDataText(tr, coltag='td'):
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]
    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow:
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs:
        rows.append(rowgetDataText(tr, 'td') )
    return rows

  def getCompaniesBySector2(self, sector, myCompany=None):
    self.getAllSectors()
    self.fetchFinanceData("getCompaniesBySector", sector=sector)
    companiesTicker = []
    localCompanies = self.allCompaniesInSector.find_all("tbody", {})
    responseDepth = self.tableDataText(localCompanies[0])
    response = []
    for currentCompany in responseDepth:
      if myCompany != currentCompany[1]:
        response.append([currentCompany[1], float(currentCompany[4].replace(",", "")) * float(currentCompany[3].replace(",", ""))])
    response.sort(key = lambda x: x[1], reverse=True)
    return [key[0] for key in response]

  # def getCompaniesBySector(self, sector):
  #   self.getAllSectors()
  #   self.fetchFinanceData("getCompaniesBySector", sector=sector)
  #   companiesTicker = []
  #   localCompanies = self.allCompaniesInSector.find_all("td", {"class": "text-left"})
  #   for sector in localCompanies:
  #     hrefName = sector.find_all("a", {})
  #     if hrefName != None and len(hrefName) == 1:
  #       companiesTicker.append(hrefName[0].string)
  #   return companiesTicker
  def getTotalRevenueFromSoup(self):
    return self.valueByName('Total Revenue')
  def getEBITDAFromSoup(self):
    return self.valueByName('EBITDA')
  def getNetIncomeCommonStockFromSoup(self):
    return self.valueByName('Net Income Common Stockholders')
  def getNameBySym(self, sym):
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'longName' in financeInfo and financeInfo['longName'] != None:
      return financeInfo['longName']
    return UNDEF_VALUE
  def getSectorBySym(self, sym):
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'sector' in financeInfo and financeInfo['sector'] != None:
      return financeInfo['sector'] + " Sector"
    return UNDEF_VALUE
  def getVolumeBySym(self, sym):
    self.fetchFinanceData("rapid", sym=sym)
    if len(self.response["results"]) > 0 and "shares" in self.response["results"][0]:
      return self.response["results"][0]["shares"]
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'volume' in financeInfo and financeInfo['volume'] != None:
      return financeInfo['volume']
    return UNDEF_VALUE
  def getPriceBySym(self, sym):
    self.fetchFinanceData("rapid", sym=sym)
    if len(self.response["results"]) > 0 and "sharePriceAdjustedClose" in self.response["results"][0]:
      return self.response["results"][0]["sharePriceAdjustedClose"]
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'regularMarketPrice' in financeInfo and financeInfo['regularMarketPrice'] != None:
      return financeInfo['regularMarketPrice']
    return UNDEF_VALUE
  def getTotalRevenueBySym(self, sym):
    self.fetchFinanceData("rapid", sym=sym)
    if len(self.response["results"]) > 0 and "costOfRevenue" in self.response["results"][0]:
      return self.response["results"][0]["costOfRevenue"]
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'sales' in financeInfo and financeInfo['sales'] != None:
      return financeInfo['sales']
    self.fetchFinanceData("yExtendFinance", sym)
    sales = self.getTotalRevenueFromSoup()
    if sales != None:
      return sales
    return UNDEF_VALUE

  def getDebtByWsj(self):
    fields = self.wsjCompany.find_all("td", {})
    for field in fields:
      currentTableRow = field.find_all("span", {})
      isCorrect = False
      objects = []
      for cTable in currentTableRow:
        if "Total Debt to EBITDA" in cTable:
          isCorrect = True
        objects.append(cTable)
      if isCorrect:
        secondRec = objects[1].find_all("span", {})
        for obj in secondRec:
          return obj.string
    return UNDEF_VALUE

  def getDebtBySym(self, sym):
    self.fetchFinanceData("rapid", sym=sym)
    if len(self.response["results"]) > 0 and "debtCurrent" in self.response["results"][0]:
      return self.response["results"][0]["debtCurrent"]
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'debt' in financeInfo and financeInfo['debt'] != None:
      return financeInfo['debt']
    return UNDEF_VALUE
    #self.fetchFinanceData("wsj", sym=sym)
    # value = self.getDebtByWsj()
    # if value != UNDEF_VALUE:
    #   return float(value) * self.getEBITDABySym(sym)
  def getEBITDABySym(self, sym):
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'EBITDA' in financeInfo and financeInfo['EBITDA'] != None:
      return financeInfo['EBITDA']
    self.fetchFinanceData("yExtendFinance", sym)
    EBITDA = self.getEBITDAFromSoup()
    if EBITDA != None:
      return EBITDA
    self.fetchFinanceData("rapid", sym=sym)
    if len(self.response["results"]) > 0 and "enterpriseValueOverEBITDA" in self.response["results"][0]:
      return self.response["results"][0]["enterpriseValueOverEBITDA"]
    return UNDEF_VALUE
  def getNetIncomeCommonStockBySym(self, sym):
    self.fetchFinanceData("rapid", sym=sym)
    if len(self.response["results"]) > 0 and "netIncomeCommonStock" in self.response["results"][0]:
      return self.response["results"][0]["netIncomeCommonStock"]
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'Income' in financeInfo and financeInfo['Income'] != None:
      return financeInfo['Income']
    self.fetchFinanceData("yExtendFinance", sym)
    EBITDA = self.getNetIncomeCommonStockFromSoup()
    if EBITDA != None:
      return EBITDA
    return UNDEF_VALUE
  def getMarketCapBySim(self, sym):
    price = self.getPriceBySym(sym)
    volume = self.getVolumeBySym(sym)
    if price == UNDEF_VALUE or volume == UNDEF_VALUE:
      return UNDEF_VALUE
    return price * volume
  def getCompanyValueBySym(self, sym):
    marketCap = self.getMarketCapBySim(sym)
    debt = self.getDebtBySym(sym)
    if marketCap == UNDEF_VALUE or debt == UNDEF_VALUE:
      return UNDEF_VALUE
    return marketCap + debt
  def getEvSalesBySym(self, sym):
    companyValue = self.getCompanyValueBySym(sym)
    totalRevenue = self.getTotalRevenueBySym(sym)
    if companyValue == UNDEF_VALUE or totalRevenue == UNDEF_VALUE:
      return UNDEF_VALUE
    if totalRevenue == 0:
      return 0
    return companyValue / totalRevenue
  def getVEBITBABySym(self, sym):
    companyValue = self.getCompanyValueBySym(sym)
    EBITDA = self.getEBITDABySym(sym)
    if companyValue == UNDEF_VALUE or EBITDA == UNDEF_VALUE:
      return UNDEF_VALUE
    if EBITDA == 0:
      return 0
    return companyValue / EBITDA
  def getPEBySym(self, sym):
    marketCap = self.getMarketCapBySim(sym)
    netIncome = self.getNetIncomeCommonStockBySym(sym)
    if marketCap == UNDEF_VALUE or netIncome == UNDEF_VALUE:
      return UNDEF_VALUE
    if netIncome == 0:
      return 0
    return marketCap / netIncome

