import QualysAPI
import xml.etree.ElementTree as ET
# TODO Implement exceptions


def getTagSet(api: QualysAPI.QualysAPI, sr: ET.Element):
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
    print('QualysTagProcessor: Downloading Asset Tag data... ', end='')

    # Filter criteria must be provided in the following format
    # [
    #   [ "Criteria1 Field", "Criteria1 Operator", "Criteria1 Value"],
    #   [ "name", "EQUALS", "foobar"]
    # ]
    if filterlist is not None:
        if not isinstance(filterlist, list):
            print('Failed\ntagprocessor.py:getTags - Invalid filters parameter, must be list of lists ([[]])')
            return None
        elif (not isinstance(filterlist[0], list)) or len(filterlist) == 0:
            print('Failed\ntagprocessor.py:getTags - Invalid filter content or no filters specified')
            return None
        else:
            for f in filterlist:
                criteria = ET.SubElement(filters, 'Criteria')
                criteria.set('field', f[0])
                criteria.set('operator', f[1])
                criteria.text = f[2]

    prefs = ET.SubElement(sr, 'preferences')
    start = ET.SubElement(prefs, 'startFromOffset')
    start.text = str(offset)
    lim = ET.SubElement(prefs, 'limitResults')
    lim.text = str(limit)

    tags = ET.Element('data')
    while not atEnd:
        try:
            tagset = getTagSet(api=api, sr=sr)
        except:
            print('Failed\nFATAL: QualysTagProcessor.getTagSet() FAILED')
            return None

        for t in tagset.findall('.//Tag'):
            tags.append(t)
        if tagset.find('hasMoreRecords').text == 'true':
            offset = offset + limit
            start.text = str(offset)
        else:
            atEnd = True
        del tagset
    print('Success')
    return tags


def pruneSystemTags(tags: ET.Element):
    print('QualysTagProcessor: Pruning system-generated tags... ', end='')
    for n in ['Business Units', 'Asset Groups', 'Malware Domain Assets']:
        # Find named system tag
        t = tags.find('.//*[name="%s"]' % n)
        if t is None:
            print("Failed\nERROR: %s NOT FOUND" % n)
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
    print('Success')
    return tags


def restructureTags(tags: ET.Element):
    print('QualysTagProcessor: Restructuring Tags... ', end='')
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
    # So we convert the XML to a string to do the replacement
    xmlstr = ET.tostring(tags, method='xml', encoding='utf-8').decode()
    tmpstr = xmlstr.replace('<list>', '<set>')
    tagstr = tmpstr.replace('</list>', '</set>')
    # Then convert back to an XML object and return it
    tags = ET.fromstring(tagstr)
    print('Success')
    # Strip out all <created>, <modified>, <id> and <parentTagId> nodes
    for t in tags.findall('.//*Tag'):
        if t.find('id') is not None:
            t.remove(t.find('id'))
        if t.find('created') is not None:
            t.remove(t.find('created'))
        if t.find('modified') is not None:
            t.remove(t.find('modified'))
        if t.find('parentTagId') is not None:
            t.remove(t.find('parentTagId'))
    return tags


def handleSystemParents(target_api: QualysAPI.QualysAPI, tags: ET.Element):
    # Cloud Agent and Asset Search tags are a special case
    # The parent is system-generated however children are user-generated
    # For Cloud Agent tags we simply re-parent the children to the target's Cloud Agent tag
    # For Asset Search tags, the parent only exists in the target subscription when an Asset Search tag is created
    #   so we simply create a new parent tag (with a different name, so as to avoid errors later) and re-parent the
    #   children to it
    queryurl = "%s/qps/rest/2.0/search/am/tag" % target_api.server
    sr = ET.Element('ServiceRequest')
    filters = ET.SubElement(sr, 'filters')
    criteria = ET.SubElement(filters, 'Criteria')
    criteria.set('field', 'name')
    criteria.set('operator', 'EQUALS')
    criteria.text = 'Cloud Agent'
    payload = ET.tostring(sr, method='html', encoding='utf-8').decode()
    resp = target_api.makeCall(url=queryurl, payload=payload)
    if resp.find('.//id') is None:
        print('ERROR: Failed to get ID for Cloud Agent tag')
        return None
    tagID_cloudagent = resp.find('.//id').text

    # Handle Cloud Agent tags
    ca_tree = tags.find('.//Tag/[name="Cloud Agent"]')
    # If the Cloud Agent tag has children, we need to process them
    if ca_tree.find('children') is not None:
        ca_children = ca_tree.find('children')
        # Sometimes there is a children node but not a list node
        if ca_children.find('list') is not None:
            ca_list = ca_children.find('list')
            for ca_tag in ca_list.findall('./*Tag'):
                # First add the parentTagId node
                parent = ET.SubElement(ca_tag, 'parentTagId')
                parent.text = tagID_cloudagent
                # remove the tag from the child list
                ca_list.remove(ca_tag)
                # Then add it to the root
                tags.append(ca_tag)
    tags.remove(ca_tree)

    # Handle Asset Search tags
    asp_tag = ET.SubElement(tags, 'Tag')
    asp_tagname = ET.SubElement(asp_tag, 'name')
    asp_tagname.text = 'Imported Asset Search Tags'
    asp_children = ET.SubElement(asp_tag, 'children')
    asp_tagset = ET.SubElement(asp_children, 'set')

    as_tree = tags.find('.//Tag/[name="Asset Search Tags"]')
    # If the Asset Search tag has children, we need to process them
    if as_tree.find('children') is not None:
        as_children = as_tree.find('children')
        if as_children.find('set') is not None:
            as_list = as_children.find('set')
            for as_tag in as_list.findall('Tag'):
                # remove the tag from the child list
                as_list.remove(as_tag)
                # then add it to the new parent
                asp_tagset.append(as_tag)
    tags.remove(as_tree)
    return tags


def createTags(api: QualysAPI.QualysAPI, tags: ET.Element):
    print('QualysTagProcessor: Creating Tags... ', end='')
    print('Consuming %s API calls... ' % str(len(tags.findall('./Tag'))))
    # Wrap each root-level tag in a ServiceRequest
    counter = 1
    for tag in tags.findall('./Tag'):
        if tag.find('id') is not None:
            tag.remove(tag.find('id'))
        if tag.find('created') is not None:
            tag.remove(tag.find('created'))
        if tag.find('modified') is not None:
            tag.remove(tag.find('modified'))
        print('%s: ' % str(counter), end='')

        sr = ET.Element('ServiceRequest')
        data = ET.SubElement(sr, 'data')
        data.append(tag)
        xmlstr = ET.tostring(sr, method='html', encoding='utf-8').decode()
        print('%s... ' % tag.find('name').text, end='')
        fullurl = '%s/qps/rest/2.0/create/am/tag' % api.server
        resp = api.makeCall(url=fullurl, payload=xmlstr)
        respcode = resp.find('.//responseCode').text
        if not respcode == 'SUCCESS':
            print('ERROR')
            errdetails = resp.find('.//responseErrorDetails')
            print('================================================================================')
            ET.dump(errdetails)
            print('--------------------------------------------------------------------------------')
            ET.dump(sr)
            print('--------------------------------------------------------------------------------')
        else:
            print('Success')
        counter += 1
    return True
