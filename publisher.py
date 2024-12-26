import paho.mqtt.client as mqtt
import os
import time
import random

topic = "message"
broker_ip = '192.168.0.3'
username = 'test'
password = 'test'
message = 'AUTOEVER'

def on_connect(__,userdata,flags,reasonCode):
    if reasonCode == 0:
        print("connected OK")
    else:
        print("Error: connection failed, Return Code =", reasonCode)

def on_disconnect(client, userdata, flags, rc=0):
    print('Disconnected, RC:', rc)

def on_publish(client, userdata, mid):
    print("message published, MID: ", mid)

def make_message(message):
    try:
        return message.encode('utf-8')
    except Exception as e:
        print("Error encoding message: ", e)
        raise

def main(message, broker_ip, username, password, port = 1883):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    try:
        client.username_pw_set(username, password)
        client.connect(broker_ip, port)
        client.loop_start() #client.loop()

        
        message = make_message(message)
        client.publish(topic, message, qos=2)

        client.loop_stop()

        print(f"Success sending message: {message}")
        client.disconnect()
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    while(1):
        main(str(random.randint(0,10000)), broker_ip, username, password)
        time.sleep(1)
