import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(resp: ET.ElementTree):
    return True


def getScheduleList(source_api: QualysAPI.QualysAPI, activeonly: bool = False):
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
    if xml.find('%s' % findstr) is not None:
        return xml.find(findstr).text
    else:
        return ''


def _getDays(daynums: str):
    dayswitch = {
        '0': 'sunday',
        '1': 'monday',
        '2': 'tuesday',
        '3': 'wednesday',
        '4': 'thursday',
        '5': 'friday',
        '6': 'saturday'
    }
    days = ''
    for day in daynums.split(','):
        day = day.strip()
        if days == '':
            days = dayswitch.get(day, '')
        else:
            days = '%s,%s' % (days, dayswitch.get(day, None))
    return days


def _safefindlist(xml: ET.Element, findstr: str):
    if xml.find('%s' % findstr) is not None:
        return xml.findall(findstr)
    else:
        return []


def convertScheduledScan(scan: ET.Element, appliance_map: dict):

    requeststr = 'api/2.0/fo/schedule/scan/'
    payload = {'action': 'create',
               'scan_title': scan.find('TITLE').text.replace(' ', '+'),
               'active': '1',
               'option_profile': _safefind(scan, 'OPTION_PROFILE/TITLE').replace(' ', '+'),
               'priority': _safefind(scan, 'PROCESSING_PRIORITY')[0]}

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
            payload['iscanner_id'] = '0'
        else:
            payload['iscanner_name'] = appliance_map[appliance_name]
    else:
        target_from = 'assets'
        # This scan uses Asset Tags or direct IPs
        asset_group_titles = []
        for group in _safefindlist(scan, './/ASSET_GROUP_TITLE'):
            asset_group_titles.append(group.text)
        asset_group_title_list = ','.join(asset_group_titles)
        ip = _safefind(scan, 'TARGET')
        exclude_ip_per_scan = _safefind(scan, 'EXCLUDE_IP_PER_SCAN')
        scanners_in_ag = '0'
        if appliance_name == 'All Scanners in Asset Group':
            appliance_name = ''
            scanners_in_ag = '1'

        payload['ip'] = ip
        payload['asset_groups'] = asset_group_title_list
        payload['exclude_ip_per_scan'] = exclude_ip_per_scan

        if scanners_in_ag == '1':
            payload['scanners_in_ag'] = '1'
        elif use_external_appliance:
            # When no appliance is specified, the default is to use External Appliance, so we do nothing here
            pass
        else:
            payload['iscanner_name'] = appliance_map[appliance_name]
            requeststr = '%s&iscanner_name=%s' % (requeststr, appliance_name)

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
            payload['freqency_months'] = frequency_months
            payload['day_of_month'] = day_of_month

        else:
            day_of_week = attribs['day_of_week']
            week_of_month = attribs['week_of_month']
            payload['occurrence'] = 'monthly'
            payload['freqency_months'] = frequency_months
            payload['day_of_week'] = day_of_week
            payload['week_of_month'] = week_of_month

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
        payload['resume_in_days'] = sched.find('RESUME_IN_DAYS').text

    if sched.find('RESUME_IN_HOURS') is not None:
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
    fullurl = '%s/%s' % (target_api.server, requeststr)
    resp = target_api.makeCall(url=fullurl, payload=payload)
    if not responseHandler(resp):
        print('QualysVMScanScheduleProcessor.createScheduledScan failed')
        return False
    return True
