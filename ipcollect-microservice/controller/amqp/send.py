#standards imports
import json, logging

#imports to use AMQP 1.0 communication protocol
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class Sender():
    def __init__(self):
        super(Sender, self).__init__()
        
    def send(self, server, topic, messages):
        Container(SendHandler(server,topic, messages)).run()

        
class SendHandler(MessagingHandler):
    def __init__(self, server, topic, messages):
        super(SendHandler, self).__init__()
        self.server = server
        self.topic = topic
        self.confirmed = 0
        self.data = messages
        self.total = 1

    def on_connection_error(self, event):
        logging.error("controller.amqp.sender: connection error while sending msg to server: {} for topic: {}".format(self.server, self.topic))
        return super().on_connection_error(event)
    
    def on_transport_error(self, event) -> None:
        logging.error("controller.amqp.sender: transport error while sending msg to server: {} for topic: {}".format(self.server, self.topic))
        return super().on_transport_error(event)
        
    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_sender(conn, self.topic)
   
    def on_sendable(self, event):
        logging.info("controller.amqp.sender: sending msg to topic{}".format(self.topic))
        msg = Message(body=json.dumps(self.data))
        event.sender.send(msg)
        event.sender.close()
        
    def on_rejected(self, event):
        logging.error("controller.amqp.sender: controller.amqp.sender: msg regected while sending msg to server: {} for topic: {}".format(self.server, self.topic))
        return super().on_rejected(event)
        
    def on_accepted(self, event):
        logging.info("controller.amqp.sender: msg accepted in topic {}".format(self.topic))
        print("controller.amqp.sender: controller.amqp.sender: accepted")
        self.confirmed += 1
        if self.confirmed == self.total:
            event.connection.close()
    

    def on_disconnected(self, event):
        logging.error("controller.amqp.sender: disconnected error while sending msg to server: {} for topic: {}".format(self.server, self.topic))
        self.sent = self.confirmed
