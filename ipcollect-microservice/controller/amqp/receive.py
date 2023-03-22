#standards imports
import json
import logging

#imports to use AMQP 1.0 communication protocol
from proton.handlers import MessagingHandler
from proton.reactor import Container
from pyparsing import traceback


class Receiver():
    def __init__(self):
        super(Receiver, self).__init__()
        
    def receive(self, server, topic, config, network_reader):
        logging.info("will start the rcv")
        handler = ReceiverHandler(server, topic, config, network_reader)
        container = Container(handler).run()


class ReceiverHandler(MessagingHandler):
    def __init__(self, server,topic, config, network_reader):
        super(ReceiverHandler, self).__init__()
        self.server = server
        self.topic = topic
        self.config = config
        self.network_reader = network_reader
        logging.info("will start listning for events in the topic: {}".format(self.topic))
   
    def on_start(self, event) -> None:
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.topic)

    def on_message(self, event):
        try:
            received_message = json.loads(event.message.body)
            logging.info('message received {}. On topic {}'.format(received_message, self.topic))
            self.process_message(received_message)
        except Exception:
            traceback.print_exc()

    def process_message(self, message):
        if message['action'] == 'CREATED' or message['action'] == 'UPDATE' :
            self.config.target_nodes[message['content']['name']] = message['content']['mgmtIP']
            # launch a network read, probably need to pass network reader as argument
            self.network_reader.read(self.config)
        elif message['action'] == 'DELETE':
            self.config.target_nodes.pop(message['content']['name'])

