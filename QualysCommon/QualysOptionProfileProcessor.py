import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(response):
    if response.find('.//CODE'):
        print('ERROR %s: %s' % (response.find('.//CODE').text, response.find('.//TEXT').text))
        return False
    else:
        return True


def exportOptionProfiles(source_api: QualysAPI.QualysAPI):
    """
    Exports all Option Profiles from a subscription

    Parameters:
        source_api:         An object of the class QualysAPI

    Returns:
        response:           A document of the type xml.etree.ElementTree.Element containing the full API response
    """
    fullurl = '%s/api/2.0/fo/subscription/option_profile/?action=export&include_system_option_profiles=0' %\
              source_api.server
    response = source_api.makeCall(url=fullurl, method='GET')
    if not responseHandler(response):
        return None
    return response


def importOptionProfiles(target_api: QualysAPI.QualysAPI, optionprofiles: ET.Element):
    """
    Imports Option Profiles to a subscription

    Parameters:
        target_api:         An object of the class QualysAPI

    Returns:
        response:           A document of the type xml.etree.ElementTree.Element containing the full API response
    """
    fullurl = '%s/api/2.0/fo/subscription/option_profile/?action=import' % target_api.server
    ET.indent(optionprofiles, space='  ', level=0)
    payload = ET.tostring(optionprofiles, method='xml', encoding='utf-8', short_empty_elements=False).decode()
    headers = {'Content-Type': 'text/xml'}
    response = target_api.makeCall(url=fullurl, payload=payload, headers=headers, returnwith='text')
    return response


