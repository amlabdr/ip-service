import os, logging
import pydot

class Config:
    def __init__(self):
        self.repeat_timer = os.environ.get('REPEAT_TIMER','10')
        self.controller_url = os.environ.get('CONTROLLER_URL','http://10.11.200.125:8787')
        self.network_targets_file_path = os.environ.get('NET_TARGETS', 'ipconfig-microservice/config/network_targets.dot')
        self.network_targets = self.read_network_targets()


    def read_network_targets(self):
        '''reads the network topology file and loads it to memory as a dictionary using pydot'''
        try:
            print(self.network_targets_file_path)
            graph = pydot.graph_from_dot_file(self.network_targets_file_path)
            return graph[0]
        except IOError:
            logging.error("*********** ERROR reading network targets file **********")
            exit(1)
