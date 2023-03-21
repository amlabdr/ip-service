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
        handler = ReceiverHandler(server,topic, network_reader)
        container = Container(handler)
        container.container_id = 'topology.events'
        container.create_receiver(server, 
                                  source = topic, 
                                  name = 'topology_events_container',
                                  handler = handler,
                                  context = config)


class ReceiverHandler(MessagingHandler):
    def __init__(self, server,topic, network_reader):
        super(ReceiverHandler, self).__init__()
        self.server = server
        self.topic = topic
        self.network_reader = network_reader
        logging.info("will start listning for events in the topic: {}".format(self.topic))

    def on_message(self, event):
        try:
            received_message = json.loads(event.message.body)
            config = event.receiver.context
            logging.info('message received {}. On topic {}'.format(received_message, self.topic))
            if received_message['action'] == 'CREATED' or received_message['action'] == 'UPDATE' :
                config.target_nodes[received_message['content']['name']] = received_message['content']['mgmtIP']
                # launch a network read, probably need to pass network reader as argument
                self.network_reader.read(config)
            elif received_message['action'] == 'DELETE':
                config.target_nodes.pop(received_message['content']['name'])

        except Exception:
            traceback.print_exc()

