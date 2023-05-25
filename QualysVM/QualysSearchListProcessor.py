import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI
from datetime import datetime
from urllib import parse


def responseHandler(resp: ET.Element):
    return True


def getStaticSearchLists(source_api: QualysAPI.QualysAPI, ids: str = None):
    """
    Get static search lists from a subscription

    Parameters:
        source_api:         An object of the class QualysAPI
        ids:                (Optional) A string value containing a comma-separated list of Search List IDs to get

    Returns:
        A document of type xml.etree.ElementTree.Element which contains the STATIC_LISTS element from the API response
    """
    fullurl = '%s/api/2.0/fo/qid/search_list/static/?action=list' % source_api.server
    if ids is not None:
        fullurl = '%s&ids=%s' % (fullurl, ids)
    resp = source_api.makeCall(url=fullurl, method='GET')
    if not responseHandler(resp):
        print('QualysSearchListProcessor.getStaticSearchLists failed')
        return None
    return resp.find('.//STATIC_LISTS')


def getDynamicSearchLists(source_api: QualysAPI.QualysAPI, ids: str = None):
    """
    Get dynamic search lists from a subscription

    Parameters:
        source_api:         An object of the class QualysAPI
        ids:                (Optional) A string value containing a comma-separated list of Search List IDs to get

    Returns:
        A document of type xml.etree.ElementTree.Element which contains the DYNAMIC_LISTS element from the API response
    """
    fullurl = '%s/api/2.0/fo/qid/search_list/dynamic/?action=list&show_option_profiles=0&show_distribution_groups=0&' \
              'show_report_templates=0&show_remediation_policies=0&show_qids=0' % source_api.server
    if ids is not None:
        fullurl = '%s&ids=%s' % (fullurl, ids)
    resp = source_api.makeCall(url=fullurl, method='GET')
    if not responseHandler(resp):
        print('QualysSearchListProcessor.getDynamicSearchLists failed')
        return None
    return resp.find('.//DYNAMIC_LISTS')


def convertModifiedFilters(modstring: str, modtype: str, payload: dict = None):
    """
    Convert Search List criteria into a format accepted in an API request, either in payload or URL format.  Used by
    convertDynamicSearchList() and createDynamicSearchList

    Parameters:
        modstring:          A string containing the text of the criteria to convert
        modtype:            A string containing the type of criteria to convert
        payload:            (Optional) A python dictionary containing payload data to update with the
                            converted criteria data

    Returns:
        url:                If no payload parameter is passed, returns the modified criteria in URL format
        OR
        payload:            If a payload parameter is passed, returns the updated payload containing the modified
                            criteria
    """
    modstr = ''
    strelements = modstring.split(' ')
    if strelements[0] == 'NOT':
        notstr = '%s&not_%s=1' % (modstr, modtype)
        if payload is not None:
            payload['not_%s' % modtype] = '1'
        nul = strelements.pop(0)
    else:
        if payload is not None:
            payload['not_%s' % modtype] = '0'
        notstr = '%s&not_%s=0' % (modstr, modtype)

    if len(strelements) == 1:
        startdate, enddate = strelements[0].split('-')
        if startdate == enddate and enddate == datetime.now().strftime('%m/%d/%Y'):
            if payload is not None:
                payload['%s_date_today' % modtype] = '1'
            modstr = '&%s_date_today=1' % modtype
        else:
            if payload is not None:
                payload['%s_date_between' % modtype] = strelements[0]
            modstr = '&%s_date_between=%s' % (modtype, strelements[0])
    else:
        datetype = strelements.pop(0)
        if datetype == 'Previous':
            if 'year' in strelements:
                if payload is not None:
                    payload['%s_date_in_previous' % modtype] = 'Year'
                modstr = '&%s_date_in_previous=Year' % modtype
            elif 'month' in strelements:
                if payload is not None:
                    payload['%s_date_in_previous' % modtype] = 'Month'
                modstr = '&%s_date_in_previous=Month' % modtype
            elif 'week' in strelements:
                if payload is not None:
                    payload['%s_date_in_previous' % modtype] = 'Week'
                modstr = '&%s_date_in_previous=Week' % modtype
            elif 'quarter' in strelements:
                if payload is not None:
                    payload['%s_date_in_previous' % modtype] = 'Quarter'
                modstr = '&%s_date_in_previous=Quarter' % modtype
            else:
                print('QualysSearchListProcessor.convertUserModifiedFilters failed')
                if payload is not None:
                    return None, None
                return None
        elif datetype == 'Last':
            if payload is not None:
                payload['%s_date_within_last_days' % modtype] = strelements[1]
            modstr = '&%s_date_within_last_days=%s' % (modtype, strelements[1])
    modstr.replace(', ', ',')
    url = parse.quote('%s&%s' % (notstr, modstr))
    if payload is not None:
        return payload
    return url


def convertOther(otherstring: str, payload: dict = None):
    """
    Convert non-modifier elements of a search list into a format accepted by an API call.  Used by
    convertDynamicSearchList() and createDynamicSearchList()

    Parameters:
        otherstring:            A string value comma-delimited list of the parameters to convert
        payload:                (Optional) A python dictionary containing payload data to update with the converted
                                parameter

    Returns:
        retstr:                 If no payload parameter passed, the converted parameters in URL format
        OR
        payload:                If a payload parameter was passed, the updated payload containing the modified
                                parameters
    """
    retstr = ''
    elist = otherstring.split(', ')
    if 'Not exploitable due to configuration' in elist:
        if payload is not None:
            payload['qids_not_Exploitable'] = '1'
        else:
            retstr = '%s&qids_not_exploitable=1' % retstr
    if 'Non-running services' in elist:
        if payload is not None:
            payload['non_running_services'] = '1'
        else:
            retstr = '%s&non_running_services=1' % retstr
    if '2008 Sans 20' in elist:
        if payload is not None:
            payload['sans_20'] = '1'
        else:
            retstr = '%s&sans_20=1'
    if payload is not None:
        return payload
    else:
        return retstr


def createDynamicSearchList(target_api: QualysAPI.QualysAPI, searchlist: ET.Element, simulate: bool = False):
    """
    Create a dynamic search list from a source XML document

    Parameters:
        target_api:             An object of class QualysAPI
        searchlist:             A document of type xml.etree.ElementTree.Element containing the search list
                                data
        simulate:               If True, outputs the URL to the console and does not make the API call to create
                                the search list
                                If False, makes the API call to create the search list

    Returns:
         resp:                  A document of type xml.etree.ElementTree.Element containing the full API response
    """
    searchliststr = ''
    # criteria = searchlist.find('CRITERIA')
    criteria_map = {
        'vuln_title': 'VULNERABILITY_TITLE',
        'not_vuln_title': 'VULNERABILITY_TITLE',
        'discovery_methods': 'DISCOVERY_METHOD',
        'auth_types': 'AUTHENTICATION_TYPE',
        'user_configuration': 'USER_CONFIGURATION',
        'categories': 'CATEGORY',
        'not_categories': 'CATEGORY',
        'confirmed_severities': 'CONFIRMED_SEVERITY',
        'potential_severities': 'POTENTIAL_SEVERITY',
        'ig_severities': 'INFORMATION_SEVERITY',
        'products': 'PRODUCT',
        'not_products': 'PRODUCT',
        'patch_available': 'PATCH_AVAILABLE',
        'virtual_patch_available': 'VIRTUAL_PATCH_AVAILABLE',
        'cve_ids': 'CVE_ID',
        'not_cve_ids': 'CVE_ID',
        'exploitability': 'EXPLOITABILITY',
        'malware_associated': 'ASSOCIATED_MALWARE',
        'vendor_refs': 'VENDOR_REFERENCE',
        'not_vendor_refs': 'VENDOR_REFERENCE',
        'bugtraq_id': 'BUGTRAQ_ID',
        'not_bugtraq_id': 'BUGTRAQ_ID',
        'vuln_details': 'VULNERABILITY_DETAILS',
        'compliance_details': 'COMPLIANCE_DETAILS',
        'supported_modules': 'SUPPORTED_MODULES',
        'compliance_types': 'COMPLIANCE_TYPES',
        'qualys_top_lists': 'QUALYS_TOP_20',
        'cpe': 'CPE',
        'qids_not_exploitable': 'OTHER',
        'non_running_services': 'OTHER',
        'sans_20': 'OTHER',
        'nac_nam': 'NETWORK_ACCESS',
        'cvss_base': 'CVSS_BASE_SCORE',
        'cvss_temp': 'CVSS_TEMPORAL_SCORE',
        'cvss_access_vector': 'CVSS_ACCESS_VECTOR',
        'cvss_base_operand': 'CVSS_BASE_SCORE_OPERAND',
        'cvss_temp_operand': 'CVSS_TEMPORAL_SCORE_OPERAND',
        'cvss3_base': 'CVSS3_BASE_SCORE',
        'cvss3_temp': 'CVSS3_TEMPORAL_SCORE',
        'cvss3_base_operand': 'CVSS3_BASE_SCORE_OPERAND',
        'cvss3_temp_operand': 'CVSS3_TEMPORAL_SCORE_OPERAND',
        'user_modified': 'USER_MODIFIED',
        'published': 'PUBLISHED',
        'service_modified': 'SERVICE_MODIFIED'
    }

    globalsl = '0'
    if searchlist.find('GLOBAL').text == 'Yes':
        globalsl = '1'
    fullurl = '%s/api/2.0/fo/qid/search_list/dynamic/?action=create&title=%s&global=%s&%s' % (
        target_api.server,
        parse.quote(searchlist.find('TITLE').text),
        globalsl,
        searchliststr)
    if searchlist.find('COMMENTS') is not None:
        fullurl = '%s&comments=%s' % (fullurl, parse.quote(searchlist.find('COMMENTS').text))

    criteria = searchlist.find('CRITERIA')
    done_other = False
    for param in criteria_map.keys():
        if criteria_map[param] == 'OTHER' and criteria.find('OTHER') is not None:
            if done_other:
                continue
            fullurl = '%s&%s' % (fullurl, convertOther(criteria.find('OTHER').text))
            done_other = True
            continue
        if criteria_map[param] == 'USER_MODIFIED' and criteria.find('USER_MODIFIED') is not None:
            fullurl = '%s&%s' % (fullurl, convertModifiedFilters(criteria.find('USER_MODIFIED').text,
                                                                 'user_modified'))
            continue
        if criteria_map[param] == 'SERVICE_MODIFIED' and criteria.find('SERVICE_MODIFIED') is not None:
            fullurl = '%s&%s' % (fullurl, convertModifiedFilters(criteria.find('SERVICE_MODIFIED').text,
                                                                 'service_modified'))
            continue
        if criteria_map[param] == 'PUBLISHED' and criteria.find('PUBLISHED') is not None:
            fullurl = '%s&%s' % (fullurl, convertModifiedFilters(criteria.find('PUBLISHED').text, 'published'))
            continue
        if criteria_map[param] == 'DISCOVERY_METHOD':
            if criteria.find('DISCOVERY_METHOD').text == 'All':
                fullurl = '%s&%s' % (fullurl, 'discovery_methods=ALL')
            else:
                dm = criteria.find('DISCOVERY_METHOD').text
                if dm.find(' and ') >= 0:
                    dmlist = dm.split(' and ')
                    dmstr = ','.join(dmlist)
                else:
                    dmstr = dm
                fullurl = '%s&%s' % (fullurl, 'discovery_methods=%s' % dmstr)
            continue
        if criteria_map[param] == 'PATCH_AVAILABLE' and criteria.find('PATCH_AVAILABLE') is not None:
            if criteria.find('PATCH_AVAILABLE').text == 'Yes':
                fullurl = '%s&%s' % (fullurl, 'patch_available=1')
            else:
                fullurl = '%s&%s' % (fullurl, 'patch_available=0')
            continue
        if criteria_map[param] == 'VIRTUAL_PATCH_AVAILABLE' and criteria.find('VIRTUAL_PATCH_AVAILABLE') is not None:
            if criteria.find('VIRTUAL_PATCH_AVAILABLE').text == 'Yes':
                fullurl = '%s&%s' % (fullurl, 'virtual_patch_available=1')
            else:
                fullurl = '%s&%s' % (fullurl, 'virtual_patch_available=0')
            continue
        if criteria_map[param] == 'QUALYS_TOP_20' and criteria.find('QUALYS_TOP_20') is not None:
            toplists = []
            for toplist in criteria.find('QUALYS_TOP_20').text.split(','):
                if toplist == 'Top Internal 10':
                    toplists.append('Internal_10')
                if toplist == 'Top External 10':
                    toplists.append('External_10')
            fullurl = '%s&qualys_top_lists=%s' % (fullurl, ','.join(toplists))
            continue
        if criteria.find('%s' % criteria_map[param]) is not None:
            if param[0:4] == 'not_':
                val = '0'
                if criteria.find('%s' % criteria_map[param]).text[0:3] == 'NOT':
                    val = '1'
                fullurl = '%s&%s=%s' % (fullurl, param, val)
            else:
                if criteria_map[param][0:4] == 'NOT ':
                    fullurl = '%s&%s=%s' % (fullurl, param, parse.quote(
                        criteria.find('%s' % criteria_map[param]).text[4:]))
                else:
                    fullurl = '%s&%s=%s' % (fullurl, param, parse.quote(criteria.find('%s' % criteria_map[param]).text))

    if simulate:
        print('Request String : %s' % fullurl)
        return ''

    resp = target_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysSearchListProcessor.createDynamicSearchList failed')
        return None
    return resp


def convertDynamicSearchList(searchlist: ET.Element):
    """
    Converts a dynamic search list from XML format to URL/Payload format, excluding the FQDN

    Parameters:
        searchlist:             A document of type xml.etree.ElementTree.Element containing the search list data

    Returns:
        None, None              If an error is encountered during conversion of the XML data
        url, payload:
            url:                A string containing the URL, excluding the FQDN, of the API call to create the
                                dynamic search list
            payload:            A python dictionary containing the payload data to be used in the API call
    """
    searchliststr = ''
    url = '/api/2.0/fo/qid/search_list/dynamic/'
    payload = {'action': 'create'}

    criteria_map = {
        'vuln_title': 'VULNERABILITY_TITLE',
        'not_vuln_title': 'VULNERABILITY_TITLE',
        'discovery_methods': 'DISCOVERY_METHOD',
        'auth_types': 'AUTHENTICATION_TYPE',
        'user_configuration': 'USER_CONFIGURATION',
        'categories': 'CATEGORY',
        'not_categories': 'CATEGORY',
        'confirmed_severities': 'CONFIRMED_SEVERITY',
        'potential_severities': 'POTENTIAL_SEVERITY',
        'ig_severities': 'INFORMATION_SEVERITY',
        'products': 'PRODUCT',
        'not_products': 'PRODUCT',
        'patch_available': 'PATCH_AVAILABLE',
        'virtual_patch_available': 'VIRTUAL_PATCH_AVAILABLE',
        'cve_ids': 'CVE_ID',
        'not_cve_ids': 'CVE_ID',
        'exploitability': 'EXPLOITABILITY',
        'malware_associated': 'ASSOCIATED_MALWARE',
        'vendor_refs': 'VENDOR_REFERENCE',
        'not_vendor_refs': 'VENDOR_REFERENCE',
        'bugtraq_id': 'BUGTRAQ_ID',
        'not_bugtraq_id': 'BUGTRAQ_ID',
        'vuln_details': 'VULNERABILITY_DETAILS',
        'compliance_details': 'COMPLIANCE_DETAILS',
        'supported_modules': 'SUPPORTED_MODULES',
        'compliance_types': 'COMPLIANCE_TYPES',
        'qualys_top_lists': 'QUALYS_TOP_20',
        'cpe': 'CPE',
        'qids_not_exploitable': 'OTHER',
        'non_running_services': 'OTHER',
        'sans_20': 'OTHER',
        'nac_nam': 'NETWORK_ACCESS',
        'cvss_base': 'CVSS_BASE_SCORE',
        'cvss_temp': 'CVSS_TEMPORAL_SCORE',
        'cvss_access_vector': 'CVSS_ACCESS_VECTOR',
        'cvss_base_operand': 'CVSS_BASE_SCORE_OPERAND',
        'cvss_temp_operand': 'CVSS_TEMPORAL_SCORE_OPERAND',
        'cvss3_base': 'CVSS3_BASE_SCORE',
        'cvss3_temp': 'CVSS3_TEMPORAL_SCORE',
        'cvss3_base_operand': 'CVSS3_BASE_SCORE_OPERAND',
        'cvss3_temp_operand': 'CVSS3_TEMPORAL_SCORE_OPERAND'
    }

    globalsl = '0'
    fullurl = ''
    if searchlist.find('GLOBAL').text == 'Yes':
        globalsl = '1'
    payload['title'] = searchlist.find('TITLE').text
    payload['global'] = globalsl

    if searchlist.find('COMMENTS') is not None:
        payload['comments'] = searchlist.find('COMMENTS').text

    criteria = searchlist.find('CRITERIA')
    for param in criteria_map.keys():
        if criteria_map[param] == 'OTHER' and criteria.find('OTHER') is not None:
            payload = convertOther(otherstring=criteria.find('OTHER').text, payload=payload)
            continue
        if criteria_map[param] == 'USER_MODIFIED' and criteria.find('USER_MODIFIED') is not None:
            payload = convertModifiedFilters(criteria.find('USER_MODIFIED').text, 'user_modified', payload=payload)
            if payload is None:
                return None, None
            continue
        if criteria_map[param] == 'SERVICE_MODIFIED' and criteria.find('SERVICE_MODIFIED') is not None:
            payload = convertModifiedFilters(criteria.find('SERVICE_MODIFIED').text, 'service_modified',
                                             payload=payload)
            if payload is None:
                return None, None
            continue
        if criteria_map[param] == 'PUBLISHED' and criteria.find('PUBLISHED') is not None:
            payload = convertModifiedFilters(criteria.find('PUBLISHED').text, 'published', payload=payload)
            if payload is None:
                return None, None
            continue
        if criteria_map[param] == 'DISCOVERY_METHOD':
            if criteria.find('DISCOVERY_METHOD').text == 'All':
                payload['discovery_methods'] = 'ALL'
            else:
                dm = criteria.find('DISCOVERY_METHOD').text
                if dm.find(' and ') >= 0:
                    dmlist = dm.split(' and ')
                    dmstr = ','.join(dmlist)
                else:
                    dmstr = dm
                payload['discovery_methods'] = dmstr

            continue
        if criteria_map[param] == 'PATCH_AVAILABLE' and criteria.find('PATCH_AVAILABLE') is not None:
            if criteria.find('PATCH_AVAILABLE').text == 'Yes':
                payload['patch_available'] = '1'
            else:
                payload['patch_available'] = '0'

            continue
        if criteria_map[param] == 'VIRTUAL_PATCH_AVAILABLE' and criteria.find('VIRTUAL_PATCH_AVAILABLE') is not None:
            if criteria.find('VIRTUAL_PATCH_AVAILABLE').text == 'Yes':
                payload['virtual_patch_available'] = '1'
            else:
                payload['virtual_patch_available'] = '0'

            continue
        if criteria_map[param] == 'QUALYS_TOP_20' and criteria.find('QUALYS_TOP_20') is not None:
            toplists = []
            for toplist in criteria.find('QUALYS_TOP_20').text.split(','):
                if toplist == 'Top Internal 10':
                    toplists.append('Internal_10')
                if toplist == 'Top External 10':
                    toplists.append('External_10')
            payload['qualys_top_lists'] = ','.join(toplists)

            continue
        if criteria.find('%s' % criteria_map[param]) is not None:
            if param[0:4] == 'not_':
                val = '0'
                if criteria.find('%s' % criteria_map[param]).text[0:3] == 'NOT':
                    val = '1'
                payload[param] = val
            else:
                if criteria_map[param][0:4] == 'NOT ':
                    payload[param] = criteria.find('%s' % criteria_map[param]).text[4:]
                else:
                    payload[param] = criteria.find('%s' % criteria_map[param]).text
                    fullurl = '%s&%s=%s' % (fullurl, param, parse.quote(criteria.find('%s' % criteria_map[param]).text))

    return url, payload


def convertStaticSearchList(searchlist: ET.Element):
    """
    Converts a static search list from XML format to URL/Payload format, excluding the FQDN

    Parameters:
        searchlist:             A document of type xml.etree.ElementTree.Element containing the search list data

    Returns:
        None, None              If an error is encountered during conversion of the XML data
        url, payload:
            url:                A string containing the URL, excluding the FQDN, of the API call to create the
                                dynamic search list
            payload:            A python dictionary containing the payload data to be used in the API call
    """

    comments = ''
    is_global = '0'
    qidlist = []
    url = '/api/2.0/fo/qid/search_list/static/'

    title = searchlist.find('TITLE').text
    if searchlist.find('GLOBAL') == 'Yes':
        is_global = '1'
    if searchlist.find('COMMENTS') is not None:
        comments = searchlist.find('COMMENTS').text
    for qid in searchlist.findall('.//QID'):
        qidlist.append(qid.text)

    payload = {'action': 'create',
               'title': title,
               'qids': ','.join(qidlist),
               'global': is_global}

    if comments != '':
        payload['comments'] = comments
    return url, payload


def createStaticSearchList(target_api: QualysAPI.QualysAPI, searchlist: ET.Element, simulate: bool = False):
    """
    Create a static search list from a source XML document

    Parameters:
        target_api:             An object of class QualysAPI
        searchlist:             A document of type xml.etree.ElementTree.Element containing the search list
                                data
        simulate:               If True, outputs the URL to the console and does not make the API call to create
                                the search list
                                If False, makes the API call to create the search list

    Returns:
         resp:                  A document of type xml.etree.ElementTree.Element containing the full API response
    """
    comments = ''
    isGlobal = '0'
    qidlist = []

    title = searchlist.find('TITLE').text
    if searchlist.find('GLOBAL') == 'Yes':
        isGlobal = '1'
    if searchlist.find('COMMENTS') is not None:
        comments = searchlist.find('COMMENTS').text
    for qid in searchlist.findall('.//QID'):
        qidlist.append(qid.text)

    fullurl = '%s/api/2.0/fo/qid/search_list/static/?action=create&title=%s&qids=%s&global=%s' % (
        target_api.server,
        title,
        ','.join(qidlist),
        isGlobal)

    if comments != '':
        fullurl = '%s&%s' % (fullurl, comments)

    if simulate:
        print('Request URL : %s' % fullurl)
        return fullurl

    resp = target_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysSearchListProcessor.createStaticSearchList failed')
        return None
    return resp
