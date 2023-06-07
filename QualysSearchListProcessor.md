# QualysSearchListProcessor module


### QualysSearchListProcessor.convertDynamicSearchList(searchlist: Element)
Converts a dynamic search list from XML format to URL/Payload format, excluding the FQDN

Parameters:

    searchlist:             A document of type xml.etree.ElementTree.Element containing the search list data

Returns:

    None, None              If an error is encountered during conversion of the XML data
    url, payload:

    > url:                A string containing the URL, excluding the FQDN, of the API call to create the

    >     dynamic search list

    > payload:            A python dictionary containing the payload data to be used in the API call


### QualysSearchListProcessor.convertModifiedFilters(modstring: str, modtype: str, payload: dict | None = None)
Convert Search List criteria into a format accepted in an API request, either in payload or URL format.  Used by
convertDynamicSearchList() and createDynamicSearchList

Parameters:

    modstring:          A string containing the text of the criteria to convert
    modtype:            A string containing the type of criteria to convert
    payload:            (Optional) A python dictionary containing payload data to update with the

    > converted criteria data

Returns:

    url:                If no payload parameter is passed, returns the modified criteria in URL format
    OR
    payload:            If a payload parameter is passed, returns the updated payload containing the modified

    > criteria


### QualysSearchListProcessor.convertOther(otherstring: str, payload: dict | None = None)
Convert non-modifier elements of a search list into a format accepted by an API call.  Used by
convertDynamicSearchList() and createDynamicSearchList()

Parameters:

    otherstring:            A string value comma-delimited list of the parameters to convert
    payload:                (Optional) A python dictionary containing payload data to update with the converted

    > parameter

Returns:

    retstr:                 If no payload parameter passed, the converted parameters in URL format
    OR
    payload:                If a payload parameter was passed, the updated payload containing the modified

    > parameters


### QualysSearchListProcessor.convertStaticSearchList(searchlist: Element)
Converts a static search list from XML format to URL/Payload format, excluding the FQDN

Parameters:

    searchlist:             A document of type xml.etree.ElementTree.Element containing the search list data

Returns:

    None, None              If an error is encountered during conversion of the XML data
    url, payload:

    > url:                A string containing the URL, excluding the FQDN, of the API call to create the

    >     dynamic search list

    > payload:            A python dictionary containing the payload data to be used in the API call


### QualysSearchListProcessor.createDynamicSearchList(target_api: QualysAPI, searchlist: Element, simulate: bool = False)
Create a dynamic search list from a source XML document

Parameters:

    target_api:             An object of class QualysAPI
    searchlist:             A document of type xml.etree.ElementTree.Element containing the search list

    > data

    simulate:               If True, outputs the URL to the console and does not make the API call to create

        the search list
        If False, makes the API call to create the search list

Returns:

    resp:                  A document of type xml.etree.ElementTree.Element containing the full API response


### QualysSearchListProcessor.createStaticSearchList(target_api: QualysAPI, searchlist: Element, simulate: bool = False)
Create a static search list from a source XML document

Parameters:

    target_api:             An object of class QualysAPI
    searchlist:             A document of type xml.etree.ElementTree.Element containing the search list

    > data

    simulate:               If True, outputs the URL to the console and does not make the API call to create

        the search list
        If False, makes the API call to create the search list

Returns:

    resp:                  A document of type xml.etree.ElementTree.Element containing the full API response


### QualysSearchListProcessor.getDynamicSearchLists(source_api: QualysAPI, ids: str | None = None)
Get dynamic search lists from a subscription

Parameters:

    source_api:         An object of the class QualysAPI
    ids:                (Optional) A string value containing a comma-separated list of Search List IDs to get

Returns:

    A document of type xml.etree.ElementTree.Element which contains the DYNAMIC_LISTS element from the API response


### QualysSearchListProcessor.getStaticSearchLists(source_api: QualysAPI, ids: str | None = None)
Get static search lists from a subscription

Parameters:

    source_api:         An object of the class QualysAPI
    ids:                (Optional) A string value containing a comma-separated list of Search List IDs to get

Returns:

    A document of type xml.etree.ElementTree.Element which contains the STATIC_LISTS element from the API response


### QualysSearchListProcessor.responseHandler(resp: Element)
