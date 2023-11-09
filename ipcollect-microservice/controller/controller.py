import time 
from keycloak.keycloak_openid import KeycloakOpenID
import jwt

from net.notification_subscriber import NotificationSubscriber
from .amqp.receive import Receiver
from .amqp.send import Sender
from .request.request import Request

class ControllerService:
    def __init__(self, config, reader) -> None:
        self.config = config
        self.reader = reader
        self.controller_rest_url = ( 'http://' + 
                                    config.controller_ip +
                                    ':' +
                                    config.controller_rest_port)
        self.controller_amqp_url = ( config.amqp_broker +
                                    ':' +
                                    config.controller_amqp_port)
        self.username = config.controller_rest_username
        self.password = config.controller_rest_password
        self.token = None
        self.token_acquired_time = None        
        self.request = Request()
        self.collection_sender = Sender()
        self.status_sender = Sender()
        self.event_receiver = Receiver(config)
        self.notification_subscriber = NotificationSubscriber(config)

    def publish_collected_topology(self, topic, message):
        self.collection_sender.send(self.controller_amqp_url,topic, message)
       
    def publish_interface_status(self, topic, message):
        self.status_sender.send(self.controller_amqp_url,topic, message)
       
    def subcribe_to_topology_events(self, topic):
        self.event_receiver.receive(self.controller_amqp_url, topic, self)

    def subscribe_to_interface_status(self):
        self.notification_subscriber.subscribe_to_interface_status()
    
    def login(self):
        login_url = "http://"+self.config.controller_ip+":"+self.config.controller_auth_port
        keycloak_openid = KeycloakOpenID(server_url=login_url,
                                 client_id="multiverse-access",
                                 realm_name="multiverse")
        self.token = keycloak_openid.token(self.username, self.password)
        print(type(self.token))
        print(self.token)
        self.token_acquired_time = time.time()

    def token_is_expired(self):
        if self.token:
            if time.time() >= self.token_acquired_time + self.token['expires_in']:
                return True
        return False

    def get_token(self):
        if not self.token or self.token_is_expired():
            self.login()
        return self.token

    def post_file(self, url, filename):
        """Method to post a file to the controller
        Args:
            filename : name of the file to post
        return:
            response
        """
        self.get_token()
        response = self.request.post_request_file(url,filename = filename, token = self.token['access_token'])
        
        return response
    
    def post_json(self, url, json_data):
        """Method to post a file to the controller
        Args:
            filename : name of the file to post
        return:
            response
        """
        self.get_token()
        response = self.request.post_request_json(url,data = json_data, token = self.token['access_token'])
        
        return response
    
    def get(self,url):
        """Method to post a file to the controller
        Args:
            filename : name of the file to post
        return:
            response
        """
        self.get_token()
        response = self.request.get_request(url, token = self.token['access_token'])
        
        return response
