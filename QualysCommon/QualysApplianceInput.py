import csv
import xml.etree.ElementTree as ET
import QualysAPI


# Appliance map should be in the format:
#   { source_appliance_id: target_appliance_id }
#
# When reading from a file, the file should be in the format:
#   source_appliance_id, target_appliance_id


def readApplianceMap(inputfile: str):
    """
    Reads a CSV file containing a map of appliance IDs and returns a Python Dictionary containing that map.

    Expected CSV file format:
        source_appliance_id,target_appliance_id

    Parameters:
         inputfile:         A string containing the filename of the CSV file to read

    Returns:
        appliancemap:       A Python Dictionary containing the source appliance ID as the key and the target appliance
                            ID as the value for each entry in the input file
    """
    appliancemap = {}
    with open(inputfile, 'r') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in rowreader:
            appliancemap[row[0]] = row[1]
    csvfile.close()

    return appliancemap


def generateApplianceMap(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI,
                         appliance_name_map: dict = None):
    """
    Generates an appliance map for appliances in source and target subscriptions

    Parameters:
        source_api:         An object of the class QualysAPI for the source subscription
        target_api:         An object of the class QualysAPI for the target subscription
        appliance_name_map: (Optional) A Python Dictionary containing a map of the source and target appliance names
                            where the source name is the key and the target name is the value

    Returns:
         appliancemap:      A Python Dictionary containing a map of the appliance IDs where the source appliance ID is
                            the key and the target appliance ID is the value

        or

        None:               If there is an error in the API calls or where a mismatch occurs, a None value is returned
    """
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

        if appliance_name_map is None:
            tgtappliance = targetlist.find('.//*[NAME="%s"]' % srcappliancename)
        else:
            tgtappliance = targetlist.find('.//*[NAME="%s"]' % appliance_name_map[srcappliancename])

        if tgtappliance is None:
            print('ERROR: Unable to find Appliance %s in target subscription' % appliance_name_map[srcappliancename])
            return None
        appliancemap[srcapplianceid] = tgtappliance.find('ID').text
    return appliancemap
