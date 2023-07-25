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

    print(ctrl.config)
    
    # get subnets
    subnets = json.loads(ctrl.get(url = ctrl.controller_rest_url+ctrl.config.controller_qnet_subnet_prefix))

    # get target nodes by subnet_id
    for subnet in subnets:
        if subnet['name'] == 'dc-qnet':
            nodes_url = ctrl.controller_rest_url + ctrl.config.controller_nodes_per_subnet_prefix
            nodes_url = nodes_url.replace('ID', str(subnet['id']))
            nodes = json.loads(ctrl.get(url=nodes_url))
            for node in nodes:
                if node['type'] == 'ROUTER':
                    ctrl.config.network_targets[node['name']] = node 
    print(ctrl.config.network_targets)
    
    # start periodic reader thread
    periodic_collection_thread = Thread(target=ctrl.reader.read, args=(ctrl, ctrl.config.repeat_timer))
    periodic_collection_thread.start()
    time.sleep(1)
    
    # start event listner on topology.event
    subscribe_to_topolgy_events_thread = Thread(target=ctrl.subcribe_to_topology_events,
                                                args=(ctrl.config.amqp_configuration_events_topic,))
    subscribe_to_topolgy_events_thread.start()

    # start subscribtion to interface status thread
    subscribe_to_interface_status_thread = Thread(target=ctrl.subscribe_to_interface_status)
    subscribe_to_interface_status_thread.start()

if __name__ == '__main__':
    run()


