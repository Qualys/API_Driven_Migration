from API_Driven_Migration.QualysCommon import QualysAPI


def responseHandler(response):
    if response.find('.//CODE'):
        print('ERROR %s: %s' % (response.find('.//CODE').text, response.find('.//TEXT').text))
        return False
    else:
        return True


def getNetworks(source_api: QualysAPI.QualysAPI):
    fullurl = '%s/api/2.0/fo/network/?action=list' % source_api.server
    resp = source_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        return None

    networks = {}
    netlist = resp.find('.//NETWORK_LIST')
    for network in netlist.findall('NETWORK'):
        if network.find('ID').text == '0':
            continue
        networks[network.find('ID').text] = network.find('NAME').text

    return networks


def getNetworksXML(source_api: QualysAPI.QualysAPI):
    fullurl = '%s/api/2.0/fo/network/?action=list' % source_api.server
    resp = source_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        return None

    return resp


def createNetworks(target_api: QualysAPI.QualysAPI, networks: dict):
    # Creates Networks defined in the networks dictionary parameter
    # Returns a dictionary network mapping {oldID: newID, ...}
    # Returns None on any failure
    baseurl = '%s/api/2.0/fo/network/?action=create&' % target_api.server
    netmap = {}
    for netid in networks.keys():
        fullurl = '%sname=%s' % (baseurl, networks[netid])
        resp = target_api.makeCall(url=fullurl)
        if not responseHandler(resp):
            return None
        newid = resp.find('.//VALUE').text
        netmap[netid] = newid
    return netmap


def generateNetworkMap(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI):
    srcurl = '%s/api/2.0/fo/network/?action=list' % source_api.server
    tgturl = '%s/api/2.0/fo/network/?action=list' % target_api.server

    srcresp = source_api.makeCall(url=srcurl)
    if not responseHandler(srcresp):
        return None
    tgtresp = target_api.makeCall(url=tgturl)
    if not responseHandler(tgtresp):
        return None

    srclist = srcresp.find('.//NETWORK_LIST')
    tgtlist = tgtresp.find('.//NETWORK_LIST')
    netmap = {}
    for net in srclist.findall('NETWORK'):
        if net.find('ID').text == '0':
            continue
        netname = net.find('NAME').text

        # Networks beginning 'Global' or 'Qualys' are reserved for system use
        if netname.find('Global') == 0 or netname.find('Qualys') == 0:
            continue

        netid = net.find('ID').text
        tgtnet = tgtlist.find(".//NETWORK/[NAME='%s']" % netname)
        # tgtnet = tgtlist.find('.//[NAME="%s"]/..' % netname)
        if tgtnet is None:
            print('ERROR: Could not find Network %s in target subscription' % netname)
            return None
        tgtnetid = tgtnet.find('ID').text
        netmap[netid] = tgtnetid
    return netmap
