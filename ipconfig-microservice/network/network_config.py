import os, logging, traceback, re, json, copy
from ncclient import manager
from ncclient.operations import RPCError

class Network_config:
    def __init__(self,config):
        self.action_translator={"CREATED":"create", "DELETING":"delete", "UPDATED":"replace"}
        self.netconf_xml_templates = config.netconf_xml_templates
        self.status_msgs = {"default":{"success":"UP","fail":"DOWN"},
                            "SVI":{"success":"UP","fail":"DELETED"},
                            "INTERFACE":{"success":"UP","fail":"DELETED"}
                            }
    
    def fill_xml_template(self,template_file, configuration):
        # Read the XML template from the file
        with open(template_file, "r") as f:
            xml_template = f.read()
        
        action = self.action_translator[configuration["action"]]
        xml_template = re.sub("{operation}",action , xml_template)
        for param, value in configuration["content"].items():
            if type(value)==list:
                pattern = r'\{(.*)\{'+param+r'\}(.*)\}'
                # Find the trunk-vlans field in the XML input using regex
                #match = re.search(pattern, xml_template)
                matches = []

                for match in re.finditer(pattern, xml_template):
                    matches.append(match.group())
                print(matches)
                for match in matches:
                    new_content = ''
                    for element in value:
                        new_content += re.sub(f"{{{param}}}", str(element), match[1:-1])
                    # Replace the old trunk-vlans field with the updated one
                    xml_template = re.sub(match, new_content, xml_template)
            else:
                xml_template = re.sub(f"{{{param}}}", str(value), xml_template)
        return xml_template

    def fill_xml_config(self,config):
        # Read the XML template from the file
        with open(self.netconf_xml_templates+"/config.xml", "r") as f:
            xml_template = f.read()
        xml_template = re.sub("{configuration}", config, xml_template)
        print(xml_template)
        return xml_template

    
    def get_template_file(self, configuration):
        if configuration["resource"] == "VLAN_MEMBER":
            if configuration["content"]["mode"] == "Access":
                template_file = self.netconf_xml_templates+"/VLAN_MEMBER_Access.xml"
            elif configuration["content"]["mode"] == "Trunk":
                template_file = self.netconf_xml_templates+"/VLAN_MEMBER_Trunk.xml"
            elif configuration["content"]["mode"] == "None":
                template_file = self.netconf_xml_templates+"/VLAN_MEMBER_None.xml"
            else: pass
        else:
            template_file = self.netconf_xml_templates+"/"+configuration["resource"]+".xml"
        return template_file
    def get_config_list(self, configuration):
        config_list = []
        if (configuration["resource"] == "INTERFACE" or configuration["resource"] == "SVI" or configuration["resource"] == "IP_ROUTER" ) and configuration["action"] == "UPDATED":
            configuration["action"] = "DELETING"
            print(configuration)
            config_list.append(copy.deepcopy(configuration))
            configuration["action"] = "CREATED"
            config_list.append(copy.deepcopy(configuration))
        else:
            config_list.append(configuration)
        return config_list

    def config_network(self, event, backup = False):
        device = event["content"]["host"]
        configuration=event
        try:
            # Connect to the netconf server
            netconfClient = manager.connect(
                host= device,
                port=os.environ.get("NETCONF_PORT"),
                username = os.environ.get("NETCONF_USER"),
                password = os.environ.get("NETCONF_PASSWORD"),
                hostkey_verify=False,)
            del configuration["content"]["host"]
            config_list = self.get_config_list(configuration)
            print(config_list)
            for configuration in config_list:
                xml_obj = ""
                template_file = self.get_template_file(configuration)
                xml_obj += self.fill_xml_template(template_file, configuration)
                xml_configuration=self.fill_xml_config(xml_obj)
                try:
                    reply = netconfClient.edit_config(target="candidate", config=xml_configuration)
                    print(reply)
                except Exception as e:
                    print(traceback.format_exc())
                    print(e)
                    logging.error(f"Error editing configuration: {e}")
                    if configuration["resource"] in self.status_msgs:
                        return self.status_msgs[configuration["resource"]]["fail"]
                    else:
                        return self.status_msgs["default"]["fail"]
                    

                # Commit the changes and save them to the running configuration
                try:
                    netconfClient.commit()
                    
                except RPCError as e:
                    logging.error(f"Error committing and saving changes: {e}")
                    netconfClient.discard_changes()
                    if configuration["resource"] in self.status_msgs:
                        return self.status_msgs[configuration["resource"]]["fail"]
                    else:
                        return self.status_msgs["default"]["fail"]
        except Exception as e:
            logging.error(f"Error: {e}")
        if configuration["action"]=="DELETING":
            return "DELETED"
        else:
            return self.status_msgs["default"]["success"]