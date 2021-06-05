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
  response["sector"] = dataPath.getSectorBySym(name)
  response["totalRevenue"] = dataPath.getTotalRevenueBySym(name)
  response["debt"] = dataPath.getDebtBySym(name)
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

def getCompaniesInSector(sector, name):
  response = {}
  response['companies'] = dataPath.getCompaniesBySector2(sector, myCompany=name)
  return response

def getBestCompanies(sector, name):
  sectorCompanies = getCompaniesInSector(sector, name)
  companies = []
  for index in range(5):
    companies.append(getCompanyDataByAbreviation(sectorCompanies['companies'][index]))
    print("Done querying ", sectorCompanies['companies'][index])
    time.sleep(5.5)
  return companies

def getCompanyExtendedValues(name):
  response = {}
  response["evSales"] = {}
  response["evSales"]["netIncomeForCommonStakeholder"] = dataPath.getNetIncomeCommonStockBySym(name)
  response["evSales"]["totalRevenue"] = dataPath.getTotalRevenueBySym(name)
  response["evSales"]["EBITDA"] = dataPath.getEBITDABySym(name)
  response["evSales"]["debt"] = dataPath.getDebtBySym(name)
  response["evSales"]["volume"] = dataPath.getVolumeBySym(name)
  response["evEBITDA"] = {}
  response["evEBITDA"]["netIncomeForCommonStakeholder"] = response["evSales"]["netIncomeForCommonStakeholder"]
  response["evEBITDA"]["totalRevenue"] = response["evSales"]["totalRevenue"]
  response["evEBITDA"]["EBITDA"] = response["evSales"]["EBITDA"]
  response["evEBITDA"]["debt"] = response["evSales"]["debt"]
  response["evEBITDA"]["volume"] = response["evSales"]["volume"]
  response["pe"] = {}
  response["pe"]["netIncomeForCommonStakeholder"] = response["evSales"]["netIncomeForCommonStakeholder"]
  response["pe"]["totalRevenue"] = response["evSales"]["totalRevenue"]
  response["pe"]["EBITDA"] = response["evSales"]["EBITDA"]
  response["pe"]["debt"] = response["evSales"]["debt"]
  response["pe"]["volume"] = response["evSales"]["volume"]
  return response

#print(getCompanyDataByAbreviation("AAPL"))
#print(getCompanyExtendedValues("MLM"))
#print(getAllSectors())
#print(getBestCompanies('Industrials Sector'))
#print(dataPath.getCompaniesBySector2('Industrials Sector'))
#print(dataPath.getCompaniesBySectorV2("Technology Sector"))