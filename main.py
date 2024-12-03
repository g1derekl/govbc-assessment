import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from rule import conditions
from rule_engine import Rule

# Load configuration settings from .env file
load_dotenv()

MQTT_SERVER = os.getenv("MQTT_SERVER", "test.mosquitto.org")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1833))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "test/foo/bar")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

rule = Rule(conditions=conditions)

def on_connect(client, userdata, flags, reason_code):
    """Callback function to subscribe to a topic upon successful connection"""
    print(f"Connected with result code {reason_code}")
    client.subscribe(f"BRE/calculateWinterSupplementInput/{MQTT_TOPIC}")

def on_message(client, userdata, msg):
    """Callback function to handle incoming messages from message queue"""
    print(f"Message received at {msg.topic}: {str(msg.payload)}")
    input_ = json.loads(msg.payload)
    try:
        print("Running input data through rule engine")
        output = rule.evaluate(input_)
        print(f"Eligibility determined: {json.dumps(output)}")
        mqttc.publish(f"BRE/calculateWinterSupplementOutput/{MQTT_TOPIC}", json.dumps(output))
    except Exception as e:
        print(f"Error: {e}")
        error_message = "Sorry, an error occurred. Please try again."
        mqttc.publish(f"BRE/calculateWinterSupplementOutput/{MQTT_TOPIC}", error_message)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(MQTT_SERVER, MQTT_PORT)

mqttc.loop_forever()