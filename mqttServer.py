import paho.mqtt.client as mqtt

class MqttClass():
    def __init__(self):
        pass
    
    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + "\n")

def server():
    print("Mosquitto Iniciado")
    mqttc = mqtt.Client()
    mqttClass = MqttClass()
    mqttc.on_message = mqttClass.on_message
    mqttc.connect("localhost", 1883, 60)
    # m = mqttc.subscribe("content/#/#", 0)

    mqttc.subscribe("content/+/+", 0)

    mqttc.loop_forever()

if __name__ == "__main__":
    try:
        server()
    except:
        print("Erro generico no Mosquitto")