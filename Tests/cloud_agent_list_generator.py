import json
import argparse
from QualysCommon.QualysAPI import QualysAPI
from QualysCloudAgent import CloudAgentListGenerator
from sys import exit
from getpass import getpass

if __name__ == '__main__':
    # Script entry point
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', help='Username')
    parser.add_argument('-p', help='Password')
    parser.add_argument('-P', help='Enable proxy')
    parser.add_argument('-U', help='Proxy URL')
    parser.add_argument('-a', help='API Base URL')
    parser.add_argument('-d', action='store_true', help='Enable debug output')
    parser.add_argument('-k', action='append', nargs='+', help='Source Activation Key ID')
    parser.add_argument('-t', help='Target Activation Key ID')

    args = parser.parse_args()

    password = ''

    if args.u is None:
        print('No username provided')
        exit(1)

    if args.p is None:
        print('No password provided')
        exit(1)

    if args.p == '-':
        password = getpass('Enter password for user %s : ' % args.u)
    else:
        password = args.p

    if args.P:
        if args.U is None:
            print('Proxy enabled but no proxy URL specified')
            exit(1)

    if args.a is None:
        print('No API base URL specified')
        exit(1)

    api = QualysAPI(svr=args.a, usr=args.u, passwd=password, debug=args.d)

    win_f = open('%s_windows.csv' % args.t, mode='w')
    lin_f = open('%s_linux.csv' % args.t, mode='w')

    all_assets = []
    for key in args.k:
        asset_list = CloudAgentListGenerator.getAssets(api=api, key=key[0])
        for asset in asset_list:
            if asset['HostAsset']['agentInfo']['platform'] == 'Windows':
                win_f.write('%s,%s\n' % (asset['HostAsset']['agentInfo']['agentId'], asset['HostAsset']['name']))
                print('%s,%s' % (asset['HostAsset']['agentInfo']['agentId'], asset['HostAsset']['name']))
            else:
                lin_f.write('%s,%s\n' % (asset['HostAsset']['agentInfo']['agentId'], asset['HostAsset']['name']))
                print('%s,%s' % (asset['HostAsset']['agentInfo']['agentId'], asset['HostAsset']['name']))

    win_f.close()
    lin_f.close()
