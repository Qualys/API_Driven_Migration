import xml.etree.ElementTree as ET
import QualysAPI


def responseHandler(response: ET.Element):
    if response.find('.//CODE') is None:
        return True
    else:
        print('ERROR %s: %s' % (response.find('.//CODE').text, response.find('.//TEXT').text))
        return False


def getAssetGroups(source_api: QualysAPI.QualysAPI):
    fullurl = '%s/api/2.0/fo/asset/group/?action=list&show_attributes=ALL' % source_api.server
    resp = source_api.makeCall(url=fullurl)

    if not responseHandler(resp):
        return None

    aglist = resp.find('.//ASSET_GROUP_LIST')
    allurls = []
    baseurl = '/api/2.0/fo/asset/group/?action=add&'
    addurl = baseurl
    for ag in aglist.findall('ASSET_GROUP'):
        title=ag.find('TITLE').text
