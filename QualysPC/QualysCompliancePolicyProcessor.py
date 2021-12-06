import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(resp: ET.Element):
    return True


def getPolicyList(source_api: QualysAPI.QualysAPI):
    fullurl = '%s/api/2.0/fo/compliance/policy/?action=list&details=None' % source_api.server
    resp = source_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysCompliancePolicyProcessor.getPolicyList failed')
        return None
    policylist = []
    ids = resp.find('.//ID_SET')
    for policyid in ids.findall('ID'):
        policylist.append(policyid.text)
    return policylist


def exportPolicy(source_api: QualysAPI.QualysAPI, policyid: str):
    fullurl = '%s/api/2.0/fo/compliance/policy/?action=export&show_user_controls=1&show_appendix=0&id=%s' % (
        source_api.server, policyid)
    resp = source_api.makeCall(url=fullurl, returnwith='text')

    return resp


def importPolicy(target_api: QualysAPI.QualysAPI, policyname: str, policy: str):
    fullurl = '%s/api/2.0/fo/compliance/policy/?action=import&create_user_controls=1&title=%s' % (target_api.server,
                                                                                                  policyname)
    headers = {'Content-Type': 'text/xml'}
    resp = target_api.makeCall(url=fullurl, payload=policy, method='POST', headers=headers)
    if not responseHandler(resp):
        print('QualysCompliancePolicyProcessor.importPolicy failed')
        return None
    return resp


def addAssetGroups(target_api: QualysAPI.QualysAPI, policyid: str, asset_group_ids: str, evaluate: bool = False):
    fullurl = '%s/api/2.0/fo/compliance/policy/?action=add_asset_group_ids' % target_api.server
    if evaluate:
        fullurl = '%s&evaluate_now=1' % fullurl
    else:
        fullurl = '%s&evaluate_now=0' % fullurl

    fullurl = '%s&id=%s&asset_group_ids=%s' % (fullurl, policyid, asset_group_ids)

    resp = target_api.makeCall(url=fullurl, method='POST')
    if not responseHandler(resp):
        print('QualysComplianceProcessor.addAssetGroups failed')
        return None
    return resp
