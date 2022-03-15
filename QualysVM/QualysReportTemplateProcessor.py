import xml.etree.ElementTree as ET
from API_Driven_Migration.QualysCommon import QualysAPI


def responseHandler(response: ET.Element):
    return True


def getReportTemplates(source_api: QualysAPI.QualysAPI):
    scanurl = '%s/api/2.0/fo/report/template/scan/?action=export&report_format=xml' % source_api.server
    pciurl = '%s/api/2.0/fo/report/template/pciscan/?action=export&report_format=xml' % source_api.server
    patchurl = '%s/api/2.0/fo/report/template/patch/?action=export&report_format=xml' % source_api.server
    mapurl = '%s/api/2.0/fo/report/template/map/?action=export&report_format=xml' % source_api.server

    print('Getting Scan Templates')
    scantemplates = source_api.makeCall(url=scanurl, method='GET')
    if not responseHandler(scantemplates):
        print('ERROR: Could not get Scan Templates')
    print('Getting PCI Templates')
    pcitemplates = source_api.makeCall(url=pciurl, method='GET')
    if not responseHandler(scantemplates):
        print('ERROR: Could not get PCI Templates')

    print('Getting Patch Templates')
    patchtemplates = source_api.makeCall(url=patchurl, method='GET')
    if not responseHandler(scantemplates):
        print('ERROR: Could not get Patch Templates')

    print('Getting Map Templates')
    maptemplates = source_api.makeCall(url=mapurl, method='GET')
    if not responseHandler(scantemplates):
        print('ERROR: Could not get Map Templates')

    templates = {'scan': scantemplates,
                 'pci': pcitemplates,
                 'patch': patchtemplates,
                 'map': maptemplates}

    return templates


def convertScanTemplate(scantemplate: ET.Element):
    url = '/api/2.0/fo/report/template/scan/'

    payload = {'action': 'create', 'report_format': 'brokeAF'}

    # Title
    payload['title'] = scantemplate.find('TITLE/INFO[@key="title"]').text

    # Target
    payload['scan_selection'] = scantemplate.find('TARGET/INFO[@key="scan_selection"]').text
    if scantemplate.find('TARGET/INFO[@key="include_trending"]') is not None:
        payload['include_trending'] = scantemplate.find('TARGET/INFO[@key="include_trending"]').text
    if scantemplate.find('TARGET/INFO[@key="limit_timeframe"]') is not None:
        payload['limit_timeframe'] = scantemplate.find('TARGET/INFO[@key="limit_timeframe"]').text
    if scantemplate.find('TARGET/INFO[@key="selection_type"]') is not None:
        payload['selection_type'] = scantemplate.find('TARGET/INFO[@key="selection_type"]').text
    if scantemplate.find('TARGET/INFO[@key="selection_range"]') is not None:
        payload['selection_range'] = scantemplate.find('TARGET/INFO[@key="selection_range"]').text
    if scantemplate.find('TARGET/INFO[@key="asset_groups"]') is not None:
        payload['asset_groups'] = scantemplate.find('TARGET/INFO[@key="asset_groups"]').text
    if scantemplate.find('TARGET/INFO[@key="network"]') is not None:
        payload['network'] = scantemplate.find('TARGET/INFO[@key="network"]').text
    if scantemplate.find('TARGET/INFO[@key="ips"]') is not None:
        payload['ips'] = scantemplate.find('TARGET/INFO[@key="ips"]').text
    if scantemplate.find('TARGET/INFO[@key="tag_set_by"]') is not None:
        payload['tag_set_by'] = scantemplate.find('TARGET/INFO[@key="tag_set_by"]').text
    if scantemplate.find('TARGET/INFO[@key="tag_set_include"]') is not None:
        payload['tag_set_include'] = scantemplate.find('TARGET/INFO[@key="tag_set_include"]').text
    if scantemplate.find('TARGET/INFO[@key="tag_include_selector"]') is not None:
        payload['tag_include_selector'] = scantemplate.find('TARGET/INFO[@key="tag_include_selector"]').text
    if scantemplate.find('TARGET/INFO[@key="tag_set_exclude"]') is not None:
        payload['tag_set_exclude'] = scantemplate.find('TARGET/INFO[@key="tag_set_exclude"]').text
    if scantemplate.find('TARGET/INFO[@key="tag_exclude_selector"]') is not None:
        payload['tag_exclude_selector'] = scantemplate.find('TARGET/INFO[@key="tag_exclude_selector"]').text
    if scantemplate.find('TARGET/INFO[@key="hosts_with_cloud_agents"]') is not None:
        payload['hosts_with_cloud_agents'] = scantemplate.find('TARGET/INFO[@key="hosts_with_cloud_agents"]').text

    # Display
    if scantemplate.find('DISPLAY/INFO[@key="graph_business_risk"]') is not None:
        payload['graph_business_risk'] = scantemplate.find('DISPLAY/INFO[@key="graph_business_risk"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_vuln_over_time"]') is not None:
        payload['graph_vuln_over_time'] = scantemplate.find('DISPLAY/INFO[@key="graph_vuln_over_time"]').text
    if scantemplate.find('DISPLAY/INFO[@key="display_text_summary"]') is not None:
        payload['display_text_summary'] = scantemplate.find('DISPLAY/INFO[@key="display_text_summary"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_status"]') is not None:
        payload['graph_status'] = scantemplate.find('DISPLAY/INFO[@key="graph_status"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_potential_status"]') is not None:
        payload['graph_potential_status'] = scantemplate.find('DISPLAY/INFO[@key="graph_potential_status"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_severity"]') is not None:
        payload['graph_severity'] = scantemplate.find('DISPLAY/INFO[@key="graph_severity"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_potential_severity"]') is not None:
        payload['graph_potential_severity'] = scantemplate.find('DISPLAY/INFO[@key="graph_potential_severity"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_ig_severity"]') is not None:
        payload['graph_ig_severity'] = scantemplate.find('DISPLAY/INFO[@key="graph_ig_severity"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_top_categories"]') is not None:
        payload['graph_top_categories'] = scantemplate.find('DISPLAY/INFO[@key="graph_top_categories"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_top_vulns"]') is not None:
        payload['graph_top_vulns'] = scantemplate.find('DISPLAY/INFO[@key="graph_top_vulns"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_os"]') is not None:
        payload['graph_os'] = scantemplate.find('DISPLAY/INFO[@key="graph_os"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_services"]') is not None:
        payload['graph_services'] = scantemplate.find('DISPLAY/INFO[@key="graph_services"]').text
    if scantemplate.find('DISPLAY/INFO[@key="graph_top_ports"]') is not None:
        payload['graph_top_ports'] = scantemplate.find('DISPLAY/INFO[@key="graph_top_ports"]').text
    if scantemplate.find('DISPLAY/INFO[@key="display_custom_footer"]') is not None:
        payload['display_custom_footer'] = scantemplate.find('DISPLAY/INFO[@key="display_custom_footer"]').text
    if scantemplate.find('DISPLAY/INFO[@key="display_custom_footer_text"]') is not None:
        payload['display_custom_footer_text'] = scantemplate.find(
            'DISPLAY/INFO[@key="display_custom_footer_text"]').text
    if scantemplate.find('DISPLAY/INFO[@key="sort_by"]') is not None:
        payload['sort_by'] = scantemplate.find('DISPLAY/INFO[@key="sort_by"]').text
    if scantemplate.find('DISPLAY/INFO[@key="cvss"]') is not None:
        payload['cvss'] = scantemplate.find('DISPLAY/INFO[@key="cvss"]').text
    if scantemplate.find('DISPLAY/INFO[@key="host_details"]') is not None:
        payload['host_details'] = scantemplate.find('DISPLAY/INFO[@key="host_details"]').text
    if scantemplate.find('DISPLAY/INFO[@key="host_ag_details"]') is not None:
        payload['host_ag_details'] = scantemplate.find('DISPLAY/INFO[@key="host_ag_details"]').text
    if scantemplate.find('DISPLAY/INFO[@key="qualys_system_ids"]') is not None:
        payload['qualys_system_ids'] = scantemplate.find('DISPLAY/INFO[@key="qualys_system_ids"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_text_summary"]') is not None:
        payload['include_text_summary'] = scantemplate.find('DISPLAY/INFO[@key="include_text_summary"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details"]') is not None:
        payload['include_vuln_details'] = scantemplate.find('DISPLAY/INFO[@key="include_vuln_details"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_threat"]') is not None:
        payload['include_vuln_details_threat'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_threat"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_impact"]') is not None:
        payload['include_vuln_details_impact'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_impact"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_solution"]') is not None:
        payload['include_vuln_details_solution'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_solution"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_vpatch"]') is not None:
        payload['include_vuln_details_vpatch'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_vpatch"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_compliance"]') is not None:
        payload['include_vuln_details_compliance'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_compliance"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_exploit"]') is not None:
        payload['include_vuln_details_exploit'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_exploit"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_malware"]') is not None:
        payload['include_vuln_details_malware'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_malware"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_results"]') is not None:
        payload['include_vuln_details_results'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_results"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_appendix"]') is not None:
        payload['include_vuln_details_appendix'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_appendix"]').text
    if scantemplate.find('DISPLAY/INFO[@key="exclude_account_id"]') is not None:
        payload['exclude_account_id'] = scantemplate.find('DISPLAY/INFO[@key="exclude_account_id"]').text
    if scantemplate.find('DISPLAY/INFO[@key="include_vuln_details_reopened"]') is not None:
        payload['include_vuln_details_reopened'] = scantemplate.find(
            'DISPLAY/INFO[@key="include_vuln_details_reopened"]').text
    if scantemplate.find('DISPLAY/INFO[@key="metadata_ec2_instances"]') is not None:
        payload['metadata_ec2_instances'] = scantemplate.find('DISPLAY/INFO[@key="metadata_ec2_instances"]').text
    if scantemplate.find('DISPLAY/INFO[@key="cloud_provider_metadata"]') is not None:
        payload['cloud_provider_metadata'] = scantemplate.find('DISPLAY/INFO[@key="cloud_provider_metadata"]').text

    # Filter
    if scantemplate.find('FILTER/INFO[@key="selective_vulns"]') is not None:
        payload['selective_vulns'] = scantemplate.find('FILTER/INFO[@key="selective_vulns"]').text
    if scantemplate.find('FILTER/INFO[@key="search_list_ids"]') is not None:
        payload['search_list_ids'] = scantemplate.find('FILTER/INFO[@key="search_list_ids"]').text
    if scantemplate.find('FILTER/INFO[@key="exclude_qid_option"]') is not None:
        payload['exclude_qid_option'] = scantemplate.find('FILTER/INFO[@key="exclude_qid_option"]').text
    if scantemplate.find('FILTER/INFO[@key="exclude_search_list_ids"]') is not None:
        payload['exclude_search_list_ids'] = scantemplate.find('FILTER/INFO[@key="exclude_search_list_ids"]').text
    if scantemplate.find('FILTER/INFO[@key="included_os"]') is not None:
        payload['included_os'] = scantemplate.find('FILTER/INFO[@key="included_os"]').text
    if scantemplate.find('FILTER/INFO[@key="status_new"]') is not None:
        payload['status_new'] = scantemplate.find('FILTER/INFO[@key="status_new"]').text
    if scantemplate.find('FILTER/INFO[@key="status_active"]') is not None:
        payload['status_active'] = scantemplate.find('FILTER/INFO[@key="status_active"]').text
    if scantemplate.find('FILTER/INFO[@key="status_reopen"]') is not None:
        payload['status_reopen'] = scantemplate.find('FILTER/INFO[@key="status_reopen"]').text
    if scantemplate.find('FILTER/INFO[@key="status_fixed"]') is not None:
        payload['status_fixed'] = scantemplate.find('FILTER/INFO[@key="status_fixed"]').text
    if scantemplate.find('FILTER/INFO[@key="vuln_active"]') is not None:
        payload['vuln_active'] = scantemplate.find('FILTER/INFO[@key="vuln_active"]').text
    if scantemplate.find('FILTER/INFO[@key="vuln_disabled"]') is not None:
        payload['vuln_disabled'] = scantemplate.find('FILTER/INFO[@key="vuln_disabled"]').text
    if scantemplate.find('FILTER/INFO[@key="vuln_ignored"]') is not None:
        payload['vuln_ignored'] = scantemplate.find('FILTER/INFO[@key="vuln_ignored"]').text
    if scantemplate.find('FILTER/INFO[@key="potential_active"]') is not None:
        payload['potential_active'] = scantemplate.find('FILTER/INFO[@key="potential_active"]').text
    if scantemplate.find('FILTER/INFO[@key="potential_disabled"]') is not None:
        payload['potential_disabled'] = scantemplate.find('FILTER/INFO[@key="potential_disabled"]').text
    if scantemplate.find('FILTER/INFO[@key="potential_ignored"]') is not None:
        payload['potential_ignored'] = scantemplate.find('FILTER/INFO[@key="potential_ignored"]').text
    if scantemplate.find('FILTER/INFO[@key="ig_active"]') is not None:
        payload['ig_active'] = scantemplate.find('FILTER/INFO[@key="ig_active"]').text
    if scantemplate.find('FILTER/INFO[@key="ig_disabled"]') is not None:
        payload['ig_disabled'] = scantemplate.find('FILTER/INFO[@key="ig_disabled"]').text
    if scantemplate.find('FILTER/INFO[@key="ig_ignored"]') is not None:
        payload['ig_ignored'] = scantemplate.find('FILTER/INFO[@key="ig_ignored"]').text
    if scantemplate.find('FILTER/INFO[@key="display_non_running_kernels"]') is not None:
        payload['display_non_running_kernels'] = scantemplate.find(
            'FILTER/INFO[@key="display_non_running_kernels"]').text
    if scantemplate.find('FILTER/INFO[@key="exclude_non_running_kernel"]') is not None:
        payload['exclude_non_running_kernel'] = scantemplate.find('FILTER/INFO[@key="exclude_non_running_kernel"]').text
    if scantemplate.find('FILTER/INFO[@key="exclude_non_running_services"]') is not None:
        payload['exclude_non_running_services'] = scantemplate.find(
            'FILTER/INFO[@key="exclude_non_running_services"]').text
    if scantemplate.find('FILTER/INFO[@key="exclude_superceded_patches"]') is not None:
        payload['exclude_superceded_patches'] = scantemplate.find('FILTER/INFO[@key="exclude_superceded_patches"]').text
    if scantemplate.find('FILTER/INFO[@key="exclude_qids_not_exploitable_due_to_configuration"]') is not None:
        payload['exclude_qids_not_exploitable_due_to_configuration'] = scantemplate.find(
            'FILTER/INFO[@key="exclude_qids_not_exploitable_due_to_configuration"]').text
    if scantemplate.find('FILTER/INFO[@key="categories_list"]') is not None:
        payload['categories_list'] = scantemplate.find('FILTER/INFO[@key="categories_list"]').text

    # Service Ports
    if scantemplate.find('SERVICSPORTS/INFO[@key="required_services"]') is not None:
        payload['required_services'] = scantemplate.find('SERVICSPORTS/INFO[@key="required_services"]').text
    if scantemplate.find('SERVICSPORTS/INFO[@key="unauthorized_services"]') is not None:
        payload['unauthorized_services'] = scantemplate.find('SERVICSPORTS/INFO[@key="unauthorized_services"]').text
    if scantemplate.find('SERVICSPORTS/INFO[@key="services_info"]') is not None:
        payload['services_info'] = scantemplate.find('SERVICSPORTS/INFO[@key="services_info"]').text
    if scantemplate.find('SERVICSPORTS/INFO[@key="required_ports"]') is not None:
        payload['required_ports'] = scantemplate.find('SERVICSPORTS/INFO[@key="required_ports"]').text
    if scantemplate.find('SERVICSPORTS/INFO[@key="unauthorized_ports"]') is not None:
        payload['unauthorized_ports'] = scantemplate.find('SERVICSPORTS/INFO[@key="unauthorized_ports"]').text

    # User Access
    if scantemplate.find('USERACCESS/INFO[@key="report_access_users"]') is not None:
        payload['report_access_users'] = scantemplate.find('USERACCESS/INFO[@key="report_access_users"]').text
    if scantemplate.find('USERACCESS/INFO[@key="global"]') is not None:
        payload['global'] = scantemplate.find('USERACCESS/INFO[@key="global"]').text

    return url, payload
