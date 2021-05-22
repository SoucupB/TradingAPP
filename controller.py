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

def getCompaniesInSector(sector):
  response = {}
  response['companies'] = dataPath.getCompaniesBySector(sector)
  return response

def getBestCompanies(sector):
  sectorCompanies = getCompaniesInSector(sector)
  companies = []
  for index in range(5):
    companies.append(getCompanyDataByAbreviation(sectorCompanies['companies'][index]))
    time.sleep(0.9)
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

def writeToCsv():
  with open('investing.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    data = getBestCompanies('Utilities Sector')
    writer.writerow(["Company Name", "Volume", "Market Cap", "Net Dept", "Company Value", "Total Revenue", "EBITDA", "Net Income Common Stockholders", "EV/Sales", "V/EBITBA", "P/E"])
    for elements in data:
      writer.writerow([elements["name"], elements["volume"], elements["marketCap"], elements["dept"], elements["companyValue"],
                       elements["totalRevenue"], elements["EBITDA"], elements["netIncomeForCommonStakeholder"], elements['evSales'], elements['vEBITBA'], elements['pe']])
    # writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
    # writer.writerow([2, "Tim Berners-Lee", "World Wide Web"])
    # writer.writerow([3, "Guido van Rossum", "Python Programming"])

#print(getCompanyDataByAbreviation("WBAI"))
#print(getCompanyExtendedValues("MLM"))
#print(getAllSectors())
#print(getCompaniesInSector('Energy Sector'))
writeToCsv()
print(getBestCompanies('Utilities Sector'))
