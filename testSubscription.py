import QualysAPI
import QualysSubscriptionProcessor
import xml.etree.ElementTree as ET

def testSubscription(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    configxml = QualysSubscriptionProcessor.exportSubscriptionConfig(api=source_api)
    if simulate:
        print('================================================================================')
        print('SUBSCRIPTION PREFERENCES')
        print('********************************************************************************')
        ET.dump(configxml)
        print('================================================================================')
        return None
    else:
        response = QualysSubscriptionProcessor.importSubscriptionConfig(api=target_api, configxml=configxml)
        return response
