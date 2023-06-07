# QualysOptionProfileProcessor module


### QualysOptionProfileProcessor.exportOptionProfiles(source_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI))
Exports all Option Profiles from a subscription

Parameters:

    source_api:         An object of the class QualysAPI

Returns:

    response:           A document of the type xml.etree.ElementTree.Element containing the full API response


### QualysOptionProfileProcessor.importOptionProfiles(target_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), optionprofiles: Element)
Imports Option Profiles to a subscription

Parameters:

    target_api:         An object of the class QualysAPI

Returns:

    response:           A document of the type xml.etree.ElementTree.Element containing the full API response


### QualysOptionProfileProcessor.responseHandler(response)
