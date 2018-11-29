#!/usr/bin/env python

import os
import logging
from time import sleep
import miio
import paho.mqtt.client as mqtt

TOPICS = {}

def main():
    logging.basicConfig(level=logging.INFO)

    ip = os.environ.get('MIROBO_IP')
    token = os.environ.get('MIROBO_TOKEN')

    vac = miio.Vacuum(ip, token)
    info = vac.info()
    device_identifier = info.mac_address.replace(':', '').lower()

    TOPICS['battery'] = f'/mirobo/status/{device_identifier}/battery'
    TOPICS['sensor_dirt_hours'] = f'/mirobo/status/{device_identifier}/sensor_dirt_hours'
    TOPICS['sensor_filter_hours'] = f'/mirobo/status/{device_identifier}/sensor_filter_hours'

    client = mqtt.Client('mirobo')
    client.loop_start()
    client.connect('mosquitto', 1883, 60)
    while True:
        status = vac.status()
        consumable_status = vac.consumable_status()
        client.publish(TOPICS['battery'], status.battery)
        client.publish(TOPICS['sensor_dirt_hours'], int(consumable_status.sensor_dirty.seconds / 60 / 60))
        client.publish(TOPICS['sensor_filter_hours'], int(consumable_status.filter.seconds / 60 / 60))
        sleep(5*60)

if __name__ == '__main__':
    main()
