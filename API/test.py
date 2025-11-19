import paho.mqtt.client as paho_cli
from psutil._common import shwtemp
import json
from pathlib import Path

data: dict[str, list[shwtemp]]

message = "ProxmoxMonitoring/udesktop/CPU/acpitz/0/current"

def subscribe():
    try:
        mqttc = paho_cli.Client()
        mqttc.on_connect = _on_connect
        mqttc.on_message = _on_message
        mqttc.connect(host="localhost")
        mqttc.subscribe("ProxmoxMonitoring/#")
        mqttc.loop_forever()
    except Exception as ex:
        mqttc.disconnect()
        raise ex

def _on_connect(client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")

def _on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

subscribe()