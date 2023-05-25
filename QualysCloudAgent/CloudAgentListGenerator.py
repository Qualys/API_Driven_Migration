from QualysCommon import QualysAPI
from xml.etree import ElementTree as ET
import json


def getActivationKeys(api: QualysAPI.QualysAPI):
    """
    Obtains from a subscription the list of Cloud Agent Activation Keys

    Parameters:
        api:        An object of the class QualysAPI

    Returns:
        keys:       A list containing the Cloud Agent Activation Keys in JSON format
    """
    fullurl = '%s/qps/rest/1.0/search/ca/agentactkey/' % api.server
    startat = 1
    pagesize = 1000
    keys = []
    endofdata = False

    while not endofdata:
        sr = ET.Element('ServiceRequest')
        pref = ET.SubElement(sr, 'preferences')
        sfo = ET.SubElement(pref, 'startFromOffset')
        sfo.text = str(startat)
        lr = ET.SubElement(pref, 'limitResults')
        lr.text = str(pagesize)

        payload = ET.tostring(sr, encoding='utf-8', method='xml').decode()
        headers = {'Content-type': 'text/xml', 'Accept': 'application/json'}
        resp = api.makeCall(url=fullurl, payload=payload, headers=headers, returnwith='text')
        jresp = json.loads(resp)
        keys.extend(jresp["ServiceResponse"]["data"])
        if jresp["ServiceResponse"]["hasMoreRecords"] == 'false':
            endofdata = True
        startat = startat + pagesize

    return keys


def getAssets(api: QualysAPI.QualysAPI, key: str):
    """
    Obtains the Cloud Agent asset data for assets registered under a given Cloud Agent Activation Key

    Parameters:
        api:        An object of the class QualysAPI
        key:        A string value containing the Activation Key UUID

    Returns:
        assets:     A list containing the assets registered under the given Cloud Agent Activation Key
    """
    fullurl = '%s/qps/rest/2.0/search/am/hostasset/?fields=name,agentInfo.agentId,agentInfo.platform' % api.server
    startat = 1
    pagesize = 1000
    assets = []
    endofdata = False
    while not endofdata:
        sr = ET.Element('ServiceRequest')
        pref = ET.SubElement(sr, 'preferences')
        sfo = ET.SubElement(pref, 'startFromOffset')
        sfo.text = str(startat)
        lr = ET.SubElement(pref, 'limitResults')
        lr.text = str(pagesize)
        filters = ET.SubElement(sr, 'filters')
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'activationKey')
        criteria.set('operator', 'EQUALS')
        criteria.text = key

        payload = ET.tostring(sr, encoding='utf-8', method='xml').decode()
        headers = {'Content-type': 'text/xml', 'Accept': 'application/json'}
        resp = api.makeCall(url=fullurl, payload=payload, headers=headers, returnwith='text')
        jresp = json.loads(resp)
        assets.extend(jresp["ServiceResponse"]["data"])
        if jresp["ServiceResponse"]["hasMoreRecords"] == 'false':
            endofdata = True
        startat = startat + pagesize

    return assets


def outputList(assets: list, keyid: str):
    """
    Writes the Cloud Agent asset data in CSV format, in preparation for Cloud Agent migration.

    Parameters:
        assets:     List of assets as provided by getAssets
        keyid:      A string value containing the UUID of the target Cloud Agent Activation Key to which the
                    assets will be reassigned

    Returns:
        Nothing

    Outputs:
        keyid.csv:  Where 'keyid' is the value of the passed 'keyid' parameter
    """
    outfile = "%s.csv" % keyid
    with open(outfile, 'w') as f:
        for asset in assets:
            print("%s : %s" % (asset["HostAsset"]["agentInfo"]["agentId"], asset["HostAsset"]["name"]), file=f)
    return


def createActivationKey(api: QualysAPI.QualysAPI, activationKey: dict):
    """
    Creates a new Cloud Agent Activation Key

    Parameters:
         api:               Object of the QualysAPI class
         activationKey:     Python Dictionary containing the details of the new Activation Key.  Can be a single
                            Activation Key from the list provided by getActivationKeys()

    Returns:
          resp:             The HTTP response from the API request to create the new Activation Key
    """
    fullurl = '%s/qps/rest/1.0/create/ca/agentactkey/' % api.server
    sr = ET.Element('ServiceRequest')
    data = ET.SubElement(sr, 'data')
    actkey = ET.SubElement(data, 'AgentActKey')
    title = ET.SubElement(actkey, 'title')
    title.text = activationKey["AgentActKey"]["title"]
    keytype = ET.SubElement(actkey, 'type')
    keytype.text = activationKey["AgentActKey"]["type"]
    modules = ET.SubElement(actkey, 'modules')
    modlist = ET.SubElement(modules, 'list')
    for mod in activationKey["AgentActKey"]["modules"]["list"]:
        modh1 = ET.SubElement(modlist, 'ActivationKeyModule')
        module = ET.SubElement(modh1, 'license')
        module.text = mod["ActivationKeyModule"]["license"]

    modh1 = ET.SubElement(modlist, 'ActivationKeyModule')
    module = ET.SubElement(modh1, 'license')
    module.text = 'GAV'
    tags = ET.SubElement(actkey, 'tags')
    taglist = ET.SubElement(tags, 'list')
    for t in activationKey["AgentActKey"]["tags"]["list"]:
        tag = ET.SubElement(taglist, "Tag")
        name = ET.SubElement(tag, 'name')
        name.text = t["Tag"]["name"]

    payload = ET.tostring(sr, encoding='utf-8', method='xml').decode()
    resp = api.makeCall(url=fullurl, payload=payload)
    return resp


def compareActivationKeys(src_key: dict, tgt_key: dict):
    """
    Compares the names and activated modules of two Cloud Agent Activation Keys to ensure compatibility for migration

    Parameters:
        src_key:            A dictionary object containing the data for a single Cloud Agent Activation Key from the
                            source subscription, as obtained by getActivationKeys()
        tgt_key:            A dictionary object containing the data for a single Cloud Agent Activation Key from the
                            target subscription, as obtained by getActivationKeys()

    Returns:
        True if names and activated modules match
        False if names or activated modules do not match
    """
    # Compare names
    if src_key["AgentActKey"]["name"] != tgt_key["AgentActKey"]["name"]:
        return False

    # Compare module activations
    src_mods = []
    tgt_mods = []
    for mod in src_key["AgentActKey"]["modules"]["list"]:
        src_mods.append(mod["ActivationKeyModule"]["license"])
    for mod in tgt_key["AgentActKey"]["modules"]["list"]:
        tgt_mods.append(mod["ActivationKeyModule"]["license"])

    for mod in src_mods:
        if mod not in tgt_mods:
            return False

    return True

