import xml.etree.ElementTree as ET
from API_Driven_Migration.QualysCommon import QualysAPI


def responseHandler(resp):
    return_elem = resp.find('.//RETURN')
    if return_elem.attrib['status'] == 'SUCCESS':
        return True, '', ''
    else:
        return False, return_elem.attrib['number'], return_elem.find('MESSAGE').text




def generateURLs(userlist: ET.Element):
    fullurl = ''

    user_attribs = {
        'user_role': 'USER_ROLE',
        'business_unit': 'BUSINESS_UNIT',
        'first_name': 'CONTACT_INFO/FIRSTNAME',
        'last_name': 'CONTACT_INFO/LASTNAME',
        'title': 'CONTACT_INFO/TITLE',
        'phone': 'CONTACT_INFO/PHONE',
        'fax': 'CONTACT_INFO/FAX',
        'email': 'CONTACT_INFO/EMAIL',
        'company': 'CONTACT_INFO/COMPANY',
        'address1': 'CONTACT_INFO/ADDRESS1',
        'address2': 'CONTACT_INFO/ADDRESS2',
        'city': 'CONTACT_INFO/CITY',
        'country': 'CONTACT_INFO/COUNTRY',
        'state': 'CONTACT_INFO/STATE',
        'zip_code': 'CONTACT_INFO/ZIP_CODE',
        'time_zone_code': 'CONTACT_INFO/TIME_ZONE_CODE',
        'external_id': 'EXTERNAL_ID'
    }

    urllist = []

    for user in userlist.findall('USER'):
        fullurl = ''
        for attrib in user_attribs.keys():
            if user.find(user_attribs[attrib]) is not None:
                attrib_value = user.find(user_attribs[attrib]).text
                if attrib == 'business_unit':
                    if attrib_value != 'Unassigned':
                        fullurl = '%s&%s=%s' % (fullurl, attrib, attrib_value)
                else:
                    fullurl = '%s&%s=%s' % (fullurl, attrib, user.find(user_attribs[attrib]).text)

        if user.find('ASSIGNED_ASSET_GROUPS') is not None:
            asset_group_list = []
            for asset_group in user.findall('.//ASSET_GROUP_TITLE'):
                asset_group_list.append(asset_group.text)
            fullurl = '%s&asset_groups=%s' % (fullurl, ','.join(asset_group_list))

        fullurl = fullurl.replace(' ', '+')
        urllist.append(fullurl)

    return urllist


def getUsers(source_api: QualysAPI.QualysAPI):
    fullurl = "%s/msp/user_list.php" % source_api.server
    resp = source_api.makeCall(url=fullurl)

    return resp.find('USER_LIST')


def createUsers(target_api: QualysAPI.QualysAPI, urllist: list, send_email: bool = True, simulate: bool = False):
    if send_email:
        email = 'send_email=1'
    else:
        email = 'send_email=0'
    if simulate:
        print("QualysUserProcessor Simulation Output")
    for url in urllist:
        fullurl = '%s/msp/user.php?action=add&%s%s' % (target_api.server, email, url)
        if simulate:
            print(fullurl)
        else:
            resp = target_api.makeCall(url=fullurl)
            if not responseHandler(resp):
                print('QualysUserProcessor.createUsers failed')
                return False
    return True


def convertUser(user: ET.Element, send_email: bool = True, use_prefix: str = None, replace_all: str = None):
    user_attribs = {
        'user_role': 'USER_ROLE',
        'business_unit': 'BUSINESS_UNIT',
        'first_name': 'CONTACT_INFO/FIRSTNAME',
        'last_name': 'CONTACT_INFO/LASTNAME',
        'title': 'CONTACT_INFO/TITLE',
        'phone': 'CONTACT_INFO/PHONE',
        'fax': 'CONTACT_INFO/FAX',
        'email': 'CONTACT_INFO/EMAIL',
        'address1': 'CONTACT_INFO/ADDRESS1',
        'address2': 'CONTACT_INFO/ADDRESS2',
        'city': 'CONTACT_INFO/CITY',
        'country': 'CONTACT_INFO/COUNTRY',
        'state': 'CONTACT_INFO/STATE',
        'zip_code': 'CONTACT_INFO/ZIP_CODE',
        'time_zone_code': 'CONTACT_INFO/TIME_ZONE_CODE',
        'external_id': 'EXTERNAL_ID'
    }

    payload = {'action': 'add'}
    if send_email:
        payload['send_email'] = '1'
    else:
        payload['send_email'] = '0'

    for attrib in user_attribs.keys():
        if user.find(user_attribs[attrib]) is not None:
            attrib_value = user.find(user_attribs[attrib]).text

            # The user_role attribute must be in lower case on creation, but is capitalized in the output
            # Also spaces appear in the output which must be replaced with an underscore (_) for input
            if attrib == 'user_role':
                payload[attrib] = user.find(user_attribs[attrib]).text.lower().replace(' ', '_')
            # Business units may have a prefix, but Unassigned must not be prefixed
            elif attrib == 'business_unit':
                if attrib_value != 'Unassigned':
                    if use_prefix is None:
                        payload[attrib] = attrib_value
                    else:
                        payload[attrib] = '%s %s' % (use_prefix, attrib_value)
                else:
                    payload['business_unit'] = 'Unassigned'
            # The 'Auto' time zone code must be set with time_zone_code=''
            elif attrib == 'time_zone_code' and attrib_value == 'Auto':
                payload[attrib] = ''
            else:
                payload[attrib] = user.find(user_attribs[attrib]).text
        elif attrib == 'business_unit':
            payload[attrib] = 'Unassigned'

    if user.find('ASSIGNED_ASSET_GROUPS') is not None:
        asset_group_list = []
        for asset_group in user.findall('.//ASSET_GROUP_TITLE'):
            if use_prefix is not None and asset_group.text != 'All':
                asset_group_list.append('%s %s' % (use_prefix, asset_group.text))
            elif replace_all is not None and asset_group.text == 'All':
                asset_group_list.append(replace_all)
            else:
                asset_group_list.append(asset_group.text)
        payload['asset_groups'] = ','.join(asset_group_list)
    elif replace_all is not None:
        if user.find('USER_ROLE').text != 'Manager' and user.find('USER_ROLE').text != 'Unit Manager':
            if user.find('BUSINESS_UNIT') is None:
                payload['asset_groups'] = replace_all

    return payload


def createUser(target_api: QualysAPI.QualysAPI, payload: dict):
    url = '%s/msp/user.php' % target_api.server
    payload['action'] = 'add'
    resp = target_api.makeCall(url=url, payload=payload)
    return responseHandler(resp)

