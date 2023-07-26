import json
import os, logging

class Config:
    def __init__(self):
        self.controller_ip = os.environ.get('CONTROLLER','10.11.200.125')
        self.controller_rest_port = os.environ.get('CONTROLLER_REST_PORT','8787')
        self.controller_amqp_port = os.environ.get('CONTROLLER_AMQP_PORT','5672')
        self.controller_rest_username = os.environ.get('CONTROLLER_REST_USERNAME', 'admin')
        self.controller_rest_password = os.environ.get('CONTROLLER_REST_PASSWORD', 'admin')
        self.config_file_path = os.environ.get('CONFIG', 'config/config.json')
        self.network_targets = {}
        self.load_nodes()

    def load_nodes(self):
        with open(self.config_file_path, 'r') as f:
            config = json.load(f)
            self.controller_login_prefix = config.get("CONTROLLER_LOGIN_PREFIX")
            self.controller_qnet_subnet_prefix = config.get("CONTROLLER_QNET_SUBNET_PREFIX")
            self.controller_nodes_per_subnet_prefix = config.get("CONTROLLER_NODES_PER_SUBNET_PREFIX")
            self.amqp_configuration_events_topic = config.get("AMQP_CONFIGURATION_EVENTS_TOPIC")
            self.net_targets = config.get("NET_TARGETS")
            self.netconf_xml_templates = config.get("NETCONF_XML_TEMPLATES")
            self.controller_rest_port = config.get("CONTROLLER_REST_PORT")
        logging.info('reading network targets from file successful')

    def __str__(self):
        return f"""
        Config(
            Controller IP: {self.controller_ip},
            Controller REST Port: {self.controller_rest_port},
            Controller AMQP Port: {self.controller_amqp_port},
            Controller REST Username: {self.controller_rest_username},
            Controller REST Password: {self.controller_rest_password},
            Config File Path: {self.config_file_path},
            Network Targets: {self.network_targets},
            Controller Login Prefix: {self.controller_login_prefix},
            Controller Qnet Subnet Prefix: {self.controller_qnet_subnet_prefix},
            Controller Nodes Per Subnet Prefix: {self.controller_nodes_per_subnet_prefix},
            AMQP Configuration Events Topic: {self.amqp_configuration_events_topic},
            Net Targets: {self.net_targets},
            Netconf XML Templates: {self.netconf_xml_templates}
        )
        """

