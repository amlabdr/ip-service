
def remove_xml_attributes(elem):
    for child in elem:
        remove_xml_attributes(child)
        child.attrib.clear()
        child.tag = child.tag.split('}')[-1]
