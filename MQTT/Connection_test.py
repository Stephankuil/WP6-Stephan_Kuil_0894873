import paho.mqtt.client as mqtt

BROKER = "4abaa784a435421ba0190c9884dd2b89.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "Stephan"
PASSWORD = "Geheimwachtwoord1"

def on_connect(client, userdata, flags, rc):
    print("Connect result:", rc)

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()

client.on_connect = on_connect

client.connect(BROKER, PORT)
client.loop_start()

input("Enter om te stoppen...\n")
client.loop_stop()