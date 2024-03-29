#standards imports
import json, traceback, logging, re, time
from datetime import datetime
from threading import Thread

#imports to use AMQP 1.0 communication protocol
from proton.handlers import MessagingHandler
from proton.reactor import Container
from .send import Sender

sender = Sender()
RESOURCE = {"PORT":"LTP","BRIDGE_GROUP":"LTP","INTERFACE":"CTP","SVI":"CTP","VLAN":"CTP","VLAN_MEMBER":"CTP","ROUTER":"NODE"}


class Receiver():
    def __init__(self):
        super(Receiver, self).__init__()
        
    def receive_event(self, server, topic, network, supported):
        print("will start the rcv")
        Container(event_Receiver_handller(server,topic, network, supported)).run()


class event_Receiver_handller(MessagingHandler):
    def __init__(self, server,topic, network,supported):
        super(event_Receiver_handller, self).__init__()
        self.server = server
        self.topic = topic
        self.network = network
        self.supported = supported
        logging.info("Agent will start listning for events in the topic: {}".format(self.topic))
        

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.topic)

    def process_event(self, network_config):
        print("event:", network_config)
        logging.info("now will call config in network")
        status = self.network.config_network(network_config)
        return status

    def on_message(self, event):
        try:
            jsonData = json.loads(event.message.body)
            if jsonData["resource"] not in self.supported:
                return
            logging.info("msg received {}".format(jsonData))
            status = self.process_event(jsonData)
            topic='topic://'+'topology.status'
            status_msg = {}
            status_msg["resourceId"]=int(jsonData["resourceId"])
            status_msg["resourceType"]=RESOURCE[jsonData["resource"]]
            status_msg["resourceStatus"]=status
            print("status msg",status_msg)
            if jsonData["action"]=="DELETED" and status == "DOWN":
                pass
            else:
                sender.send(self.server,topic, status_msg)

            
        except Exception:
            traceback.print_exc()
            