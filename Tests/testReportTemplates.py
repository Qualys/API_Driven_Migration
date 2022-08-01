import xml.etree.ElementTree as ET
from API_Driven_Migration.QualysVM import QualysReportTemplateProcessor
from API_Driven_Migration.QualysCommon import QualysAPI


def testReportTemplates(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    templateslist = QualysReportTemplateProcessor.getReportTemplates(source_api=source_api)

    if simulate:
        scantemplates = ET.tostring(templateslist[0], method='html', encoding='utf-8').decode()
        pcitemplates = ET.tostring(templateslist[1], method='html', encoding='utf-8').decode()
        patchtemplates = ET.tostring(templateslist[2], method='html', encoding='utf-8').decode()
        maptemplates = ET.tostring(templateslist[3], method='html', encoding='utf-8').decode()

        print('================================================================================')
        print('REPORT TEMPLATES')
        print('********************************************************************************')
        print('%s' % scantemplates)
        print('--------------------------------------------------------------------------------')
        print('%s' % pcitemplates)
        print('--------------------------------------------------------------------------------')
        print('%s' % patchtemplates)
        print('--------------------------------------------------------------------------------')
        print('%s' % maptemplates)
        print('================================================================================')
        return True
    else:
        return QualysReportTemplateProcessor.createReportTemplates(target_api=target_api, templates=templateslist)
