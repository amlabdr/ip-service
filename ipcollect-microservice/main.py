import json, time
from config.config import Config
from net.reader import Reader
from controller.controller import ControllerService
from threading import Thread

def run():

    config = Config()
    ctrl = ControllerService(config)
    
    # 1. get subnets
    subnets = ctrl.get(url="http://10.11.200.125:8787/api/topology/subnet/type/QNET")
    # 2. get target nodes by subnet_id
    config.network_targets = ctrl.get(url='http://10.11.200.125:8787/api/topology/'+subnet.id+'/nodes')
    # 3. start periodic reader thread
    result = {}
    reader = Reader() 
    periodic_collection_thread = Thread(target=reader.read, args=(config))
    result = reader.result
    json_data = json.dumps(result,indent=2)
    with open("/tmp/result.json", 'w') as json_file:ZZ
        json_file.write(json_data)
        json_file.close()
    
    # 4. subscribe to topology events in a seperate thread
    ctrl.publish_collected_topology(topic = 'topic://topology.collection', message = result)
    ctrl.subcribe_to_topology_events(topic = 'topic://topology.events',
                                     config = config,
                                     network_reader = reader)
    print("Done")
    
if __name__ == '__main__':
    run()

