# QualysApplianceProcessor module


### QualysApplianceProcessor.createAppliance(target_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), name: str, polling_interval: str = '180', asset_group: str | None = None)
Create a new scanner appliance in the target subscription with the provided name, polling interval and optionally
asset group assignment.

Parameters:

    target_api:         An object of the type QualysAPI
    name:               A string containing the name of the scanner appliance
    polling_interval:   A string containing the required polling interval in seconds of the scanner appliance,

    > defaults to 180 seconds

    asset_group:        A string containing the name of the Asset Group to assign the scanner appliance to,

        defaults to None indicating no Asset Group assignment

Returns:

    A string value containing the ID of the new scanner appliance


### QualysApplianceProcessor.getAppliances(source_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI))
Get a list of appliances with full details

Parameters:

    source_api:         An object of the class QualysAPI

Returns:

    resp:               An document of type xml.etree.ElementTree.Element containing the APPLIANCE_LIST

        element of the API response

    or

    None if an error occurs or no appliances are contained in the output


### QualysApplianceProcessor.getStaticRoutes(appliance: Element)
Gets the configured static routes from a document of type xml.etree.ElementTree.Element containing scanner
appliance data

Parameters:

    appliance:      An XML document of type xml.etree.ElementTree.Element containing appliance data

Returns:

    routes:         A list of static route strings for use in a further API call to configure an appliance

        (e.g. ‘10.30.0.0|255.255.255.0|10.20.0.1|route30’)


### QualysApplianceProcessor.getVLANs(appliance: Element)
Get the configured VLANS from a document of type xml.etree.elementTree.Element containing scanner appliance data

Parameters:

    appliance:          An XML document of type xml.etree.ElementTree.Element containing appliance data

Returns:

    vlans:              A list of VLAN strings for use in a further API call to configure an appliance

        (e.g. ‘20|10.20.0.0|255.255.255.0|vlan20’)


### QualysApplianceProcessor.replicateAppliance(target_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), appliance: Element)
Creates a new scanner appliance in the target subscription to match the name and configuration of another
appliance.  Uses the createAppliance() and updateAppliance() functions.

Parameters:

    target_api:         An object of the class QualysAPI
    appliance:          A document of the type xml.etree.ElementTree.Element containing scanner appliance data

Returns:

    The ID of the new appliance

    or

    None if the appliance creation failed


### QualysApplianceProcessor.responseHandler(resp: Element)

### QualysApplianceProcessor.updateAppliance(target_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), appliance_id: str, vlans: list, routes: list)
Update an appliance with VLAN and Static Route information

Parameters:

    target_api:         An object of type QualysAPI
    appliance_id:       The ID of the scanner appliance to update
    vlans:              A list of VLAN strings as provided by getVLANs()
    routes:             A list of Static Route strings as provided by getStaticRoutes()

Returns:

    True if appliance was successfully updated
    False if appliance update failed
