from fastapi import FastAPI
import paho.mqtt.client as paho_cli
import threading

app = FastAPI()

class SharedData:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = ""

shared_data = SharedData()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/ProxmoxMonitoring/#")


def on_message(client, userdata, msg):
    decoded = msg.payload.decode()
    print(f"Received: {decoded}")
    
    with shared_data.lock:
        shared_data.value = decoded

def start_mqtt():
    mqttc = paho_cli.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect("localhost", 1883)
    mqttc.loop_forever()   # run forever in this thread

@app.on_event("startup")
def startup_event():
    t = threading.Thread(target=start_mqtt, daemon=True)
    t.start()

@app.get("/")
async def root():
    with shared_data.lock:
        return {"data": shared_data.value}
