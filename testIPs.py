import xml.etree.ElementTree as ET
import sys
import QualysAPI
import QualysIPProcessor


def handleResponse(response: ET.Element):
    if response.find('.//CODE') is not None:
        return False
    else:
        return True


def testIPs(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool):
    addurl = QualysIPProcessor.getIPTrackedVM(source_api=source_api)
    if simulate:
        print('%s' % addurl)
    else:
        response = QualysIPProcessor.createIPTrackedVM(target_api=target_api, addurl=addurl)
        if not handleResponse(response=response):
            print('ERROR: QualysIPProcessor.migrateIPTrackedVM() failed to create new IPs')
            ET.dump(response)
            sys.exit(1)

    addurl = QualysIPProcessor.getIPTrackedPC(source_api=source_api)
    if simulate:
        print('%s' % addurl)
    else:
        response = QualysIPProcessor.createIPTrackedPC(target_api=target_api, addurl=addurl)
        if not handleResponse(response=response):
            print('ERROR: QualysIPProcessor.migrateIPTrackedPC() failed to create new IPs')
            ET.dump(response)
            sys.exit(1)

    addurl = QualysIPProcessor.getDNSTrackedVM(source_api=source_api)
    if simulate:
        print('%s' % addurl)
    else:
        response = QualysIPProcessor.createDNSTrackedVM(target_api=target_api, addurl=addurl)
        if not handleResponse(response=response):
            print('ERROR: QualysIPProcessor.migrateDNSTrackedVM() failed to create new IPs')
            ET.dump(response)
            sys.exit(1)

    addurl = QualysIPProcessor.getDNSTrackedPC(source_api=source_api)
    if simulate:
        print('%s' % addurl)
    else:
        response = QualysIPProcessor.createDNSTrackedPC(target_api=target_api, addurl=addurl)
        if not handleResponse(response=response):
            print('ERROR: QualysIPProcessor.migrateDNSTrackedPC() failed to create new IPs')
            ET.dump(response)
            sys.exit(1)

    addurl = QualysIPProcessor.getNETBIOSTrackedVM(source_api=source_api)
    if simulate:
        print('%s' % addurl)
    else:
        response = QualysIPProcessor.createNETBIOSTrackedVM(target_api=target_api, addurl=addurl)
        if not handleResponse(response=response):
            print('ERROR: QualysIPProcessor.migrateNETBIOSTrackedVM() failed to create new IPs')
            ET.dump(response)
            sys.exit(1)

    addurl = QualysIPProcessor.getNETBIOSTrackedPC(source_api=source_api)
    if simulate:
        print('%s' % addurl)
    else:
        response = QualysIPProcessor.createNETBIOSTrackedPC(target_api=target_api, addurl=addurl)
        if not handleResponse(response=response):
            print('ERROR: QualysIPProcessor.migrateNETBIOSTrackedPC() failed to create new IPs')
            ET.dump(response)
            sys.exit(1)
