FROM  python:3

WORKDIR /ipconfig-microservice

COPY . /ipconfig-microservice

# proxy env variables
ENV http_proxy=http://10.11.200.200:3131
ENV https_proxy=http://10.11.200.200:3131

RUN pip3 install --no-cache-dir -r requirements.txt

# Controller env variables
#ENV CONTROLLER_URL 'http://10.11.200.125:8787'
#ENV CONTROLLER_IP '10.11.200.125'
ENV CONTROLLER_REST_USERNAME 'admin'
ENV CONTROLLER_REST_PASSWORD 'admin'
ENV CONTROLLER_REST_PORT '8787'
ENV CONTROLLER_AMQP_PORT '5672'
# Controller prefixes
#ENV CONTROLLER_LOGIN_PREFIX '/api/login/user'
#ENV CONTROLLER_QNET_SUBNET_PREFIX '/api/topology/subnet/type/QNET'
#ENV CONTROLLER_NODES_PER_SUBNET_PREFIX '/api/topology/subnet/ID/nodes'

# Netconf env variables
ENV NETCONF_PORT '830'
ENV NETCONF_USER 'ocnos'
ENV NETCONF_PASSWORD 'ocnos'

# AMQP vars

#ENV AMQP_CONFIGURATION_EVENTS_TOPIC 'topic://configuration.event'

# Other
#ENV NETCONF_XML_TEMPLATES '/ipconfig-microservice/network/ocnos_service/xml_templates'

CMD ["python3", "main.py"]
