import csv
import xml.etree.ElementTree as ET
import QualysAPI

# Appliance map should be in the format:
#   source_appliance_id, target_appliance_id

def readApplianceMap(inputfile: str):
    appliancemap = {}
    with open(inputfile, 'r') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in rowreader:
            appliancemap[row[0]] = row[1]
    csvfile.close()

    return appliancemap

def generateApplianceMap(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI):
    appliancemap = {}
    srcurl = '%s/api/2.0/fo/appliance/?action=list' % source_api.server
    tgturl = '%s/api/2.0/fo/appliance/?action=list' % target_api.server
    sourceresp = source_api.makeCall(srcurl)
    targetresp = target_api.makeCall(tgturl)

    sourcelist = sourceresp.find('.//APPLIANCE_LIST')
    targetlist = targetresp.find('.//APPLIANCE_LIST')

    for sourceappliance in sourcelist.findall('APPLIANCE'):
        srcappliancename = sourceappliance.find('NAME').text
        srcapplianceid = sourceappliance.find('ID').text
        tgtappliance = targetlist.find('.//[NAME="%s"]/..' % srcappliancename)
        if tgtappliance is None:
            print('ERROR: Unable to find Appliance %s in target subscription')
            return None
        tgtapplianceid = tgtappliance.find('ID').text
        appliancemap[srcapplianceid] = tgtapplianceid
    return appliancemap
