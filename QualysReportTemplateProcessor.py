import xml.etree.ElementTree as ET
import QualysAPI


def responseHandler(response: ET.Element):
    return True


def getReportTemplates(source_api: QualysAPI.QualysAPI):
    scanurl = '%s/api/2.0/fo/report/template/scan/?action=export&report_format=xml' % source_api.server
    pciurl = '%s/api/2.0/fo/report/template/pciscan/?action=export&report_format=xml' % source_api.server
    patchurl = '%s/api/2.0/fo/report/template/patch/?action=export&report_format=xml' % source_api.server
    mapurl = '%s/api/2.0/fo/report/template/mapscan/?action=export&report_format=xml' % source_api.server

    scantemplates = source_api.makeCall(url=scanurl, method='GET')
    pcitemplates = source_api.makeCall(url=pciurl, method='GET')
    patchtemplates = source_api.makeCall(url=patchurl, method='GET')
    maptemplates = source_api.makeCall(url=mapurl, method='GET')

    return [scantemplates, pcitemplates, patchtemplates, maptemplates]


def createReportTemplates(target_api: QualysAPI.QualysAPI, templates: list):
    scanurl = '%s/api/2.0/fo/report/template/scan/?action=create&report_format=xml' % target_api.server
    pciurl = '%s/api/2.0/fo/report/template/pciscan/?action=create&report_format=xml' % target_api.server
    patchurl = '%s/api/2.0/fo/report/template/patch/?action=create&report_format=xml' % target_api.server
    mapurl = '%s/api/2.0/fo/report/template/mapscan/?action=create&report_format=xml' % target_api.server

    scanpayload = ET.tostring(templates[0], method='html', encoding='utf-8').decode()
    pcipayload = ET.tostring(templates[1], method='html', encoding='utf-8').decode()
    patchpayload = ET.tostring(templates[2], method='html', encoding='utf-8').decode()
    mappayload = ET.tostring(templates[3], method='html', encoding='utf-8').decode()

    scanresponse = target_api.makeCall(url=scanurl, payload=scanpayload)
    pciresponse = target_api.makeCall(url=pciurl, payload=pcipayload)
    patchresponse = target_api.makeCall(url=patchurl, payload=patchpayload)
    mapresponse = target_api.makeCall(url=mapurl, payload=mappayload)

    if not (responseHandler(scanresponse) or responseHandler(pciresponse) or responseHandler(patchresponse) or
            responseHandler(mapresponse)):
        return False
    return True
