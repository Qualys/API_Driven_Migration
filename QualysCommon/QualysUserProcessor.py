import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(resp):
    return True


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
    if not responseHandler(resp):
        print('QualysUserProcessor.getUsers failed')
        return None
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
