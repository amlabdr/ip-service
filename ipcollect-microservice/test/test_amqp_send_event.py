import unittest
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

class AMQPMessageSender(MessagingHandler):
    def __init__(self, message):
        super(AMQPMessageSender, self).__init__()
        self.message = message

    def on_start(self, event):
        event.container.create_sender("amqp://localhost:5672/topic")

    def on_sendable(self, event):
        event.sender.send(self.message)
        event.sender.close()
        event.connection.close()

class AMQPMessageSenderTest(unittest.TestCase):
    def test_send_amqp_message(self):
        message = Message()
        message.address = "topic://topology.event"
        message.body = {
            'resource': 'NODE',
            'action': 'CREATED',
            'content': {
                'id': 20,
                'name': 'dcqnet-ctrl-01',
                'type': 'ROUTER',
                'mgmtIp': '10.11.200.13',
                'platform': 'OCNOS'
            }
        }

        handler = AMQPMessageSender(message)
        container = Container(handler)
        container.run()

if __name__ == '__main__':
    unittest.main()

