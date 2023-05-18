import json
from config.config import Config
from net.reader import Reader
from controller.controller import ControllerService

def run():
    config = Config()
    result = {}
    reader = Reader() 
    reader.read(config) # read from topology service (HTTP: login (return token), get subnets (with token), pick up one subnet (dc-qnet, id), read nodes w/ subent Id -> target_nodes)
    result = reader.result
    json_data = json.dumps(result,indent=2)
    with open("/tmp/result.json", 'w') as json_file:
        json_file.write(json_data)
        json_file.close()
    ctrl = ControllerService('10.11.200.125:5672')
    ctrl.publish_collected_topology(topic = 'topic://topology.collection', message = result)
    ctrl.subcribe_to_topology_events(topic = 'topic://topology.events',
                                     config = config,
                                     network_reader = reader)
    print("Done")
    
if __name__ == '__main__':
    run()


