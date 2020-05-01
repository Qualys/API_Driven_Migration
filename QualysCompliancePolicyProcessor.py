import xml.etree.ElementTree as ET
import QualysAPI


# TODO Fix How policies are exported and imported - it is a very picky system, and this script is very broken


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
