from QualysCommon import QualysAPI
from QualysVM import QualysVMScanScheduleProcessor


def testVMScanSchedule(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    scanlist = QualysVMScanScheduleProcessor.getScheduleList(source_api=source_api)
    for scan in scanlist.findall('.//SCAN'):
        requeststr = QualysVMScanScheduleProcessor.convertScheduledScan(scan=scan)
        if requeststr is None:
            print('Scheduled Scan Conversion failed')
        if simulate:
            fullurl = '%s/%s' % (target_api.server, requeststr)
            fullurl.replace(' ', '+')
            print(fullurl)
        else:
            resp = QualysVMScanScheduleProcessor.createScheduledScan(target_api=target_api, requeststr=requeststr)
            if resp is None:
                print("Error creating scheduled scan")
    return True
