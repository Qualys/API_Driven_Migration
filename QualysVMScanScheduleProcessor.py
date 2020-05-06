import xml.etree.ElementTree as ET
import QualysAPI

# TODO Cloud Perimeter Scan jobs need to be handled here, they need different parameters

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


def _safefindlist(xml: ET.Element, findstr: str):
    if xml.find('%s' % findstr) is not None:
        return xml.findall(findstr)
    else:
        return []

def convertScheduledScan(scan: ET.Element):
    requeststr = ''
    scan_title = scan.find('TITLE').text
    active = '1'
    option_profile_title = _safefind(scan, 'OPTION_PROFILE/TITLE')
    priority = _safefind(scan, 'PROCESSING_PRIORITY')
    requeststr = '%s&scan_title=%s&option_profile=%s&priority=%s' % (
        requeststr, scan_title.replace(' ', '+'),
        option_profile_title.replace(' ', '+'),
        priority[0]
    )

    appliance_name = _safefind(scan, 'ISCANNER_NAME')

    # Targets - Tags or Asset Groups
    if scan.find('ASSET_TAGS'):
        # This scan uses Asset Tags, not Asset Groups
        target_from = 'tags'
        tag_include_selector = _safefind(scan, 'ASSET_TAGS/TAG_INCLUDE_SELECTOR')
        tag_set_include = _safefind(scan, 'ASSET_TAGS/TAG_SET_INCLUDE')
        use_ip_nt_range_tag = _safefind(scan, 'ASSET_TAGS/USE_IP_NT_RANGE_TAGS')
        tag_set_exclude = _safefind(scan, 'ASSET_TAGS/TAG_SET_EXCLUDE')
        tag_exclude_selector = _safefind(scan, 'ASSET_TAGS/TAG_EXCLUDE_SELECTOR')

        scanners_in_tagset = '0'
        if appliance_name == 'All Scanners in TagSet':
            appliance_name = ''
            scanners_in_tagset = '1'

        requeststr = '%s&target_from=tags&tag_include_selector=%s&tag_set_include=%s&use_ip_nt_range_tag=%s' \
                     '&tag_set_exclude=%s&tag_exclude_selector=%s' % (requeststr,
                                                                      tag_include_selector,
                                                                      tag_set_include,
                                                                      use_ip_nt_range_tag,
                                                                      tag_set_exclude,
                                                                      tag_exclude_selector)
        if scanners_in_tagset == '1':
            requeststr = '%s&scanners_in_tagset=1' % requeststr
        else:
            requeststr = '%s&iscanner_name=%s' % (requeststr, appliance_name)
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

        requeststr = '%s&ip=%s&asset_groups=%s&exclude_ip_per_scan=%s' % (requeststr, ip, asset_group_title_list,
                                                                          exclude_ip_per_scan)
        if scanners_in_ag == '1':
            requeststr = '%s&scanners_in_ag=1' % requeststr
        else:
            requeststr = '%s&iscanner_name=%s' % (requeststr, appliance_name)

    # Schedule
    sched = scan.find('SCHEDULE')
    if sched.find('WEEKLY') is not None:
        frequency_weeks = sched.find('WEEKLY').get('frequency_weeks')
        weekdays = sched.find('WEEKLY').get('weekdays)')
        requeststr = '%s&occurrence=weekly&frequency_weeks=%s&weekdays=%s' % (requeststr, frequency_weeks, weekdays)
    elif sched.find('DAILY') is not None:
        frequency_days = sched.find('DAILY').get('frequency_days')
        requeststr = '%s&occurrence=daily&frequency_days=%s' % (requeststr, frequency_days)
    elif sched.find('MONTHLY') is not None:
        attribs = sched.find('MONTHLY').attrib
        frequency_months = attribs['frequency_months']
        if 'day_of_month' in attribs.keys():
            day_of_month = attribs['day_of_month']
            requeststr = '%s&occurrence=monthly&frequency_months=%s&day_of_month=%s' % (requeststr,
                                                                                        frequency_months,
                                                                                        day_of_month)
        else:
            day_of_week = attribs['day_of_week']
            week_of_month = attribs['week_of_month']
            requeststr = '%s&occurrence=monthly&frequency_months=%s&day_of_week=%s&week_of_month=%s' % \
                         (requeststr, frequency_months, day_of_week, week_of_month)
    else:
        print('Unusual schedule frequency - could not find WEEKLY, DAILY or MONTHLY')
        return None

    start_hour = sched.find('START_HOUR').text
    start_minute = sched.find('START_MINUTE').text
    time_zone_code = sched.find('TIME_ZONE/TIME_ZONE_CODE').text
    observe_dst = 'no'
    if sched.find('DST_SELECTED').text == '1':
        observe_dst = 'yes'
    requeststr = '%s&start_hour=%s&start_minute=%s&observe_dst=%s&time_zone_code=%s' % (
        requeststr, start_hour, start_minute, observe_dst, time_zone_code)
    if sched.find('MAX_OCCURRENCE') is not None:
        requeststr = '%s&recurrence=%s' % (requeststr, sched.find('MAX_OCCURRENCE').text)
    if sched.find('END_AFTER') is not None:
        requeststr = '%s&end_after=%s' % (requeststr, sched.find('END_AFTER').text)
    if sched.find('END_AFTER_MINS') is not None:
        requeststr = '%s&end_after_mins=%s' % (requeststr, sched.find('END_AFTER_MINS').text)
    if sched.find('PAUSE_AFTER_HOURS') is not None:
        requeststr = '%s&pause_after_hours=%s' % (requeststr, sched.find('PAUSE_AFTER_HOURS').text)
    if sched.find('RESUME_IN_DAYS') is not None:
        requeststr = '%s&resume_in_days=%s' % (requeststr, sched.find('RESUME_IN_DAYS').text)
    if sched.find('RESUME_IN_HOURS') is not None:
        requeststr = '%s&resume_in_hours=%s' % (requeststr, sched.find('RESUME_IN_HOURS').text)

    # Notifications
    if scan.find('NOTIFICATIONS/*') is not None:
        notifications = scan.find('NOTIFICATIONS')
        if notifications.find('BEFORE_LAUNCH') is not None:
            requeststr = '%s&before_notify=1&before_notify_unit=%s&before_notify_time=%s&before_notify_message=%s' % (
                requeststr,
                notifications.find('BEFORE_LAUNCH/UNIT').text,
                notifications.find('BEFORE_LAUNCH/TIME').text,
                notifications.find('BEFORE_LAUNCH/MESSAGE').text
            )
        if notifications.find('AFTER_COMPLETE') is not None:
            requeststr = '%s&after_notify=1&after_notify_message=%s' % (
                requeststr, notifications.find('AFTER_COMPLETE/MESSAGE').text)

    # Networks ID
    if scan.find('NETWORK_ID') is not None:
        requeststr = '%s&ip_network_id=%s' % (requeststr, scan.find('NETWORK_ID').text)

    # EC2 targets
    if scan.find('CLOUD_DETAILS/CONNECTOR/NAME') is not None:
        connector_name = scan.find('CLOUD_DETAILS/CONNECTOR/NAME').text
        ec2_endpoint = scan.find('EC2_INSTANCE/EC2_ENDPOINT').text
        requeststr = '%s&connector_name=%s&ec2_endpoint=%s' % (requeststr, connector_name, ec2_endpoint)

    return requeststr

def createScheduledScan(target_api: QualysAPI.QualysAPI, requeststr: str):
    fullurl = '%s/%s' % (target_api.server, requeststr)
    fullurl.replace(' ', '+')
    resp = target_api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysVMScanScheduleProcessor.createScheduledScan failed')
        return False
    return True
