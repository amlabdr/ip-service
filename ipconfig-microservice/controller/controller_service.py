import logging, os
from http.server import HTTPServer
from .http_server.server import httpHandller
from .amqp.receive import Receiver


class Controller_service:
    def __init__(self,config):
        self.cfg = config
        self.http_handller = httpHandller
        self.token = ""


    def run_http_server(self, network):
        #logging.basicConfig(level=logging.INFO)
        server = "localhost"
        port = 8383
        server_address = (server, port)
        logging.info("server address is {}".format(server_address))
        
        self.http_handller.init_network(self.http_handller, network= network)
        httpd = HTTPServer(server_address, self.http_handller)
        logging.info('Starting http server...\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logging.info('Stopping httpd...\n')
    
    def subscribe2events(self,network):
        logging.basicConfig(level=logging.INFO)
        topic = self.cfg.amqp_configuration_events_topic
        url = self.cfg.amqp_broker +":"+ self.cfg.controller_amqp_port
        logging.info("Agent will start lesstning for events from the controller")
        print("url: ", url)
        print("topic: ", topic)
        receiver = Receiver()
        supported = ["BRIDGE_GROUPE", "INTERFACE", "PORT", "SVI", "VLAN_MEMBER", "VLAN","IP_ROUTER"]
        receiver.receive_event(url,topic, network=network,supported=supported)