import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(resp: ET.Element):
    if resp is None:
        return False
    return True


def getVirtualHosts(source_api: QualysAPI.QualysAPI, networks: bool = False):
    hostlist = []

    fullurl = '%s/api/2.0/fo/asset/vhost/?action=list' % source_api.server
    resp = source_api.makeCall(url=fullurl, method='GET')
    if not responseHandler(resp):
        print('QualysVirtualHostProcessor.getVirtualHosts ERROR: Could not obtain  Virtual Host list from source')
        return None
    if resp.find('RESPONSE/VIRTUAL_HOST_LIST') is not None:
        for host in resp.findall('.//VIRTUAL_HOST'):
            vhost = {}
            fqdns = []
            vhost['IP'] = host.find('IP').text
            vhost['PORT'] = host.find('PORT').text
            for fqdn in host.findall('FQDN'):
                fqdns.append(fqdn.text)
            vhost['FQDNS'] = fqdns
            if networks:
                if host.find('NETWORK_ID') is None:
                    print('QualysVirtualHostProcessor.getVirtualHosts ERROR: Networks enabled but no Network ID found')
                    return None
                vhost['NETWORK_ID'] = host.find('NETWORK_ID').text
            hostlist.append(vhost)
    else:
        print('QualysVirtualHostProcessor.getVirtualHosts ERROR: Cannot find Virtual Host List in output')
        return None

    return hostlist


def convertVirtualHosts(vhostlist: list):
    urllist = []
    vhost: dict
    for vhost in vhostlist:
        url = '/api/2.0/fo/asset/vhost/?action=create&ip=%s&port=%s&fqdn=%s' % (
            vhost['IP'],
            vhost['PORT'],
            ','.join(vhost['FQDNS'])
        )
        if 'NETWORK_ID' in vhost.keys():
            url = '%s&network_id=%s' % (url, vhost['NETWORK_ID'])
        urllist.append(url)
    return urllist


def createVirtualHosts(urllist: list, target_api: QualysAPI.QualysAPI):
    for url in urllist:
        fullurl = '%s%s' % (target_api.server, url)
        resp = target_api.makeCall(url=fullurl)
        if not responseHandler(resp):
            print('QualysVirtualHostProcessor.createVirtualHosts ERROR: Could not validate response')
            return False
    return True
