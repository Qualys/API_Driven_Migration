# QualysTagProcessor module


### QualysTagProcessor.checkResponse(resp: Element)
Checks an API response for errors

Parameters:

    resp:           A document of type xml.etree.ElementTree.Element containing a full API response

Returns:

    True           If the XML does not contain an error
    False          If the XML contains an error


### QualysTagProcessor.createSingleTag(api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), tag: Element)
Creates a single tag from tag data

Parameters:

    api:        An object of class QualysAPI
    tag:        A document of type xml.etree.Element.ElementTree containing tag data for a single tag

Returns:

    resp:       A document of type xml.etree.Element.ElementTree containing the full API response


### QualysTagProcessor.createTags(api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), tags: Element)
Create tag hierarchies from downloaded, restructured, reparented, pruned and prepared tag data.  Makes a single API
call per top-level tag to include all child tags.

Parameters:

    api:        An object of class QualysAPI
    tags:       A document of type xml.etree.Element.ElementTree containing tag data

Returns:

    True


### QualysTagProcessor.getTagSet(api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), sr: Element)
Submits an API call to obtain a TagSet

Parameters:

    api:        An object of the class QualysAPI
    sr:         A document of type xml.etree.ElementTree.Element containing a valid ServiceRequest

Returns:

    resp:       If the response does not contain an error, returns a document of type xml.etree.ElementTree.Element

        containing the full API response

    None        If the response contains an error


### QualysTagProcessor.getTags(api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), filterlist: list | None = None)
Submits an API call to get all tags in a subscription, optionally filtered with a list of filter specifications

Parameters:

    api:            An object of the class QualysAPI
    filterlist:     An optional parameter specifying a list of filter criteria in the format

    > [

    >     [ “Criteria 1 Field”, “Criteria 1 Operator”, “Criteria 1 Value” ]
    >     [ “Criteria 2 Field”, “Criteria 2 Operator”, “Criteria 2 Value” ]

    > ]

Returns:

    tags:           A XML document of type xml.etree.ElementTree.Element containing the tag data


### QualysTagProcessor.handleSystemParents(target_api: [QualysAPI](QualysAPI.md#QualysAPI.QualysAPI), tags: Element)
Reparents user-created children of system-managed tags to allow removal of system-managed tags using
pruneSystemTags()

Parameters:

    target_api:     An object of type QualysAPI
    tags:           A document of type xml.etree.ElementTree.Element containing tag data

Returns:

    tags:           A document of type xml.etree.ElementTree.Element containing tag data with children of

        system-managed tags reparented to new tags


### QualysTagProcessor.prepareTags(tags: Element)
Prepare tag data for submission in a ServiceRequest as part of an API call to create tag hierarchy from
downloaded, restructured, reparented and pruned tag data.  Removes id, created and modified tag fields.

Parameters:

    tags:       A document of type xml.etree.Element.ElementTree containing tag data

Returns:

    tags:       A document of type xml.etree.Element.ElementTree containing tag data with id, created and modified

        elements removed


### QualysTagProcessor.pruneSystemTags(tags: Element)
Remove system-managed tags from downloaded tags list

Parameters:

    tags:           A document of type xml.etree.ElementTree.Elements containing downloaded tag data

Returns:

    tags:           A document of type xml.etree.ElementTree.Elements containing tag data with system-managed

        tags removed


### QualysTagProcessor.reparentTag(tags: Element, parentname: str)
Reparents all tags in a tag set to a new parent tag

Parameters:

    tags:       A document of type xml.etree.Element.ElementTree containing tag data
    parentname: The name of the new parent tag

Returns:

    newdata:  A document of type xml.etree.Element.ElementTree containing reparented tag data


### QualysTagProcessor.restructureTags(tags: Element)
Restructures downloaded tag data to move full tag data into parent/child tag structures.  A pre-requisite for
using downloaded tag data to recreate tag hierarchy and structure

Parameters:

    tags:       A document of type xml.etree.ElementTree.Element containing downloaded tag data

Returns:

    tags:       A document of type xml.etree.ElementTree.Element containing restructured tag data
