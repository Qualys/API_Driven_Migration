from QualysCommon.QualysAPI import QualysAPI
from xml.etree import ElementTree


def get_configuration_profile_ids(source_api: QualysAPI):
    """
    Obtains all Cloud Agent Configuration Profiles from a subscription.  Supports paginated output by making
    multiple API calls and combining the 'data' element from the responses into a single XML data object

    Parameters:
        source_api:             An object of the class QualysAPI

    Returns:
        data:                   The combined 'data' elements from the API responses

        or

        None if an error was encountered when making an API call
    """
    url = '%s/qps/rest/1.0/search/ca/agentconfig/?fields=id,name' % source_api.server

    payload = ElementTree.Element('ServiceRequest')

    at_end = False
    data = ElementTree.Element('data')

    while not at_end:

        resp = source_api.makeCall(url=url, payload=payload)

        if resp is None:
            return None

        for cp in resp.findall('.//AgentConfig'):
            data.append(cp)

        if resp.find('.//hasMoreRecords').text == 'false':
            at_end = True

    return data


def get_configuration_profile(source_api: QualysAPI, id: str):
    """
    Obtains a single Cloud Agent Configuration Profile

    Parameters:
        source_api:             An object of the class QualysAPI
        id:                     A string containing the ID of the Configuration Profile to obtain

    Returns:
        resp:                   An object of the type xml.etree.ElementTree.Element containing the XML response to the
                                API request, and which includes the Configuration Profile data
    """
    url = '%s/qps/rest/1.0/get/ca/agentconfig/%s' % (source_api.server, id)

    resp = source_api.makeCall(url=url, method='GET')

    return resp


def create_configuration_profile(target_api: QualysAPI, config_profile: ElementTree.Element):
    """
    Creates a Cloud Agent Configuration Profile from an XML data object.

    Parameters:
        target_api:             An object of the class QualysAPI
        config_profile:         An object of the type xml.etree.ElementTree.Element containing the Configuration Profile
                                data

    Returns:
         resp:                  An object of the type xml.etree.ElementTree.Element containing the XML response to the
                                API request
    """
    url = '%s/qps/rest/1.0/create/ca/agentconfig/' % target_api.server

    payload = ElementTree.Element('ServiceRequest')
    data = ElementTree.SubElement(payload, 'data')
    data.append(config_profile)

    resp = target_api.makeCall(url=url, payload=ElementTree.tostring(payload, method='xml', encoding='utf-8',
                                                                     short_empty_elements=False).decode())

    return resp


def prepare_configuration_profile(config_profile: ElementTree.Element):
    """
    Prepares data obtained by get_configuration_profile() for creation by create_configuration_profile().  This
    function removes certain system-managed elements from the data, such as the 'createdBy', 'id', 'createdDate'.

    Parameters:
         config_profile:            An object of the type xml.etree.ElementTree.Element containing the Configuration
                                    Profile data, as obtained by get_configuration_profile()

    Returns:
        config_profile:             An object of the type xml.etree.ElementTree.Element containing the prepared
                                    Configuration Profile data, to be used by create_configuration_profile()
    """
    config_profile.remove(config_profile.find('id'))
    config_profile.remove(config_profile.find('createdDate'))
    if config_profile.find('createdBy') is not None:
        config_profile.remove(config_profile.find('createdBy'))
    if config_profile.find('totalAgents') is not None:
        config_profile.remove(config_profile.find('totalAgents'))
    for config_tag in config_profile.findall('.//ConfigTag'):
        config_tag.remove(config_tag.find('id'))
        config_tag.remove(config_tag.find('uuid'))
    if config_profile.find('tags/tagSetUuid') is not None:
        config_profile.find('tags').remove(config_profile.find('tags/tagSetUuid'))
    if config_profile.find('tags/excludeResolution') is not None:
        exc_res = ElementTree.SubElement(config_profile.find('tags'), 'excludeResolution')
        exc_res.text = 'ANY'

    return config_profile
