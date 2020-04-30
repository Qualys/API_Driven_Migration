from datetime import datetime
import QualysAPI
import xml.etree.ElementTree as ET
import QualysSearchListProcessor


def testSearchLists(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI, simulate: bool = False):
    print('Getting Dynamic Search Lists')
    dynamicLists = QualysSearchListProcessor.getDynamicSearchLists(source_api=source_api)
    print('Getting Static Search Lists')
    staticLists = QualysSearchListProcessor.getStaticSearchLists(source_api=source_api)

    for slist in dynamicLists.findall('DYNAMIC_LIST'):
        resp = QualysSearchListProcessor.createDynamicSearchList(target_api=target_api, searchlist=slist, simulate=True)
        if resp is None:
            print('testSearchLists Failed')
            return False

    for slist in staticLists.findall('STATIC_LIST'):
        resp = QualysSearchListProcessor.createStaticSearchList(target_api=target_api, searchlist=slist, simulate=True)
        if resp is None:
            print('testSearchLists Failed')
            return False
    return True

