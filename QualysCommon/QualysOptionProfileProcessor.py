import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(response):
    if response.find('.//CODE'):
        print('ERROR %s: %s' % (response.find('.//CODE').text, response.find('.//TEXT').text))
        return False
    else:
        return True


def exportOptionProfiles(source_api: QualysAPI.QualysAPI):
    fullurl = '%s/api/2.0/fo/subscription/option_profile/?action=export&include_system_option_profiles=0' %\
              source_api.server
    response = source_api.makeCall(url=fullurl, method='GET')
    if not responseHandler(response):
        return None
    return response


def importOptionProfiles(target_api: QualysAPI.QualysAPI, optionprofiles: ET.Element):
    fullurl = '%s/api/2.0/fo/subscription/option_profile/?action=import' % target_api.server
    payload = ET.tostring(optionprofiles, method='html', encoding='utf-8').decode()
    response = target_api.makeCall(url=fullurl, payload=payload)
    if not responseHandler(response):
        return False
    return True
