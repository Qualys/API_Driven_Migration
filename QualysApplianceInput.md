# QualysApplianceInput module


### QualysApplianceInput.generateApplianceMap(source_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), target_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), appliance_name_map: dict | None = None)
Generates an appliance map for appliances in source and target subscriptions

Parameters:

    source_api:         An object of the class QualysAPI for the source subscription
    target_api:         An object of the class QualysAPI for the target subscription
    appliance_name_map: (Optional) A Python Dictionary containing a map of the source and target appliance names

    > where the source name is the key and the target name is the value

Returns:

    > appliancemap:      A Python Dictionary containing a map of the appliance IDs where the source appliance ID is

    >     the key and the target appliance ID is the value

    or

    None:               If there is an error in the API calls or where a mismatch occurs, a None value is returned


### QualysApplianceInput.readApplianceMap(inputfile: str)
Reads a CSV file containing a map of appliance IDs and returns a Python Dictionary containing that map.

Expected CSV file format:

    source_appliance_id,target_appliance_id

Parameters:

    inputfile:         A string containing the filename of the CSV file to read

Returns:

    appliancemap:       A Python Dictionary containing the source appliance ID as the key and the target appliance

        ID as the value for each entry in the input file
