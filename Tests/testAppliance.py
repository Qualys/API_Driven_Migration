import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI, QualysApplianceProcessor


def testAppliances(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, appliances: list = None,
                   simulate: bool = False):
    if appliances is not None:
        appls = '&ids=%s' % (','.join(appliances))
    else:
        appls = []

    appl_list = QualysApplianceProcessor.getAppliances(source_api=source_api, appliances=appls)

    if simulate:
        print('%s' % (ET.tostring(appl_list, method='html', encoding='utf-8').decode()))
        return True

    mapping = {}
    for appl in appl_list.findall('APPLIANCE'):
        old_id = appl.find('ID').text
        new_id = QualysApplianceProcessor.replicateAppliance(target_api=target_api, appliance=appl)
        if new_id is None:
            print('testAppliances failed')
            return False
        mapping[old_id] = new_id
    return True

