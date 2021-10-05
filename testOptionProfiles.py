import xml.etree.ElementTree as ET
import QualysOptionProfileProcessor
import QualysAPI


def testOptionProfiles(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    optionprofiles = QualysOptionProfileProcessor.exportOptionProfiles(source_api=source_api)
    if optionprofiles is None:
        return False

    if simulate:
        print('================================================================================')
        print('OPTION PROFILES')
        print('********************************************************************************')
        xmlstr = ET.tostring(optionprofiles, method='html', encoding='utf-8').decode()
        print('%s' % xmlstr)
        print('================================================================================')
        return True
    else:
        return QualysOptionProfileProcessor.importOptionProfiles(target_api=target_api, optionprofiles=optionprofiles)
