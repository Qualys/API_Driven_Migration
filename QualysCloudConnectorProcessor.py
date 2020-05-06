import xml.etree.ElementTree as ET
import QualysAPI


def responseHandler(resp: ET.Element):
    return True


def generateConnectorMap(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI):
    connectormap = {}
    srcurl = '%s/qps/rest/2.0/search/am/assetdataconnector/?fields=id,name,type' % source_api.server
    tgturl = '%s/qps/rest/2.0/search/am/assetdataconnector/?fields=id,name,type' % target_api.server

    slist = source_api.makeCall(url=srcurl)
    tlist = target_api.makeCall(url=tgturl)

    if slist.find('.//AssetDataConnector') is None:
        print('QualysCloudConnectorProcessor.generateConnectorMap: Failed to generate list of source connectors')
        return None
    if tlist.find('.//AssetDataConnector') is None:
        print('QualysCloudConnectorProcessor.generateConnectorMap: Failed to generate list of target connectors')
        return None

    for adc in slist.findall('.//AssetDataConnector'):
        if tlist.find('.//AssetDataConnector/[name="%s"]' % adc.find('name').text) is None:
            print('QualysCloudConnectorProcessor.generateConnectorMap: Could not match %s with target'
                  % adc.find('name').text)
            continue
        connectormap[slist.find('name').text] = [slist.find('id').text, tlist.find('id').text]
    del slist, tlist
    return connectormap


def getConnectorList(source_api: QualysAPI.QualysAPI, names: list = None):
    fullurl = '%s/qps/rest/2.0/search/am/awsassetdataconnector' % source_api.server
    sr = ET.Element('ServiceRequest')
    filters = ET.SubElement(sr, 'filters')
    if names is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'name')
        criteria.set('operator', 'IN')
        criteria.text = ",".join(names)
    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()

    resp = source_api.makeCall(url=fullurl, payload=payload)
    if not responseHandler(resp):
        print('QualysCloudConnectorProcessor.getConnectorList failed')
        return None
    return resp


def createConnector(target_api: QualysAPI.QualysAPI, adc: ET.Element):
    pass


def pruneConnector(adc: ET.Element):
    if adc.find('.//authRecord'):
        if adc.find('authRecord').text != '':
            print('AWS Asset Data Connectors with Authentication Records cannot be migrated, skipping %s' %
                  adc.find('name').text)
            return None
    if adc.find('.//arn') is None:
        print('No ARN value found for AWS Asset Data Connector %s - skipping' % adc.find('name').text)
        return None
    for prune in ['id', 'lastSync', 'connectorState', 'type']:
        prune_element = adc.find(prune)
        adc.remove(prune_element)
    if adc.find('defaultTags/list') is not None:
        adc.find('defaultTags/list').tag = 'set'
    if adc.find('activation/list') is not None:
        adc.find('activation/list').tag = 'set'

    return adc


