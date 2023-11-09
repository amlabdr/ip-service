import os
from threading import Thread
from ncclient import manager
from ncclient.operations import RPCError


from controller.amqp.send import Sender
from utils.common import xml_preprocessing_notification
from net.readers.notification_reader import NotificationReader

filter = '''
<filter type="subtree">
      <interface-link-state-change-notification xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface">
        <name/>
        <oper-status/>
      </interface-link-state-change-notification>
</filter>
'''

class NotificationSubscriber:
    def __init__(self, config):
        self.config = config
        self.result = {}
        #add a dict of managers key=target_node value=manager 
        #in order to close the session if a node is deleted

    # pass manager as argument 
    def subscribe_to_interface_status(self):
        for target_node in self.config.network_targets.values():
            with manager.connect(host = target_node['mgmtIp'], 
                                 port = self.config.netconf_port,
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
                #wait_for_notifications = Thread(target=self.wait_for_notifications, args=(m, target_node))
                #wait_for_notifications.start()
                while True:
                    self.result = {}
                    notification = m.take_notification(block=True)
                    notification_dict = xml_preprocessing_notification(notification.notification_xml)
                    notification_reader = NotificationReader(target_node['name'], notification_dict)
                    notification_reader.read()
                    self.result = notification_reader.result
                    if self.result['resourceStatus'] != '':
                    # send result to AMQP topic topology.status
                        sender = Sender()
                        sender.send(self.config.controller_ip,
                                    self.config.amqp_topology_interface_status_topic,
                                    self.result)

                        print('Interface notification SENT')
                        print(self.result)
    
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
            sender.send(self.config.controller_ip,
                        self.config.amqp_topology_interface_status_topic,
                        self.result)
            print('Interface notification SENT')
            print(self.result)
            

    def remove_subscribtion_to_interface_status(self):
        pass

 
