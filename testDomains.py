import xml.etree.ElementTree as ET
import QualysDomainProcessor
import QualysAPI


def testDomains(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    addurls = QualysDomainProcessor.getDomains(source_api=source_api)
    if simulate:
        print('================================================================================')
        print('DOMAINS')
        print('********************************************************************************')
        for url in addurls:
            print('%s' % url)
        print('================================================================================')
    else:
        QualysDomainProcessor.createDomains(target_api=target_api, allurls=addurls)
