import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(resp: ET.Element):
    return True


def getVLANs(appliance: ET.Element):
    """
    Get the configured VLANS from a document of type xml.etree.elementTree.Element containing scanner appliance data

    Parameters:
        appliance:          An XML document of type xml.etree.ElementTree.Element containing appliance data

    Returns:
        vlans:              A list of VLAN strings for use in a further API call to configure an appliance
                            (e.g. '20|10.20.0.0|255.255.255.0|vlan20')
    """
    vlans = []
    if len(appliance.findall('.//VLAN')) == 0:
        return None
    for vlan in appliance.findall('.//VLAN'):
        vlan_string = '%s|%s|%s|%s' % (
            vlan.find('ID').text,
            vlan.find('IP_ADDRESS').text,
            vlan.find('NETMASk').text,
            vlan.find('NAME').text
        )
        vlans.append(vlan_string)
    return vlans


def getStaticRoutes(appliance: ET.Element):
    """
    Gets the configured static routes from a document of type xml.etree.ElementTree.Element containing scanner
    appliance data

    Parameters:
        appliance:      An XML document of type xml.etree.ElementTree.Element containing appliance data

    Returns:
        routes:         A list of static route strings for use in a further API call to configure an appliance
                        (e.g. '10.30.0.0|255.255.255.0|10.20.0.1|route30')
    """
    routes = []
    if appliance.find('STATIC_ROUTES') is None:
        return None
    for route in appliance.findall('.//ROUTE'):
        route_string = '%s|%s|%s|%s' % (
            route.find('IP_ADDRESS').text,
            route.find('NETMASK').text,
            route.find('GATEWAY').text,
            route.find('NAME').text
        )
        routes.append(route_string)
    return routes


def getAppliances(source_api: QualysAPI.QualysAPI):
    """
    Get a list of appliances with full details

    Parameters:
        source_api:         An object of the class QualysAPI

    Returns:
        resp:               An document of type xml.etree.ElementTree.Element containing the APPLIANCE_LIST
                            element of the API response

        or

        None if an error occurs or no appliances are contained in the output
    """
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
    """
    Update an appliance with VLAN and Static Route information

    Parameters:
        target_api:         An object of type QualysAPI
        appliance_id:       The ID of the scanner appliance to update
        vlans:              A list of VLAN strings as provided by getVLANs()
        routes:             A list of Static Route strings as provided by getStaticRoutes()

    Returns:
        True if appliance was successfully updated
        False if appliance update failed
    """
    baseurl = '%s/api/2.0/fo/appliance/?action=update&id=%s&set_vlans=%s&set_routes=%s' % (
        appliance_id, target_api.server, ','.join(vlans), ','.join(routes))
    resp = target_api.makeCall(url=baseurl)
    if not responseHandler(resp):
        print('QualysApplianceProcessor.updateAppliance failed')
        return False
    return True


def createAppliance(target_api: QualysAPI.QualysAPI, name: str, polling_interval: str = '180', asset_group: str = None):
    """
    Create a new scanner appliance in the target subscription with the provided name, polling interval and optionally
    asset group assignment.

    Parameters:
        target_api:         An object of the type QualysAPI
        name:               A string containing the name of the scanner appliance
        polling_interval:   A string containing the required polling interval in seconds of the scanner appliance,
                            defaults to 180 seconds
        asset_group:        A string containing the name of the Asset Group to assign the scanner appliance to,
                            defaults to None indicating no Asset Group assignment

    Returns:
        A string value containing the ID of the new scanner appliance
    """
    fullurl = '%s/api/2.0/fo/appliance/?action=create&name=%s&polling_interval=%s&asset_group=%s' % (
        target_api.server, name, polling_interval, asset_group)
    resp = target_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysApplianceProcessor.createAppliance failed')
        return None
    return resp.find('.//*ID').text


def replicateAppliance(target_api: QualysAPI.QualysAPI, appliance: ET.Element):
    """
    Creates a new scanner appliance in the target subscription to match the name and configuration of another
    appliance.  Uses the createAppliance() and updateAppliance() functions.

    Parameters:
        target_api:         An object of the class QualysAPI
        appliance:          A document of the type xml.etree.ElementTree.Element containing scanner appliance data

    Returns:
        The ID of the new appliance

        or

        None if the appliance creation failed
    """
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
