from TaxiExecute import TaxiClientToDatabase
from DatabaseClient import DatabaseConnect
from TimeManager import *

############# CONFIG ############# 
#------------- TAXII CLIENT -------------
OTX_TAXI_CLIENT = {"hostURL":'otx.alienvault.com'
                   ,"useHHTPS":True
                   , "discoveryPath":'taxii/discovery'
                   , "usernameKey" : ""
                   , "password" : ''
                   , "collectionNames": ['']
                   }

ESSET_TAXI_CLIENT = {"hostURL":'eti.eset.com'
                   ,"useHHTPS":True
                   , "discoveryPath":'/taxiiservice/discovery'
                   , "usernameKey" : ""
                   , "password" : ''
                   , "collectionNames": ['']
                   }

#------------- DATE -------------
#Must be in format: YYYY-MM-DDTHH:MM:SS.ssssss+/-hh:mm (ISO8601)
#To specify specific time, use BEGIN_DATE. Otherwise, script will find a file 
# -- If LAST_TIME_UPDATE.txt file NOT FOUND and BEGIN_DATE = None, script will Download All
BEGIN_DATE = None

#------------- DATABASE -------------
DATABASE_HOST_NAME = ""

DATABASE_USERNAME  = ""

DB_USER_PASSWORD = ""

DATABASE_NAME = ""

AUTH_PLUGIN = "mysql_native_password"


#################### MAIN ########################
#Create a time manager
timeManager = TimeManager(BEGIN_DATE)
#Create a database Client
databaseClient = DatabaseConnect(DATABASE_HOST_NAME,DATABASE_USERNAME,DB_USER_PASSWORD,DATABASE_NAME,AUTH_PLUGIN)
#Create a AlientVault TAXII Client and Connect to database
alientvaultTaxiAndDatabaseConnect = TaxiClientToDatabase(OTX_TAXI_CLIENT['hostURL']
                                                         ,OTX_TAXI_CLIENT['useHHTPS']
                                                         ,OTX_TAXI_CLIENT['discoveryPath']
                                                         ,OTX_TAXI_CLIENT['usernameKey'],
                                                         OTX_TAXI_CLIENT['password']
                                                         ,OTX_TAXI_CLIENT['collectionNames'],databaseClient,timeManager)
esetTaxiAndDatabaseConnect = TaxiClientToDatabase(ESSET_TAXI_CLIENT['hostURL']
                                                         ,ESSET_TAXI_CLIENT['useHHTPS']
                                                         ,ESSET_TAXI_CLIENT['discoveryPath']
                                                         ,ESSET_TAXI_CLIENT['usernameKey'],
                                                         ESSET_TAXI_CLIENT['password']
                                                         ,ESSET_TAXI_CLIENT['collectionNames'],databaseClient,timeManager)
#Download STIXX File and Insert to database
esetTaxiAndDatabaseConnect.get_STIX_and_insert_database()
alientvaultTaxiAndDatabaseConnect.get_STIX_and_insert_database()
#Update time
timeManager.write_time_to_file()