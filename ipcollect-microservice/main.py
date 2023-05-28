import json
from threading import Thread

from config.config import Config
from net.reader import Reader
from controller.controller import ControllerService

def run():

    config = Config()
    ctrl = ControllerService(config)
    
    # 1. get subnets
    subnets = json.loads(ctrl.get(url="http://10.11.200.125:8787/api/topology/subnet/type/QNET"))
    # 2. get target nodes by subnet_id
    for subnet in subnets:
        if subnet['name'] == 'dc-qnet':
            nodes = json.loads(ctrl.get(url='http://10.11.200.125:8787/api/topology/subnet/'+str(subnet['id'])+'/nodes'))
            for node in nodes:
                if node['type'] == 'ROUTER':
                    config.network_targets = node
            print(config.network_targets)
    # 3. start periodic reader thread
    result = {}
    reader = Reader() 
    reader.read(config) # read from topology service (HTTP: login (return token), get subnets (with token), pick up one subnet (dc-qnet, id), read nodes w/ subent Id -> target_nodes)
    result = reader.result
    json_data = json.dumps(result,indent=2)
    with open("/tmp/result.json", 'w') as json_file:
        json_file.write(json_data)
        json_file.close()
    
    ctrl.publish_collected_topology(topic = 'topic://topology.collection', message = result)
    ctrl.subcribe_to_topology_events(topic = 'topic://topology.events',
                                     config = config,
                                     network_reader = reader)
    print("Done")
    
if __name__ == '__main__':
    run()


