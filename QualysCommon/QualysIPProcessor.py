import QualysAPI
from xml.etree import ElementTree as ET

# TODO Convert DNS and NETBIOS convert functions to use payload

def getIPTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    """
    Get a list of IP addresses using IP Tracking in VM

    Parameters:
        source_api:         An object of type QualysAPI
        geturl:             A boolean value, True to get the URL and Payload for a subsequent API call.  Defaults to
                            True.  If True, overrides value of getipset
        getipset:           True to get the list of IPs.  Defaults to False.  Ignored if geturl is True

    Returns:
        url,payload:        If geturl is True and getipset is False:
            url:            The URL to be used in an API call to add the IPs to a subscription
            payload:        The payload to be used in the above API call

        ip_set:             If getipset is True and geturl is False, returns a list of strings containing IP addresses

        or

        None:               If no IP addresses using IP tracking are found in the VM subscription
    """
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
    """
    Convert an IP set into an API call using a url/payload pair.

    Parameters:
        ip_set:         A list of IP addresses as generated by getIPTrackedVM() with getipset=True and geturl=False

    Returns:
        url,payload:
            baseurl:        URL call to use in API call to add IP addresses to the VM subscription with IP Tracking method
            payload:        Payload to be used in above API call
    """
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
    """
    Make API call to add IP addresses to a VM subscription using the IP Tracking method

    Parameters:
        target_api:         An object of the class QualysAPI
        addurl:             The URL of the API call
        payload:            A Python Dictionary containing the payload to use in the API call

    Returns:
         resp:              A document of the type xml.etree.ElementTree.Element containing the full API response
    """
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getIPTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    """
    Get a list of IP addresses using IP Tracking in PC

    Parameters:
        source_api:         An object of type QualysAPI
        geturl:             A boolean value, True to get the URL and Payload for a subsequent API call.  Defaults to
                            True.  If True, overrides value of getipset
        getipset:           True to get the list of IPs.  Defaults to False.  Ignored if geturl is True

    Returns:
        url,payload:        If geturl is True and getipset is False:
            url:            The URL to be used in an API call to add the IPs to a subscription
            payload:        The payload to be used in the above API call

        ip_set:             If getipset is True and geturl is False, returns a list of strings containing IP addresses

        or

        None:               If no IP addresses using IP tracking are found in the PC subscription
    """

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
    """
    Convert an IP set into an API call for VM using a url/payload pair.

    Parameters:
        ip_set:         A list of IP addresses as generated by getIPTrackedVM() with getipset=True and geturl=False

    Returns:
        url,payload:
            baseurl:        URL call to use in API call to add IP addresses to the PC subscription with IP Tracking method
            payload:        Payload to be used in above API call
    """

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
    """
    Make API call to add IP addresses to a PC subscription using the IP Tracking method

    Parameters:
        target_api:         An object of the class QualysAPI
        addurl:             The URL of the API call
        payload:            A Python Dictionary containing the payload to use in the API call

    Returns:
         resp:              A document of the type xml.etree.ElementTree.Element containing the full API response
    """

    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getDNSTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    """
    Get a list of IP addresses using DNS Tracking in VM

    Parameters:
        source_api:         An object of type QualysAPI
        geturl:             A boolean value, True to get the URL and Payload for a subsequent API call.  Defaults to
                            True.  If True, overrides value of getipset
        getipset:           True to get the list of IPs.  Defaults to False.  Ignored if geturl is True

    Returns:
        url,payload:        If geturl is True and getipset is False:
            url:            The URL to be used in an API call to add the IPs to a subscription
            payload:        The payload to be used in the above API call

        ip_set:             If getipset is True and geturl is False, returns a list of strings containing IP addresses

        or

        None:               If no IP addresses using DNS tracking are found in the VM subscription
    """
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=0&certview_enabled=0&tracking_method=DNS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    if ip_set is None:
        return None

    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=DNS&enable_vm=1&enable_pc=0&ips='

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
    """
    Convert an IP set into an API call using a url/payload pair.

    Parameters:
        ip_set:         A list of IP addresses as generated by getDNSTrackedVM() with getipset=True and geturl=False

    Returns:
        url,payload:
            baseurl:        URL call to use in API call to add IP addresses to the VM subscription with DNS Tracking method
            payload:        Payload to be used in above API call
    """

    addurl = '/api/2.0/fo/asset/ip/'
    payload = {'action': 'add', 'tracking_method': 'DNS', 'enable_vm': '1', 'enable_pc': '0', 'ips': ''}

    for ip in ip_set.findall('*'):
        if payload['ips'] == '':
            payload['ips'] = '%s%s' % (payload['ips'], ip.text)
        else:
            payload['ips'] = '%s,%s' % (payload['ips'], ip.text)

    return addurl, payload


def createDNSTrackedVM(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    """
    Make API call to add IP addresses to a VM subscription using the DNS Tracking method

    Parameters:
        target_api:         An object of the class QualysAPI
        addurl:             The URL of the API call
        payload:            A Python Dictionary containing the payload to use in the API call

    Returns:
         resp:              A document of the type xml.etree.ElementTree.Element containing the full API response
    """

    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getDNSTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    """
    Get a list of IP addresses using DNS Tracking in PC

    Parameters:
        source_api:         An object of type QualysAPI
        geturl:             A boolean value, True to get the URL and Payload for a subsequent API call.  Defaults to
                            True.  If True, overrides value of getipset
        getipset:           True to get the list of IPs.  Defaults to False.  Ignored if geturl is True

    Returns:
        url,payload:        If geturl is True and getipset is False:
            url:            The URL to be used in an API call to add the IPs to a subscription
            payload:        The payload to be used in the above API call

        ip_set:             If getipset is True and geturl is False, returns a list of strings containing IP addresses

        or

        None:               If no IP addresses using DNS tracking are found in the PC subscription
    """

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
    """
    Convert an IP set into an API call using a url/payload pair.

    Parameters:
        ip_set:         A list of IP addresses as generated by getDNSTrackedPC() with getipset=True and geturl=False

    Returns:
        url,payload:
            baseurl:        URL call to use in API call to add IP addresses to the PC subscription with DNS Tracking method
            payload:        Payload to be used in above API call
    """

    addurl = '/api/2.0/fo/asset/ip/'
    payload = {'action': 'add', 'tracking_method': 'DNS', 'enable_vm': '0', 'enable_pc': '1', 'ips': ''}

    for ip in ip_set.findall('*'):
        if payload['ips'] == '':
            payload['ips'] = '%s%s' % (payload['ips'], ip.text)
        else:
            payload['ips'] = '%s,%s' % (payload['ips'], ip.text)

    return addurl, payload


def createDNSTrackedPC(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    """
    Make API call to add IP addresses to a PC subscription using the DNS Tracking method

    Parameters:
        target_api:         An object of the class QualysAPI
        addurl:             The URL of the API call
        payload:            A Python Dictionary containing the payload to use in the API call

    Returns:
         resp:              A document of the type xml.etree.ElementTree.Element containing the full API response
    """

    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getNETBIOSTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    """
    Get a list of IP addresses using NETBIOS Tracking in VM

    Parameters:
        source_api:         An object of type QualysAPI
        geturl:             A boolean value, True to get the URL and Payload for a subsequent API call.  Defaults to
                            True.  If True, overrides value of getipset
        getipset:           True to get the list of IPs.  Defaults to False.  Ignored if geturl is True

    Returns:
        url,payload:        If geturl is True and getipset is False:
            url:            The URL to be used in an API call to add the IPs to a subscription
            payload:        The payload to be used in the above API call

        ip_set:             If getipset is True and geturl is False, returns a list of strings containing IP addresses

        or

        None:               If no IP addresses using NETBIOS tracking are found in the VM subscription
    """

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
    """
    Convert an IP set into an API call using a url/payload pair.

    Parameters:
        ip_set:         A list of IP addresses as generated by getNETBIOSTrackedVM() with getipset=True and geturl=False

    Returns:
        url,payload:
            baseurl:        URL call to use in API call to add IP addresses to the VM subscription with NETBIOS
                            Tracking method
            payload:        Payload to be used in above API call
    """

    addurl = '/api/2.0/fo/asset/ip/'
    payload = {'action': 'add', 'tracking_method': 'NETBIOS', 'enable_vm': '1', 'enable_pc': '0', 'ips': ''}

    for ip in ip_set.findall('*'):
        if payload['ips'] == '':
            payload['ips'] = '%s%s' % (payload['ips'], ip.text)
        else:
            payload['ips'] = '%s,%s' % (payload['ips'], ip.text)

    return addurl, payload


def createNETBIOSTrackedVM(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    """
    Make API call to add IP addresses to a VM subscription using the NETBIOS Tracking method

    Parameters:
        target_api:         An object of the class QualysAPI
        addurl:             The URL of the API call
        payload:            A Python Dictionary containing the payload to use in the API call

    Returns:
         resp:              A document of the type xml.etree.ElementTree.Element containing the full API response
    """

    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp


def getNETBIOSTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    """
    Get a list of IP addresses using NETBIOS Tracking in PC

    Parameters:
        source_api:         An object of type QualysAPI
        geturl:             A boolean value, True to get the URL and Payload for a subsequent API call.  Defaults to
                            True.  If True, overrides value of getipset
        getipset:           True to get the list of IPs.  Defaults to False.  Ignored if geturl is True

    Returns:
        url,payload:        If geturl is True and getipset is False:
            url:            The URL to be used in an API call to add the IPs to a subscription
            payload:        The payload to be used in the above API call

        ip_set:             If getipset is True and geturl is False, returns a list of strings containing IP addresses

        or

        None:               If no IP addresses using NETBIOS tracking are found in the PC subscription
    """

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
    """
    Convert an IP set into an API call using a url/payload pair.

    Parameters:
        ip_set:         A list of IP addresses as generated by getNETBIOSTrackedPC() with getipset=True and geturl=False

    Returns:
        url,payload:
            baseurl:        URL call to use in API call to add IP addresses to the VM subscription with NETBIOS
                            Tracking method
            payload:        Payload to be used in above API call
    """

    addurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=NETBIOS&enable_vm=0&enable_pc=1&ips='
    payload = {'action': 'add', 'tracking_method': 'NETBIOS', 'enable_vm': '0', 'enable_pc': '1', 'ips': ''}

    for ip in ip_set.findall('*'):
        if payload['ips'] == '':
            payload['ips'] = '%s%s' % (payload['ips'], ip.text)
        else:
            payload['ips'] = '%s,%s' % (payload['ips'], ip.text)

    return addurl, payload


def createNETBIOSTrackedPC(target_api: QualysAPI.QualysAPI, addurl: str, payload: dict):
    """
    Make API call to add IP addresses to a PC subscription using the NETBIOS Tracking method

    Parameters:
        target_api:         An object of the class QualysAPI
        addurl:             The URL of the API call
        payload:            A Python Dictionary containing the payload to use in the API call

    Returns:
         resp:              A document of the type xml.etree.ElementTree.Element containing the full API response
    """

    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    return resp
