import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def exportSubscriptionConfig(api: QualysAPI.QualysAPI):
    """
    Export all subscription configuration settings

    Parameters:
        api:            An object of the class QualysAPI

    Returns:
        response:       A document of type xml.etree.ElementTree.Element containing the full XML API response
    """
    fullurl = "%s/api/2.0/fo/subscription/index.php?action=export" % api.server
    response = api.makeCall(url=fullurl, method='GET')
    return response


def importSubscriptionConfig(api: QualysAPI.QualysAPI, configxml: ET.Element):
    """
    Import subscription configuration settings from XML obtained by exportSubscriptionConfig()

    Parameters:
        api:            An object of the class QualysAPI
        configxml:      An XML document of type xml.etree.ElementTree.Element as obtained by getSubscriptionConfig()

    Returns:
        response:       A XML document of type xml.etree.ElementTree.Element containing the full API response
    """
    fullurl = "%s/api/2.0/fo/subscription/index.php?action=import" % api.server
    payload = ET.tostring(configxml, method='html', encoding='utf-8').decode()
    headers = {'Content-type': 'text/xml'}
    response = api.makeCall(url=fullurl, method='POST', payload=payload, headers=headers)
    return response
