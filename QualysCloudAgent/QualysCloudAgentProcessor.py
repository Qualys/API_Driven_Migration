from API_Driven_Migration.QualysCommon.QualysAPI import QualysAPI
from xml.etree import ElementTree


def get_configuration_profile_ids(source_api: QualysAPI):
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
    url = '%s/qps/rest/1.0/get/ca/agentconfig/%s' % (source_api.server, id)

    resp = source_api.makeCall(url=url, method='GET')

    return resp


def create_configuration_profile(target_api: QualysAPI, config_profile: ElementTree.Element):
    url = '%s/qps/rest/1.0/create/ca/agentconfig/' % target_api.server

    payload = ElementTree.Element('ServiceRequest')
    data = ElementTree.SubElement(payload, 'data')
    data.append(config_profile)

    resp = target_api.makeCall(url=url, payload=ElementTree.tostring(payload, method='xml', encoding='utf-8',
                                                                     short_empty_elements=False).decode())

    return resp


def prepare_configuration_profile(config_profile: ElementTree.Element):
    config_profile.remove(config_profile.find('id'))
    config_profile.remove(config_profile.find('createdDate'))
    config_profile.remove(config_profile.find('createdBy'))
    config_profile.remove(config_profile.find('totalAgents'))
    for config_tag in config_profile.findall('.//ConfigTag'):
        config_tag.remove(config_tag.find('id'))
        config_tag.remove(config_tag.find('uuid'))
    config_profile.find('tags').remove(config_profile.find('tags/tagSetUuid'))
    if config_profile.find('tags/excludeResolution') is None:
        exc_res = ElementTree.SubElement(config_profile.find('tags'), 'excludeResolution')
        exc_res.text = 'ANY'

    return config_profile
