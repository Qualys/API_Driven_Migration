import xml.etree.ElementTree as ET
from API_Driven_Migration.QualysCommon import QualysAPI
from API_Driven_Migration.QualysPC import QualysCompliancePolicyProcessor
import copy


def testCompliancePolicy(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    print('testCompliancePolicy: Getting Policy List')
    policylist = QualysCompliancePolicyProcessor.getPolicyList(source_api=source_api)
    policies = {}
    for policy in policylist:
        print('testCompliancePolicy: Getting policy for policyid %s' % policy)
        resp = QualysCompliancePolicyProcessor.exportPolicy(source_api=source_api, policyid=policy)
        if resp is None:
            print('testCompliancePolicy: Failed, could not get policy')
            return False
        policies[policy] = resp

    if simulate:
        print('%s policies exported' % len(policies))
        # return True

    # TODO Test importing, then fix it because it will be broken
    for pol in policies.keys():
        polxml = policies[pol]
        polet = ET.fromstring(polxml)
        polname = polet.find('.//TITLE').text
        print('Creating policy : %s' % polname)
        debugflag = copy.deepcopy(target_api.debug)
        target_api.debug = True
        resp = QualysCompliancePolicyProcessor.importPolicy(target_api=target_api, policyname=polname, policy=polxml)
        target_api.debug = debugflag
    return True
