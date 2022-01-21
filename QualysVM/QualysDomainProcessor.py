import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(response: ET.Element):
    xmlreturn = response.find('.//RETURN')
    if xmlreturn.get('status') == 'SUCCESS':
        return True
    else:
        print('ERROR %s: %s' % (xmlreturn.get('number'), xmlreturn.text))
        return False


def getDomains(source_api: QualysAPI.QualysAPI):
    fullurl = '%s/msp/asset_domain_list.php' % source_api.server
    response = source_api.makeCall(url=fullurl)
    if response.find('.//CODE') is not None:
        print("FATAL: Error getting domain list")
        return None

    if response.find('.//DOMAIN') is None:
        print('No domains found')
        return None

    allurls = []
    addurl = '/msp/asset_domain.php?action=add'
    for domain in response.findall('.//DOMAIN'):
        # All domains have a domain name
        dname = domain.find('DOMAIN_NAME').text
        addurl = '%s&domain=%s' % (addurl, dname)
        # Some domains have a Netblock, some do not
        if domain.find('NETBLOCK') is None:
            continue
        else:
            netblock = ''
            for range in domain.findall('NETBLOCK/RANGE'):
                startip = range.find('START').text
                endip = range.find('END').text
                if not netblock == '':
                    netblock = '%s,' % netblock
                if startip == endip:
                    netblock = '%s' % startip
                else:
                    netblock = '%s-%s' % (startip, endip)
            addurl = '%s&netblock=%s' % (addurl, netblock)
        allurls.append(addurl)

    return allurls


def createDomains(target_api: QualysAPI.QualysAPI, allurls: list):
    for url in allurls:
        addurl = '%s/msp/asset_domain.php?action=add&%s' % (target_api.server, url)
        response = target_api.makeCall(url=addurl)
        if not responseHandler(response=response):
            return False
    return True


def editDomain(target_api: QualysAPI.QualysAPI, url: str):
    url = '%s/msp/asset_domain.php?action=edit&%s' % (target_api.server, url)
    response = target_api.makeCall(url=url)
    if not responseHandler(response):
        return None
    return response


def createDomainSingle(target_api: QualysAPI.QualysAPI, url: str):
    url = '%s/msp/asset_domain.php?action=add&%s' % (target_api.server, url)
    response = target_api.makeCall(url=url)
    if not responseHandler(response):
        return None
    return response


def getDomainsXML(source_api: QualysAPI.QualysAPI):
    fullurl = '%s/msp/asset_domain_list.php' % source_api.server
    response = source_api.makeCall(url=fullurl)
    if response.find('.//CODE') is not None:
        print("FATAL: Error getting domain list")
        return None

    if response.find('.//DOMAIN') is None:
        print('No domains found')
        return None
    return response
