import json
import os, logging

class Config:
    def __init__(self):
        self.repeat_timer = os.environ.get('COLLECTION_REPEAT_TIMER','60')
        self.controller_ip = os.environ.get('CONTROLLER_IP','10.11.200.125')
        self.controller_rest_port = os.environ.get('CONTROLLER_REST_PORT','8787')
        self.controller_amqp_port = os.environ.get('CONTROLLER_AMQP_PORT','5672')
        self.controller_rest_username = os.environ.get('CONTROLLER_REST_USERNAME', 'admin')
        self.controller_rest_password = os.environ.get('CONTROLLER_REST_PASSWORD', 'admin')
        
        self.network_targets_file_path = os.environ.get('NET_TARGETS', 'config/network_targets.dot')
        self.load_nodes()

    def load_nodes(self):
        with open(self.network_targets_file_path) as f:
            network_targets = f.read()
            self.network_targets = json.loads(network_targets)
            logging.info('reading network targets from file successful')
