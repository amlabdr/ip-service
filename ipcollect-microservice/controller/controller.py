from .amqp.receive import Receiver
from .amqp.send import Sender
import time, logging
from .request.request import Request

class ControllerService:
    def __init__(self, controller_host) -> None:
        '''
        controller_host = "10.11.200.125:5672"
        '''
        self.controller_host = controller_host
        self.collection_sender = Sender()
        self.status_sender = Sender()
        self.event_receiver = Receiver()
        self.token = ""

    def publish_collected_topology(self, topic, message):
        self.collection_sender.send(self.controller_host,topic, message)
       
    def publish_interface_status(self, topic, message):
        self.status_sender.send(self.controller_host,topic, message)
       
    def subcribe_to_topology_events(self, topic, config, network_reader):
        self.event_receiver.receive(self.controller_host,topic, config, network_reader)

    def controllerAuthentication(self, authentication_period:int):
        """Method to authenticate to the controller
        Args:
            authentication_periode(int) : period of refreshing the authentification Token
        return:
            Token(str)
        """
        while True:
            #update TOKEN EVERY PERIODE
            current_request = Request()
            data = {
                'username': self.cfg.conf_file_contents['CONTROLLER_AUTH']['username'],
                'password': self.cfg.conf_file_contents['CONTROLLER_AUTH']['password']
            }
            url = self.cfg.controller_url + "/api/login/user"
            try:
                response = current_request.postRequestJson(url,data)
                print(response.json())
                self.token = response.json()['token']
                #self.token = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
            except:    
                logging.exception("An exception  during Authentification")
            time.sleep(authentication_period)
       
    def post(self,filename):
        """Method to post a file to the controller
        Args:
            filename : name of the file to post
        return:
            response
        """
        response = self.request.postRequest(filename = filename, token = self.token)
        logging.info("post response to {} is : {}".format(self.request.url,response))
        return response