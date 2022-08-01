import xml.etree.ElementTree as ET
from API_Driven_Migration.QualysCommon import QualysAPI


def responseHandler(resp: ET.Element):
    return True


def listExceptions(api: QualysAPI.QualysAPI, status: str = None, truncation_limit: int = 1000):

    fullurl = '%s/api/2.0/fo/compliance/exception/?action=list&details=All' % api.server
    if status is not None:
        if status in ['Pending', 'Approved', 'Rejected', 'Expired']:
            fullurl = '%s&status=%s' % (fullurl, status)
        else:
            print('ERROR: QualysComplianceExceptionProcessor.listExceptions: status %s not recognised.  Must be '
                  '\'Pending\', \'Approved\', \'Rejected\' or \'Expired\'')
            return None

    exceptions = ET.Element('EXCEPTION_LIST')
    url = '%s&truncation_limit=%s' % (fullurl, str(truncation_limit))
    more_results = True

    while more_results:
        resp = api.makeCall(url=url)

        if resp.find('RESPONSE/WARNING/URL') is not None:
            url = resp.find('RESPONSE/WARNING/URL').text
            more_results = True
        else:
            more_results = False

        for i in resp.findall('.//EXCEPTION'):
            exceptions.append(i)
    return exceptions, resp


def requestException(api: QualysAPI.QualysAPI, controlid: str, hostid: str, policyid: str, technologyid: str,
                     assigneeid: str, comments: str, reopen: bool = False, instancestring: str = None):
    fullurl = '%s/api/2.0/fo/compliance/exception/?action=request' % api.server
    fullurl = '%s&control_id=%s&host_id=%s&policy_id=%s&technology_id=%s&assignee_id=%s&comments=%s' % \
              (fullurl, controlid, hostid, policyid, technologyid, assigneeid, comments)

    if reopen:
        fullurl = '%s&reopen_on_evidence_change=1' % fullurl
    else:
        fullurl = '%s&reopen_on_evidence_change=0' % fullurl

    resp = api.makeCall(url=fullurl, method='POST')
    if not responseHandler(resp):
        print('ERROR: QualysComplianceExceptionProcessor.requestException failed')
        return None

    return resp


def updateException(api: QualysAPI.QualysAPI, exceptions: str, comments: str, reassignto: str = None,
                    reopen: bool = False, status: str = None, end_date: str = None):
    fullurl = '%s/api/2.0/fo/compliance/exception/?action=update' % api.server
    fullurl = '%s&exception_numbers=%s&comments=%s' % (fullurl, exceptions, comments)
    if reassignto is not None:
        fullurl = '%s&reassign_to=%s' % (fullurl, reassignto)
    if reopen:
        fullurl = '%s&reopen_on_evidence_change=1' % fullurl
    if status is not None:
        fullurl = '%s&status=%s' % (fullurl, status)
    if end_date is not None:
        fullurl = '%s&end_date=%s' % (fullurl, end_date)

    resp = api.makeCall(url=fullurl)
    if not responseHandler(resp):
        print('ERROR: QualysComplianceExceptionProcessor.updateException failed')
        return None

    return resp


def deleteException(api: QualysAPI.QualysAPI, exceptions: str):
    fullurl = '%s/api/2.0/fo/compliance/exception/?action=delete&exception_numbers=%s' % (api.server, exceptions)
    resp = api.makeCall(fullurl)
    if not responseHandler(resp):
        print('ERROR: QualysComplianceExceptionProcessor.requestException failed')
        return None
    return resp


