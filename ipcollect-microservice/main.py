import json
from threading import Thread
import os
import time

from config.config import Config
from net.reader import Reader
from controller.controller import ControllerService

def run():

    config = Config()
    reader = Reader(config) 
    ctrl = ControllerService(config, reader)
    
    # get subnets
    subnets = json.loads(ctrl.get(url = ctrl.controller_rest_url+os.environ.get('CONTROLLER_QNET_SUBNET_PREFIX')))
    # get target nodes by subnet_id
    for subnet in subnets:
        if subnet['name'] == 'dc-qnet':
            nodes_url = ctrl.controller_rest_url + os.environ.get('CONTROLLER_NODES_PER_SUBNET_PREFIX')
            nodes_url = nodes_url.replace('ID', str(subnet['id']))
            nodes = json.loads(ctrl.get(url=nodes_url))
            for node in nodes:
                if node['type'] == 'ROUTER':
                    ctrl.config.network_targets[node['id']] = node 
    print(ctrl.config.network_targets)
    # start periodic reader thread
    periodic_collection_thread = Thread(target=ctrl.reader.read, args=(ctrl, os.environ.get('COLLECTION_REPEAT_TIMER')))
    periodic_collection_thread.start()
    time.sleep(1)
    # start event listner on topology.event
    subscribe_to_topolgy_events_thread = Thread(target=ctrl.subcribe_to_topology_events,
                                                args=("topic://topology.event",))
    subscribe_to_topolgy_events_thread.start()
    
if __name__ == '__main__':
    run()


