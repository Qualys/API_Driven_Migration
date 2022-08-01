from API_Driven_Migration.QualysCommon import QualysAPI, QualysNetworkProcessor


def testNetworks(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    nets = QualysNetworkProcessor.getNetworks(source_api=source_api)
    if simulate:
        for net in nets.keys():
            print('================================================================================')
            print('NETWORKS')
            print('********************************************************************************')
            print('%s:[%s]', (net, nets[net]))
            print('================================================================================')
    else:
        netmap = QualysNetworkProcessor.createNetworks(target_api=target_api, networks=nets)
        if netmap is not None:
            print('Networks created:')
            for net in netmap.keys():
                print('%s:[%s]', (net, netmap[net]))

    netmap = QualysNetworkProcessor.generateNetworkMap(source_api=source_api, target_api=target_api)
    if netmap is not None:
        print('Generated Network Map:')
        for net in netmap.keys():
            print('%s:[%s]', (net, netmap[net]))
