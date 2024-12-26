import paho.mqtt.client as mqtt
import base64
import os
from kvaser_can import Kvaser
from kvaser_can import split_data_into_chunks
import time
import tqdm

topic_file = 'file'
topic_name = 'file_name'
topic_user = 'user'
userId = 'admin'
userPw = '1234'
broker_ip = '192.168.65.1'

file_name = None
file_data = None
user_name = None

def on_connect(client, userdata, flags, reasonCode):
    if reasonCode == 0:
        print("Connected successfully.")
        client.subscribe(topic_file)
        client.subscribe(topic_name)
        client.subscribe(topic_user)

    else:
        print(f"Failed to connect, return code {reasonCode}")

def on_disconnect(client, userdata, flags, rc = 0):
    print(str(rc) + '/')

def on_messagee(client, userdata, msg):
    global file_name, file_data, user_name
    try:
        payload = msg.payload.decode('utf-8')        
        topic = msg.topic
        if topic == topic_file:
            file_data = base64.b64decode((payload))
        elif topic == topic_name:
            file_name = payload
        elif topic == topic_user:
            user_name = payload

        if file_data and file_name and user_name:
            tmp_dir = os.path.join(os.getcwd(), 'temporary') # import os 
            os.makedirs(tmp_dir, exist_ok= True)
            file_path = os.path.join(tmp_dir, file_name)
            with open(file_path, 'wb') as file:
                file.write(file_data)
            print(f"Receive the file from {user_name}: {file_name}")

            update_flag = 1
            while(update_flag):
                choose = input("Do you want to update?(yes/no)")
                if choose == 'yes':
                    with open(file_path, 'rb') as file:
                        data = file.read()
                    message = file_name.encode('utf-8') + b':' + data
                    flag = 1
                    i = 0
                    while(flag):
                        try:
                            send_file(message)
                            flag = 0
                            print(i)
                            i += 1
                        except:
                            print("Retry send file")
                            time.sleep(5)
                    print("Send success!")
                    update_flag = 0
                else:
                    print("wait 10 second")
                    time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")

def send_file(message):
    transmitter = Kvaser()
    message = transmitter.mkdata(message)
    chunks = split_data_into_chunks(message)
    for chunk in tqdm.tqdm(chunks):
        transmitter.transmit_data(123, chunk)
        time.sleep(0.02) # import time

def check_update():
    tmp_dir = os.path.join(os.getcwd(), 'temporary')
    update_list = os.listdir(tmp_dir)
    if update_list:
        for file in update_list:
            try:
                file_path = os.path.join(tmp_dir, file)
                update_flag = 1
                while(update_flag):
                    choose = input("Do you want to exist update?(yes/no)")
                    if choose == 'yes':
                        with open(file_path, 'rb') as file:
                            data = file.read()
                        message = file_name.encode('utf-8') + b':' + data
                        flag = 1
                        i = 0
                        while(flag):
                            try:
                                send_file(message)
                                flag = 0
                                print(i)
                                i += 1
                            except:
                                print("Retry send file")
                                time.sleep(5)
                        print("Send success!")
                        update_flag
                    else:
                        print("wait 10 second")
                        time.sleep(10)
            except:
                print("Update Error")

def main():
    port = 1883
    client = mqtt.Client()
    client.username_pw_set(userId, userPw)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_messagee
    client.connect(broker_ip, port, keepalive = 60)
    client.loop_forever()

if __name__ == "__main__":
    main()