from API_Driven_Migration.QualysCommon import QualysAPI
import xml.etree.ElementTree as ET


def searchWebApplication(api: QualysAPI.QualysAPI, webappid: str = None, name: str = None, url: str = None,
                         tagname: str = None, tagid: int = None, createddate: str = None, updateddate: str = None,
                         isscheduled: bool = None, isscanned: bool = None, lastscanstatus: str = None):

    sr = ET.Element('ServiceRequest')
    filters = ET.Element('filters')
    if webappid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'id')
        criteria.set('operator', 'IN')
        criteria.text = webappid

    if name is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = name

    if url is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'url')
        criteria.set('operator', 'CONTAINS')
        criteria.text = url

    if tagname is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = tagname

    if tagid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.id')
        criteria.set('operator', 'CONTAINS')
        criteria.text = str(tagid)

    if createddate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'createdDate')
        criteria.set('operator', 'GREATER')
        criteria.text = createddate

    if updateddate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'updatedDate')
        criteria.set('operator', 'GREATER')
        criteria.text = updateddate

    if isscheduled is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'isScheduled')
        criteria.set('operator', 'CONTAINS')
        criteria.text = str(isscheduled)

    if isscanned is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'isScanned')
        criteria.set('operator', 'CONTAINS')
        criteria.text = str(isscanned)

    if lastscanstatus is not None:
        if lastscanstatus in ['SUBMITTED', 'RUNNING', 'FINISHED', 'TIME_LIMIT_EXCEEDED', 'SCAN_NOT_LAUNCHED',
                              'SCANNER_NOT_AVAILABLE', 'ERROR', 'CANCELED']:
            criteria = ET.SubElement(filters, 'Criteria')
            criteria.set('field', 'lastScan.status')
            criteria.set('operator', 'IN')
            criteria.text = lastscanstatus

    if len(filters) > 0:
        sr.append(filters)
    prefs = ET.SubElement(sr, 'preferences')
    verbose = ET.SubElement(prefs, 'verbose')
    verbose.text = 'true'

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    url = '%s/qps/rest/3.0/search/was/webapp' % api.server
    resp = api.makeCall(url=url, payload=payload)

    return resp


def getWebApp(api: QualysAPI.QualysAPI, webappid: str):
    fullurl = '%s/qps/rest/3.0/get/was/webapp/%s' % (api.server, webappid)
    resp = api.makeCall(method='GET', url=fullurl)

    return resp


def createWebApp(api: QualysAPI.QualysAPI, payloadxml: ET.Element):
    fullurl = '%s/qps/rest/3.0/create/was/webapp' % api.server
    payload = ET.tostring(payloadxml, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, method='POST', payload=payload)

    return resp


def updateWebAppFromXML(api: QualysAPI.QualysAPI, payloadxml: ET.Element, webappid: int):
    fullurl = '%s/qps/rest/3.0/update/was/webapp/%s' % (api.server, str(webappid))
    payload = ET.tostring(payloadxml, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, method='POST', payload=payload)

    return resp


def downloadSeleniumScript(api: QualysAPI.QualysAPI, webappid: str, scriptid: str):
    fullurl = '%s/qps/rest/3.0/downloadSeleniumScript/was/webapp/' % api.server
    sr = ET.Element('ServiceRequest')
    filters = ET.SubElement(sr, 'filters')
    idcriteria = ET.SubElement(filters, 'Criteria')
    idcriteria.set('field', 'id')
    idcriteria.set('operator', 'EQUALS')
    idcriteria.text = webappid
    scriptcriteria = ET.SubElement(filters, 'Criteria')
    scriptcriteria.set('field', 'crawlingScripts.id')
    scriptcriteria.set('operator', 'EQUALS')
    scriptcriteria.text = scriptid
    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()

    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def searchSchedule(api: QualysAPI.QualysAPI, scheduleid: str = None, name: str = None, ownerid: str = None,
                   createddate: str = None, updated: str = None, active: bool = None, type: str = None,
                   webappname: str = None, webappid: str = None, webapptags: str = None, webapptagsid: str = None,
                   invalid: bool = None, lastScan: bool = None, lastscandate: str = None, lastscanstatus: str = None,
                   multi: bool = None):
    fullurl = '%s/qps/rest/3.0/search/was/wasscanschedule' % api.server

    sr = ET.Element('ServiceRequest')
    filters = ET.Element('filters')

    if scheduleid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'id')
        criteria.set('operator', 'IN')
        criteria.text = scheduleid

    if name is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = name

    if ownerid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'owner.id')
        criteria.set('operator', 'IN')
        criteria.text = ownerid

    if createddate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'createdDate')
        criteria.set('operator', 'GREATER')
        criteria.text = createddate

    if updated is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'updatedDate')
        criteria.set('operator', 'GREATER')
        criteria.text = updated

    if active is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'active')
        criteria.set('operator', 'EQUALS')
        criteria.text = str(active)

    if type is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'type')
        criteria.set('operator', 'IN')
        criteria.text = type

    if webappname is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'webApp.name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = webappname

    if webappid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'webApp.id')
        criteria.set('operator', 'IN')
        criteria.text = webappid

    if webapptags is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'webApp.tags')
        criteria.set('operator', 'NONE')
        criteria.text = webapptags

    if webapptagsid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'webApp.tags.id')
        criteria.set('operator', 'IN')
        criteria.text = id

    if invalid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'invalid')
        criteria.set('operator', 'EQUALS')
        criteria.text = str(invalid)

    if lastScan is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'lastScan')
        criteria.set('operator', 'NONE')
        criteria.text = str(lastScan)

    if lastscandate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'lastScan.launchedDate')
        criteria.set('operator', 'GREATER')
        criteria.text = lastscandate

    if lastscanstatus is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'lastScan.status')
        criteria.set('operator', 'IN')
        criteria.text = lastscanstatus

    if multi is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'multi')
        criteria.set('operator', 'EQUALS')
        criteria.text = str(multi)

    if len(filters) > 0:
        sr.append(filters)

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()

    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def getSchedule(api: QualysAPI.QualysAPI, id: str):
    fullurl = '%s/qps/rest/3.0/get/was/wasscanschedule/%s' % (api.server, id)

    resp = api.makeCall(url=fullurl, method='GET')
    return resp


def createScheduleFromXML(api: QualysAPI.QualysAPI, schedulexml: ET.Element):
    fullurl = '%s/qps/rest/3.0/create/was/wasscanschedule' % api.server
    payload = ET.tostring(schedulexml, method='xml', encoding='utf-8').decode()

    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def updateSchedule(api: QualysAPI.QualysAPI, schedulexml: ET.Element):
    fullurl = '%s/qps/rest/3.0/update/was/wasscanschedule' % api.server
    payload = ET.tostring(schedulexml, method='xml', encoding='utf-8').decode()

    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def searchReport(api: QualysAPI.QualysAPI, name: str = None, tagsid: str = None, tagsname: str = None,
                 creationdate: str = None, reporttype: str = None, reportformat: str = None, status: str = None):
    fullurl = '%s/qps/rest/3.0/search/was/report' % api.server
    payload = ""

    sr = ET.Element('ServiceRequest')
    filters = ET.SubElement(sr, 'filters')

    if name is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = name

    if tagsid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.id')
        criteria.set('operator', 'IN')
        criteria.text = tagsid

    if tagsname is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = tagsname

    if creationdate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'creationDate')
        criteria.set('operator', 'CONTAINS')
        criteria.text = creationdate

    if reporttype is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'type')
        criteria.set('operator', 'CONTAINS')
        criteria.text = reporttype

    if reportformat is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'format')
        criteria.set('operator', 'CONTAINS')
        criteria.text = reportformat

    if status is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'status')
        criteria.set('operator', 'CONTAINS')
        criteria.text = status

    if len(filters) > 0:
        payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()

    resp = api.makeCall(fullurl, payload=payload)

    return resp


def getReport(api: QualysAPI.QualysAPI, reportid: int):
    fullurl = '%s/qps/rest/3.0/get/was/report/%s' % (api.server, str(reportid))
    resp = api.makeCall(url=fullurl, method='GET')
    return resp


def updateReport(api: QualysAPI.QualysAPI, reportid: int):
    fullurl = '%s/qps/rest/3.0/update/was/report/%s' % (api.server, str(reportid))
    resp = api.makeCall(url=fullurl, method='GET')
    return resp


def createReportFromXML(api: QualysAPI.QualysAPI, reportxml: ET.Element):
    fullurl = '%s/qps/rest/3.0/create/was/report' % api.server
    sr = ET.Element('ServiceRequest')
    data = ET.SubElement(sr, 'data')
    data.append(reportxml)

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def createBaseReport(reporttype: str, reportname: str, reportformat: str = None, templateid: int = None):

    sr = ET.Element('ServiceRequest')
    data = ET.SubElement(sr, 'data')
    report = ET.SubElement(data, 'Report')
    xmlname = ET.SubElement(report, 'name')
    xmlname.text = reportname
    xmltype = ET.SubElement(report, 'type')
    xmltype.text = reporttype

    if reportformat is not None:
        formatxml = ET.SubElement(report, 'format')
        formatxml.text = reportformat

    if templateid is not None:
        templatexml = ET.SubElement(report, 'template')
        idxml = ET.SubElement(templatexml, 'id')
        idxml.text = str(templateid)

    return sr


def createWebAppReport(api: QualysAPI.QualysAPI, reportname: str, webappids: str = None, reportformat: str = None,
                       templateid: int = None, tagincludeids: str = None, tagincludeopt: str = 'ANY',
                       tagexcludeids: str = None, tagexcludeopt: str = 'ANY'):

    fullurl = '%s/qps/rest/3.0/create/was/report' % api.server

    sr = createBaseReport(reporttype='WAS_WEBAPP_REPORT', reportname=reportname, reportformat=reportformat,
                          templateid=templateid)
    report = sr.find('ServiceRequest/data/Report')
    config = ET.SubElement(report, 'config')
    warpt = ET.SubElement(config, 'webAppReport')
    tgt = ET.SubElement(warpt, 'target')

    if webappids is not None:
        webapps = ET.SubElement(tgt, 'webapps')
        for webappid in webappids.split(','):
            webapp = ET.SubElement(webapps, 'WebApp')
            idxml = ET.SubElement(webapp, 'id')
            idxml.text = webappid.strip()

    if tagincludeids is not None:
        tags = ET.SubElement(tgt, 'tags')
        included = ET.SubElement(tags, 'included')
        includeopt = ET.SubElement(included, 'option')
        includeopt.text = tagincludeopt
        taglist = ET.SubElement(included, 'tagList')
        for tagid in tagincludeids.split(','):
            tag = ET.SubElement(taglist, 'Tag')
            idxml = ET.SubElement(tag, 'id')
            idxml.text = tagid

        if tagexcludeids is not None:
            excluded = ET.SubElement(tags, 'excluded')
            excludeopt = ET.SubElement(excluded, 'option')
            excludeopt.text = tagexcludeopt
            taglist = ET.SubElement(excluded, 'tagList')
            for tagid in tagexcludeids.split(','):
                tag = ET.SubElement(taglist, 'Tag')
                idxml = ET.SubElement(tag, 'id')
                idxml.text = tagid

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def createScanReport(api: QualysAPI.QualysAPI, reportname: str, targetscans: str, filtersearchlistids: str = None,
                     filterurls: str = None, filterstatus: str = None, filtershowpatched: str = 'SHOW_BOTH',
                     filterignoredreasons: str = None, displaycontents: str = None, displaygraphs: str = None,
                     displaygroups: str = None, rawlevels: str = None, filtersshowignored: bool = None,
                     reportformat: str = None, templateid: int = None):

    fullurl = '%s/qps/rest/3.0/create/was/report' % api.server

    sr = createBaseReport(reporttype='WAS_SCAN_REPORT',
                          reportname=reportname, reportformat=reportformat, templateid=templateid)
    report = sr.find('ServiceRequest/data/Report')
    config = ET.SubElement(report, 'config')
    scanrpt = ET.SubElement(config, 'scanReport')
    tgt = ET.SubElement(scanrpt, 'target')
    scans = ET.SubElement(tgt, 'WasScan')
    idxml = ET.SubElement(scans, 'id')
    idxml.text = targetscans

    if displaycontents is not None and displaygraphs is not None and displaygroups is not None and rawlevels is not None:
        display = ET.SubElement(scanrpt, 'display')
        contents = ET.SubElement(display, 'contents')
        for content in displaycontents.split(','):
            contentxml = ET.SubElement(contents, 'ScanReportContent')
            contentxml.text = content

        graphs = ET.SubElement(display, 'graphs')
        for graph in displaygraphs.split(','):
            graphxml = ET.SubElement(graphs, 'ScanReportGraph')
            graphxml.text = graph

        groups = ET.SubElement(display, 'groups')
        for group in displaygroups.split(','):
            groupxml = ET.SubElement(groups, 'ScanReportGroup')
            groupxml.text = group

        if rawlevels is not None:
            options = ET.SubElement(display, 'options')
            rawlevelsxml = ET.SubElement(options, 'rawLevels')
            rawlevelsxml.text = rawlevels

    if (filtershowpatched is not None) or \
            (filterurls is not None) or \
            (filterstatus is not None) or \
            (filtersshowignored is not None) or \
            (filtersearchlistids is not None) or \
            (filterignoredreasons is not None):

        filters = ET.SubElement(report, 'filters')

        if filtershowpatched is not None:
            showpatched = ET.SubElement(filters, 'showPatched')
            showpatched.text = filtershowpatched

        if filtersearchlistids is not None:
            searchlists = ET.SubElement(filters, 'searchlists')
            for searchlist in filtersearchlistids.split(','):
                slxml = ET.SubElement(searchlists, 'SearchList')
                idxml = ET.SubElement(slxml, 'id')
                idxml.text = searchlist.strip()

        if filterstatus is not None:
            statuses = ET.SubElement(filters, 'status')
            for status in filterstatus.split(','):
                statusxml = ET.SubElement(statuses, 'ScanFindingStatus')
                statusxml.text = status.strip()

        if filterurls is not None:
            for url in filterurls.split(','):
                urlxml = ET.SubElement(filters, 'url')
                urlxml.text = url.strip()

        if filtersshowignored is not None or filterignoredreasons is not None:
            remediation = ET.SubElement(filters, 'remediation')

            if filtersshowignored is not None:
                showignored = ET.SubElement(remediation, 'showIgnored')
                showignored.text = str(filtersshowignored).lower()

            if filterignoredreasons is not None:
                ignoredreasons = ET.SubElement(remediation, 'ignoredReasons')
                for reason in filterignoredreasons.split(','):
                    ignoredreason = ET.SubElement(ignoredreasons, 'IgnoredReason')
                    ignoredreason.text = reason

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def createScorecardReport(api: QualysAPI.QualysAPI, reportname: str, webappids: str = None,
                          inctagids: str = None, inctagopts: str = None,
                          exctagids: str = None, exctagopts: str = None,
                          searchlistids: str = None, scanstatus: str = None, authstatus: str = None,
                          reportformat: str = None,
                          scandatestart: str = None, scandateend: str = None,
                          displaycontents: str = None, displaygraphs: str = None, displaygroups: str = None,
                          displayoptions: str = None):

    fullurl = '%s/qps/rest/3.0/create/was/report' % api.server

    sr = createBaseReport(reporttype='WAS_SCORECARD_REPORT',
                          reportname=reportname, reportformat=reportformat)
    report = sr.find('ServiceRequest/data/Report')
    config = ET.SubElement(report, 'config')
    scorecard = ET.SubElement(config, 'scorecardReport')
    tgt = ET.SubElement(scorecard, 'target')

    if inctagids is not None and webappids is not None:
        print('ERROR: QualysWASProcessor.createScorecardReport failed - specify targets with tags or webapp IDs, '
              'not both')
        return None

    if (scandatestart is not None and scandateend is None) or (scandatestart is None and scandateend is not None):
        print('ERROR: QualysWASProcessor.createScorecardReport failed - must specify stand AND end dates')
        return None

    if webappids is not None:
        webapps = ET.SubElement(tgt, 'webapps')
        for webappid in webappids.split(','):
            webapp = ET.SubElement(webapps, 'WebApp')
            idxml = ET.SubElement(webapp, 'id')
            idxml.text = webappid.strip()

    if inctagids is not None:
        tags = ET.SubElement(tgt, 'tags')
        included = ET.SubElement(tags, 'included')
        includeopt = ET.SubElement(included, 'option')
        includeopt.text = inctagopts
        taglist = ET.SubElement(included, 'tagList')
        for tagid in inctagids.split(','):
            tag = ET.SubElement(taglist, 'Tag')
            idxml = ET.SubElement(tag, 'id')
            idxml.text = tagid

        if exctagids is not None:
            excluded = ET.SubElement(tags, 'excluded')
            excludeopt = ET.SubElement(excluded, 'option')
            excludeopt.text = exctagopts
            taglist = ET.SubElement(excluded, 'tagList')
            for tagid in exctagids.split(','):
                tag = ET.SubElement(taglist, 'Tag')
                idxml = ET.SubElement(tag, 'id')
                idxml.text = tagid

    if searchlistids is not None or scandatestart is not None or scanstatus is not None or authstatus is not None:
        filters = ET.SubElement(scorecard, 'filters')

        if searchlistids is not None:
            searchlists = ET.SubElement(filters, 'searchlists')
            for searchlist in searchlistids.split(','):
                slistxml = ET.SubElement(searchlists, 'SearchList')
                idxml = ET.SubElement(slistxml, 'id')
                idxml.text = searchlist.strip()

        if scandatestart is not None:
            scandate = ET.SubElement(filters, 'scanDate')
            start = ET.SubElement(scandate, 'startDate')
            start.text = scandatestart
            end = ET.SubElement(scandate, 'endDate')
            end.text = scandateend

        if scanstatus is not None:
            scanstatusxml = ET.SubElement(filters, 'scanStatus')
            scanstatusxml.text = scanstatus

        if authstatus is not None:
            authstatusxml = ET.SubElement(filters, 'scanAuthStatus')
            authstatusxml.text = authstatus

    if displaycontents is not None or displayoptions is not None or displaygroups is not None or \
            displaygraphs is not None:

        display = ET.SubElement(scorecard, 'display')

        if displaycontents is not None:
            contents = ET.SubElement(display, 'contents')
            for content in displaycontents.split(','):
                contentxml = ET.SubElement(contents, 'ScorecardReportContent')
                contentxml.text = content.strip()

        if displayoptions is not None:
            options = ET.SubElement(display, 'options')
            rawlevels = ET.SubElement(options, 'rawLevels')
            rawlevels.text = displayoptions

        if displaygroups is not None:
            groups = ET.SubElement(display, 'groups')
            for group in displaygroups.split(','):
                groupxml = ET.SubElement(groups, 'scorecardReportGroup')
                groupxml.text = group.strip()

        if displaygraphs is not None:
            graphs = ET.SubElement(display, 'graphs')
            for graph in displaygraphs.split(','):
                graphxml = ET.SubElement(graphs, 'ScorecardReportGraph')
                graphxml.text = graph.strip()

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def createCatalogReport(api: QualysAPI.QualysAPI, reportname: str, reportformat: str = None,
                        filters_url: str = None, filters_ip: str = None,
                        filters_os: str = None, filters_status: str = None,
                        scandate_start: str = None, scandate_end: str = None,
                        display_contents: str = None, display_graphs: str = None, display_groups: str = None,
                        display_options: str = None):

    fullurl = '%s/qps/rest/3.0/create/was/report' % api.server
    sr = createBaseReport(reporttype='WAS_CATALOG_REPORT',
                          reportname=reportname, reportformat=reportformat)
    report = sr.find('ServiceRequest/data/Report')

    config = ET.SubElement(report, 'config')
    catalog = ET.SubElement(config, 'catalogReport')

    if scandate_start is not None and scandate_end is None or scandate_start is None and scandate_end is not None:
        print('ERROR: QualysWASProcessor.createCatalogReport failed - Start Date and End Date must be specified '
              'together')
        return None

    if display_contents is not None or display_options is not None or display_groups is not None or \
            display_graphs is not None:

        display = ET.SubElement(catalog, 'display')

        if display_contents is not None:
            contents = ET.SubElement(display, 'contents')
            for content in display_contents.split(','):
                contentxml = ET.SubElement(contents, 'CatalogReportContent')
                contentxml.text = content.strip()

        if display_options is not None:
            options = ET.SubElement(display, 'options')
            rawlevels = ET.SubElement(options, 'rawLevels')
            rawlevels.text = display_options

        if display_groups is not None:
            groups = ET.SubElement(display, 'groups')
            for group in display_groups.split(','):
                groupxml = ET.SubElement(groups, 'CatalogReportContent')
                groupxml.text = group.strip()

        if display_graphs is not None:
            graphs = ET.SubElement(display, 'graphs')
            for graph in display_graphs.split(','):
                graphxml = ET.SubElement(graphs, 'CatalogReportContent')
                graphxml.text = graph

    if scandate_start is not None or filters_status is not None or filters_url is not None or filters_ip is not None \
            or filters_os is not None:
        filters = ET.SubElement(catalog, 'filters')

        if scandate_start is not None:
            scandate = ET.SubElement(filters, 'scanDate')
            start = ET.SubElement(scandate, 'startDate')
            start.text = scandate_start
            end = ET.SubElement(scandate, 'endDate')
            end.text = scandate_end

        if filters_status is not None:
            status = ET.SubElement(filters, 'status')
            for entrystatus in filters_status.split(','):
                statusxml = ET.SubElement(status, 'EntryStatus')
                statusxml.text = filters_status.strip()

        if filters_url is not None:
            for url in filters_url.split(','):
                urlxml = ET.SubElement(filters, 'url')
                urlxml.text = url.strip()

        if filters_ip is not None:
            for ip in filters_ip.split(','):
                ipxml = ET.SubElement(filters, 'ip')
                ipxml.text = ip.strip()

        if filters_os is not None:
            for os in filters_os.split(','):
                osxml = ET.SubElement(filters, 'os')
                osxml.text = os

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def searchOptionProfiles(api: QualysAPI.QualysAPI, profileid: str = None, profilename: str = None,
                         tagname: str = None, tagid: int = None,
                         createddate: str = None, updateddate: str = None,
                         usedbywebapps: bool = None, usedbyschedules: bool = None,
                         ownername: str = None, owneruser: str = None):

    fullurl = '%s/qps/rest/3.0/search/was/optionprofile' % api.server
    sr = ET.Element('ServiceRequest')
    filters = ET.SubElement(sr, 'filters')

    if profileid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'id')
        criteria.set('operator', 'EQUALS')
        criteria.text = profileid

    if profilename is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'name')
        criteria.set('operator', 'EQUALS')
        criteria.text = profilename

    if tagname is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.name')
        criteria.set('operator', 'EQUALS')
        criteria.text = tagname

    if tagid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.id')
        criteria.set('operator', 'EQUALS')
        criteria.text = tagid

    if createddate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'createdDate')
        criteria.set('operator', 'GREATER')
        criteria.text = createddate

    if updateddate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'updatedDate')
        criteria.set('operator', 'GREATER')
        criteria.text = updateddate

    if usedbywebapps is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'usedByWebApps')
        criteria.set('operator', 'EQUALS')
        criteria.text = str(usedbywebapps).lower()

    if usedbyschedules is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'usedBySchedules')
        criteria.set('operator', 'EQUALS')
        criteria.text = str(usedbyschedules).lower()

    if ownername is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'owner.name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = ownername

    if owneruser is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'owner.username')
        criteria.set('operator', 'EQUALS')
        criteria.text = owneruser

    if len(filters) > 0:
        payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    else:
        payload = ""

    resp = api.makeCall(url=fullurl, payload=payload)

    return resp


def getOptionProfile(api: QualysAPI.QualysAPI, profileid: int):
    fullurl = '%s/qps/rest/3.0/get/was/optionprofile/%s' % (api.server, str(profileid))
    resp = api.makeCall(url=fullurl, method='GET')
    return resp


def createOptionProfileFromXML(api: QualysAPI.QualysAPI, profilexml: ET.Element):
    fullurl = '%s/qps/rest/3.0/create/was/optionprofile' % api.server
    payload = ET.tostring(profilexml, method='xml', encoding='utf-8').decode()

    resp = api.makeCall(url=fullurl, payload=payload)
    return resp


def createOptionProfile(api: QualysAPI.QualysAPI):
    pass


def updateOptionProfile(api: QualysAPI.QualysAPI):
    pass


def searchDNSOverride(api: QualysAPI.QualysAPI, recordid: str = None, recordname: str = None,
                      tagid: str = None, tagname: str = None,
                      createddate: str = None, updateddate: str = None,
                      ownerid: str = None, ownername: str = None, owneruser: str = None):
    fullurl = '%s/qps/rest/3.0/search/was/dnsoverride/' % api.server
    sr = ET.Element('ServiceRequest')
    filters = ET.SubElement(sr, 'filters')

    if recordid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'id')
        criteria.set('operator', 'IN')
        criteria.text = recordid

    if recordname is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = recordname

    if tagid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.id')
        criteria.set('operator', 'IN')
        criteria.text = tagid

    if tagname is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = tagname

    if createddate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'createDate')
        criteria.set('operator', 'GREATER')
        criteria.text = createddate

    if updateddate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'updatedDate')
        criteria.set('operator', 'GREATER')
        criteria.text = updateddate

    if ownerid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'owner.id')
        criteria.set('operator', 'EQUALS')
        criteria.text = ownerid

    if ownername is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'owner.name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = ownername

    if owneruser is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'owner.username')
        criteria.set('operator', 'CONTAINS')
        criteria.text = owneruser

    if len(filters) > 0:
        payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    else:
        payload = ""

    resp = api.makeCall(url=fullurl, payload=payload)
    return resp


def getDNSOverride(api: QualysAPI.QualysAPI, recordid: int):
    fullurl = '%s/qps/rest/3.0/get/was/dnsoverride/%s' % (api.server, str(recordid))
    resp = api.makeCall(url=fullurl)
    return resp


def createDNSOverride(api: QualysAPI.QualysAPI, name: str, mappings: list, tagids: str = None):
    fullurl = '%s/qps/rest/3.0/create/was/dnsoverride/' % api.server
    sr = ET.Element('ServiceRequest')
    data = ET.SubElement(sr, 'data')
    dnsoverride = ET.SubElement(data, 'DnsOverride')
    recordname = ET.SubElement(dnsoverride, 'name')
    recordname.text = name
    overridemaps = ET.SubElement(dnsoverride, 'mappings')
    mapset = ET.SubElement(overridemaps, 'set')
    for mapping in mappings:
        override = ET.SubElement(mapset, 'DnsMapping')
        hostname = ET.SubElement(override, 'hostName')
        hostname.text = mapping['hostName']
        ipaddr = ET.SubElement(override, 'ipAddress')
        ipaddr.text = mapping['ipAddress']

    if tagids is not None:
        tags = ET.SubElement(dnsoverride, 'tags')
        tagset = ET.SubElement(tags, 'set')
        for tagid in tagids.split(','):
            tagxml = ET.SubElement(tagset, 'Tag')
            tagidxml = ET.SubElement(tagxml, 'id')
            tagidxml.text = tagid.strip()

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, payload=payload)
    return resp


def updateDNSOverride(api: QualysAPI.QualysAPI, name: str,
                      add_mappings: list = None, remove_mappings: list = None,
                      tagids: str = None):
    fullurl = '%s/qps/rest/3.0/update/was/dnsoverride/' % api.server
    sr = ET.Element('ServiceRequest')
    data = ET.SubElement(sr, 'data')
    dnsoverride = ET.SubElement(data, 'DnsOverride')
    recordname = ET.SubElement(dnsoverride, 'name')
    recordname.text = name
    if add_mappings is not None or remove_mappings is not None:
        overridemaps = ET.SubElement(dnsoverride, 'mappings')

        if add_mappings is not None:
            add = ET.SubElement(overridemaps, 'add')
            for add_mapping in add_mappings:
                override = ET.SubElement(add, 'DnsMapping')
                hostname = ET.SubElement(override, 'hostName')
                hostname.text = add_mapping['hostName']
                ipaddr = ET.SubElement(override, 'ipAddress')
                ipaddr.text = add_mapping['ipAddress']

        if remove_mappings is not None:
            remove = ET.SubElement(overridemaps, 'add')
            for add_mapping in add_mappings:
                override = ET.SubElement(remove, 'DnsMapping')
                hostname = ET.SubElement(override, 'hostName')
                hostname.text = add_mapping['hostName']
                ipaddr = ET.SubElement(override, 'ipAddress')
                ipaddr.text = add_mapping['ipAddress']

    if tagids is not None:
        tags = ET.SubElement(dnsoverride, 'tags')
        tagset = ET.SubElement(tags, 'set')
        for tagid in tagids.split(','):
            tagxml = ET.SubElement(tagset, 'Tag')
            tagidxml = ET.SubElement(tagxml, 'id')
            tagidxml.text = tagid.strip()

    payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    resp = api.makeCall(url=fullurl, payload=payload)
    return resp


def searchAuthRecord(api: QualysAPI.QualysAPI, recordid: str = None, recordname: str = None,
                     tagids: str = None, tagname: str = None,
                     createdate: str = None, updateddate: str = None,
                     lastscandate: str = None, lastscanauthstatus: str = None,
                     isused: bool = None, contents: str = None):
    fullurl = '%s/qps/rest/3.0/search/was/webappauthrecord' % api.server

    sr = ET.Element('ServiceRequest')
    filters = ET.SubElement(sr, 'filters')

    if recordid is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'id')
        criteria.set('operator', 'IN')
        criteria.text = recordid

    if recordname is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = recordname

    if tagids is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.id')
        criteria.set('operator', 'IN')
        criteria.text = tagids

    if tagname is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'tags.name')
        criteria.set('operator', 'CONTAINS')
        criteria.text = tagname

    if createdate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'createdDate')
        criteria.set('operator', 'GREATER')
        criteria.text = createdate

    if updateddate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'updatedDate')
        criteria.set('operator', 'GREATER')
        criteria.text = updateddate

    if lastscandate is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'lastScan.date')
        criteria.set('operator', 'GREATER')
        criteria.text = lastscandate

    if lastscanauthstatus is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'lastScan.authStatus')
        criteria.set('operator', 'IN')
        criteria.text = lastscanauthstatus

    if isused is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'isUsed')
        criteria.set('operator', 'EQUALS')
        criteria.text = str(isused).lower()

    if contents is not None:
        criteria = ET.SubElement(filters, 'Criteria')
        criteria.set('field', 'id')
        criteria.set('operator', 'IN')
        criteria.text = contents

    if len(filters) > 0:
        payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    else:
        payload = ''

    resp = api.makeCall(url=fullurl, payload=payload)
    return resp



def getAuthRecord(api: QualysAPI.QualysAPI, recordid: int):
    fullurl = '%s/qps/rest/3.0/get/was/webappauthrecord/%s' % (api.server, str(recordid))

    resp = api.makeCall(url=fullurl)
    return resp


def createAuthRecordFromXML(api: QualysAPI.QualysAPI, authrecordxml: ET.Element):
    fullurl = '%s/qps/rest/3.0/create/was/webappauthrecord' % api.server

    if authrecordxml.find('data') is None:
        sr = ET.Element('ServiceRequest')
        data = ET.SubElement(sr, 'data')
        data.append(authrecordxml)
        payload = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    else:
        payload = ET.tostring(authrecordxml, method='xml', encoding='utf-8').decode()

    resp = api.makeCall(url=fullurl, payload=payload)
    return resp


def createAuthRecord(api: QualysAPI.QualysAPI):
    pass


def updateAuthRecord(api: QualysAPI.QualysAPI):
    pass
