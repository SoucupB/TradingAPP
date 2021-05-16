import yfinance as yf
from get_all_tickers import get_tickers as gt
import time
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re, requests
import io

def current_milli_time():
    return round(time.time() * 1000)

UNDEF_VALUE = -1

class DataPath():
  def __init__(self):
    self.yfinance = None
    self.yFinanceExtend = None
    self.timeStamp = 20000 # 20 secunde
    self.callUnixTime = {}
  def fetchFinanceData(self, name, sym):
    if name == "yfinance":
      if self.yfinance == None or (name + sym in self.callUnixTime and current_milli_time() - self.callUnixTime[name + sym] >= self.timeStamp):
        self.yfinance = yf.Ticker(sym)
        self.callUnixTime[name + sym] = current_milli_time()
    if name == "yExtendFinance":
      url = f"https://finance.yahoo.com/quote/{sym}/financials?ltr=1"
      if self.yFinanceExtend == None or(name + sym in self.callUnixTime and current_milli_time() - self.callUnixTime[name + sym] >= self.timeStamp):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.yFinanceExtend = soup
  def valueByName(self, name):
    if self.yFinanceExtend == None or not len(self.yFinanceExtend):
      return None
    spanName = self.yFinanceExtend.find_all("span", {"class": "Va(m)"}, text=re.compile(name))
    if not len(spanName):
      return None
    c_ID = int(spanName[0]["data-reactid"])
    spanValue = self.yFinanceExtend.find_all("span", {"data-reactid": str(c_ID + 3)})
    if not len(spanValue):
      return None
    return int(spanValue[0].string.replace(",", ""))
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
  def getVolumeBySym(self, sym):
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'volume' in financeInfo and financeInfo['volume'] != None:
      return financeInfo['volume']
    return UNDEF_VALUE
  def getPriceBySym(self, sym):
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'regularMarketPrice' in financeInfo and financeInfo['regularMarketPrice'] != None:
      return financeInfo['regularMarketPrice']
    return UNDEF_VALUE
  def getTotalRevenueBySym(self, sym):
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'sales' in financeInfo and financeInfo['sales'] != None:
      return financeInfo['sales']
    self.fetchFinanceData("yExtendFinance", sym)
    sales = self.getTotalRevenueFromSoup()
    if sales != None:
      return sales
    return UNDEF_VALUE
  def getDeptBySym(self, sym):
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'depth' in financeInfo and financeInfo['depth'] != None:
      return financeInfo['depth']
    return UNDEF_VALUE
  def getEBITDABySym(self, sym):
    self.fetchFinanceData("yfinance", sym)
    financeInfo = self.yfinance.info
    if 'EBITDA' in financeInfo and financeInfo['EBITDA'] != None:
      return financeInfo['EBITDA']
    self.fetchFinanceData("yExtendFinance", sym)
    EBITDA = self.getEBITDAFromSoup()
    if EBITDA != None:
      return EBITDA
    return UNDEF_VALUE
  def getNetIncomeCommonStockBySym(self, sym):
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
    dept = self.getDeptBySym(sym)
    if marketCap == UNDEF_VALUE or dept == UNDEF_VALUE:
      return UNDEF_VALUE
    return marketCap + dept
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
