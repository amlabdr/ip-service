import os
from threading import Thread
from ncclient import manager
from ncclient.operations import RPCError


from controller.amqp.send import Sender
from utils.common import xml_preprocessing_notification
from net.readers.notification_reader import NotificationReader

class NotificationSubscriber:
    def __init__(self, config):
        self.config = config
        self.result = {}

    # add function that calls the while loop waiting for notifications in a new thread
    # pass manager as argument 
    def subscribe_to_interface_status(self):
        for target_node in self.config.network_targets:
            with manager.connect(host = target_node, 
                                 port = os.environ.get('NETCONF_PORT'),
                                 username = os.environ.get('NETCONF_USER'),
                                 password = os.environ.get('NETCONF_PASSWORD'),
                                 hostkey_verify = False) as m:
                # Create the subscription
                try:
                    m.create_subscription(filter=filter)
                except RPCError as e:
                    print(f"Failed to create subscription: {e}")
                    exit(1) 
                # Wait for and process the notification messages
                # launch in thread
                Thread wait_for_notifications = Thread(target=self.wait_for_notifications, args=(m, target_node))
    
    def wait_for_notifications(self, manager, target_node):
        while True:
            self.result = {}
            notification = manager.take_notification()
            notification_dict = xml_preprocessing_notification(notification.notification_xml)
            notification_reader = NotificationReader(target_node, notification_dict)
            notification_reader.read()
            self.result = notification_reader.result
            # send result to AMQP topic topology.status
            sender = Sender()
            sender.send(os.environ.get('CONTROLLER_IP'),
                        os.environ.get('AMQP_INTERFACE_STATUS_TOPIC'),
                        self.result)
            

    def remove_subscribtion_to_interface_status(self):
        pass

 
