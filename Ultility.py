from stix.core import STIXPackage
from lxml import etree
import re
import tldextract

class Ultility:
    #Open a XML file
    @staticmethod
    def openXMLFile(filename):
        file = open(filename,'r')
        return file.read()

    #Print Result
    @staticmethod
    def print_result(blockOfXML,numberOfDomains,duplicatedDomains):
        print('---------------------- Block of XML Processed: ',blockOfXML,' -----------------------')
        print('Number of INSERTED domains: ',numberOfDomains)
        print('Number of DUPLICATED domains: ',duplicatedDomains)
        print('----------------------------------------------------------------------------')
        
    @staticmethod
    def print_error(blockOfXML,exception):
        print('---------------------- Block of XML Processed: ',blockOfXML,' -----------------------')
        print('ERROR: ',exception)
        print("THIS BLOCK TERMINATED")
        print('----------------------------------------------------------------------------')

    @staticmethod
    def get_converted_domain(rawDomain):
        address = tldextract.extract(rawDomain)
        #Remove case IPv4 URL (http://192.169.0.1/) Regex: ^ for begining, d+ for any number, \. for .
        if not re.match("^\d+\.\d+\.\d+\.\d+",address.domain):
            return address.domain + '.' + address.suffix
        else:
            return None

    @staticmethod
    def get_domain_from_XML(XMLData,hostURL):
        #Conevert XML to STIX Object -> dictionary
        stixPackage = STIXPackage.from_xml(etree.fromstring(XMLData))
        stixDict = stixPackage.to_dict()
        
        domains = []
        #Check type of XML
        acceptableDataType = ['URIObjectType', 'DomainNameObjectType']
        #Loop through every Indicator
        for indicator in stixDict['indicators']:
            dataType = indicator['observable']['object']['properties']['xsi:type']
            #Check data can be converted to domain or not?
            if (dataType in acceptableDataType):
                rawDomain = indicator['observable']['object']['properties']['value']
                # eti.eset.com has domain nested in another tag
                if (hostURL=='eti.eset.com'):
                    rawDomain = rawDomain['value']
                domain = Ultility.get_converted_domain(rawDomain)
                if domain is not None:
                    domains.append(domain)
        #Remove Duplicated Domains
        domains = list(dict.fromkeys(domains))
        return domains