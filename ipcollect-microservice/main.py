import json
from config.config import Config
from net.reader import Reader
from controller.controller import ControllerService

def run():
    config = Config()
    result = {}
    reader = Reader() 
    #reader.read(config)
    result = reader.result
    ctrl = ControllerService('10.11.200.125:5672')
    ctrl.publish_collected_topology(topic = 'topic://topology.collection', message = result)
    ctrl.subcribe_to_topology_events(topic = 'topic://topology.events',
                                     config = config,
                                     network_reader = reader)
    json_data = json.dumps(result,indent=2)
    with open("/tmp/result.json", 'w') as json_file:
        json_file.write(json_data)
        json_file.close()
    print("Done")
    
if __name__ == '__main__':
    run()


