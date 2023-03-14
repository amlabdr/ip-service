#standards imports
import logging

#imports to use AMQP 1.0 communication protocol
from proton.handlers import MessagingHandler
from proton.reactor import Container


class Receiver():
    def __init__(self):
        super(Receiver, self).__init__()
        
    def receive_event(self, server, topic, network):
        print("will start the rcv")
        Container(event_Receiver_handller(server,topic, network)).run()


class event_Receiver_handller(MessagingHandler):
    def __init__(self, server,topic, network):
        super(event_Receiver_handller, self).__init__()
        self.server = server
        self.topic = topic
        self.network = network
        logging.info("will start listning for events in the topic: {}".format(self.topic))
        

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.topic)

    

    def on_message(self, event):
        pass
        '''DO PROCESSING'''
            