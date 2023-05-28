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

def expand_range_string(input_string):
    if '..' in input_string:
        start, end = input_string.split('..')
        return [str(i) for i in range(int(start), int(end)+1)]
    else:
        return [input_string]

    #def list_is_flat(input_list):
    #    if not isinstance(input_list, list):
    #        return True
    #    for element in input_list:
    #        if isinstance(element, list):
    #            return False
    #    return True

def flatten_nested_list(input_list):
    result = []
    for element in input_list:
        if isinstance(element, list) :
            result.extend(flatten_nested_list(element))
        else:
            result.append(element)
    return result

# returns value from dictionary with nested keys and returns default value if key doesn't exist
def get_value(obj, keys, default_result=""):
   for key in keys:
       try:
           obj = obj[key]
       except KeyError:
           return default_result
   return obj
