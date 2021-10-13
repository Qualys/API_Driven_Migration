import csv
import xml.etree.ElementTree as ET
import QualysAPI

# Appliance map should be in the format:
#   { source_appliance_id: target_appliance_id }
#
# When reading from a file, the file should be in the format:
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

    if sourcelist is None:
        print('QualysApplianceInput.generateApplianceMap ERROR: Unable to obtain appliance list from source '
              'subscription')
        if source_api.debug:
            print(ET.tostring(sourceresp, method='xml', encoding='utf-8').decode())
        return None

    if targetlist is None:
        print('QualysApplianceInput.generateApplianceMap Error: Unable to obtain appliance list from target '
              'subscription')
        if target_api.debug:
            print(ET.tostring(targetresp, method='xml', encoding='utf-8').decode())
        return None

    for sourceappliance in sourcelist.findall('APPLIANCE'):
        srcappliancename = sourceappliance.find('NAME').text
        srcapplianceid = sourceappliance.find('ID').text
        tgtappliance = targetlist.find('.//*[NAME="%s"]/..' % srcappliancename)
        if tgtappliance is None:
            print('ERROR: Unable to find Appliance %s in target subscription')
            return None
        tgtapplianceid = tgtappliance.find('ID').text
        appliancemap[srcapplianceid] = tgtapplianceid
    return appliancemap
