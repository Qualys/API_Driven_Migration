import xml.etree.ElementTree as ET
from API_Driven_Migration.QualysCommon import QualysAPI, QualysCloudConnectorProcessor


def testCloudConnector(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    adclist = QualysCloudConnectorProcessor.getConnectorList(source_api=source_api)
    if adclist is None:
        print('testCloudConnector failed')
        return False

    for adc in adclist.findall('.//*AwsAssetDataConnector'):
        adc = QualysCloudConnectorProcessor.pruneConnector(adc)
        if adc is None:
            continue
        if simulate:
            print('Ready to create %s' % adc.find('name').text)
            print(ET.tostring(adc, method='html', encoding='utf-8').decode())
            continue
        else:
            result = QualysCloudConnectorProcessor.createConnector(target_api=target_api, adc=adc)
            if result is not None:
                print('Successfully created %s' % adc.find('name').text)
            else:
                print('Failed to create %s' % adc.find('name').text)
    return True
