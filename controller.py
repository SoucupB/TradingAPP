import queries as qe

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

print(getCompanyDataByAbreviation("MLM"))
