import sys
import QualysAPI
import QualysTagProcessor


def testTags(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI):
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
