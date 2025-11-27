import paho.mqtt.client as paho_cli
from psutil._common import shwtemp
import json
import socket
from pathlib import Path

def sim():

    temp = simulatetemps()
    temps : list[str] = {}

    for key, datas in temp:
        

    

    return {"name" : socket.gethostname(),
            "data": [simulatetemps()] }

def simulatetemps(): 
    return {"acpitz": [shwtemp('', 11, None, None),
                       shwtemp('', 11, None, None)],
            "nvme": [shwtemp('', 23, 89.85, 89.85), 
                     shwtemp('', 23, 89.85, 89.85)],
                "pch_skylake": [shwtemp('', 44, None, None)],
                "coretemp": [shwtemp('Package id 1', 76, 100, 100), 
                        shwtemp('Core 0', 76, 100, 100),
                        shwtemp('Core 1', 76, 100, 100)]}

print(json.dumps(sim()))