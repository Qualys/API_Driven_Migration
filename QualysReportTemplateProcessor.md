# QualysReportTemplateProcessor module


### QualysReportTemplateProcessor.convertScanTemplate(scantemplate: Element)
Convert a Scan Report Template from its XML format into a URL/payload, excluding the FQDN, with which to recreate
the template in a new subscription

Parameters:

    scantemplate:           A document of type xml.etree.ElementTree.Element containing the XML data which defines

        the report template

Returns:

    None                    If errors are encountered during the conversion
    OR
    url,payload:

    > url                 The URL, excluding the FQDN, of an API call to create a new Scan Template
    > payload             The payload to use in the API call


### QualysReportTemplateProcessor.getMapReportTemplates(source_api: QualysAPI)
Get all Map Report Templates from a subscription

Parameters:

    source_api:             An object of class QualysAPI

Returns:

    maptemplates:          A document of type xml.etree.ElementTree.Element containing the full API response


### QualysReportTemplateProcessor.getPCIReportTemplates(source_api: QualysAPI)
Get all PCI Report Templates from a subscription

Parameters:

    source_api:             An object of class QualysAPI

Returns:

    pcitemplates:          A document of type xml.etree.ElementTree.Element containing the full API response


### QualysReportTemplateProcessor.getPatchReportTemplates(source_api: QualysAPI)
Get all Patch Report Templates from a subscription

Parameters:

    source_api:             An object of class QualysAPI

Returns:

    patchtemplates:         A document of type xml.etree.ElementTree.Element containing the full API response


### QualysReportTemplateProcessor.getReportTemplates(source_api: QualysAPI)
Get all Report Templates from a subscription

Parameters:

    source_api:         An object of class QualysAPI

Returns

    templates:          A python dictionary containing the keys ‘scan’, ‘pci’, ‘patch’, and ‘map’ where the values

        of each are return values from getScanReportTemplates(), getPCIReportTemplates(),
        getPatchReportTemplates() and getMapReportTemplates() respectively


### QualysReportTemplateProcessor.getScanReportTemplates(source_api: QualysAPI)
Get all Scan Report Templates from a subscription.

Parameters:

    source_api:             An object of class QualysAPI

Returns:

    scantemplates:          A document of type xml.etree.ElementTree.Element containing the full API response


### QualysReportTemplateProcessor.responseHandler(response: Element)
