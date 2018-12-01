#!/usr/bin/env python

import argparse
import logging
import requests
from time import sleep

import paho.mqtt.client as mqtt


def on_connect(client, _userdata, _flags, rc):
    if rc == 0:
        client.is_connected = True
        logging.info('Connected')
    else:
        logging.error(f'Connection error, code={rc}')


def on_disconnect(client, _userdata, rc):
    client.is_connected = False
    if rc == 0:
        logging.info('Disconnected')
    else:
        logging.error(f'Disconected due to an error, code={rc}')


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('box_id', type=str, nargs='+', help='box id to fetch and publish to MQTT')
    args = parser.parse_args()

    mqtt.Client.is_connected = False
    client = mqtt.Client('opensensemap')
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.loop_start()
    client.connect('mosquitto', 1883, 60)
    while True:
        for box_id in args.box_id:
            topics = {}
            try:
                r = requests.get(f'https://api.opensensemap.org/boxes/{box_id}')
                for s in r.json()['sensors']:
                    if s['icon'] == 'osem-thermometer':
                        topics[f'opensensemap/status/{box_id}/temperature'] = s['lastMeasurement']['value']
                    elif s['icon'] == 'osem-humidity':
                        topics[f'opensensemap/status/{box_id}/humidity'] = s['lastMeasurement']['value']
                for topic, payload in topics.items():
                    publish(client, topic, payload)
            except Exception:
                logging.error(f'Error updating box: {box_id}')
        # Wait 5m
        sleep(5 * 60)


def publish(client, topic, payload):
    while not client.is_connected:
        logging.info('Waiting for connection')
        sleep(1)
    logging.info(f'Publishing {topic} {payload}')
    client.publish(topic, str(payload))


if __name__ == '__main__':
    main()
