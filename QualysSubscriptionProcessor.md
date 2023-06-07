# QualysSubscriptionProcessor module


### QualysSubscriptionProcessor.exportSubscriptionConfig(api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI))
Export all subscription configuration settings

Parameters:

    api:            An object of the class QualysAPI

Returns:

    response:       A document of type xml.etree.ElementTree.Element containing the full XML API response


### QualysSubscriptionProcessor.importSubscriptionConfig(api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), configxml: Element)
Import subscription configuration settings from XML obtained by exportSubscriptionConfig()

Parameters:

    api:            An object of the class QualysAPI
    configxml:      An XML document of type xml.etree.ElementTree.Element as obtained by getSubscriptionConfig()

Returns:

    response:       A XML document of type xml.etree.ElementTree.Element containing the full API response
