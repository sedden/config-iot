FROM node:8.12.0-alpine

ENV HOMEKIT2MQTT_VERSION 1.1.2

RUN apk add --no-cache dbus avahi-compat-libdns_sd

RUN apk add --no-cache --virtual .build-deps \
	avahi-dev \
        g++ \
        make \
        python \
    && npm install -g homekit2mqtt@$HOMEKIT2MQTT_VERSION --unsafe-perm \
    && apk del .build-deps

RUN mkdir -p /homekit2mqtt/config /homekit2mqtt/data
VOLUME ["/homekit2mqtt/config", "/homekit2mqtt/data"]

ENTRYPOINT ["/usr/local/bin/homekit2mqtt", "-m", "/homekit2mqtt/config/mapfile.json", "-s", "/homekit2mqtt/data"]