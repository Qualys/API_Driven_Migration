# QualysNetworkProcessor module


### QualysNetworkProcessor.createNetworks(target_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), networks: dict)
Creates Networks in a subscription from a list of networks obtained with getNetworks(), and creates a Network
Map linking source and target network IDs

Parameters:

    target_api:         An object of the class QualysAPI
    networks:           A python dictionary containing Networks data, as obtained with getNetworks()

Returns:

    netmap:             A python dictionary containing the Network Map where the old Network ID is the key and

        then new Network ID is the target


### QualysNetworkProcessor.generateNetworkMap(source_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), target_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI))
Generates a Network Map linking old Network IDs to new Network IDs

Parameters:

    source_api:         An object of the class QualysAPI
    target_api:         An object of the class QualysAPI

Returns:

    netmap:             A python dictionary containing the Network Map where the old Network ID is the key and

        then new Network ID is the target


### QualysNetworkProcessor.getNetworks(source_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI))
Get a list of Networks from a subscription

Parameters:

    source_api:     An object of the class QualysAPI

Returns:

    networks:      A python dictionary containing the Networks where the ID is the key and the Name is the value


### QualysNetworkProcessor.responseHandler(response)
