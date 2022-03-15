import xml.etree.ElementTree as ET
from API_Driven_Migration.QualysCommon import QualysAPI


def responseHandler(resp: ET.Element):
    return True


def getAppliances(source_api: QualysAPI.QualysAPI, appliances: list = None):
    fullurl = '%s/api/2.0/fo/appliance/?action=list&output_mode=full' % source_api.server

    resp = source_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysApplianceProcessor.getAppliances failed')
        return None
    if resp.find('.//APPLIANCE_LIST') is not None:
        return resp.find('.//APPLIANCE_LIST')
    print('QualysApplianceProcessor.getAppliances failed: no Appliance List found')
    return None


def updateAppliance(target_api: QualysAPI.QualysAPI, appliance_id: str, vlans: list, routes: list):
    baseurl = '%s/api/2.0/fo/appliance/?action=update&id=%s&set_vlans=%s&set_routes=%s' % (
        appliance_id, target_api.server, ','.join(vlans), ','.join(routes))
    resp = target_api.makeCall(url=baseurl)
    if not responseHandler(resp):
        print('QualysApplianceProcessor.updateAppliance failed')
        return False
    return True


def createAppliance(target_api: QualysAPI.QualysAPI, name: str, polling_interval: str = '180', asset_group: str = None):
    fullurl = '%s/api/2.0/fo/appliance/?action=create&name=%s&polling_interval=%s&asset_group=%s' % (
        target_api.server, name, polling_interval, asset_group)
    resp = target_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysApplianceProcessor.createAppliance failed')
        return None
    return resp.find('.//*ID').text


def replicateAppliance(target_api: QualysAPI.QualysAPI, appliance: ET.Element):
    name = appliance.find('.//NAME').text
    poll = appliance.find('.//POLLING_INTERVAL').text.split(' ')[0]
    vlansxml = appliance.find('.//VLANS')
    routesxml = appliance.find('.//STATIC_ROUTES')
    vlans = []
    routes = []
    tags = []
    if appliance.find('.//ASSET_GROUP_COUNT').text == '0':
        assetgroupsxml = None
    else:
        assetgroupsxml = appliance.find('.//ASSET_GROUP_LIST')
    tagsxml = appliance.find('.//ASSET_TAGS_LIST')

    for vlan in vlansxml.findall('VLAN'):
        name = vlan.find('NAME').text
        ipv4addr = vlan.find('IP_ADDRESS').text
        mask = vlan.find('NETMASK').text
        vlanid = vlan.find('ID').text
        vlans.append('%s|%s|%s|%s|%s|%s' % (vlanid, ipv4addr, mask, name, '', ''))

    for route in routesxml.findall('ROUTE'):
        ipv4addr = route.find('IP_ADDRESS').text
        name = route.find('NAME').text
        mask = route.find('NETMASK').text
        ipv4gw = route.find('GATEWAY').text
        routes.append('%s|%s|%s|%s|%s|%s' % (ipv4addr, mask, ipv4gw, name, '', ''))

    new_appliance = createAppliance(target_api=target_api, name=name, polling_interval=poll)
    if new_appliance is None:
        print('QualysApplianceProcessor.replicateAppliance failed')
        return None

    if updateAppliance(target_api=target_api, appliance_id=new_appliance, vlans=vlans, routes=routes):
        return new_appliance
    print('QualysApplianceProcessor.replicateAppliance failed')
    return None
