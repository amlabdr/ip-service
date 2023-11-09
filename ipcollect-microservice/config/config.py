import json
import os, logging

class Config:
    def __init__(self):
        self.controller_ip = os.environ.get('CONTROLLER','10.11.200.125')
        self.amqp_broker = os.environ.get('AMQP_BROKER','10.11.200.125')
        self.controller_auth_port = os.environ.get('CONTROLLER_AUTH_PORT','8888')
        self.controller_rest_port = os.environ.get('CONTROLLER_REST_PORT','8787')
        self.controller_amqp_port = os.environ.get('CONTROLLER_AMQP_PORT','5672')
        self.controller_rest_username = os.environ.get('CONTROLLER_REST_USERNAME', 'ip')
        self.controller_rest_password = os.environ.get('CONTROLLER_REST_PASSWORD', 'ip123$')
        self.config_file_path = os.environ.get('CONFIG', 'config/config.json')
        self.network_targets = {}
        self.netconf_port = os.environ.get('NETCONF_PORT','830')
        self.load_nodes()

    def load_nodes(self):
        with open(self.config_file_path, 'r') as f:
            config = json.load(f)
            self.repeat_timer = config.get('COLLECTION_REPEAT_TIMER')
            self.controller_login_prefix = config.get("CONTROLLER_LOGIN_PREFIX")
            self.controller_qnet_subnet_prefix = config.get("CONTROLLER_QNET_SUBNET_PREFIX")
            self.controller_nodes_per_subnet_prefix = config.get("CONTROLLER_NODES_PER_SUBNET_PREFIX")
            self.amqp_topology_collection_topic = config.get("AMQP_TOPOLOGY_COLLECTION_TOPIC")
            self.amqp_configuration_events_topic = config.get("AMQP_CONFIGURATION_EVENTS_TOPIC")
            self.amqp_topology_interface_status_topic = config.get("AMQP_TOPOLOGY_INTERFACE_STATUS_TOPIC")
            self.collection_repeat_timer = config.get("COLLECTION_REPEAT_TIMER")
            self.netconf_xml_templates = config.get("NETCONF_XML_TEMPLATES")
            self.controller_rest_port = config.get("CONTROLLER_REST_PORT")
        logging.info('reading network targets from file successful')

    def __str__(self):
        return f"""
        Config(
            Repeat Timer: {self.repeat_timer},
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
            AMQP Topology Collection Topic: {self.amqp_topology_collection_topic},
            AMQP Configuration Events Topic: {self.amqp_configuration_events_topic},
            AMQP Topology Interface Status Topic: {self.amqp_topology_interface_status_topic},
            Collection Repeat Timer: {self.collection_repeat_timer},
            Netconf XML Templates: {self.netconf_xml_templates}
        )
        """

