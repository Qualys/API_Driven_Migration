import xml.etree.ElementTree as ET
import QualysAPI


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

    schedulelist = []
    for scan in resp.findall('.//SCAN'):
        schedulelist.append(scan)
    return schedulelist


def _safefind(xml: ET.Element, findstr: str):
    if xml.find(findstr) is not None:
        return xml.find(findstr).text
    return ''


def _safefindlist(xml: ET.Element, findstr: str):
    if xml.find(findstr) is not None:
        return xml.findall(findstr)
    return []


def convertScheduledScan(scan: ET.Element):
    requeststr = '/api/2.0/fo/schedule/scan/compliance/?action=create'
    scan_title = scan.find('TITLE').text
    option_profile_title = _safefind(scan, 'OPTION_PROFILE/TITLE')
    requeststr = '%s&scan_title=%s&option_title=%s' % (
        requeststr, scan_title.replace(' ', '+'),
        option_profile_title.replace(' ', '+'))

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
        tag_set_exclude = _safefind(scan, 'ASSET_TAGS/TAG_SET_EXCLUDE')
        tag_exclude_selector = _safefind(scan, 'ASSET_TAGS/TAG_EXCLUDE_SELECTOR')

        if appliance_name == 'All Scanners in TagSet':
            appliance_name = ''
            scanners_in_tagset = True
        else:
            scanners_in_tagset = False

        requeststr = '%s&target_from=tags' \
                     '&tag_include_selector=%s' \
                     '&tag_set_include=%s' \
                     '&use_ip_nt_range_tag=%s' \
                     '&tag_set_exclude=%s' \
                     '&tag_exclude_selector=%s' % (requeststr,
                                                   tag_include_selector,
                                                   tag_set_include,
                                                   use_ip_nt_range_tag,
                                                   tag_set_exclude,
                                                   tag_exclude_selector)

        if scanners_in_tagset:
            requeststr = '%s&scanners_in_tagset=1' % requeststr
        elif use_external_appliance:
            requeststr = '%s&iscanner_id=0' % requeststr
        else:
            requeststr = '%s&iscanner_name=%s' % (requeststr, appliance_name)
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

        requeststr = '%s&ip=%s' \
                     '&asset_groups=%s' % (requeststr, ip, asset_group_title_str)
        if exclude_ip_per_scan != '':
            requeststr = '%s&exclude_ip_per_scan=%s' % (requeststr, exclude_ip_per_scan)

        if scanners_in_ag:
            requeststr = '%s&scanners_in_ag=1' % requeststr
        elif use_external_appliance:
            requeststr = '%s&iscanner_id=0' % requeststr
        else:
            requeststr = '%s&iscanner_name=%s' % (requeststr, appliance_name)

    # Schedule
    sched = scan.find('SCHEDULE')
    if sched.find('WEEKLY') is not None:
        frequency_weeks = sched.find('WEEKLY').get('frequency_weeks')
        weekdays = sched.find('WEEKLY').get('weekdays')
        requeststr = '%s&occurrence=weekly' \
                     '&frequency_weeks=%s' \
                     '&weekdays=%s' % (requeststr,
                                       frequency_weeks,
                                       weekdays)
    elif sched.find('DAILY') is not None:
        frequency_days = sched.find('DAILY').get('frequency_days')
        requeststr = '%s&occurrence=daily' \
                     '&frequency_days=%s' % (requeststr, frequency_days)
    elif sched.find('MONTHLY') is not None:
        attribs = sched.find('MONTHLY').attrib
        frequency_months = attribs['frequency_months']
        if 'day_of_month' in attribs.keys():
            day_of_month = attribs['day_of_month']
            requeststr = '%s&occurrence=monthly' \
                         '&frequency_months=%s' \
                         '&day_of_month=%s' % (requeststr,
                                               frequency_months,
                                               day_of_month)
        else:
            day_of_week = attribs['day_of_week']
            week_of_month = attribs['week_of_month']
            requeststr = '%s&occurrence=monthly' \
                         '&frequency_months=%s' \
                         '&day_of_week=%s' \
                         '&week_of_month=%s' % (requeststr,
                                                frequency_months,
                                                day_of_week,
                                                week_of_month)
    else:
        print('Unusual schedule frequency - could not find WEEKLY, DAILY or MONTHLY')
        return None

    start_hour = _safefind(sched, 'START_HOUR')
    start_minute = _safefind(sched, 'START_MINUTE')
    tz_code = _safefind(sched, 'TIME_ZONE/TIME_ZONE_CODE')
    observe_dst = 'no'
    if sched.find('DST_SELECTED').text == '1':
        observe_dst = 'yes'

    requeststr = '%s&start_hour=%s' \
                 '&start_minute=%s' \
                 '&observe_dst=%s' \
                 '&time_zone_code=%s' % (requeststr,
                                         start_hour,
                                         start_minute,
                                         observe_dst,
                                         tz_code)

    if sched.find('MAX_OCCURRENCE') is not None:
        requeststr = '%s&recurrence=%s' % (requeststr, _safefind(sched, 'MAX_OCCURRENCE'))
    if sched.find('END_AFTER') is not None:
        requeststr = '%s&end_after=%s' % (requeststr, _safefind(sched, 'END_AFTER'))
    if sched.find('END_AFTER_MINS') is not None:
        requeststr = '%s&end_after_mins=%s' % (requeststr, _safefind(sched, 'END_AFTER_MINS'))
    if sched.find('PAUSE_AFTER_HOURS') is not None:
        requeststr = '%s&pause_after_hours=%s' % (requeststr, _safefind(sched, 'PAUSE_AFTER_HOURS'))
    if sched.find('RESUME_IN_DAYS') is not None:
        requeststr = '%s&resume_in_days=%s' % (requeststr, _safefind(sched, 'RESUME_IN_DAYS'))
    if sched.find('RESUME_IN_HOURS') is not None:
        requeststr = '%s&resume_in_hours=%s' % (requeststr, _safefind(sched, 'RESUME_IN_HOURS'))

    # Notifications
    if scan.find('NOTIFICATIONS/*') is not None:
        notifications = scan.find('NOTIFICATIONS')
        if notifications.find('BEFORE_LAUNCH') is not None:
            requeststr = '%s&before_notify=1' \
                         '&before_notify_unit=%s' \
                         '&before_notify_time=%s' \
                         '&before_notify_message=%s' % (requeststr,
                                                        _safefind(notifications, 'BEFORE_LAUNCH/UNIT'),
                                                        _safefind(notifications, 'BEFORE_LAUNCH/TIME'),
                                                        _safefind(notifications, 'BEFORE_LAUNCH/MESSAGE'))

        if notifications.find('AFTER_COMPLETE') is not None:
            requeststr = '%s&after_notify=1&after_notify_message=%s' % (requeststr,
                                                                        _safefind(notifications,
                                                                                  'AFTER_COMPLETE/MESSAGE'))

    # Networks ID
    if scan.find('NETWORK_ID') is not None:
        requeststr = '%s&ip_network_id=%s' % (requeststr, _safefind(scan, 'NETWORK_ID'))

    # EC2 targets
    if scan.find('CLOUD_DETAILS/CONNECTOR/NAME') is not None:
        connector_name = _safefind(scan, 'CLOUD_DETAILS/CONNECTOR/NAME')
        ec2_endpoint = _safefind(scan, 'EC"_INSTANCE/EC2_ENDPOINT')
        requeststr = '%s&connector_name=%s&ec2_endpoint=%s' % (requeststr, connector_name, ec2_endpoint)

    requeststr = '%s&active=%s' % (requeststr, _safefind(scan, 'ACTIVE'))
    requeststr = requeststr.replace(' ', '+')
    return requeststr


def createScheduledPCScan(api: QualysAPI.QualysAPI, requeststr: str):
    fullurl = '%s/%s' % (api.server, requeststr)
    fullurl.replace(' ', '+')
    resp = api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('QualysComplianceScanScheduleProcessor.createScheduledPCScan failed')
        return False
    return True
