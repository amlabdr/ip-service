import xmltodict
import xml.etree.ElementTree as ET
import json
from ncclient import manager

from utils.common import remove_xml_attributes
from config.config import Config
from net.reader import Reader
from net.readers.interface_reader import InterfaceReader
from net.readers.lldp_reader import LldpReader
from net.readers.metadata_reader import MetadataReader
from net.readers.vlan_reader import VlanReader

def run():
    config = Config()
    xml_template_dict = {
        'metadata':'net/xml_templates/get_system.xml',
        'interfaces':'net/xml_templates/get_interfaces.xml',
        'lldp':'net/xml_templates/get_lldp.xml',
        'vlan':'net/xml_templates/get_vlan.xml',
    }
    
    reader_dict = {
        'metadata': MetadataReader,
        'interfaces': InterfaceReader,
        'lldp': LldpReader,
        'vlan': VlanReader,
    }
    
    # target host info 
    auth = {
        "host":"10.11.200.13",
        "port":"830",
        "username":"ocnos",
        "password":"ocnos",
    }
    
    result = {}
    reader = Reader(config) 
    for cmd in xml_template_dict:
        with manager.connect_ssh(host=auth["host"],port = auth["port"],username = auth["username"],password = auth["password"],hostkey_verify= False) as m:
            template_file = open(xml_template_dict[cmd])
            template = template_file.read()
            config = m.get(filter=('subtree', template)).xml
            root = ET.fromstring(config)
            remove_xml_attributes(root)
            root_dict = xmltodict.parse(ET.tostring(root))
            root_dict = root_dict['ns0:rpc-reply']['data']
            if cmd == 'interfaces':
                reader = InterfaceReader(root_dict)
            elif cmd =='vlan':
                reader = VlanReader(root_dict)
            elif cmd == 'lldp':
                reader = LldpReader(root_dict)
            elif cmd == 'metadata':
                template_file = open(xml_template_dict['interfaces'])
                template = template_file.read()
                config = m.get(filter=('subtree', template)).xml
                iface_root = ET.fromstring(config)
                remove_xml_attributes(iface_root)
                iface_dict = xmltodict.parse(ET.tostring(iface_root))
                iface_dict = iface_dict['ns0:rpc-reply']['data']
                reader = MetadataReader(root_dict, iface_dict)
            reader.read()
            result[cmd] = reader.result
    
    json_data = json.dumps(result,indent=2)
    with open("/tmp/result.json", 'w') as json_file:
        json_file.write(json_data)
        json_file.close()
    print("Done")

if __name__ == '__main__':
    run()


