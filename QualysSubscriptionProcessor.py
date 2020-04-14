import xml.etree.ElementTree as ET
import QualysAPI


def exportSubscriptionConfig(api: QualysAPI.QualysAPI):
    fullurl = "%s/api/2.0/fo/subscription/index.php?action=export" % api.server
    response = api.makeCall(url=fullurl, method='GET')
    return response


def importSubscriptionConfig(api: QualysAPI.QualysAPI, configxml: ET.Element):
    fullurl = "%s/api/2.0/fo/subscription/index.php?action=import" % api.server
    payload = ET.tostring(configxml, method='html', encoding='utf-8').decode()
    headers = {'Content-type': 'text/xml'}
    response = api.makeCall(url=fullurl, method='POST', payload=payload, headers=headers)
    return response
