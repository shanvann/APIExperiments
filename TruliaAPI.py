#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET


class LocationInfo(object):

  def __init__(self,api_key):
    print "LocationInfo initiated"
    self.LibraryName = "LocationInfo" 
    self.api_key = api_key 

  def urlGenerator(self,FunctionName,parameters):
    URL_head = 'http://api.trulia.com/webservices.php?'
    lib ='library='+ self.LibraryName
    func = '&function=' + FunctionName
    apikey = '&apikey=' + self.api_key  
    if len(parameters) > 0:
      params = ["&%s=%s"%(param,val) for param,val in parameters] 
    else:
      params = []
    URL = "".join([URL_head]+[lib]+[func]+params+[apikey])
    print URL
    return URL

  def get_data(self,root,params):
    data = []
    for a in root.findall(params[0]+"/"+params[1]+"/"+params[2]): #response
      data_array = []
      dummy = ([data_array.append(a.find(param).text) for param in params[3]])
      data.append(data_array)
    return data
  
  def getCitiesInState(self,state): #"cityId","name","longitude","latitude"	   
  #Retrieves all cities in a state.    
    FunctionName = "getCitiesInState"
    parameters = []
    parameters.append(["state",state])
    requestURL = self.urlGenerator(FunctionName,parameters)
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    params = ['response',self.LibraryName,"city",["cityId","name","longitude","latitude"]]
    return self.get_data(root,params)

  def getCountiesInState(self,state): #"countyId","name","longitude","latitude"
  #Retrieves all counties in a state.	
    FunctionName = "getCountiesInState"
    parameters = []
    parameters.append(["state",state])
    requestURL = self.urlGenerator(FunctionName,parameters)
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    params = ['response',self.LibraryName,"county",["countyId","name","longitude","latitude"]]
    return self.get_data(root,params)
      
  def getNeighborhoodsInCity(self,state,city): #"id","name"	
  #Retrieves all Neighborhoods in a city.  
    FunctionName = "getNeighborhoodsInCity"
    parameters = []
    parameters.append(["city",city])
    parameters.append(["state",state])
    requestURL = self.urlGenerator(FunctionName,parameters)
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    params = ['response',self.LibraryName,"neighborhood",["id","name"]]
    return self.get_data(root,params)
    
  def getStates(self): #"name","stateCode","longitude","latitude"    
  #Retrieves all 50 states.
    FunctionName = "getStates"
    parameters = []        
    requestURL = self.urlGenerator(FunctionName,parameters)     
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    params = ['response',self.LibraryName,"state",["name","stateCode","longitude","latitude"]]
    return self.get_data(root,params)   
  
  def getZipCodesInState(self,state): #"name","longitude","latitude"    
  #Retrieves all ZIP codes in a state.            
    FunctionName = "getZipCodesInState"
    parameters = []
    parameters.append(["state",state])
    requestURL = self.urlGenerator(FunctionName,parameters)
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    params = ['response',self.LibraryName,"zipCode",["name","longitude","latitude"]]
    return self.get_data(root,params)

class TruliaStats(object):

  def __init__(self,api_key):
    #print "TruliaStats initiated"
    self.LibraryName = "TruliaStats" 
    self.api_key = api_key 

  def urlGenerator(self,FunctionName,parameters,startDate,endDate,statType="all"):
    URL_head = 'http://api.trulia.com/webservices.php?'
    lib ='library='+ self.LibraryName
    func = '&function=' + FunctionName
    apikey = '&apikey=' + self.api_key  
    start_date = "&startDate=" + startDate
    end_date = "&endDate=" + endDate
    stat_type = "&statType=" + statType
    if len(parameters) > 0:
      params = ["&%s=%s"%(param,val) for param,val in parameters] 
    else:
      params = []
    URL = "".join([URL_head]+[lib]+[func]+params+[start_date]+[end_date]+[stat_type]+[apikey])
    print URL
    return URL

  def get_data(self,root,root_param):
    data = []
    for a in root.findall(root_param[0]):
      data_array = []
      dummy = ([data_array.append(a.find(param).text) for param in root_param[1]])
      data.append(data_array)
    return data
  
  def getCityStats(self,state,city,startDate,endDate,statType):	   
  #Retrieves all cities in a state.    
    FunctionName = "getCityStats"
    parameters = []
    parameters.append(["state",state])
    parameters.append(["city",city])
    requestURL = self.urlGenerator(FunctionName,parameters,startDate,endDate)
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    traffic_root = ['response/%s/listingStats/trafficStat'%self.LibraryName,["date","percentStateTraffic","percentNationalTraffic"]]
    listing_root = ['response/%s/listingStats/listingStat/listingPrice/subcategory'%self.LibraryName,["type","numberOfProperties","medianListingPrice","averageListingPrice"]]                                       
    if statType == "traffic":
      return self.get_data(root,traffic_root)  
    elif statType == "listing":
      return self.get_data(root,listing_root)  
    else:                              
      return [self.get_data(root,traffic_root),self.get_data(root,listing_root)]

  def getCountyStats(self,state,county,startDate,endDate,statType): 
  #Retrieves all counties in a state.	
    FunctionName = "getCountyStats"
    parameters = []
    parameters.append(["state",state])
    parameters.append(["county",county])
    requestURL = self.urlGenerator(FunctionName,parameters,startDate,endDate)
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    traffic_root = ['response/%s/trafficStats/trafficStat'%self.LibraryName,["date","percentStateTraffic","percentNationalTraffic"]]
    listing_root = ['response/%s/listingStats/listingStat/listingPrice/subcategory'%self.LibraryName,["type","numberOfProperties","medianListingPrice","averageListingPrice"]]    
    if statType == "traffic":
      return self.get_data(root,traffic_root)  
    elif statType == "listing":
      return self.get_data(root,listing_root)  
    else:                              
      return [self.get_data(root,traffic_root),self.get_data(root,listing_root)]
      
  def getNeighborhoodStats(self,state,city,neighborhoodId,startDate,endDate,statType):	
  #Retrieves all Neighborhoods in a city.  
    FunctionName = "getNeighborhoodStats"
    parameters = []
    parameters.append(["neighborhoodId",neighborhoodId])
    requestURL = self.urlGenerator(FunctionName,parameters,startDate,endDate)
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    traffic_root = ['response/%s/trafficStats/trafficStat'%self.LibraryName,["date","percentCityTraffic","percentStateTraffic","percentNationalTraffic"]]
    listing_root = ['response/%s/listingStats/listingStat/listingPrice/subcategory'%self.LibraryName,["type","numberOfProperties","medianListingPrice","averageListingPrice"]]                                       
    if statType == "traffic":
      return self.get_data(root,traffic_root)  
    elif statType == "listing":
      return self.get_data(root,listing_root)  
    else:                              
      return [self.get_data(root,traffic_root),self.get_data(root,listing_root)]
    
  def getStateStats(self,state,startDate,endDate,statType):        
  #Retrieves all 50 states.
    FunctionName = "getStateStats"
    parameters = []       
    parameters.append(["state",state]) 
    requestURL = self.urlGenerator(FunctionName,parameters,startDate,endDate)    
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    traffic_root = ['response/%s/trafficStats/trafficStat'%self.LibraryName,["date","percentNationalTraffic"]]
    listing_root = ['response/%s/listingStats/listingStat/listingPrice/subcategory'%self.LibraryName,["type","numberOfProperties","medianListingPrice","averageListingPrice"]]                                       
    if statType == "traffic":
      return self.get_data(root,traffic_root)  
    elif statType == "listing":
      return self.get_data(root,listing_root)  
    else:                              
      return [self.get_data(root,traffic_root),self.get_data(root,listing_root)]

  def getZipCodeStats(self,state,zipcode,startDate,endDate,statType):	    
  #Retrieves all ZIP codes in a state.            
    FunctionName = "getZipCodeStats"
    parameters = []
    parameters.append(["zipCode",zipcode])
    requestURL = self.urlGenerator(FunctionName,parameters,startDate,endDate)
    #print urllib.urlopen(requestURL).read()
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    traffic_root = ['response/%s/trafficStats/trafficStat'%self.LibraryName,["date","percentStateTraffic","percentNationalTraffic"]]
    listing_root = ['response/%s/listingStats/listingStat/listingPrice/subcategory'%self.LibraryName,["type","numberOfProperties","medianListingPrice","averageListingPrice"]]                                       
    if statType == "traffic":
      return self.get_data(root,traffic_root)  
    elif statType == "listing":
      return self.get_data(root,listing_root)  
    else:                              
      return [self.get_data(root,traffic_root),self.get_data(root,listing_root)]
    

def main():
  api_data = [a.strip().split()[1] for a in open("apikey","r").readlines() if "Key:" in a.strip().split()]
  api_key = api_data[0]
  state = "CA"
  city = "San Francisco"
  county = "Santa Clara"
  neighborhoodId = "1386"
  startDate = "2011-02-06"
  endDate ="None"
  statType = "all"
  zipcode = "94041"

  a = LocationInfo(api_key) 
  b = TruliaStats(api_key)
 
  print "1",a.getStates()
  print "2",a.getCitiesInState(state)
  print "3",a.getCountiesInState(state)
  print "4",a.getNeighborhoodsInCity(state,city)
  print "5",a.getZipCodesInState(state)

  print "6",b.getCityStats(state,city,startDate,endDate,statType)
  print "7",b.getCountyStats(state,county,startDate,endDate,statType)
  print "8",b.getNeighborhoodStats(state,city,neighborhoodId,startDate,endDate,statType)
  print "9",b.getStateStats(state,startDate,endDate,statType)
  print "10",b.getZipCodeStats(state,zipcode,startDate,endDate,statType)
  
if __name__=="__main__":
  main()
