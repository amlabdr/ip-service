import xml.etree.ElementTree as ET
import ncclient
from ncclient import manager
import os

from net.readers.interface_reader import InterfaceReader
from net.readers.lldp_reader import LldpReader
from net.readers.metadata_reader import MetadataReader
from net.readers.vlan_reader import VlanReader
from utils.common import xml_preprocessing

class Reader:
    def __init__(self):
        self.nodes = {}
        self.result = {}
        self.xml_template_dict = {
            'metadata':'net/xml_templates/get_system.xml',
            'interfaces':'net/xml_templates/get_interfaces.xml',
            'lldp':'net/xml_templates/get_lldp.xml',
            'vlan':'net/xml_templates/get_vlan.xml',
        }
    
    def __str__(self) -> str:
        return f'Reader = {vars(self)}'

    def load_nodes(self, config):
        for node in config.network_targets:
            self.nodes[node['name']] = node

    def load_xml_template(self, template_path):
        with open(template_path) as template_file:
            xml_template_content = template_file.read()
        return xml_template_content
    
    def read_result_file(self, file_path):
        with open(file_path) as result_file:
            xml_result_content = result_file.read()
        return xml_result_content
    
    def read(self, config, ctrl):
        self.load_nodes(config)
        for node_name, node_content in self.nodes.items():
            self.result[node_name] = {}
            self.result[node_name]['metadata'] = self.read_metadata(node_content)
            self.result[node_name]['interfaces'] = self.read_interfaces(node_content)
            self.result[node_name]['lldp'] = self.read_lldp(node_content)
            self.result[node_name]['vlan'] = self.read_vlan(node_content)
        ctrl.publish_collected_topology(topic = os.environ.get('AMQP_TOPOLOGY_COLLECTION_TOPIC'), message = self.result)
           
    def read_metadata(self, node):
        #since lldp only identifies neighbors by their MAC address, we need to retreive the MAC address of the device first
        #the MAC address of the device if the MAC address of its management interface which is provided using the interface template
        connection_manager = self.connect_to_netconf_server(node)
        interface_template = self.load_xml_template(self.xml_template_dict['interfaces'])
        xml_result = connection_manager.get(filter=('subtree', interface_template)).xml
        interface_dict = xml_preprocessing(xml_result)

        #now we can get the metadata and the MetadataReader will add the MAC address to the metadata result
        metadata_template = self.load_xml_template(self.xml_template_dict['metadata'])
        xml_result = connection_manager.get(filter=('subtree', metadata_template)).xml
        metadata_dict = xml_preprocessing(xml_result)

        reader = MetadataReader(metadata_dict, interface_dict)
        reader.read()
        connection_manager.close_session()

        return reader.result

    def read_interfaces(self, node):
        connection_manager = self.connect_to_netconf_server(node)
        interface_template = self.load_xml_template(self.xml_template_dict['interfaces'])
        xml_result = connection_manager.get(filter=('subtree', interface_template)).xml
        interface_dict = xml_preprocessing(xml_result)
        reader = InterfaceReader(interface_dict)
        reader.read()
        connection_manager.close_session()
        return reader.result

    def read_lldp(self, node):
        connection_manager = self.connect_to_netconf_server(node)
        lldp_template = self.load_xml_template(self.xml_template_dict['lldp'])
        xml_result = connection_manager.get(filter=('subtree', lldp_template)).xml
        lldp_dict = xml_preprocessing(xml_result)
        reader = LldpReader(lldp_dict)
        reader.read()
        connection_manager.close_session()
        return reader.result

    def read_vlan(self, node):
        connection_manager = self.connect_to_netconf_server(node)
        vlan_template = self.load_xml_template(self.xml_template_dict['vlan'])
        xml_result = connection_manager.get(filter=('subtree', vlan_template)).xml
        vlan_dict = xml_preprocessing(xml_result)
        reader = VlanReader(vlan_dict)
        reader.read()
        connection_manager.close_session()
        return reader.result

    def connect_to_netconf_server(self, node):
        try:
            return manager.connect_ssh(host = node['mgmtIP'],
                                port = 830,
                                username = node['username'],
                                password = node['password'],
                                hostkey_verify = False)
        except ncclient.NCClientError:
            return 


