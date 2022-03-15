from API_Driven_Migration.QualysCommon import QualysAPI
import argparse
from xml.etree import ElementTree as ET
import json


def getActivationKeys(api: QualysAPI.QualysAPI):
    fullurl='%s/qps/rest/1.0/search/ca/agentactkey/' % api.server
    startat = 1
    pagesize=1000
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
    fullurl = '%s/qps/rest/2.0/search/am/hostasset/?fields=name,agentInfo.agentId' % api.server
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
    outfile = "%s.txt" % keyid
    with open(outfile, 'w') as f:
        for asset in assets:
            print("%s : %s" % (asset["HostAsset"]["agentInfo"]["agentId"], asset["HostAsset"]["name"]), file=f)
    return


def createActivationKey(api: QualysAPI.QualysAPI, activationKey: dict):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_username', help='API Username in source subscription')
    parser.add_argument('source_password', help='API User Password in source subscription')
    parser.add_argument('source_api_url', help='URL of the API service in the source subscription'
                                               '(e.g. https://qualysapi.qualys.com)')
    parser.add_argument('target_username', help='API Username in target subscription')
    parser.add_argument('target_password', help='API User Password in target subscription')
    parser.add_argument('target_api_url', help='URL of the API service in the target subscription'
                                               '(e.g. https://qualysapi.qg2.apps.qualys.com)')

    parser.add_argument('-p', '--proxyenable', action='store_true', help='Use HTTPS Proxy (required -u or --proxyurl')
    parser.add_argument('-u', '--proxyurl', help='Proxy URL (requires -p or --proxyenable)')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    parser.add_argument('-s', '--simulate', action='store_true', help='Simulate - obtain data from source, do not send '
                                                                      'to target')

    args = parser.parse_args()

    src_api = QualysAPI.QualysAPI(svr=args.source_api_url, usr=args.source_username, passwd=args.source_password,
                                  proxy=args.proxyurl, enableProxy=args.proxyenable, debug=args.debug)

    tgt_api = QualysAPI.QualysAPI(svr=args.target_api_url, usr=args.target_username, passwd=args.target_password,
                                  proxy=args.proxyurl, enableProxy=args.proxyenable, debug=args.debug)

    src_keys = getActivationKeys(api=src_api)
    tgt_keys = getActivationKeys(api=tgt_api)

