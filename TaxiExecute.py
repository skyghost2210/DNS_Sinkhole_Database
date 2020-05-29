from cabby import create_client
from DatabaseClient import DatabaseConnect
from Ultility import Ultility
from TimeManager import TimeManager
import warnings

class TaxiClientToDatabase:

    def __init__(self,hostURL,useHTTPS,discoveryPath,usernameKey,userPassword,collectionNames,myDatabase,timeManager):
        self.hostURL=hostURL
        self.useHTTPS=useHTTPS
        self.discoveryPath=discoveryPath
        self.usernameKey=usernameKey
        self.userPassword=userPassword
        self.collectionNames=collectionNames
        self.myDatabase=myDatabase
        self.timeManager=timeManager
        self.client = self.set_TAXI_client()

    #Create a TAXI client
    def set_TAXI_client(self):
        #Create a Client
        client = create_client(self.hostURL,use_https = self.useHTTPS,discovery_path = self.discoveryPath)
        client.set_auth(username = self.usernameKey, password = self.userPassword)
        return client

    #Poll content for AlientVault Taxi Server
    def get_STIX_and_insert_database(self):
        print ("-------------------- HOST URL: ",self.hostURL,"----------------------")
        #Ingnore Warning
        warnings.filterwarnings("ignore")
        for collectionName in self.collectionNames:
            
            print ("-------------------- Collection Name: ",collectionName,"----------------------")
            
            content_blocks = self.client.poll(collection_name=collectionName,begin_date=self.timeManager.time)
        
            blockOfXML = 0
            #Prevent Error during connection from server (504)
            try:
                for block in content_blocks:
                    blockOfXML+=1
                    domains=[]
                    #Convert XML data to list of domains
                    domains = Ultility.get_domain_from_XML(block.content,self.hostURL)
                    #Loop through each domain in the list
                    numberOfDomains,duplicatedDomains = self.myDatabase.load_to_database(domains)
                    #Print result to Terminal
                    Ultility.print_result(blockOfXML,numberOfDomains,duplicatedDomains)
            except Exception as e:
                Ultility.print_error(blockOfXML,e)
                continue
        return
        
    #Detec provided services
    def getServicesInfo(self):
        services = self.client.discover_services()
        for service in services:
            print('Service type={s.type}, address={s.address}'.format(s=service))
            
    def get_all_collections_name(self):
        a=[]
        for collection in self.client.get_collections():
            a.append(collection.name)
        print(a)
