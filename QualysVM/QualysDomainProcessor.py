import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(response: ET.Element):
    """
    Handles an API response

    Parameters:
        response:           A document of type xml.etree.ElementTree.Element containing the full API response

    Returns:
        True                If the response was valid
        False               If the response contains errors
    """
    xmlreturn = response.find('.//RETURN')
    if xmlreturn.get('status') == 'SUCCESS':
        return True
    else:
        print('ERROR %s: %s' % (xmlreturn.get('number'), xmlreturn.text))
        return False


def getDomains(source_api: QualysAPI.QualysAPI):
    """
    Get a list of URLs, excluding the FQDN, with which Domains can be created in a subscription

    Parameters:
        source_api:         An object of the class QualysAPI

    Returns:
        allurls:            A list of strings containing the URLs, excluding the FQDN, which can be used to create
                            the domains which exist in the source subscription
    """
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
    """
    Create the domains generated by getDomains()

    Parameters:
        target_api:             An object of the class QualysAPI
        allurls:                A list of URLS, excluding the FQDN, generated by getDomains()

    Returns:
        True                    if all domains were successfully added
        False                   if one of the domains was not successfully added.  Returns on the first occurence of
                                an error
    """
    for url in allurls:
        addurl = '%s/msp/asset_domain.php?action=add&%s' % (target_api.server, url)
        response = target_api.makeCall(url=addurl)
        if not responseHandler(response=response):
            return False
    return True


def editDomain(target_api: QualysAPI.QualysAPI, url: str):
    """
    Edits an existing Domain using the specified URL parameters

    Parameters:
        target_api:             An object of the class QualysAPI
        url:                    A string containing the URL parameters required to perform the edit operation

    Returns
        response:               A document of type xml.etree.ElementTree.Element containing the full API response if
                                the edit operation was successful
        OR
        None                    If the create operation was unsuccessful
    """
    url = '%s/msp/asset_domain.php?action=edit&%s' % (target_api.server, url)
    response = target_api.makeCall(url=url)
    if not responseHandler(response):
        return None
    return response


def createDomainSingle(target_api: QualysAPI.QualysAPI, url: str):
    """
    Creates a single domain using the specified URL parameters

    Parameters:
        target_api:             An object of the class QualysAPI
        url:                    A string containing the URL parameters required to perform the create operation

    Returns
        response:               A document of type xml.etree.ElementTree.Element containing the full API response if
                                the operation was successful
        OR
        None                    If the create operation was unsuccessful
    """
    url = '%s/msp/asset_domain.php?action=add&%s' % (target_api.server, url)
    response = target_api.makeCall(url=url)
    if not responseHandler(response):
        return None
    return response


def getDomainsXML(source_api: QualysAPI.QualysAPI):
    """
    Gets the full XML output for the list of Domains

    Parameters:
        source_api:             An object of the class QualysAPI

    Returns:
        response:               A document of type xml.etree.ElementTree.Element containing the full API response
    """
    fullurl = '%s/msp/asset_domain_list.php' % source_api.server
    response = source_api.makeCall(url=fullurl)
    if response.find('.//CODE') is not None:
        print("FATAL: Error getting domain list")
        return None

    if response.find('.//DOMAIN') is None:
        print('No domains found')
        return None
    return response
