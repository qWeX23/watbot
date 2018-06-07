import os
import cv2
import glob
import argparse
import numpy as np
from tqdm import tqdm

def load_img(path):
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    return img

def load_dir(path,n=None):
    imgs = [load_img(path) for path in tqdm(glob.glob(path)[:n])]
    imgs = np.asarray(imgs)
    return imgs

def shuffle(img,lab):
    indexs = np.arange(len(img))
    np.random.shuffle(indexs)
    simg = img[indexs]
    slab = lab[indexs]
    return simg, slab

if __name__ == '__main__':
    #example: python make_dataset.py /home/alec/datasets/pubg test1
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help='top level directory (containing Dacia)')
    parser.add_argument('suffix', help= 'suffix for file names')
    parser.add_argument('-width', default=48, type=int, help='resize width')
    parser.add_argument('-height', default=27, type=int, help='resize height')

    args = parser.parse_args()
    globals().update(vars(args))

    pos_imgs = load_dir(os.path.join(data_dir, '*/Dacia/*.png'))
    neg_imgs = load_dir(os.path.join(data_dir, '*/NotDacia/*.png'))
    imgs = np.concatenate([pos_imgs, neg_imgs])
    labels = np.concatenate([np.ones(len(pos_imgs)), np.zeros(len(neg_imgs))], 0).astype(np.int32)
    imgs,labels = shuffle(imgs,labels)
    np.save(os.path.join(data_dir, 'imgs_%dw_%dh_%s.npy'%(width, height,suffix)), imgs)
    np.save(os.path.join(data_dir, 'labels_%dw_%dh_%s.npy'%(width, height,suffix)), labels)
