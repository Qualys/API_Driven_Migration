from API_Driven_Migration.QualysCommon import QualysAPI, QualysUserProcessor


def testUsers(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    users = QualysUserProcessor.getUsers(source_api)
    userlist = QualysUserProcessor.generateURLs(users)
    if simulate:
        for url in userlist:
            print(url)
            return True

    if not QualysUserProcessor.createUsers(target_api, userlist):
        print('testUsers failed')
        return False

    return True
