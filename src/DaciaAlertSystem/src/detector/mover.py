import os
import glob
import shutil
from collections import Counter

src_dir = '/home/qwex/Desktop/dirty/1/Dacia/'
dst_dir = '/home/qwex/Desktop/dirty/1/NotDacia/'

src_paths = glob.glob(os.path.join(src_dir,'**'))

src_fnames = [os.path.basename(src_path) for src_path in src_paths]
src_floats = [float(src_fname[:-4]) for src_fname in src_fnames]

begin=1505092772.3439262
end=1505093551.4946036

move_fnames = [src_fname for src_float,src_fname in zip(src_floats,src_fnames) if begin <= src_float and end >= src_float]

src_paths=[os.path.join(src_dir,move_fname) for move_fname in move_fnames]
dst_paths=[os.path.join(dst_dir,move_fname) for move_fname in move_fnames]

for src_path,dst_path in zip(src_paths,dst_paths):
    shutil.move(src_path,dst_path)
    print ("moved "+dst_path)
