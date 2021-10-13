import QualysAPI
import QualysAssetGroupProcessor
import QualysNetworkProcessor
import QualysApplianceInput


def testAssetGroups(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False,
                    networks: bool = True):
    if networks:
        netmap = QualysNetworkProcessor.generateNetworkMap(source_api=source_api, target_api=target_api)
        if not netmap:
            print('FATAL: Could not generate Networks map')
            return False
    else:
        netmap = None

    appliancemap = QualysApplianceInput.generateApplianceMap(source_api=source_api, target_api=target_api)
    if not appliancemap:
        print('FATAL: Could not generate Appliance map')
        return False

    assetgroups = QualysAssetGroupProcessor.getAssetGroups(source_api=source_api)
    if assetgroups is None:
        print('FATAL: Could not get Asset Groups')
        return False
    urllist = QualysAssetGroupProcessor.convertAssetGroups(aglist=assetgroups, netmap=netmap, appliancemap=appliancemap)
    if urllist is None:
        print('FATAL: Could not convert Asset Groups')
        return False

    if simulate:
        print('================================================================================')
        print('ASSET GROUPS')
        print('********************************************************************************')
        for url in urllist:
            print('%s%s' % (target_api.server, url))
    else:
        print('Creating Asset Groups')
        result = QualysAssetGroupProcessor.createAssetGroups(target_api=target_api, urllist=urllist)
        if not result:
            print('FATAL: Could not create Asset Groups')
            return False
