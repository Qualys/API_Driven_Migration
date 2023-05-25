import xml.etree.ElementTree as ET
from QualysCommon import QualysAPI


def responseHandler(resp: ET.Element):
    return True


def listExceptions(api: QualysAPI.QualysAPI, status: str = None, truncation_limit: int = 1000):
    """
    Get list of Exceptions in subscription

    Parameters:
        api:                An object of class QualysAPI
        status:             An optional string containing the status of the Exceptions to include
                            Must be one of 'Pending', 'Approved', 'Rejected' or 'Expired'
        truncation_limit:   An integer value used to limit the number of results returned in a single API call.  Will
                            continue to make further API calls using the same limit until all Exceptions have been
                            downloaded.

    Returns:
        None                If an error occurs or an invalid Status value is provided
        exceptions, resp:
            exceptions:     A document of type xml.etree.Element.ElementTree containing Exceptions data
            resp:           A document of type xml.etree.Element.ElementTree containing the full response from the
                            final API call
    """
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
                     assigneeid: str, comments: str, reopen: bool = False):
    """
    Generates a new Exception Request

    Parameters:
        api:            An object of class QualysAPI
        controlid:      The CID of the control for which the exception is being requested
        hostid:         The Host ID of the host for which the exception is being requested
        policyid:       The Policy ID of the policy for which the exception is being requested
        technologyid:   The Technology ID of the technology for which the exception is being requested
        assigneeid:     The User ID of the assignee of the requested exception
        comments:       The comments to be included in the exception request
        reopen:         If True, re-open the request when evidence changes.
                        If False, does not re-open the request when evidence changes.
                        Defaults to False

    Returns:
        None            If an error was encountered
        OR
        resp:           A document of type xml.etree.Element.ElementTree containing the full API response

    """
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
    """
    Updates an Exception Request

    Parameters:
        api:            An object of class QualysAPI
        exceptions:     A string containing a comma-separated list of exception numbers
        comments:       Comments to add to the exception(s)
        reassignto:     An optional string containing the User ID of the user to reassign the Exception to.
                        Defaults to None, signifying "do not reassign"
        reopen:         An optional Boolean value signifying whether to re-open the Exception if the underlying
                        evidence changes.
                        Defaults to False
        status:         An optional string value containing the new Status of the Exception.
                        Must be one of 'Approved' or 'Rejected'
                        Defaults to None, signifying no change in status
        end_date:       An optional string value containing the new date/time for the expiry of the Exception.
                        Defaults to None, signifying no change in the expiry date

    Returns:
        resp:           A document of type xml.etree.Element.ElementTree containing the full API response
        OR
        None            If an error is encountered in the API response
    """
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
    """
    Delete one or more Exceptions

    Parameters:
        api:            An object of class QualysAPI
        exceptions:     A string containing a comma-separated list of exception numbers to delete

    Returns:
        resp:           A document of type xml.etree.Element.ElementTree containing the full API response
        OR
        None            If an error is encountered in the API response
    """
    fullurl = '%s/api/2.0/fo/compliance/exception/?action=delete&exception_numbers=%s' % (api.server, exceptions)
    resp = api.makeCall(fullurl)
    if not responseHandler(resp):
        print('ERROR: QualysComplianceExceptionProcessor.requestException failed')
        return None
    return resp


