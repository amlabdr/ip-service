import json
import os, logging

class Config:
    def __init__(self):
        self.repeat_timer = os.environ.get('REPEAT_TIMER','10')
        self.controller_url = os.environ.get('CONTROLLER_URL','http://10.11.200.125:8787')
        self.network_targets_file_path = os.environ.get('NET_TARGETS', 'ipcollect-microservice/config/network_targets.dot')
        self.load_nodes()

    def load_nodes(self):
        with open(self.network_targets_file_path) as f:
            network_targets = f.read()
            self.network_targets = json.loads(network_targets)
            logging.info('reading network targets from file successful')
