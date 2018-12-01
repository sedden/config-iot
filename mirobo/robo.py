#!/usr/bin/env python

import os
import logging
from time import sleep
import miio
import paho.mqtt.client as mqtt

TOPICS = {}

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.is_connected=True
        logging.info('Connected')
    else:
        logging.error(f'Connection error, code={rc}')


def on_disconnect(client, userdata, rc):
    client.is_connected=False
    if rc==0:
        logging.info('Disconnected')
    else:
        logging.error(f'Disconected due to an error, code={rc}')


def main():
    logging.basicConfig(level=logging.INFO)

    ip = os.environ.get('MIROBO_IP')
    token = os.environ.get('MIROBO_TOKEN')

    vac = miio.Vacuum(ip, token)
    info = vac.info()
    device_identifier = info.mac_address.replace(':', '').lower()

    TOPICS['firmware_version'] = f'mirobo/status/{device_identifier}/firmware_version'
    TOPICS['battery'] = f'mirobo/status/{device_identifier}/battery'
    TOPICS['fanspeed'] = f'mirobo/status/{device_identifier}/fanspeed'
    TOPICS['is_on'] = f'mirobo/status/{device_identifier}/is_on'
    TOPICS['sensor_dirt_hours'] = f'mirobo/status/{device_identifier}/sensor_dirt_hours'
    TOPICS['filter_hours'] = f'mirobo/status/{device_identifier}/filter_hours'
    TOPICS['main_brush_hours'] = f'mirobo/status/{device_identifier}/main_brush_hours'
    TOPICS['side_brush_hours'] = f'mirobo/status/{device_identifier}/side_brush_hours'
    TOPICS['cleaning_summary_count'] = f'mirobo/status/{device_identifier}/cleaning_summary_count'
    TOPICS['cleaning_summary_total_area'] = f'mirobo/status/{device_identifier}/cleaning_summary_total_area'
    TOPICS['cleaning_summary_total_hours'] = f'mirobo/status/{device_identifier}/cleaning_summary_total_hours'

    mqtt.Client.is_connected=False
    client = mqtt.Client('mirobo')
    client.on_connect=on_connect
    client.on_disconnect=on_disconnect
    client.loop_start()
    client.connect('mosquitto', 1883, 60)
    while True:
        try:
            # device info
            publish(client, TOPICS['firmware_version'], info.firmware_version)

            # status
            status = vac.status()
            publish(client, TOPICS['battery'], float(status.battery))
            publish(client, TOPICS['fanspeed'], status.fanspeed)
            publish(client, TOPICS['is_on'], status.is_on)

            # consumables
            consumable_status = vac.consumable_status()
            publish(client, TOPICS['sensor_dirt_hours'], float(consumable_status.sensor_dirty.total_seconds() / 3600))
            publish(client, TOPICS['filter_hours'], float(consumable_status.filter.total_seconds() / 3600))
            publish(client, TOPICS['main_brush_hours'], float(consumable_status.main_brush.total_seconds() / 3600))
            publish(client, TOPICS['side_brush_hours'], float(consumable_status.side_brush.total_seconds() / 3600))

            # cleaning stats
            clean_history = vac.clean_history()
            publish(client, TOPICS['cleaning_summary_count'], float(clean_history.count))
            publish(client, TOPICS['cleaning_summary_total_area'], float(clean_history.total_area))
            publish(client, TOPICS['cleaning_summary_total_hours'], float(clean_history.total_duration.total_seconds() / 3600))
        except:
            logging.error("Error getting device status")
        sleep(5*60)


def publish(client, topic, payload):
    while not client.is_connected:
        logging.info('Waiting for connection')
        sleep(1)
    logging.info(f'Publishing {topic} {payload}')
    client.publish(topic, str(payload))


if __name__ == '__main__':
    main()
