import json
from threading import Thread
import os
import time

from config.config import Config
from net.reader import Reader
from controller.controller import ControllerService

def run():

    config = Config()
    ctrl = ControllerService(config)
    
    # 1. get subnets
    subnets = json.loads(ctrl.get(url = ctrl.controller_rest_url+os.environ.get('CONTROLLER_QNET_SUBNET_PREFIX')))
    # 2. get target nodes by subnet_id
    for subnet in subnets:
        if subnet['name'] == 'dc-qnet':
            nodes_url = ctrl.controller_rest_url + os.environ.get('CONTROLLER_NODES_PER_SUBNET_PREFIX')
            nodes_url = nodes_url.replace('ID', str(subnet['id']))
            nodes = json.loads(ctrl.get(url=nodes_url))
            for node in nodes:
                if node['type'] == 'ROUTER':
                    config.network_targets.append(node)
    print(config.network_targets)
    # 3. start periodic reader thread
    reader = Reader() 
    periodic_collection_thread = Thread(target=reader.read, args=(config, ctrl, os.environ.get('COLLECTION_REPEAT_TIMER')))
    periodic_collection_thread.start()
    time.sleep(1)

    
    ctrl.subcribe_to_topology_events(topic = 'topic://topology.event',
                                     config = config,
                                     network_reader = reader)
    print("Done")
    
if __name__ == '__main__':
    run()


