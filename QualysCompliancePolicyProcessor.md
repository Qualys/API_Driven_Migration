# QualysCompliancePolicyProcessor module

### QualysCompliancePolicyProcessor.addAssetGroups(target_api: QualysAPI, policyid: str, asset_group_ids: str, evaluate: bool = False)
Add Asset Groups to a policy’s scope

Parameters:

    target_api:         An object of class QualysAPI
    policyid:           A string value containing the ID of the policy to update
    asset_group_ids:    A string value containing a comma-separated list of Asset Group IDs
    evaluate:           A boolean value to signal if the policy should be re-evaluated after the update

Response:

    resp:               A document of type xml.etree.ElementTree.Element containing the full API response

### QualysCompliancePolicyProcessor.exportPolicy(source_api: QualysAPI, policyid: str)
Export a policy

Parameters:

    source_api:         An object of class QualysAPI
    policyid:           A string value containing a policy ID

Returns:

    resp:               A string value containing raw XML, representing the policy content

### QualysCompliancePolicyProcessor.getFullPolicyList(source_api: QualysAPI)
Get a full list of policies

Parameters:

    source_api:         An object of class QualysAPI

Returns:

    policy_list:        A list of python dictionaries containing policy data, used in payloads to recreate

        the policy

### QualysCompliancePolicyProcessor.getPolicyIDList(source_api: QualysAPI)
Get a list of policy IDs

Parameters:

    source_api:         An object of type QualysAPI

Returns:

    policylist:         A python list of string values containing policy IDs, representing all policy IDs in a

        subscription

### QualysCompliancePolicyProcessor.importPolicy(target_api: QualysAPI, policyname: str, policy: str)
Import a policy

Parameters:

    target_api:         An object of class QualysAPI
    policyname:         A string value containing the name to give the policy
    policy:             A string value containing the raw XML, representing the policy content, as exported

    > by exportPolicy()

Returns:

    resp:               A document of type xml.etree.ElementTree.Element containing the full API response

### QualysCompliancePolicyProcessor.responseHandler(resp: Element)

### QualysCompliancePolicyProcessor.setAssetGroupAssignment(target_api: QualysAPI, asset_group_ids: str, policy_id: str)
Set and override the Asset Groups in a policy’s scope

Parameters:

    target_api:         An object of class QualysAPI
    asset_group_ids:    A string containing a comma-separated list of Asset Group IDs
    policy_id:          A string containing the ID of the policy to update

Returns:

    resp:               A document of type xml.etree.ElementTree.Element containing the full API response
