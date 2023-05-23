FROM  python:3.8-slim-buster

WORKDIR /ipcollection-microservice

COPY . /ipcollection-microservice

RUN pip install --no-cache-dir -r requirements.txt

#Environment variables
ENV CONTROLLER_REST_URL 'http://10.11.200.125:8787/'
ENV CONTROLLER_IP '10.11.200.125'
ENV CONTROLLER_REST_USERNAME 'admin'
ENV CONTROLLER_REST_PASSWORD 'admin'
ENV CONTROLLER_REST_PORT '8787'
ENV CONTROLLER_AMQP_PORT '5672'

#prefixes
ENV CONTROLLER_LOGIN_PREFIX '/api/login/user'
ENV CONTROLLER_QNET_SUBNET_PREFIX '/api/topology/subnet/type/QNET'

ENV COLLECTION_REPEAT_TIMER 60
ENV NET_TARGETS /ipcollect-microservice/config/network_targets.dot
ENV NETCONF_XML_TEMPLATES /ipcollect-microservice/net/xml_templates/

CMD ["python", "main.py"]
