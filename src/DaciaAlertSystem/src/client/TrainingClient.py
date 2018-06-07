from socket import *
from PIL import Image
from PIL import ImageGrab
import sys
import socket
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading
from queue import Queue
from enum import Enum

def log(message):
    print("[ {} ] : {}".format(datetime.now(),message))

class TypeFlagEnum(Enum):
    Not= b'0'
    Dacia = b'1'
cap_type_flag = TypeFlagEnum.Not


downsize  = 480,270
def take_screencap():
    img = ImageGrab.grab()
    img.thumbnail(downsize)
    #log('mode: '+str(img.mode))
    #log('size: '+str(img.size))
    img = img.tobytes()
    size = sys.getsizeof(img)
    log('Capture made size:'+str(size))
    return img, size

def send_image():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.1.64', 8888)

    try:
        #log('connecting to %s port %s' % server_address)
        sock.connect(server_address)
        message,x = take_screencap()
        #img = Image.frombytes('RGB',(1920,1080),message)

        sock.sendall(type_flag_q.queue[0].value)
        sock.sendall(message)
    except:
        #log('')
        log("Unexpected error:"+str(sys.exc_info()[0]))
    finally:
        log('closing socket')
        sock.close()

def run_thread():
    run = True
    if run_flag_q.get():
        while run:
            log(run_flag_q.qsize())
            if run_flag_q.empty()!=True:
                run = run_flag_q.get()
            send_image()

def start():
    run_flag_q.put(True)
    log(run_flag_q.qsize())
    t = threading.Thread(target=run_thread)
    t.start()

def dacia():
    type_flag_q.get()
    type_flag_q.put(TypeFlagEnum.Dacia)

def Not():
    type_flag_q.get()
    type_flag_q.put(TypeFlagEnum.Not)


def stop():
    run_flag_q.put(False)
    log(run_flag_q.qsize())
    log("Stopping...")

type_flag_q = Queue()
type_flag_q.put(TypeFlagEnum.Not)
run_flag_q = Queue()
top = tk.Tk()

start_button = tk.Button(top, text ="Start", command = start)
dacia_button = tk.Button(top, text="DACIA",command=dacia)
not_button = tk.Button(top,text="Not",command= Not)
stop_button = tk.Button(top,text="Stop",command = stop)


start_button.pack()
dacia_button.pack()
not_button.pack()
stop_button.pack()
top.mainloop()
