import QualysAPI
import QualysTagProcessor


def testTags(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    try:
        source_tags = QualysTagProcessor.getTags(api=source_api)
    except:
        print('FATAL: QualysTagProcessor.getTags() failed')
        return False
    if source_tags is None:
        print('FATAL: QualysTagProcessor.getTags() FAILED')
        return False

    try:
        source_tags = QualysTagProcessor.pruneSystemTags(tags=source_tags)
    except:
        print('FATAL: QualysTagProcessor.pruneSystemTags() FAILED')
        return False
    if source_tags is None:
        print('FATAL: QualysTagProcessor.pruneSystemTags() FAILED')
        return False

    try:
        target_tags = QualysTagProcessor.restructureTags(tags=source_tags)
    except:
        print('FATAL: QualysTagProcessor.restructureTags() FAILED')
        return False
    if target_tags is None:
        print('FATAL: QualysTagProcessor.restructureTags() FAILED')
        return False

    try:
        target_tags = QualysTagProcessor.handleSystemParents(target_api=target_api, tags=target_tags)
    except:
        print('FATAL: QualysTagProcessor.handleSystemParent() FAILED')
        return False
    if target_tags is None:
        print('FATAL: QualysTagProcessor.handleSystemParent() FAILED')
        return False

    if not simulate:
        try:
            return = QualysTagProcessor.createTags(api=target_api, tags=target_tags)
        except:
            print('FATAL: QualysTagProcessor.createTags() FAILED')
            return False
    else:
        print('================================================================================')
        print('TAG HIERARCHY')
        print('********************************************************************************')
        ET.dump(target_tags)
        print('================================================================================')
        return True
