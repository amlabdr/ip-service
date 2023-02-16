import logging
from http.server import HTTPServer
from .http_server.server import httpHandller

class Controller_service:
    def __init__(self,config):
        self.cfg = config
        self.url = self.cfg.controller_url
        self.http_handller = httpHandller
        self.token = ""


    def run_http_server(self, network, cfg):
        #logging.basicConfig(level=logging.INFO)
        server = "localhost"
        port = 8383
        server_address = (server, port)
        logging.info("server address is {}".format(server_address))
        
        self.http_handller.init_network(self.http_handller, network= network, cfg=cfg)
        httpd = HTTPServer(server_address, self.http_handller)
        logging.info('Starting http server...\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logging.info('Stopping httpd...\n')