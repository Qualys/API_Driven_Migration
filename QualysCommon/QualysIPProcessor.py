from QualysCommon import QualysAPI
from xml.etree import ElementTree as ET

# TODO Convert DNS and NETBIOS convert functions to use payload

def getIPTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=0&certview_enabled=0&tracking_method=IP' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    if ip_set is None:
        return None
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=IP&enable_vm=1&enable_pc=0&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def convertIPTrackedVMSet(ip_set: ET.Element):
    baseurl = '/api/2.0/fo/asset/ip/'

    payload = {
        'action': 'add',
        'tracking_method': 'IP',
        'enable_vm': '1',
        'enable_pc': '0',
        'ips': ''
    }

    for ip in ip_set.findall('*'):
        if payload['ips'] == '':
            payload['ips'] = ip.text
        else:
            payload['ips'] = '%s,%s' % (payload['ips'], ip.text)

    return baseurl, payload


def createIPTrackedVM(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getIPTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=1&certview_enabled=0&tracking_method=IP' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    if ip_set is None:
        return None

    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=IP&enable_vm=0&enable_pc=1&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def convertIPTrackedPCSet(ip_set: ET.Element):
    baseurl = '/api/2.0/fo/asset/ip/'

    payload = {
        'action': 'add',
        'tracking_method': 'IP',
        'enable_vm': '0',
        'enable_pc': '1',
        'ips': ''
    }

    for ip in ip_set.findall('*'):
        if payload['ips'] == '':
            payload['ips'] = ip.text
        else:
            payload['ips'] = '%s,%s' % (payload['ips'], ip.text)

    return baseurl, payload


def createIPTrackedPC(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getDNSTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=0&certview_enabled=0&tracking_method=DNS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    if ip_set is None:
        return None

    baseurl = '%s/api/2.0/fo/asset/ip/?action=add&tracking_method=DNS&enable_vm=1&enable_pc=0&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def convertDNSTrackedVMSet(ip_set: ET.Element):
    baseurl = '%s/api/2.0/fo/asset/ip/?action=add&tracking_method=DNS&enable_vm=1&enable_pc=0&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)

    return addurl


def createDNSTrackedVM(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getDNSTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=1&certview_enabled=0&tracking_method=DNS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    if ip_set is None:
        return None

    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=DNS&enable_vm=0&enable_pc=1&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def convertDNSTrackedPCSet(ip_set: ET.Element):
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=DNS&enable_vm=0&enable_pc=1&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)

    return addurl


def createDNSTrackedPC(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getNETBIOSTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=0&certview_enabled=0&tracking_method=NETBIOS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    if ip_set is None:
        return None

    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=NETBIOS&enable_vm=1&enable_pc=0&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def convertNETBIOSTrackedVMSet(ip_set: ET.Element):
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=NETBIOS&enable_vm=1&enable_pc=0&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)

    return addurl


def createNETBIOSTrackedVM(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    fullurl = '%s%s' % addurl
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getNETBIOSTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=1&certview_enabled=0&tracking_method=NETBIOS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    if ip_set is None:
        return None

    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=NETBIOS&enable_vm=0&enable_pc=1&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def convertNETBIOSTrackedPCSet(ip_set: ET.Element):
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=NETBIOS&enable_vm=0&enable_pc=1&ips='

    addurl = baseurl
    for ip in ip_set.findall('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)

    return addurl


def createNETBIOSTrackedPC(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp
