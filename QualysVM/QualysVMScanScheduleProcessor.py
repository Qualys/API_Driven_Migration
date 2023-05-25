import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(resp: ET.ElementTree):
    return True


def getScheduleList(source_api: QualysAPI.QualysAPI, activeonly: bool = False):
    """
    Get a list of VM Scan Schedules

    Parameters:
        source_api:             An object of class QualysAPI
        activeonly:             A boolean value to specify whether only active scan schedules should be obtained

    Returns:
        resp:                   A document of type xml.etree.ElementTree.Element containing the full API response
        OR
        None                    if an error was encountered in the API response
    """
    activestr = '0'
    if activeonly:
        activestr = '1'
    fullurl = '%s/api/2.0/fo/schedule/scan/?action=list&show_notifications=1&active=%s&show_cloud_details=1' % (
        source_api.server, activestr)
    resp = source_api.makeCall(url=fullurl, method='GET')

    if not responseHandler(resp):
        print('QualysVMScanScheduleProcessor.getScheduleList failed')
        return None
    return resp


def _safefind(xml: ET.Element, findstr: str):
    """
    INTERNAL
    Safely find an element in an XML document, return an empty string if the element was not found
    """
    if xml.find('%s' % findstr) is not None:
        return xml.find(findstr).text
    else:
        return ''


def _getDays(daynums: str):
    """
    INTERNAL
    Convert the days of the week into a string value
    """
    dayswitch = {
        '0': 'Sunday',
        '1': 'Monday',
        '2': 'Tuesday',
        '3': 'Wednesday',
        '4': 'Thursday',
        '5': 'Friday',
        '6': 'Saturday'
    }
    days = ''
    for day in daynums.split(','):
        day = day.strip()
        if days == '':
            days = dayswitch.get(day, '')
        else:
            days = '%s,%s' % (days, dayswitch.get(day, None))
    return days


def _getWeekOfMonth(wom: str):
    """
    INTERNAL
    Convert the number of a week-of-month into a string value
    """
    womswitch = {
        '1': 'first',
        '2': 'second',
        '3': 'third',
        '4': 'fourth',
        '5': 'last'
    }
    return womswitch.get(wom, None)


def _safefindlist(xml: ET.Element, findstr: str):
    """
    INTERNAL
    Safely find all instances of an element in an XML document
    """
    if xml.find('%s' % findstr) is not None:
        return xml.findall(findstr)
    else:
        return []


def convertScheduledScan(scan: ET.Element, appliance_map: dict, setactive: bool = False,
                         dist_group_map: dict = None):
    """
    Convert a Scheduled Scan from XML format into a URL/Payload format, excluding FQDN, to be used in an API call to
    recreate the scan schedule

    Parameters:
        scan:                   A document of type xml.etree.ElementTree.Element containing the scheduled scan data,
                                represents a single scan schedule from the list obtained using getScheduleList
        appliance_map:          A python dictionary containing map of old-to-new appliance data
        setactive:              (Optional) If True, creates the new scan schedule in the Active state.
                                If False, creates the new scan in the Inactive state
                                Defaults to False
        dist_group_map:         (Optional) A python dictionary containing a map of old-to-new distribution group IDs

    Returns:
        None                    If an error was encountered during conversion
        OR
        requeststr, payload:
            requeststr:         The URL, exluding FQDN, of an API call used to create the Schedule Scan
            payload:            A python dictionary containing the payload data used in the API call

    """

    requeststr = 'api/2.0/fo/schedule/scan/'
    payload = {'action': 'create',
               'scan_title': scan.find('TITLE').text,
               'option_title': _safefind(scan, 'OPTION_PROFILE/TITLE'),
               'priority': _safefind(scan, 'PROCESSING_PRIORITY')[0]}

    if setactive:
        payload['active'] = '1'
    else:
        payload['active'] = '0'

    appliance_name = _safefind(scan, 'ISCANNER_NAME')
    use_external_appliance = False
    if appliance_name == 'External Scanner':
        appliance_name = ''
        use_external_appliance = True

    # Targets - Tags or Asset Groups
    if scan.find('ASSET_TAGS'):
        # This scan uses Asset Tags, not Asset Groups
        target_from = 'tags'
        tag_include_selector = _safefind(scan, 'ASSET_TAGS/TAG_INCLUDE_SELECTOR')
        tag_set_include = _safefind(scan, 'ASSET_TAGS/TAG_SET_INCLUDE')
        use_ip_nt_range_tag = _safefind(scan, 'ASSET_TAGS/USE_IP_NT_RANGE_TAGS')

        if _safefind(scan, 'ASSET_TAGS/TAG_SET_EXCLUDE') != '':
            tag_set_exclude = _safefind(scan, 'ASSET_TAGS/TAG_SET_EXCLUDE')
            tag_exclude_selector = _safefind(scan, 'ASSET_TAGS/TAG_EXCLUDE_SELECTOR')
        else:
            tag_set_exclude = None
            tag_exclude_selector = None

        scanners_in_tagset = '0'
        if appliance_name == 'All Scanners in TagSet':
            appliance_name = ''
            scanners_in_tagset = '1'

        payload['tag_set_by'] = 'name'
        payload['target_from'] = 'tags'
        payload['tag_include_selector'] = tag_include_selector
        payload['tag_set_include'] = tag_set_include

        if use_ip_nt_range_tag is not None or use_ip_nt_range_tag != '':
            payload['use_ip_nt_range_tags'] = use_ip_nt_range_tag

        if tag_set_exclude is not None:
            payload['tag_exclude_selector'] = tag_exclude_selector
            payload['tag_set_exclude'] = tag_set_exclude

        if scanners_in_tagset == '1':
            payload['scanners_in_tagset'] = '1'
        elif use_external_appliance:
            pass
        else:
            if appliance_name.find(',') > -1:
                appliance_list = appliance_name.split(', ')
                new_appliance_list = []
                for appl in appliance_list:
                    new_appliance_list.append(appliance_map[appl])
                payload['iscanner_name'] = ','.join(new_appliance_list)
            else:
                payload['iscanner_name'] = appliance_map[appliance_name]
    else:
        # This scan uses Asset Tags or direct IPs
        scanners_in_ag = 0

        if len(_safefindlist(scan, './/ASSET_GROUP_TITLE')) > 0:
            asset_group_titles = []
            for group in _safefindlist(scan, './/ASSET_GROUP_TITLE'):
                asset_group_titles.append(group.text)
            asset_group_title_list = ','.join(asset_group_titles)
            if _safefind(scan, 'EXCLUDE_IP_PER_SCAN') != '':
                payload['exclude_ip_per_scan'] = _safefind(scan, 'EXCLUDE_IP_PER_SCAN')

            scanners_in_ag = '0'
            payload['asset_groups'] = asset_group_title_list

        if appliance_name == 'All in Asset Group':
            appliance_name = ''
            scanners_in_ag = '1'

        ip = _safefind(scan, 'TARGET')
        payload['ip'] = ip

        if scanners_in_ag == '1':
            payload['scanners_in_ag'] = '1'
        elif use_external_appliance:
            # When no appliance is specified, the default is to use External Appliance, so we do nothing here
            pass
        else:
            if appliance_name.find(',') > -1:
                appliance_list = appliance_name.split(', ')
                new_appliance_list = []
                for appl in appliance_list:
                    new_appliance_list.append(appliance_map[appl])
                payload['iscanner_name'] = ','.join(new_appliance_list)
            else:
                payload['iscanner_name'] = appliance_map[appliance_name]

    # Schedule
    sched = scan.find('SCHEDULE')
    if sched.find('WEEKLY') is not None:
        frequency_weeks = sched.find('WEEKLY').get('frequency_weeks')
        weekdays = sched.find('WEEKLY').get('weekdays')
        weekdays = _getDays(weekdays)
        payload['occurrence'] = 'weekly'
        payload['frequency_weeks'] = frequency_weeks
        payload['weekdays'] = weekdays

    elif sched.find('DAILY') is not None:
        frequency_days = sched.find('DAILY').get('frequency_days')
        payload['occurrence'] = 'daily'
        payload['frequency_days'] = frequency_days

    elif sched.find('MONTHLY') is not None:
        attribs = sched.find('MONTHLY').attrib
        frequency_months = attribs['frequency_months']
        if 'day_of_month' in attribs.keys():
            day_of_month = attribs['day_of_month']
            payload['occurrence'] = 'monthly'
            payload['frequency_months'] = frequency_months
            payload['day_of_month'] = day_of_month

        else:
            day_of_week = attribs['day_of_week']
            week_of_month = attribs['week_of_month']
            payload['occurrence'] = 'monthly'
            payload['frequency_months'] = frequency_months
            payload['day_of_week'] = day_of_week
            payload['week_of_month'] = _getWeekOfMonth(week_of_month)

    else:
        print('Unusual schedule frequency - could not find WEEKLY, DAILY or MONTHLY')
        return None

    if sched.find('DST_SELECTED').text == '1':
        observe_dst = 'yes'
    else:
        observe_dst = 'no'

    payload['start_hour'] = sched.find('START_HOUR').text
    payload['start_minute'] = sched.find('START_MINUTE').text
    payload['observe_dst'] = observe_dst
    payload['time_zone_code'] = sched.find('TIME_ZONE/TIME_ZONE_CODE').text

    if sched.find('MAX_OCCURRENCE') is not None:
        payload['recurrence'] = sched.find('MAX_OCCURRENCE').text

    if sched.find('END_AFTER') is not None:
        payload['end_after'] = sched.find('END_AFTER').text

    if sched.find('END_AFTER_MINS') is not None:
        payload['end_after_min'] = sched.find('END_AFTER_MINS').text

    if sched.find('PAUSE_AFTER_HOURS') is not None:
        payload['pause_after_hours'] = sched.find('PAUSE_AFTER_HOURS').text

    if sched.find('RESUME_IN_DAYS') is not None:
        if sched.find('RESUME_IN_DAYS').text.lower() == 'manually':
            payload['resume_in_days'] = 'Manually'
        else:
            payload['resume_in_days'] = sched.find('RESUME_IN_DAYS').text

    if sched.find('RESUME_IN_HOURS') is not None:
        if payload['resume_in_days'] != 'Manually':
            if sched.find('RESUME_IN_HOURS').text == 'manually':
                payload['resume_in_hours'] = 'Manually'
            else:
                payload['resume_in_hours'] = sched.find('RESUME_IN_HOURS').text

    # Notifications
    if scan.find('NOTIFICATIONS/*') is not None:
        notifications = scan.find('NOTIFICATIONS')
        if notifications.find('BEFORE_LAUNCH') is not None:
            payload['before_notify'] = '1'
            payload['before_notify_unit'] = notifications.find('BEFORE_LAUNCH/UNIT').text
            payload['before_notify_time'] = notifications.find('BEFORE_LAUNCH/TIME').text
            payload['before_notify_message'] = notifications.find('BEFORE_LAUNCH/MESSAGE').text

        if notifications.find('AFTER_COMPLETE') is not None:
            payload['after_notify'] = '1'
            payload['after_notify_message'] = notifications.find('AFTER_COMPLETE/MESSAGE').text

        if notifications.find('LAUNCH_DELAY') is not None:
            payload['delay_notify'] = '1'
            payload['delay_notify_message'] = notifications.find('LAUNCH_DELAY/MESSAGE').text

        if notifications.find('LAUNCH_SKIP') is not None:
            payload['skipped_notify'] = '1'
            payload['skipped_notify_message'] = notifications.find('LAUNCH_SKIP/MESSAGE').text

        if notifications.find('DEACTIVATE_SCHEDULE') is not None:
            payload['deactivate_notify'] = '1'
            payload['deactivate_notify_message'] = notifications.find('DEACTIVATE_SCHEDULE/MESSAGE').text

        if notifications.find('DISTRIBUTION_GROUPS') is not None:
            if dist_group_map is None:
                print('ERROR: No Distribution Group Map provided but Distribution Groups found in schedule '
                      'notifications')
                return None, None

            dist_group_list = []
            for dist_group in notifications.findall('DISTRIBUTION_GROUPS/DISTRIBUTION_GROUP/ID'):
                dist_group_list.append(dist_group_map[dist_group.text])
            payload['recipient_group_ids'] = ','.join(dist_group_list)

    # Networks ID
    if scan.find('NETWORK_ID') is not None:
        payload['ip_network_id'] = scan.find('NETWORK_ID').text

    # EC2 targets
    if scan.find('CLOUD_DETAILS/CONNECTOR/NAME') is not None:
        connector_name = scan.find('CLOUD_DETAILS/CONNECTOR/NAME').text
        ec2_endpoint = scan.find('EC2_INSTANCE/EC2_ENDPOINT').text
        payload['connector_name'] = connector_name
        payload['ec2_endpoint'] = ec2_endpoint

    # Cloud Perimeter Scan
    # TODO Cloud Perimeter Scans have their own create API endpoint - move this out into its own function
    if scan.find('.//SCAN_TYPE') is not None:
        if scan.find('.//SCAN_TYPE').text == 'Cloud Perimeter':
            # Add in the cloud perimeter-specific stuff here
            module = 'vm'
            cloud_provider = 'aws'
            cloud_service = 'ec2'
            include_lb_from_connector = '1'
            schedule = 'recurring'
            if scan.find('.//ELB_DNS') is not None:
                dnslist = []
                for dns in scan.findall('.//ELB_DNS/DNS'):
                    dnslist.append(dns.text)
                payload['elb_dns'] = ','.join(dnslist)

            platform_type = ''
            if scan.find('.//VPC_SCOPE').text == 'All':
                payload['platform_type'] = 'vpc_peered'
                payload['region'] = scan.find('.//CLOUD_TARGET/REGION/CODE').text

            if scan.find('.//VPC_SCOPE').text == 'Selected':
                payload['platform_type'] = 'selected_vpc'
                payload['vpc_id'] = scan.find('CLOUD_TARGET/VPC_LIST/VPC/UUID').text

            if scan.find('.//VPC_SCOPE').text == 'None':
                payload['platform_type'] = 'classic'
                payload['region'] = scan.find('.//CLOUD_TARGET_REGION/CODE').text

    return requeststr, payload


def createScheduledScan(target_api: QualysAPI.QualysAPI, requeststr: str, payload: dict):
    """
    Create a scheduled scan from a URL and Payload generated by convertScheduledScan()

    Parameters:
        target_api:                 An object of the class QualysAPI
        requeststr:                 A string containing the URL, excluding FQDN, to be used in the API call
        payload:                    A python dictionary containing the payload to be use in the API call

    Returns:
        resp:                   A document of type xml.etree.ElementTree.Element containing the full API response
    """
    fullurl = '%s/%s' % (target_api.server, requeststr)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    # if not responseHandler(resp):
    #     print('QualysVMScanScheduleProcessor.createScheduledScan failed')
    #     return False
    # return True
    return resp
