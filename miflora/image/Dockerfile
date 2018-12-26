FROM python:3-alpine

RUN apk add --no-cache bluez bluez-deprecated

ENV MIFLORA_MQTT_DAEMON_VERSION 699ec011448e7b84dde64b9a76ecfec2ac3bf39c

RUN apk add --no-cache --virtual .build-deps git && \
    rm -rf /usr/src/app && \
    git clone https://github.com/ThomDietrich/miflora-mqtt-daemon.git /usr/src/app && \
    git -C /usr/src/app checkout ${MIFLORA_MQTT_DAEMON_VERSION} && \
    apk del .build-deps

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "./miflora-mqtt-daemon.py" ]
