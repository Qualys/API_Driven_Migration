from QualysCommon import QualysAPI


def getIPTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=0&certview_enabled=0&tracking_method=IP' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=IP&enable_vm=1&enable_pc=0&ips='

    addurl = baseurl
    for ip in ip_set.find('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def createIPTrackedVM(target_api: QualysAPI.QualysAPI, addurl: str):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl)
    return resp


def getIPTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=1&certview_enabled=0&tracking_method=IP' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=IP&enable_vm=0&enable_pc=1&ips='

    addurl = baseurl
    for ip in ip_set.find('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def createIPTrackedPC(target_api: QualysAPI.QualysAPI, addurl: str):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl)
    return resp


def getDNSTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=0&certview_enabled=0&tracking_method=DNS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    baseurl = '%s/api/2.0/fo/asset/ip/?action=add&tracking_method=DNS&enable_vm=1&enable_pc=0&ips='

    addurl = baseurl
    for ip in ip_set.find('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def createDNSTrackedVM(target_api: QualysAPI.QualysAPI, addurl: str):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl)
    return resp


def getDNSTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=1&certview_enabled=0&tracking_method=DNS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=DNS&enable_vm=0&enable_pc=1&ips='

    addurl = baseurl
    for ip in ip_set.find('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def createDNSTrackedPC(target_api: QualysAPI.QualysAPI, addurl: str):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl)
    return resp


def getNETBIOSTrackedVM(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=0&certview_enabled=0&tracking_method=NETBIOS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=NETBIOS&enable_vm=1&enable_pc=0&ips='

    addurl = baseurl
    for ip in ip_set.find('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def createNETBIOSTrackedVM(target_api: QualysAPI.QualysAPI, addurl: str):
    fullurl = '%s%s' % (addurl)
    resp = target_api.makeCall(url=fullurl)
    return resp


def getNETBIOSTrackedPC(source_api: QualysAPI.QualysAPI, geturl: bool = True, getipset: bool = False):
    fullurl = '%s/api/2.0/fo/asset/ip/?action=list&compliance_enabled=1&certview_enabled=0&tracking_method=NETBIOS' \
            % source_api.server
    ip_list = source_api.makeCall(url=fullurl)
    ip_set = ip_list.find('.//IP_SET')
    baseurl = '/api/2.0/fo/asset/ip/?action=add&tracking_method=NETBIOS&enable_vm=0&enable_pc=1&ips='

    addurl = baseurl
    for ip in ip_set.find('*'):
        if addurl == baseurl:
            addurl = '%s%s' % (addurl, ip.text)
        else:
            addurl = '%s,%s' % (addurl, ip.text)
    if geturl:
        return addurl
    if getipset:
        return ip_set


def createNETBIOSTrackedPC(target_api: QualysAPI.QualysAPI, addurl: str):
    fullurl = '%s%s' % (target_api.server, addurl)
    resp = target_api.makeCall(url=fullurl)
    return resp
