import argparse
import sys
import QualysAPI
import QualysTagProcessor

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

    args = parser.parse_args()

    source_url = ''
    if args.source_qualyspod == 'PCP':
        if args.source_pcpurl is None:
            print('FATAL: qualyspod is PCP but apiurl is not specified')
            sys.exit(1)
        source_url = args.source_pcpurl
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

    try:
        source_tags = QualysTagProcessor.getTags(api=source_api)
    except:
        print('FATAL: QualysTagProcessor.getTags() failed')
        sys.exit(3)
    if source_tags is None:
        print('FATAL: QualysTagProcessor.getTags() FAILED')
        sys.exit(3)

    try:
        source_tags = QualysTagProcessor.pruneSystemTags(tags=source_tags)
    except:
        print('FATAL: QualysTagProcessor.pruneSystemTags() FAILED')
        sys.exit(4)
    if source_tags is None:
        print('FATAL: QualysTagProcessor.pruneSystemTags() FAILED')
        sys.exit(9)

    try:
        target_tags = QualysTagProcessor.restructureTags(tags=source_tags)
    except:
        print('FATAL: QualysTagProcessor.restructureTags() FAILED')
        sys.exit(5)
    if target_tags is None:
        print('FATAL: QualysTagProcessor.restructureTags() FAILED')
        sys.exit(9)

    try:
        target_tags = QualysTagProcessor.handleSystemParents(target_api=target_api, tags=target_tags)
    except:
        print('FATAL: QualysTagProcessor.handleSystemParent() FAILED')
        sys.exit(6)
    if target_tags is None:
        print('FATAL: QualysTagProcessor.handleSystemParent() FAILED')
        sys.exit(9)

    try:
        response = QualysTagProcessor.createTags(api=target_api, tags=target_tags)
    except:
        print('FATAL: QualysTagProcessor.createTags() FAILED')
        sys.exit(7)

    print('Source API Calls Made : %s' % source_api.callCount)
    print('Target API Calls Made : %s' % target_api.callCount)
