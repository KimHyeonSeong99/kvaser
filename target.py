import os
from kvaser_can import Kvaser

file_dir = 'Downloads'

def receive_file():
    transmitter = Kvaser()
    msg = transmitter.read(123)
    try:
        if msg.data == bytearray(b'\xff\x00\xff\x00\xff\x00\xff\x00'):
            flag = 1
            print('receive the flag')
            file = bytearray()
            while(flag):
                msg = transmitter.read(123)
                print(f"{msg.data}",end ='\r', flush=True)
                if msg.data == bytearray(b'\x00\xff\x00\xff\x00\xff\x00\xff'):
                    flag = 0
                else:
                    file.extend(msg.data)
            
            SplitMessage = file.split(":",1)
            file_name = SplitMessage[0].decode('utf-8')
            file_data = SplitMessage[1]

            with open(os.path.join(file_dir, file_name), "wb") as f:
                f.write(file_data)
            print("end to save the file")
            file.clear
    
    except:
        pass
        
def main():
    while True:
        receive_file()

if __name__ == "__main__":
    main()