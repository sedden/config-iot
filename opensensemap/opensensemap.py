#!/usr/bin/env python

API = 'https://api.opensensemap.org/'
BOX_ID = '58d42511c877fb0011ad4597'

import requests
import sys
import paho.mqtt.client as mqtt

r = requests.get(f"{API}/boxes/{BOX_ID}")
for s in r.json()['sensors']:
    if s['sensorType'] in ['HDC1008', 'DHT22']:
        temp_c = s['lastMeasurement']['value']
        print(temp_c)
        client = mqtt.Client('OpenSenseMap')
        client.connect('raspberrypi.local')
        client.publish(f'opensensemap/status/{BOX_ID}/temperature', temp_c)
        client.disconnect()
        sys.exit()

sys.exit(1)