from .amqp.receive import Receiver
from .amqp.send import Sender

class ControllerService:
    def __init__(self, controller_host) -> None:
        '''
        controller_host = "10.11.200.125:5672"
        '''
        self.controller_host = controller_host
        self.collection_sender = Sender()
        self.status_sender = Sender()
        self.event_receiver = Receiver()

    def publish_collected_topology(self, topic, message):
        self.collection_sender.send(self.controller_host,topic, message)
       
    def publish_interface_status(self, topic, message):
        self.status_sender.send(self.controller_host,topic, message)
       
    def subcribe_to_topology_events(self, topic, target_nodes):
        self.event_receiver.receive(self.controller_host,topic, target_nodes)
       
