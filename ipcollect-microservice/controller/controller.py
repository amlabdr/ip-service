import amqp

class ControllerService:
    def __init__(self, controller_host, amqp_userid, amqp_password) -> None:
        self.controller_host = controller_host
        self.amqp_userid = amqp_userid
        self.amqp_password = amqp_password

    def __str__(self) -> str:
        return f'ControllerService = {vars(self)}'

    def create_amqp_connection(self):
        connection = amqp.Connection(host=self.controller_host, 
                                     userid = self.amqp_userid, 
                                     password = self.amqp_password,
                                     insist = False)
        return connection.channel()

    def publish_message(self, channel, topic, message):
        channel.queue_declare(queue = topic,
                              durable = True,
                              exclusive = False,
                              auto_delete = False)
        msg = amqp.Message(body=message)
        channel.basic_publish(msg, 
                              exchange='', 
                              routing_key = topic)
       
