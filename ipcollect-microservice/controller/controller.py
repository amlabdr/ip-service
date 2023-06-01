from .amqp.receive import Receiver
from .amqp.send import Sender
from .request.request import Request
import requests
import time 
import logging
import jwt

class ControllerService:
    def __init__(self, config) -> None:
        self.controller_rest_url = ( 'http://' + 
                                    config.controller_ip +
                                    ':' +
                                    config.controller_rest_port)
        self.controller_amqp_url = ( config.controller_ip +
                                    ':' +
                                    config.controller_amqp_port)
        self.username = config.controller_rest_username
        self.password = config.controller_rest_password
        self.token = None
        self.token_acquired_time = None
        
        self.request = Request()
        self.collection_sender = Sender()
        self.status_sender = Sender()
        self.event_receiver = Receiver()

    def publish_collected_topology(self, topic, message):
        self.collection_sender.send(self.controller_amqp_url,topic, message)
       
    def publish_interface_status(self, topic, message):
        self.status_sender.send(self.controller_amqp_url,topic, message)
       
    def subcribe_to_topology_events(self, topic, config, network_reader):
        self.event_receiver.receive(self.controller_amqp_url,topic, config, network_reader, self)
    
    def login(self):
        login_url = self.controller_rest_url+'/api/login/user'
        response = requests.post(login_url, json={'username': self.username, 'password': self.password})
        if response.status_code == 200:
            self.token = response.json().get('token')
            decoded_token = jwt.decode(self.token, options={'verify_signature': False})
            self.token_acquired_time = decoded_token.get('iat')

    def token_is_expired(self):
        if self.token:
            decoded_token = jwt.decode(self.token, options={'verify_signature': False})
            expiry_time = decoded_token.get('exp')
            if time.time() >= expiry_time:
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
        response = self.request.post_request_file(url,filename = filename, token = self.token)
        
        return response
    
    def post_json(self, url, json_data):
        """Method to post a file to the controller
        Args:
            filename : name of the file to post
        return:
            response
        """
        self.get_token()
        response = self.request.post_request_json(url,data = json_data, token = self.token)
        
        return response
    
    def get(self,url):
        """Method to post a file to the controller
        Args:
            filename : name of the file to post
        return:
            response
        """
        self.get_token()
        response = self.request.get_request(url, token = self.token)
        
        return response
