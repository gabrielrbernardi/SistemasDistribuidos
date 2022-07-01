import paho.mqtt.client as mqtt

class MqttClass():
    def __init__(self):
        pass
    
    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def server():
    mqttc = mqtt.Client()
    mqttClass = MqttClass()
    mqttc.on_message = mqttClass.on_message
    mqttc.connect("localhost", 1883, 60)
    mqttc.subscribe("10000/#", 0)
    mqttc.loop_forever()

if __name__ == "__main__":
    server()