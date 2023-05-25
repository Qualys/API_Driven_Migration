from QualysCommon import QualysAPI
import xml.etree.ElementTree as ET


def checkResponse(resp: ET.Element):
    """
    Checks an API response for errors

    Parameters:
        resp:           A document of type xml.etree.ElementTree.Element containing a full API response

    Returns:
        True           If the XML does not contain an error
        False          If the XML contains an error
    """
    if resp.tag is None:
        # We don't have a ServiceResponse element, so this isn't a valid response
        print('\n\nAPI ERROR: Invalid XML returned')
        return False
    if resp.tag != 'ServiceResponse':
        print('\n\nAPI ERROR: Not a valid ServiceResponse')
        return False
    if resp.find('responseCode') is None:
        print('\n\nAPI ERROR: No responseCode element found')
        return False
    if resp.find('responseCode').text == 'SUCCESS':
        return True

    # We get a valid responseCode, but it does not indicate success.  We output the reason and the contents
    # of the responseErrorDetails
    print('\n\nAPI ERROR: %s' % resp.find('responseCode').text)
    print('Error Message : %s' % resp.find('responseErrorDetails/errorMessage').text)
    if resp.find('responseErrorDetails/errorResolution') is not None:
        print('Suggested Resolution : %s' % resp.find('responseErrorDetails/errorResolution').text)
    return False


def getTagSet(api: QualysAPI.QualysAPI, sr: ET.Element):
    """
    Submits an API call to obtain a TagSet

    Parameters:
        api:        An object of the class QualysAPI
        sr:         A document of type xml.etree.ElementTree.Element containing a valid ServiceRequest

    Returns:
        resp:       If the response does not contain an error, returns a document of type xml.etree.ElementTree.Element
                    containing the full API response
        None        If the response contains an error
    """
    fullurl = '%s/qps/rest/2.0/search/am/tag' % api.server
    payload = ET.tostring(sr, method='html', encoding='utf-8').decode()

    resp = api.makeCall(url=fullurl, payload=payload)
    if not checkResponse(resp):
        return None
    return resp


def getTags(api: QualysAPI.QualysAPI, filterlist: list = None):
    """
    Submits an API call to get all tags in a subscription, optionally filtered with a list of filter specifications

    Parameters:
        api:            An object of the class QualysAPI
        filterlist:     An optional parameter specifying a list of filter criteria in the format
                        [
                            [ "Criteria 1 Field", "Criteria 1 Operator", "Criteria 1 Value" ]
                            [ "Criteria 2 Field", "Criteria 2 Operator", "Criteria 2 Value" ]
                        ]

    Returns:
        tags:           A XML document of type xml.etree.ElementTree.Element containing the tag data
    """
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

        if tagset is None:
            # We had an error, so return None to be safe
            return None

        for t in tagset.findall('.//Tag'):
            tags.append(t)
        if tagset.find('hasMoreRecords') is not None:
            if tagset.find('hasMoreRecords').text == 'true':
                offset = offset + limit
                start.text = str(offset)
            else:
                atEnd = True
            del tagset
    print('Success')
    return tags


def pruneSystemTags(tags: ET.Element):
    """
    Remove system-managed tags from downloaded tags list

    Parameters:
        tags:           A document of type xml.etree.ElementTree.Elements containing downloaded tag data

    Returns:
        tags:           A document of type xml.etree.ElementTree.Elements containing tag data with system-managed
                        tags removed
    """
    print('QualysTagProcessor: Pruning system-generated tags... ', end='')
    for n in ['Business Units', 'Asset Groups']:
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
    t = tags.find('.//*[name="Malware Domain Assets"]')
    if t is None:
        print("INFO: Malware Domain Assets not found")
    else:
        for ts in t.findall('.//*TagSimple'):
            # get the ID
            tagid = ts.find('id').text
            # find the full tag with that ID
            fulltag = tags.find('.//Tag/[id="%s"]' % tagid)
            # get that tag's parent
            parent = tags.find('.//Tag/[id="%s"]/..' % tagid)
            # remove that tag from its parent
            parent.remove(fulltag)
    print('Success')
    return tags


def restructureTags(tags: ET.Element):
    """
    Restructures downloaded tag data to move full tag data into parent/child tag structures.  A pre-requisite for
    using downloaded tag data to recreate tag hierarchy and structure

    Parameters:
        tags:       A document of type xml.etree.ElementTree.Element containing downloaded tag data

    Returns:
        tags:       A document of type xml.etree.ElementTree.Element containing restructured tag data
    """
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
    """
    Reparents user-created children of system-managed tags to allow removal of system-managed tags using
    pruneSystemTags()

    Parameters:
        target_api:     An object of type QualysAPI
        tags:           A document of type xml.etree.ElementTree.Element containing tag data

    Returns:
        tags:           A document of type xml.etree.ElementTree.Element containing tag data with children of
                        system-managed tags reparented to new tags
    """
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


def prepareTags(tags: ET.Element):
    """
    Prepare tag data for submission in a ServiceRequest as part of an API call to create tag hierarchy from
    downloaded, restructured, reparented and pruned tag data.  Removes id, created and modified tag fields.

    Parameters:
        tags:       A document of type xml.etree.Element.ElementTree containing tag data

    Returns:
        tags:       A document of type xml.etree.Element.ElementTree containing tag data with id, created and modified
                    elements removed
    """
    for tag in tags.findall('.//Tag'):
        if tag.find('id') is not None:
            tag.remove(tag.find('id'))
        if tag.find('created') is not None:
            tag.remove(tag.find('created'))
        if tag.find('modified') is not None:
            tag.remove(tag.find('modified'))

    return tags


def createTags(api: QualysAPI.QualysAPI, tags: ET.Element):
    """
    Create tag hierarchies from downloaded, restructured, reparented, pruned and prepared tag data.  Makes a single API
    call per top-level tag to include all child tags.

    Parameters:
        api:        An object of class QualysAPI
        tags:       A document of type xml.etree.Element.ElementTree containing tag data

    Returns:
        True
    """
    print('QualysTagProcessor: Creating Tags... ', end='')
    print('Consuming %s API calls... ' % str(len(tags.findall('./Tag'))))

    # Remove all IDs and created/modified dates from tags
    for tag in tags.findall('.//Tag'):
        if tag.find('id') is not None:
            tag.remove(tag.find('id'))
        if tag.find('created') is not None:
            tag.remove(tag.find('created'))
        if tag.find('modified') is not None:
            tag.remove(tag.find('modified'))

    # Wrap each root-level tag in a ServiceRequest
    for tag in tags.findall('./Tag'):
        sr = ET.Element('ServiceRequest')
        data = ET.SubElement(sr, 'data')
        data.append(tag)
        xmlstr = ET.tostring(sr, method='xml', encoding='utf-8').decode()
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
    return True


def createSingleTag(api: QualysAPI.QualysAPI, tag: ET.Element):
    """
    Creates a single tag from tag data

    Parameters:
        api:        An object of class QualysAPI
        tag:        A document of type xml.etree.Element.ElementTree containing tag data for a single tag

    Returns:
        resp:       A document of type xml.etree.Element.ElementTree containing the full API response
    """
    sr = ET.Element('ServiceRequest')
    srdata = ET.SubElement(sr, 'data')
    srdata.append(tag)
    xmlstr = ET.tostring(sr, method='xml', encoding='utf-8').decode()
    print('Creating Tag %s' % sr.find('.//name').text)
    fullurl = '%s/qps/rest/2.0/create/am/tag' % api.server
    resp = api.makeCall(url=fullurl, payload=xmlstr)
    if not checkResponse(resp):
        print('ERROR: QualysTagProcessor.createSingleTag : Could not create Tag')
        return None
    return resp


def reparentTag(tags: ET.Element, parentname: str):
    """
    Reparents all tags in a tag set to a new parent tag

    Parameters:
        tags:       A document of type xml.etree.Element.ElementTree containing tag data
        parentname: The name of the new parent tag

    Returns:
          newdata:  A document of type xml.etree.Element.ElementTree containing reparented tag data

    """
    print('QualysTagProcessor: Reparenting Tags...', end='')
    newdata = ET.Element('data')
    newparent = ET.SubElement(newdata, 'Tag')
    newparentname = ET.SubElement(newparent, 'name')
    newparentname.text = parentname
    children = ET.SubElement(newparent, 'children')
    childset = ET.SubElement(children, 'set')

    for tag in tags.findall('./Tag'):
        childset.append(tag)

    return newdata
