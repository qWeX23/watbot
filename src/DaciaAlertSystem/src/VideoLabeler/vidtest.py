import pylab
import imageio
from enum import Enum
from collections import deque
from tqdm import tqdm
import numpy as np
import threading
from PIL import Image

class states(Enum):
    dacia = 0
    not_dacia = 1
class trash_states(Enum):
    trash = 0
    not_trash = 1



def save_img(img,current_state,num):
    #img=img[0]
    img.save(str(current_state.name)+"/test"+str(num)+".png")

def generate_frame_numbers(times,fps):
    return deque([float(convert_to_seconds(i)*fps) for i in times])

def convert_to_seconds(timestamp):
    num_list = [int(i)for i in str(timestamp)]
    total=0
    for i,e in enumerate(reversed(list(num_list))):
        if i == 0:
            total=total+e
        elif i == 1:
            total=total+(e*10)
        elif i == 2:
            total=total+(e*60)
        elif i == 3:
            total=total+((e*10)*60)
        elif i == 4:
            total=total+((e*60)*60)
        elif i == 5:
            total=total(((e*10)*60)*60)
    return float(total)

def generate_trash_time(i,fps):
    factor=2*fps
    return (i-factor, i+factor)

def run(filename,times=[]):
    downsize  = 480,270
    #times = [611,704,1109,1330,1433,1524,2143,2355]
    vid = imageio.get_reader(filename,  'ffmpeg')
    fps = vid.get_meta_data()['fps']
    toggle_times = generate_frame_numbers(times,fps)
    trash_times = [generate_trash_time(i,fps) for i in toggle_times]
    trash_times = [x for xs in trash_times for x in xs]
    trash_times = deque(trash_times)
    if toggle_times:
        current_time = toggle_times.popleft()
    else:
        current_time = -1
    if trash_times:
        current_trash_time = trash_times.popleft()
    else:
        current_trash_time = -1
    current_state = states.not_dacia
    trash_state = trash_states.not_trash
    for num, image in tqdm(enumerate(vid.iter_data())):
        #toggle current state
        if float(current_time) == num:
            if current_state == states.dacia:
                current_state = states.not_dacia
            else:
                current_state = states.dacia
            if toggle_times:
                current_time = toggle_times.popleft()
        #toggle trash time
        if current_trash_time == num:
            if trash_state == trash_states.not_trash:
                trash_state = trash_states.trash
            else:
                trash_state = trash_states.not_trash
            if trash_times:
                current_trash_time = trash_times.popleft()

        if trash_state == trash_states.not_trash:
            i=Image.fromarray(image)
            i.thumbnail(downsize)
            threading.Thread(target=save_img,args=(i,current_state,num)).start()
						
if __name__ == "__main__":
	
	import argparse

	parser = argparse.ArgumentParser(description='Process vids.')
	parser.add_argument('file', type=str, nargs='1',
                    help='filepath')

	args = parser.parse_args()
	