import QualysAPI
import xml.etree.ElementTree as ET
# TODO Implement exceptions


def getTagSet(api: QualysAPI.QualysAPI, sr: ET.Element, offset, count):
    fullurl = '%s/qps/rest/2.0/search/am/tag' % api.server
    payload = ET.tostring(sr, method='html', encoding='utf-8').decode()

    resp = api.makeCall(url=fullurl, payload=payload)
    return resp


def getTags(api: QualysAPI.QualysAPI, filterlist=None):
    tags: ET.Element
    offset = 1
    limit = 100
    atEnd = False

    sr = ET.Element('ServiceRequest')
    filters = ET.SubElement(sr, 'filters')

    # Filter criteria must be provided in the following format
    # [
    #   [ "Criteria1 Field", "Criteria1 Operator", "Criteria1 Value"],
    #   [ "name", "EQUALS", "foobar"]
    # ]
    if filterlist is not None:
        if not isinstance(filterlist, list):
            print('tagprocessor.py:getTags - Invalid filters parameter, must be list of lists ([[]])')
            return None
        elif (not isinstance(filterlist[0], list)) or len(filterlist) == 0:
            print('tagprocessor.py:getTags - Invalid filter content or no filters specified')
            return None
        else:
            for f in filterlist:
                criteria = ET.SubElement(filters, 'Criteria')
                criteria.set('field', f[0])
                criteria.set('operator', f[1])
                criteria.text = f[2]

    prefs = ET.SubElement(sr, 'preferences')
    start = ET.SubElement(prefs, 'startFromOffset')
    start.text = offset
    lim = ET.SubElement(prefs, 'limitResults')
    lim.text = limit

    tags = ET.Element('data')
    while not atEnd:
        tagset = getTagSet(api=api, sr=sr, offset=offset, count=limit)
        for t in tagset.findall('.//Tag'):
            tags.append(t)
        if tagset.find('hasMoreRecords').text == 'true':
            offset = offset + limit
        else:
            atEnd = True
        del tagset
    return tags


def pruneSystemTags(tags: ET.Element):
    # Step 1 : Prune system tags
    #               For each system tag, get child IDs and delete corresponding Tag element
    #               Remove system tag
    # Step 2 : Rebuild tag hierarchy with full tag structure
    #              For each TagSimple, (find Tag with same ID, move Tag to replace TagSimple)

    # Step 1 : Prune system tags
    for n in ['Business Units', 'Asset Groups', 'Malware Domain Assets']:
        # Find named system tag
        t = tags.find('.//*[name="%s"]' % n)
        if t is None:
            print("ERROR: %s NOT FOUND" % n)
            return None
        # For each simple tag within the system tag
        for ts in t.findall('.//*TagSimple'):
            # get the ID
            tagid = ts.find('id').text
            # find the full tag with that ID
            fulltag = tags.find('.//Tag/[id="%s"]' % tagid)
            # get that tag's parent
            parent = tags.find('.//Tag/[id="%s"]/..' % tagid)
            # remove that tag from its parent
            parent.remove(fulltag)
        # Finally remove the system tag
        tags.remove(t)


def restructureTags(tags: ET.Element):
    # Step 2 : Restructure
    # For each list node
    for listnode in tags.findall('.//*list'):
        # For each TagSimple node within each list node
        for tagsimple in listnode.findall('TagSimple'):
            # get the ID of the node
            tagid = tagsimple.find('id').text
            # get the full tag with that ID
            fulltag = tags.find('.//Tag/[id="%s"]' % tagid)
            # get the parent of that full tag
            parent = tags.find('.//Tag/[id="%s"]/..' % tagid)
            # remove the full tag from its parent
            parent.remove(fulltag)
            # append the full tag to the list node
            listnode.append(fulltag)
            # remove the TagSimple node from the list node
            listnode.remove(tagsimple)
    # The output has child tags in a <list> node, whereas the input requires a <set> node
    # So we convert the XML to a string to do the replacement and return the string
    xmlstr = ET.tostring(method='xml', encoding='utf-8').decode()
    tagstr = xmlstr.replace('<list>', '<set>')
    return tagstr


def createTags(api: QualysAPI.QualysAPI, tags: str):
    fullurl = '%s/qps/rest/2.0/create/am/tag' % api.server
    resp = api.makeCall(url=fullurl, payload=str)
    return resp