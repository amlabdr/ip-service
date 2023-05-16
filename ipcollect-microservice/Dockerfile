FROM  python:3.8-slim-buster

WORKDIR /ipcollection-microservice

COPY . /ipcollection-microservice

RUN pip install --no-cache-dir -r requirements.txt

ENV REPEAT_TIMER 10
ENV CONTROLLER_URL 'http://10.11.200.125:8787/'
ENV NET_TARGETS ~/ip-service/ipcollect-microservice/config/network_targets.dot
ENV NETCONF_XML_TEMPLATES ~/ip-service/ipcollect-microservice/net/xml_templates/

CMD ["python", "main.py"]
