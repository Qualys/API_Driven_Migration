# QualysCloudAgentProcessor module


### QualysCloudAgentProcessor.create_configuration_profile(target_api: QualysAPI, config_profile: Element)
Creates a Cloud Agent Configuration Profile from an XML data object.

Parameters:

    target_api:             An object of the class QualysAPI
    config_profile:         An object of the type xml.etree.ElementTree.Element containing the Configuration Profile

    > data

Returns:

    resp:                  An object of the type xml.etree.ElementTree.Element containing the XML response to the

        API request


### QualysCloudAgentProcessor.get_configuration_profile(source_api: QualysAPI, id: str)
Obtains a single Cloud Agent Configuration Profile

Parameters:

    source_api:             An object of the class QualysAPI
    id:                     A string containing the ID of the Configuration Profile to obtain

Returns:

    resp:                   An object of the type xml.etree.ElementTree.Element containing the XML response to the

        API request, and which includes the Configuration Profile data


### QualysCloudAgentProcessor.get_configuration_profile_ids(source_api: QualysAPI)
Obtains all Cloud Agent Configuration Profiles from a subscription.  Supports paginated output by making
multiple API calls and combining the ‘data’ element from the responses into a single XML data object

Parameters:

    source_api:             An object of the class QualysAPI

Returns:

    data:                   The combined ‘data’ elements from the API responses

    or

    None if an error was encountered when making an API call


### QualysCloudAgentProcessor.prepare_configuration_profile(config_profile: Element)
Prepares data obtained by get_configuration_profile() for creation by create_configuration_profile().  This
function removes certain system-managed elements from the data, such as the ‘createdBy’, ‘id’, ‘createdDate’.

Parameters:

    config_profile:            An object of the type xml.etree.ElementTree.Element containing the Configuration

        Profile data, as obtained by get_configuration_profile()

Returns:

    config_profile:             An object of the type xml.etree.ElementTree.Element containing the prepared

        Configuration Profile data, to be used by create_configuration_profile()
