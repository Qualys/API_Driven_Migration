import xml.etree.ElementTree as ET
import QualysAPI
import csv


def responseHandler(resp):
    return True


def generateURLs(userlist: ET.Element):
    fullurl = ''
    user_attribs = {
        'user_role': 'USER_ROLE',
        'business_unit': 'BUSINESS_UNIT',
        'asset_groups': '',
        'first_name': 'FIRSTNAME',
        'last_name': 'LASTNAME',
        'title': 'TITLE',
        'phone': 'PHONE',
        'fax': 'FAX',
        'email': 'EMAIL',
        'company': 'COMPANY',
        'address1': 'ADDRESS1',
        'address2': 'ADDRESS2',
        'city': 'CITY',
        'country': 'COUNTRY',
        'state': 'STATE',
        'zip_code': 'ZIP_CODE',
        'external_id': 'EXTERNAL_ID'
    }

    urllist = []

    for user in userlist.findall('USER'):
        for attrib in user_attribs.keys():
            if user.find(user_attribs[attrib]) is not None:
                fullurl = '%s&%s=%s' % (fullurl, attrib, user.find(user_attribs[attrib]).text)
                fullurl.replace(' ','+')
                urllist.append(fullurl)

    return urllist


def getUsers(source_api: QualysAPI.QualysAPI):
    fullurl = "%s/msp/user_list.php" % source_api.server
    resp = source_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysUserProcessor.getUsers failed')
        return None
    return resp.find('USER_LIST')


def createUsers(target_api: QualysAPI.QualysAPI, userlist: list):
    for url in userlist:
        fullurl = '%s/msp/user.php?action=add&send_email=1%s' % (target_api.server, url)
        resp = target_api.makeCall(url=fullurl)
        if not responseHandler(resp):
            print('QualysUserProcessor.createUsers failed')
            return False
    return True
