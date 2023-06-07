# QualysComplianceExceptionProcessor module

### QualysComplianceExceptionProcessor.deleteException(api: QualysAPI, exceptions: str)
Delete one or more Exceptions

Parameters:

    api:            An object of class QualysAPI
    exceptions:     A string containing a comma-separated list of exception numbers to delete

Returns:

    resp:           A document of type xml.etree.Element.ElementTree containing the full API response
    OR
    None            If an error is encountered in the API response

### QualysComplianceExceptionProcessor.listExceptions(api: QualysAPI, status: str | None = None, truncation_limit: int = 1000)
Get list of Exceptions in subscription

Parameters:

    api:                An object of class QualysAPI
    status:             An optional string containing the status of the Exceptions to include

    > Must be one of ‘Pending’, ‘Approved’, ‘Rejected’ or ‘Expired’

    truncation_limit:   An integer value used to limit the number of results returned in a single API call.  Will

        continue to make further API calls using the same limit until all Exceptions have been
        downloaded.

Returns:

    None                If an error occurs or an invalid Status value is provided
    exceptions, resp:

    > exceptions:     A document of type xml.etree.Element.ElementTree containing Exceptions data
    > resp:           A document of type xml.etree.Element.ElementTree containing the full response from the

    > > final API call

### QualysComplianceExceptionProcessor.requestException(api: QualysAPI, controlid: str, hostid: str, policyid: str, technologyid: str, assigneeid: str, comments: str, reopen: bool = False)
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

    > If False, does not re-open the request when evidence changes.
    > Defaults to False

Returns:

    None            If an error was encountered
    OR
    resp:           A document of type xml.etree.Element.ElementTree containing the full API response

### QualysComplianceExceptionProcessor.responseHandler(resp: Element)

### QualysComplianceExceptionProcessor.updateException(api: QualysAPI, exceptions: str, comments: str, reassignto: str | None = None, reopen: bool = False, status: str | None = None, end_date: str | None = None)
Updates an Exception Request

Parameters:

    api:            An object of class QualysAPI
    exceptions:     A string containing a comma-separated list of exception numbers
    comments:       Comments to add to the exception(s)
    reassignto:     An optional string containing the User ID of the user to reassign the Exception to.

    > Defaults to None, signifying “do not reassign”

    reopen:         An optional Boolean value signifying whether to re-open the Exception if the underlying

        evidence changes.
        Defaults to False

    status:         An optional string value containing the new Status of the Exception.

        Must be one of ‘Approved’ or ‘Rejected’
        Defaults to None, signifying no change in status

    end_date:       An optional string value containing the new date/time for the expiry of the Exception.

        Defaults to None, signifying no change in the expiry date

Returns:

    resp:           A document of type xml.etree.Element.ElementTree containing the full API response
    OR
    None            If an error is encountered in the API response
