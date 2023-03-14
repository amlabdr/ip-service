from .amqp.receive import Receiver
from .amqp.send import Sender

class ControllerService:
    def __init__(self, controller_host) -> None:
        self.controller_host = controller_host
        '''
        controller_host = "10.11.200.125:5672"
        '''
        self.sender = Sender()

    def publish_message(self, topic, message):
        '''
        topic = topic='topic://' + TOPIC
        message = {} dict
        '''
        self.sender.send(self.controller_host,topic, message)
       
