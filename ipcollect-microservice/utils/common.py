import xmltodict
import xml.etree.ElementTree as ET


def xml_preprocessing(xml_string):
    tree_root = ET.fromstring(xml_string)
    remove_xml_attributes(tree_root)
    root_dict = xmltodict.parse(ET.tostring(tree_root))
    root_dict = root_dict['ns0:rpc-reply']['data']
    return root_dict

def remove_xml_attributes(elem):
    for child in elem:
        remove_xml_attributes(child)
        child.attrib.clear()
        child.tag = child.tag.split('}')[-1]

def get_value(obj, keys, default_result=""):
   for key in keys:
       try:
           obj = obj[key]
       except KeyError:
           return default_result
   return obj
