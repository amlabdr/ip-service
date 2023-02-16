import os, logging, traceback, re, copy
from ncclient import manager
from ncclient.operations import RPCError

class Network_config:
    def __init__(self):
        self.topology = {}
        self.operation_translator={"CREATE":"create", "DELETE":"delete", "UPDATE":"replace", "MERGE":"merge"}
        self.netconf_xml_templates = os.environ.get('NETCONF_XML_TEMPLATES', 'ipconfig-microservice/network/ocnos_service/xml_templates/')
    
    def fill_xml_template(self,template_file, configuration):
        # Read the XML template from the file
        with open(template_file, "r") as f:
            xml_template = f.read()
        
        operation = self.operation_translator[configuration["operation"]]
        xml_template = re.sub("{operation}",operation , xml_template)
        for param, value in configuration["content"].items():
            xml_template = re.sub(f"{{{param}}}", str(value), xml_template)
        return xml_template

    def fill_xml_config(self,config):
        # Read the XML template from the file
        with open(self.netconf_xml_templates+"config.xml", "r") as f:
            xml_template = f.read()
        xml_template = re.sub("{configuration}", config, xml_template)
        return xml_template

    def get_topology(self,config):
        #get type of devices
        for node in config.network_targets.get_nodes():
            self.topology[node.get_name().replace('"','')] = node.obj_dict["attributes"]

    def config_network(self, network_config, backup = False):
        device = network_config["content"]["host"]
        if (network_config["content"]["host"] in self.topology ):
            try:
                # Connect to the netconf server
                netconfClient = manager.connect(
                    host=self.topology[device]['mgmt_ip'].replace('"',''),
                    port=830,
                    username=self.topology[device]['username'].replace('"',''),
                    password=self.topology[device]['password'].replace('"',''),
                    hostkey_verify=False,)
                configuration=copy.deepcopy(network_config)
                del configuration["content"]["host"]
                xml_obj = ""
                template_file = self.netconf_xml_templates+configuration["resource"]+"/"+configuration["resource"]+".xml"
                xml_obj += self.fill_xml_template(template_file, configuration)
                xml_configuration=self.fill_xml_config(xml_obj)
                try:
                    reply = netconfClient.edit_config(target="candidate", config=xml_configuration)
                    print(reply)
                except Exception as e:
                    print(traceback.format_exc())
                    print(e)
                    logging.error(f"Error editing configuration: {e}")

                # Commit the changes and save them to the running configuration
                try:
                    netconfClient.commit()
                    
                except RPCError as e:
                    logging.error(f"Error committing and saving changes: {e}")
                    netconfClient.discard_changes()
            except Exception as e:
                logging.error(f"Error: {e}")