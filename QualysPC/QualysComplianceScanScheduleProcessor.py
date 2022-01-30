import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(resp: ET.Element):
    if resp is not None:
        return True
    return False


def getScheduleList(api: QualysAPI.QualysAPI, activeonly: bool = True):
    activestr = '0'
    if activeonly:
        activestr = '1'
    fullurl = '%s/api/2.0/fo/schedule/scan/compliance/?action=list&show_notifications=1&show_cloud_details=1&' \
              'active=%s' % (api.server, activestr)
    resp = api.makeCall(url=fullurl, method='GET')
    if not responseHandler(resp):
        print('QualysComplianceScanScheduleProcessor.getSchedules failed')
        return None

    return resp


def _safefind(xml: ET.Element, findstr: str):
    if xml.find(findstr) is not None:
        return xml.find(findstr).text
    return ''


def _safefindlist(xml: ET.Element, findstr: str):
    if xml.find(findstr) is not None:
        return xml.findall(findstr)
    return []


def _getWeekOfMonth(wom: str):
    womswitch = {
        '1': 'first',
        '2': 'second',
        '3': 'third',
        '4': 'fourth',
        '5': 'last'
    }
    return womswitch[wom]


def _getDays(daynums: str):
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


def convertScheduledScan(scan: ET.Element, appliance_map: dict, setactive: bool = False, dist_group_map: dict = None):
    requeststr = '/api/2.0/fo/schedule/scan/compliance/'
    payload = {'action': 'create', 'scan_title': scan.find('TITLE').text,
               'option_title': _safefind(scan, 'OPTION_PROFILE/TITLE')}

    appliance_name = _safefind(scan, 'ISCANNER_NAME')
    use_external_appliance = False
    if appliance_name == 'External Scanner':
        appliance_name = ''
        use_external_appliance = True

    # Targets - Tags or Asset Groups
    if scan.find('ASSET_TAGS'):
        # This scan uses Asset Tags to define scope
        tag_include_selector = _safefind(scan, 'ASSET_TAGS/TAG_INCLUDE_SELECTOR')
        tag_set_include = _safefind(scan, 'ASSET_TAGS/TAG_SET_INCLUDE')
        use_ip_nt_range_tag = _safefind(scan, 'ASSET_TAGS/USE_IP_NT_RANGE_TAGS')

        if _safefind(scan, 'ASSET_TAGS/TAG_SET_EXCLUDE') != '':
            tag_set_exclude = _safefind(scan, 'ASSET_TAGS/TAG_SET_EXCLUDE')
            tag_exclude_selector = _safefind(scan, 'ASSET_TAGS/TAG_EXCLUDE_SELECTOR')
        else:
            tag_set_exclude = None
            tag_exclude_selector = None

        if appliance_name == 'All Scanners in TagSet':
            appliance_name = ''
            scanners_in_tagset = True
        else:
            scanners_in_tagset = False

        payload['tag_set_by'] = 'name'
        payload['target_from'] = 'tags'
        payload['tag_include_selector'] = tag_include_selector
        payload['tag_set_include'] = tag_set_include
        if use_ip_nt_range_tag is not None or use_ip_nt_range_tag != '':
            payload['use_ip_nt_range_tags'] = use_ip_nt_range_tag

        if tag_set_exclude is not None:
            payload['tag_exclude_selector'] = tag_exclude_selector
            payload['tag_set_exclude'] = tag_set_exclude

        if scanners_in_tagset:
            payload['scanners_in_tagset'] = '1'

        elif use_external_appliance:
            payload['iscanner_id'] = '0'

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
        # This scan uses Asset Groups/IPs to define scope
        asset_group_titles = []
        for group in _safefindlist(scan, './/ASSET_GROUP_TITLE'):
            asset_group_titles.append(group.text)
        asset_group_title_str = ','.join(asset_group_titles)
        ip = _safefind(scan, 'TARGET')
        exclude_ip_per_scan = _safefind(scan, 'EXCLUDE_IP_PER_SCAN')
        scanners_in_ag = False
        if appliance_name == 'All Scanners in Asset Group':
            appliance_name = ''
            scanners_in_ag = True

        payload['ip'] = ip
        payload['asset_groups'] = asset_group_title_str

        if exclude_ip_per_scan != '':
            payload['exclude_ip_per_scan'] = exclude_ip_per_scan

        if scanners_in_ag:
            payload['scanners_in_ag'] = '1'

        elif use_external_appliance:
            payload['iscanner_id'] = '0'

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

    payload['start_hour'] = _safefind(sched, 'START_HOUR')
    payload['start_minute'] = _safefind(sched, 'START_MINUTE')
    payload['observe_dst'] = observe_dst
    payload['time_zone_code'] = _safefind(sched, 'TIME_ZONE/TIME_ZONE_CODE')

    if sched.find('MAX_OCCURRENCE') is not None:
        payload['recurrence'] = _safefind(sched, 'MAX_OCCURRENCE')

    if sched.find('END_AFTER') is not None:
        payload['end_after'] = _safefind(sched, 'END_AFTER')

    if sched.find('END_AFTER_MINS') is not None:
        payload['end_after_mins'] = _safefind(sched, 'END_AFTER_MINS')

    if sched.find('PAUSE_AFTER_HOURS') is not None:
        payload['pause_after_hours'] = _safefind(sched, 'PAUSE_AFTER_HOURS')

    if sched.find('RESUME_IN_DAYS') is not None:
        if sched.find('RESUME_IN_DAYS').text.lower() == 'manually':
            payload['resume_in_days'] = 'Manually'
        else:
            payload['resume_in_days'] = _safefind(sched, 'RESUME_IN_DAYS')

    if sched.find('RESUME_IN_HOURS') is not None:
        if payload['resume_in_days'] != 'Manually':
            if sched.find('RESUME_IN_HOURS').text.lower() == 'manually':
                payload['resume_in_hours'] = 'Manually'
            else:
                payload['resume_in_hours'] = sched.find('RESUME_IN_HOURS').text

    # Notifications
    if scan.find('NOTIFICATIONS/*') is not None:
        notifications = scan.find('NOTIFICATIONS')
        if notifications.find('BEFORE_LAUNCH') is not None:
            payload['before_notify'] = '1'
            payload['before_notify_unit'] = _safefind(notifications, 'BEFORE_LAUNCH/UNIT')
            payload['before_notify_time'] = _safefind(notifications, 'BEFORE_LAUNCH/TIME')
            payload['before_notify_message'] = _safefind(notifications, 'BEFORE_LAUNCH/MESSAGE')

        if notifications.find('AFTER_COMPLETE') is not None:
            payload['after_notify'] = '1'
            payload['after_notify_message'] = _safefind(notifications, 'AFTER_COMPLETE/MESSAGE')

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
        payload['ip_network_id'] = _safefind(scan, 'NETWORK_ID')

    # EC2 targets
    if scan.find('CLOUD_DETAILS/CONNECTOR/NAME') is not None:
        connector_name = _safefind(scan, 'CLOUD_DETAILS/CONNECTOR/NAME')
        ec2_endpoint = _safefind(scan, 'EC"_INSTANCE/EC2_ENDPOINT')
        payload['connector_name'] = connector_name
        payload['ec2_endpoint'] = ec2_endpoint

    # payload['active'] = _safefind(scan, 'ACTIVE')
    if setactive:
        payload['active'] = '1'
    else:
        payload['active'] = '0'

    return requeststr, payload


def createScheduledPCScan(api: QualysAPI.QualysAPI, requeststr: str, payload: dict):
    fullurl = '%s/%s' % (api.server, requeststr)
    resp = api.makeCall(url=fullurl, payload=payload)
    # if not responseHandler(resp):
    #     print('QualysComplianceScanScheduleProcessor.createScheduledPCScan failed')
    #     return False
    # return True
    return resp