#!/usr/bin/env python

import argparse
import logging
import requests
from time import sleep

import paho.mqtt.client as mqtt


def update(box_id):
    topics = {}
    try:
        r = requests.get(f'https://api.opensensemap.org/boxes/{box_id}')
        for s in r.json()['sensors']:
            if s['icon'] == 'osem-thermometer':
                topics[f'opensensemap/status/{box_id}/temperature'] = s['lastMeasurement']['value']
            elif s['icon'] == 'osem-humidity':
                topics[f'opensensemap/status/{box_id}/humidity'] = s['lastMeasurement']['value']
        client = mqtt.Client('opensensemap')
        client.connect('mosquitto')
        for topic, payload in topics.items():
            logging.info(f'Publishing {topic} {payload}')
            client.publish(topic, payload)
        client.disconnect()
    except Exception:
        logging.error(f'Error updating box: {box_id}')


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('box_id', type=str, nargs='+', help='box id to fetch and publish to MQTT')
    args = parser.parse_args()
    while 1:
        for box_id in args.box_id:
            update(box_id)
            sleep(5 * 60)


if __name__ == '__main__':
    main()
