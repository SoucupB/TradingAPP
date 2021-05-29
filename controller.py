import queries as qe
import time
import csv

dataPath = qe.DataPath()

def getCompanies():
  return ""

def getCompanyDataByAbreviation(name):
  response = {}
  response["name"] = dataPath.getNameBySym(name)
  response["volume"] = dataPath.getVolumeBySym(name)
  response["price"] = dataPath.getPriceBySym(name)
  response["totalRevenue"] = dataPath.getTotalRevenueBySym(name)
  response["dept"] = dataPath.getDeptBySym(name)
  response["netIncomeForCommonStakeholder"] = dataPath.getNetIncomeCommonStockBySym(name)
  response["EBITDA"] = dataPath.getEBITDABySym(name)
  response["marketCap"] = dataPath.getMarketCapBySim(name)
  response["companyValue"] = dataPath.getCompanyValueBySym(name)
  response["evSales"] = dataPath.getEvSalesBySym(name)
  response["vEBITBA"] = dataPath.getVEBITBABySym(name)
  response["pe"] = dataPath.getPEBySym(name)
  return response

def getAllSectors():
  response = {}
  response["sectors"] = dataPath.getAllSectors()
  return response

def getCompanySector():
  response = {}
  return response

def getCompaniesInSector(sector):
  response = {}
  response['companies'] = dataPath.getCompaniesBySector(sector)
  return response

def getBestCompanies(sector):
  sectorCompanies = getCompaniesInSector(sector)
  companies = []
  for index in range(5):
    companies.append(getCompanyDataByAbreviation(sectorCompanies['companies'][index]))
    time.sleep(2.5)
  return companies

def getCompanyExtendedValues(name):
  response = {}
  response["evSales"] = {}
  response["evSales"]["netIncomeForCommonStakeholder"] = dataPath.getNetIncomeCommonStockBySym(name)
  response["evSales"]["totalRevenue"] = dataPath.getTotalRevenueBySym(name)
  response["evSales"]["EBITDA"] = dataPath.getEBITDABySym(name)
  response["evSales"]["dept"] = dataPath.getDeptBySym(name)
  response["evSales"]["volume"] = dataPath.getVolumeBySym(name)
  response["evEBITDA"] = {}
  response["evEBITDA"]["netIncomeForCommonStakeholder"] = response["evSales"]["netIncomeForCommonStakeholder"]
  response["evEBITDA"]["totalRevenue"] = response["evSales"]["totalRevenue"]
  response["evEBITDA"]["EBITDA"] = response["evSales"]["EBITDA"]
  response["evEBITDA"]["dept"] = response["evSales"]["dept"]
  response["evEBITDA"]["volume"] = response["evSales"]["volume"]
  response["pe"] = {}
  response["pe"]["netIncomeForCommonStakeholder"] = response["evSales"]["netIncomeForCommonStakeholder"]
  response["pe"]["totalRevenue"] = response["evSales"]["totalRevenue"]
  response["pe"]["EBITDA"] = response["evSales"]["EBITDA"]
  response["pe"]["dept"] = response["evSales"]["dept"]
  response["pe"]["volume"] = response["evSales"]["volume"]
  return response

#print(getCompanyDataByAbreviation("AAPL"))
#print(getCompanyExtendedValues("MLM"))
#print(getAllSectors())
#print(getBestCompanies('Industrials Sector'))