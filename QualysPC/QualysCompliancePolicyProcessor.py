import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI
from os.path import exists, isfile


def responseHandler(resp: ET.Element):
    return True


def getFullPolicyList(source_api: QualysAPI.QualysAPI):
    """
    Get a full list of policies

    Parameters:
        source_api:         An object of class QualysAPI

    Returns:
        policy_list:        A list of python dictionaries containing policy data, used in payloads to recreate
                            the policy
    """
    fullurl = '%s/api/2.0/fo/compliance/policy/?action=list&details=Basic' % source_api.server
    resp = source_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysCompliancePolicyProcessor.getPolicyList failed')
        return None
    policy_list = []
    for i in resp.findall('.//POLICY'):
        policy = {
            'title': i.find('TITLE').text,
            'id': i.find('ID').text
        }
        ag_list = []
        if i.find('.//ASSET_GROUP'):
            for j in i.findall('.//ASSET_GROUP/ID'):
                ag_list.append(str(j.text))

        if i.find('ASSET_GROUP_IDS') is not None:
            if i.find('ASSET_GROUP_IDS').text is not None:
                ags = i.find('ASSET_GROUP_IDS').text
                for j in ags.split(','):
                    if j.find('-') > -1:
                        start = int(j.split('-')[0])
                        end = int(j.split('-')[1]) + 1
                        for k in range(start, end):
                            ag_list.append(str(k))
                    else:
                        ag_list.append(str(j))
        if len(ag_list) > 0:
            policy['asset_groups'] = ag_list
        else:
            policy['asset_groups'] = None

        if i.find('TAG_SET_INCLUDE') is not None:
            taglist = []
            for j in i.findall('TAG_SET_INCLUDE/TAG_ID'):
                taglist.append(j.text)
        else:
            taglist = None
        policy['tag_set_include'] = taglist

        if i.find('TAG_SET_EXCLUDE') is not None:
            taglist = []
            for j in i.findall('TAG_SET_EXCLUDE/TAG_ID'):
                taglist.append(j.text)
        else:
            taglist = None
        policy['tag_set_exclude'] = taglist

        if i.find('TAG_INCLUDE_SELECTOR') is not None:
            policy['tag_include_selector'] = i.find('TAG_INCLUDE_SELECTOR').text
        else:
            policy['tag_include_selector'] = None

        if i.find('TAG_EXCLUDE_SELECTOR') is not None:
            policy['tag_exclude_selector'] = i.find('TAG_EXCLUDE_SELECTOR').text
        else:
            policy['tag_exclude_selector'] = None

        policy_list.append(policy)

    return policy_list


def getPolicyIDList(source_api: QualysAPI.QualysAPI):
    """
    Get a list of policy IDs

    Parameters:
        source_api:         An object of type QualysAPI

    Returns:
        policylist:         A python list of string values containing policy IDs, representing all policy IDs in a
                            subscription
    """
    fullurl = '%s/api/2.0/fo/compliance/policy/?action=list&details=None' % source_api.server
    resp = source_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysCompliancePolicyProcessor.getPolicyList failed')
        return None
    policylist = []
    ids = resp.find('.//ID_SET')

    # Add all the single IDs
    for policyid in ids.findall('ID'):
        policylist.append(policyid.text)

    # Some IDs are encoded into ranges, so we need to break them up into singletons
    for policyrange in ids.findall('ID_RANGE'):
        start = int(policyrange.text.split('-')[0])
        end = int(policyrange.text.split('-')[1]) + 1
        for x in range(start, end):
            policylist.append(x)

    return policylist


def exportPolicy(source_api: QualysAPI.QualysAPI, policyid: str):
    """
    Export a policy

    Parameters:
        source_api:         An object of class QualysAPI
        policyid:           A string value containing a policy ID

    Returns:
        resp:               A string value containing raw XML, representing the policy content
    """
    fullurl = '%s/api/2.0/fo/compliance/policy/?action=export&show_user_controls=1&show_appendix=0&id=%s' % (
        source_api.server, policyid)
    resp = source_api.makeCall(url=fullurl, returnwith='text')

    return resp


def importPolicy(target_api: QualysAPI.QualysAPI, policyname: str, policy: str):
    """
    Import a policy

    Parameters:
        target_api:         An object of class QualysAPI
        policyname:         A string value containing the name to give the policy
        policy:             A string value containing the raw XML, representing the policy content, as exported
                            by exportPolicy()

    Returns:
        resp:               A document of type xml.etree.ElementTree.Element containing the full API response
    """
    fullurl = '%s/api/2.0/fo/compliance/policy/?action=import&create_user_controls=1&title=%s' % (target_api.server,
                                                                                                  policyname)
    headers = {'Content-Type': 'text/xml', 'Content-Length': str(len(policy))}
    resp = target_api.makeCall(url=fullurl, payload=policy, method='POST', headers=headers)
    if not responseHandler(resp):
        print('QualysCompliancePolicyProcessor.importPolicy failed')
        return None
    return resp


def addAssetGroups(target_api: QualysAPI.QualysAPI, policyid: str, asset_group_ids: str, evaluate: bool = False):
    """
    Add Asset Groups to a policy's scope

    Parameters:
        target_api:         An object of class QualysAPI
        policyid:           A string value containing the ID of the policy to update
        asset_group_ids:    A string value containing a comma-separated list of Asset Group IDs
        evaluate:           A boolean value to signal if the policy should be re-evaluated after the update

    Response:
        resp:               A document of type xml.etree.ElementTree.Element containing the full API response
    """
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


def setAssetGroupAssignment(target_api: QualysAPI.QualysAPI, asset_group_ids: str, policy_id: str):
    """
    Set and override the Asset Groups in a policy's scope

    Parameters:
        target_api:         An object of class QualysAPI
        asset_group_ids:    A string containing a comma-separated list of Asset Group IDs
        policy_id:          A string containing the ID of the policy to update

    Returns:
        resp:               A document of type xml.etree.ElementTree.Element containing the full API response
    """
    update_url = '%s/api/2.0/fo/compliance/policy?action=set_asset_group_ids&id=%s&asset_group_ids=%s' % (
        target_api.server, policy_id, asset_group_ids)

    resp = target_api.makeCall(url=update_url)
    return resp
