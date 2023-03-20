#standards imports
import json
import logging
from sys import exc_info

#imports to use AMQP 1.0 communication protocol
from proton.handlers import MessagingHandler
from proton.reactor import Container
from pyparsing import traceback


class Receiver():
    def __init__(self):
        super(Receiver, self).__init__()
        
    def receive(self, server, topic, target_nodes):
        logging.info("will start the rcv")
        Container(ReceiverHandler(server,topic, target_nodes)).run()

class ReceiverHandler(MessagingHandler):
    def __init__(self, server,topic, target_nodes):
        super(ReceiverHandler, self).__init__()
        self.server = server
        self.topic = topic
        self.target_nodes = target_nodes
        logging.info("will start listning for events in the topic: {}".format(self.topic))

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.topic)

    def on_message(self, event):
        try:
            received_message = json.loads(event.message.body)
            logging.info('message received {}. On topic {}'.format(received_message, self.topic))
            if received_message['action'] == 'CREATED' or received_message['action'] == 'UPDATE' :
                self.target_nodes[received_message['content']['name']] = received_message['content']['mgmtIP']
                # launch a network read, probably need to pass network reader as argument
            elif received_message['action'] == 'DELETE':
                self.target_nodes.pop(received_message['content']['name'])

        except Exception:
            traceback.print_exc()

