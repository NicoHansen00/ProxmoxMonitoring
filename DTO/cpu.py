import sys
import psutil
import socket
import json
from psutil._common import shwtemp
from ..Common.mqtt import mqtt
from ..Common.store import store

def main():
    try:
        publish(psutil.sensors_temperatures() if len(sys.argv) > 1 else sim())
    except Exception as ex:
        print(ex)

def sim():
    return {"name" : socket.gethostname(),
            "data": [simulatetemperatures()] }

def read():
    return {"name" : socket.gethostname(),
            "data": [psutil.sensors_temperatures()] }

def simulatetemperatures(): 
    temperature = store.increment()
    return {"acpitz": [{"label":'', "current": temperature, "high":None, "critical":None},
                       {"label":'', "current": temperature, "high":None, "critical":None}],
            "nvme": [{"label":'Composite', "current":temperature, "high":89.85, "critical":93.85}, 
                     {"label":'Sensor 2', "current":temperature, "high":89.85, "critical":89.85}],
                "pch_skylake": [{"label":'', "current":temperature, "high":None, "critical":None}],
                "coretemp": [{"label":'Package id 0', "current":temperature, "high":100.0, "critical":100.0}, 
                        {"label":'Core 0', "current":temperature, "high":100.0, "critical":100.0},
                        {"label":'Core 1', "current":temperature, "high":100.0, "critical":100.0}]}

def publish(data: dict[str, list[shwtemp]] ):
    client = store.mqttbrokerinfo()
    mqttc = mqtt(sys.argv[1], client["port"])
    topic = "ProxmoxMonitoring/" + socket.gethostname() + "/CPU/"
    mqttc.publish(json.dumps(data), topic)

main()