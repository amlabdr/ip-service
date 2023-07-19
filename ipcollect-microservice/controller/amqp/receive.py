#standards imports
import json
import logging
import time
#imports to use AMQP 1.0 communication protocol
from proton.handlers import MessagingHandler
from pyparsing import traceback
from proton.reactor import Container
from controller.amqp.send import Sender


sender = Sender()

class Receiver():
    def __init__(self, config):
        self.config = config
        super(Receiver, self).__init__()
        
    def receive(self, server, topic, ctrl):
        print("controller.amqp.receiver: will start the receiver")
        handler = ReceiverHandler(server, topic, self.config, ctrl)
        container = Container(handler)
        container.run() 


class ReceiverHandler(MessagingHandler):
    def __init__(self, server,topic, config, ctrl):
        super(ReceiverHandler, self).__init__()
        self.server = server
        self.topic = topic
        self.config = config
        self.ctrl = ctrl
        print("controller.amqp.receiver: will start listning for events in the topic: {}".format(self.topic))
   
    def on_start(self, event) -> None:
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.topic)

    def on_message(self, event):
        try:
            received_message = json.loads(event.message.body)
            print('controller.amqp.receiver: message received {}. On topic {}'.format(received_message, self.topic))
            time.sleep(1)
            self.process_message(received_message)
        except Exception:
            traceback.print_exc()

    def process_message(self, message):
        if message['resource'] != 'ROUTER':
            return
        if message['action'] == 'CREATED' or message['action'] == 'UPDATED' :
            #{'resource': 'NODE', 'action': 'CREATED', 'content': {'id': 20, 'name': 'dcqnet-ctrl-01', 'type': 'ROUTER', 'mgmtIp': '10.11.200.13', 'platform': 'OCNOS'}}
            print('controller.amqp.receiver: action is : '+ message['action'])
            self.config.network_targets[message['content']['name']] = message['content']
            print('controller.amqp.receiver: TARGET NODES')
            print(self.config.network_targets)
            # launch a network read, probably need to pass network reader as argument
            # read from event (mgmtIp) and collect for one switch, add to target nodes -> collect target nodes every 60s
            self.ctrl.reader.read(self.ctrl, single_node = message['content'])
            # send on topic topology.collection
            sender.send(self.server, 'topic://topology.collection', self.ctrl.reader.result)
            print('controller.amqp.sender: sent')
            # add subscription to interface status
        elif message['action'] == 'DELETED':
            print('controller.amqp.receiver: action is : '+ message['action'])
            self.config.network_targets.pop(message['content']['name'], 'Key not found')
            print('controller.amqp.receiver: TARGET NODES')
            print(self.config.network_targets)
            #destroy subscription to interface status
