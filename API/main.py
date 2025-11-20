from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT
import threading

class SharedData:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = ""

shared_data = SharedData()

fast_mqtt = FastMQTT(config=MQTTConfig())

@asynccontextmanager
async def _lifespan(_app: FastAPI):
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()

app = FastAPI(lifespan=_lifespan)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("ProxmoxMonitoring/#")
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

    with shared_data.lock:
        shared_data.value = payload.decode()
    return 0

@fast_mqtt.subscribe("my/mqtt/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/")
async def func():
    with shared_data.lock:
        return {"data": shared_data.value}