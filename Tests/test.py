import argparse
import sys
from API_Driven_Migration.QualysCommon import QualysAPI
import testTags
import testSubscription
import testIPs
import testDomains
import testNetworks
import testAssetGroups
import testOptionProfiles
import testReportTemplates
import testSearchLists
import testAppliance
import testUsers
import testCompliancePolicy
import testVMScanSchedule
import testCloudConnector


def quit(exitcode: int):
    print('Source API Calls Made : %s' % source_api.callCount)
    print('Target API Calls Made : %s' % target_api.callCount)
    sys.exit(exitcode)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_username', help='API Username in source subscription')
    parser.add_argument('source_password', help='API User Password in source subscription')
    parser.add_argument('source_qualyspod', help='Location of source Qualys Subscription '
                                                 '[US01|US02|US03|EU01|EU02|IN01|PCP]')
    parser.add_argument('target_username', help='API Username in target subscription')
    parser.add_argument('target_password', help='API User Password in target subscription')
    parser.add_argument('target_qualyspod', help='Location of target Qualys Subscription '
                                                 '[US01|US02|US03|EU01|EU02|IN01|PCP]')

    parser.add_argument('-p', '--proxyenable', action='store_true', help='Use HTTPS Proxy (required -u or --proxyurl')
    parser.add_argument('-u', '--proxyurl', help='Proxy URL (requires -p or --proxyenable)')
    parser.add_argument('-a', '--apiurl', help='API URL for Qualys PCP Subscriptions.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    parser.add_argument('-s', '--simulate', action='store_true', help='Simulate - obtain data from source, do not send '
                                                                      'to target')
    parser.add_argument('-N', '--enable_networks', action='store_true', help='The Networks feature is enabled in the'
                                                                             'subscription')
    parser.add_argument('--testTags', action='store_true', help='Test Tag Migration')
    parser.add_argument('--testSubscription', action='store_true', help='Test Subscription Configuration Migration')
    parser.add_argument('--testIPs', action='store_true', help='Test IP Migration')
    parser.add_argument('--testDomains', action='store_true', help='Test Domains Migration')
    parser.add_argument('--testNetworks', action='store_true', help='Test Networks Migration')
    parser.add_argument('--testAssetGroups', action='store_true', help='Test Asset Groups Migration')
    parser.add_argument('--testOptionProfiles', action='store_true', help='Test Option Profiles Migration')
    parser.add_argument('--testReportTemplates', action='store_true', help='Test Report Templates Migration')
    parser.add_argument('--testSearchLists', action='store_true', help='Test Search List Migration')
    parser.add_argument('--testAppliances', action='store_true', help='Test Appliance Migration')
    parser.add_argument('--testUsers', action='store_true', help='Test User Migration')
    parser.add_argument('--testCompliancePolicy', action='store_true', help='Test Compliance Policy Migration')
    parser.add_argument('--testVMScanSchedule', action='store_true', help='Test VM Scan Schedule Migration')
    parser.add_argument('--testCloudConnector', action='store_true', help='Test Cloud Connector Migration')

    args = parser.parse_args()

    source_url = ''
    if args.source_qualyspod == 'PCP':
        if args.source_apiurl is None:
            print('FATAL: qualyspod is PCP but apiurl is not specified')
            sys.exit(1)
        source_url = args.source_apiurl
    else:
        source_url = QualysAPI.QualysAPI.podPicker(args.source_qualyspod)
        if source_url == 'invalid':
            print('FATAL: qualyspod \'%s\' is not recognised' % args.source_qualyspod)
            sys.exit(1)

    target_url = ''
    if args.target_qualyspod == 'PCP':
        if args.target_pcpurl is None:
            print('FATAL: qualyspod is PCP but apiurl is not specified')
            sys.exit(1)
        target_url = args.target_pcpurl
    else:
        target_url = QualysAPI.QualysAPI.podPicker(args.target_qualyspod)
        if target_url == 'invalid':
            print('FATAL: qualyspod \'%s\' is not recognised' % args.target_qualyspod)
            sys.exit(1)

    enableProxy = False
    proxyURL = ''
    if args.proxyenable:
        if args.proxyurl == '' or args.proxyurl is None:
            print('FATAL: -p or --proxyenable is specified without -u or --proxyurl')
            sys.exit(2)
        proxyURL = args.proxyurl
        enableProxy = True

    source_api = QualysAPI.QualysAPI(svr=source_url, usr=args.source_username, passwd=args.source_password,
                                     enableProxy=enableProxy, proxy=proxyURL, debug=args.debug)
    target_api = QualysAPI.QualysAPI(svr=target_url, usr=args.target_username, passwd=args.target_password,
                                     enableProxy=enableProxy, proxy=proxyURL, debug=args.debug)

    # +------------------+
    # | TESTS START HERE |
    # +------------------+

    # Tags
    if args.testTags:
        if not testTags.testTags(source_api=source_api, target_api=target_api, simulate=args.simulate):
            print('Tag test failed')
            quit(1)

    # Subscription Prefs
    if args.testSubscription:
        if not testSubscription.testSubscription(source_api=source_api, target_api=target_api,
                                                 simulate=args.simulate):
            print('Subscription Preferences test failed')
            quit(1)

    # IPs
    if args.testIPs:
        if not testIPs.testIPs(source_api=source_api, target_api=target_api, simulate=args.simulate):
            print('IPs test failed')
            quit(1)

    # Domains
    if args.testDomains:
        if not testDomains.testDomains(source_api=source_api, target_api=target_api, simulate=args.simulate):
            print('Domains test failed')
            quit(1)

    # Networks
    if not args.enable_networks:
        if args.testNetworks:
            if not testNetworks.testNetworks(source_api=source_api, target_api=target_api, simulate=args.simulate):#
                print('Networks test failed')
                quit(1)
    else:
        print('Networks feature disabled on command line.  Use --enable_networks or -N to enable')
        quit(1)

    # Asset Groups
    if args.testAssetGroups:
        if not testAssetGroups.testAssetGroups(source_api=source_api, target_api=target_api, simulate=args.simulate,
                                               networks=args.enable_networks):
            print('Asset Groups test failed')
            quit(1)

    # Option Profiles
    if args.testOptionProfiles:
        if not testOptionProfiles.testOptionProfiles(source_api=source_api, target_api=target_api,
                                                     simulate=args.simulate):
            print('Option Profiles test failed')
            quit(1)

    # Report Templates
    if args.testReportTemplates:
        if not testReportTemplates.testReportTemplates(source_api=source_api, target_api=target_api,
                                                       simulate=args.simulate):
            print('Report Templates test failed')
            quit(1)

    # Search Lists
    if args.testSearchLists:
        if not testSearchLists.testSearchLists(source_api=source_api, target_api=target_api, simulate=args.simulate):
            print('Search Lists test failed')
            quit(1)

    # Appliances
    if args.testAppliances:
        if not testAppliance.testAppliances(source_api=source_api, target_api=target_api, simulate=args.simulate):
            print('Appliance test failed')
            quit(1)

    # Users
    if args.testUsers:
        if not testUsers.testUsers(source_api=source_api, target_api=target_api, simulate=args.simulate):
            print('User test failed')
            quit(1)

    # Compliance Policies
    if args.testCompliancePolicy:
        if not testCompliancePolicy.testCompliancePolicy(source_api=source_api, target_api=target_api,
                                                         simulate=args.simulate):
            print('Compliance Policies test failed')
            quit(1)

    # VM Scan Schedules
    if args.testVMScanSchedule:
        if not testVMScanSchedule.testVMScanSchedule(source_api=source_api, target_api=target_api,
                                                     simulate=args.simulate):
            print('VM Scan Schedules test failed')
            quit(1)

    # Cloud Connectors
    if args.testCloudConnector:
        if not testCloudConnector.testCloudConnector(source_api=source_api, target_api=target_api,
                                                     simulate=args.simulate):
            print('Cloud Connector test failed')
            quit(1)

    quit(0)
