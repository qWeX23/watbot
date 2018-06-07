import socket
import sys
from PIL import Image
import io
import threading
from datetime import datetime
import uuid
import time
import os


def log(message):
    print("[ {} ] : {}".format(datetime.now(),message))


def start_up():
    return str(len(os.listdir('../../img')))+'/'

dir_name = start_up()
def make_path(path):
    os.make_dirs(path,exist_ok=True)

def connection_thread(connection, client_address):
    data=b''
    datasave = b''
    type_flag = b''
    try:
        print ('connection from: '+str(client_address))
        # Receive the data
        type_flag = connection.recv(1)
        while True:
            data = connection.recv(1000000)
            if data:
                datasave += data
            else:
                log('no more data from'+str(client_address))
                break
    finally:
        save_dir = 'NotDacia/'
        if(type_flag == b'1'):
            save_dir = 'Dacia/'
        connection.close()
        img = Image.frombytes('RGB',(480,270),datasave)
        path = '../../img/'+dir_name+save_dir
        make_path(path)
        file_name = str(time.time())+'.png'
        img.save(path+file_name)
        log(type_flag)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('192.168.1.64', 8888)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
# Listen for incoming connections
sock.listen()
while True:
    # Wait for a connection
    log('waiting for a connection')
    connection, client_address = sock.accept()
    log('creating thread')
    t = threading.Thread(target=connection_thread, args=(connection,client_address))
    t.start()
