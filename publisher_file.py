import paho.mqtt.client as mqtt
import os
import time
import random
import base64

topic_name = "file_name"
topic_file = "file"
topic_user = "user"
broker_ip = '192.168.65.1'
username = 'test' #broker id
password = 'test' #broker pw

def on_connect(__,userdata,flags,reasonCode):
    if reasonCode == 0:
        print("connected OK")
    else:
        print("Error: connection failed, Return Code =", reasonCode)

def on_disconnect(client, userdata, flags, rc=0):
    print('Disconnected, RC:', rc)

def on_publish(client, userdata, mid):
    print("message published, MID: ", mid)

def make_message(file_path):
    try:
        with open(file_path, "rb") as file:
            message = base64.b64encode(file.read()) #추가 import base64
        return message
    except FileNotFoundError as e:
        print("Error File not find: ", e)
        raise
    except Exception as e:
        print("Error encoding message: ", e)
        raise

def send_file_to_broker(publish_file, broker_ip, username, password, port = 1883):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    try:
        client.username_pw_set(username, password)
        client.connect(broker_ip, port)
        client.loop_start() #client.loop()

        message = make_message(publish_file)
        file_name = os.path.basename(publish_file)
        client.publish(topic_name, file_name, qos = 2)
        client.publish(topic_user, username, qos = 2)
        client.publish(topic_file, message, qos= 2)

        client.loop_stop()

        client.disconnect()
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    while(1):
        time.sleep(1)
