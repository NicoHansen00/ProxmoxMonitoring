import paho.mqtt.publish as paho_pub
import paho.mqtt.client as paho_cli

class mqtt:
    def __init__(self, hostname: str="localhost", port: int=1883):
        self.hostname = hostname
        self.port = port

    def publish(self, message: str, topic: str="/" ):
        if type(message) and type(topic) is not str:
            raise Exception("Object is not string")
        try:
            paho_pub.single(topic=topic, payload=message, hostname=self.hostname, port=self.port)
        except Exception as ex:
            raise ex
            
    def subscribe(self, topics: str=["/"]):
        try:
            mqttc = paho_cli.Client()
            mqttc.on_connect = self._on_connect
            mqttc.on_message = self._on_message
            mqttc.connect(host=self.hostname, port=self.port)
            if len(topics) > 1:
                print("Subcribed topics:")
            else:
                print("Subscribed topic:")
            for topic in topics:
                print(topic)
                mqttc.subscribe(topic)
            mqttc.loop_forever()
        except Exception as ex:
            mqttc.disconnect()
            raise ex
    
    def _on_connect(self, client, userdata, flags, reason_code):
        print(f"Connected with result code {reason_code}")

    def _on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
