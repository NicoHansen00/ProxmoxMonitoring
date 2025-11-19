import sys
import psutil
from psutil._common import shwtemp
from mqtt import mqtt
from store import store

def main():
    try:
        publish(psutil.sensors_temperatures() if len(sys.argv) < 2 else simulatetemps())
    except Exception as ex:
        print(ex)

def simulatetemps(): 
    temperature = store.increment()
    return {"acpitz": [shwtemp(label='', current=temperature, high=None, critical=None), 
                       shwtemp(label='', current=temperature, high=None, critical=None)],
            "nvme": [shwtemp(label='Composite', current=temperature, high=89.85, critical=93.85), 
                     shwtemp(label='Sensor 2', current=temperature, high=89.85, critical=89.85)],
            "pch_skylake": [shwtemp(label='', current=temperature, high=None, critical=None)],
            "coretemp": [shwtemp(label='Package id 0', current=temperature, high=100.0, critical=100.0), 
                         shwtemp(label='Core 0', current=temperature, high=100.0, critical=100.0),
                         shwtemp(label='Core 1', current=temperature, high=100.0, critical=100.0)]}

def publish(data: dict[str, list[shwtemp]] ):
    client = store.mqttbrokerinfo()
    mqttc = mqtt(client["ip"], client["port"])
    for name, entries in data.items():
        topic = "CPU/" + name + "/"
        for entry in entries:
            label = entry.label if len(entry.label) != 0 else entries.index(entry).__str__()
            mqttc.publish(entry.current, topic + label + "/current")
            mqttc.publish(entry.high, topic + label + "/high")
            mqttc.publish(entry.critical, topic + label + "/critical")

main()