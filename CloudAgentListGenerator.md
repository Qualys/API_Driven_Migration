# CloudAgentListGenerator module


### CloudAgentListGenerator.compareActivationKeys(src_key: dict, tgt_key: dict)
Compares the names and activated modules of two Cloud Agent Activation Keys to ensure compatibility for migration

Parameters:

    src_key:            A dictionary object containing the data for a single Cloud Agent Activation Key from the

        source subscription, as obtained by getActivationKeys()

    tgt_key:            A dictionary object containing the data for a single Cloud Agent Activation Key from the

        target subscription, as obtained by getActivationKeys()

Returns:

    True if names and activated modules match
    False if names or activated modules do not match


### CloudAgentListGenerator.createActivationKey(api: QualysAPI, activationKey: dict)
Creates a new Cloud Agent Activation Key

Parameters:

    api:               Object of the QualysAPI class
    activationKey:     Python Dictionary containing the details of the new Activation Key.  Can be a single

    > Activation Key from the list provided by getActivationKeys()

Returns:

    resp:             The HTTP response from the API request to create the new Activation Key


### CloudAgentListGenerator.getActivationKeys(api: QualysAPI)
Obtains from a subscription the list of Cloud Agent Activation Keys

Parameters:

    api:        An object of the class QualysAPI

Returns:

    keys:       A list containing the Cloud Agent Activation Keys in JSON format


### CloudAgentListGenerator.getAssets(api: QualysAPI, key: str)
Obtains the Cloud Agent asset data for assets registered under a given Cloud Agent Activation Key

Parameters:

    api:        An object of the class QualysAPI
    key:        A string value containing the Activation Key UUID

Returns:

    assets:     A list containing the assets registered under the given Cloud Agent Activation Key


### CloudAgentListGenerator.outputList(assets: list, keyid: str)
Writes the Cloud Agent asset data in CSV format, in preparation for Cloud Agent migration.

Parameters:

    assets:     List of assets as provided by getAssets
    keyid:      A string value containing the UUID of the target Cloud Agent Activation Key to which the

    > assets will be reassigned

Returns:

    Nothing

Outputs:

    keyid.csv:  Where ‘keyid’ is the value of the passed ‘keyid’ parameter
