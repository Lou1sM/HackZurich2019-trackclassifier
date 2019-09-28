import os
from PIL import Image
from PIL import ExifTags
import numpy as np
import maptracks

maptracks.load()
balise_file_paths = maptracks.get_with('balise')
distsig_file_paths = maptracks.get_with('distant_signal')
mainsig_file_paths = maptracks.get_with('main_signal')

img_dir = '/siemens/data/Trackpictures/Trackpictures_HiRes/001_-_Landquart_-_Klosters_Platz'

data, images = maptracks.load()

neg_file_names = [f for f in os.listdir(img_dir) if f not in balise_file_paths and f not in distsig_file_paths and f not in mainsig_file_paths]
print(neg_file_names[-1])
print(len(neg_file_names))

it = 4502
for neg_file_name in neg_file_names:
    img_file_path = os.path.join(img_dir, neg_file_name)
    try:
        img_file = Image.open(img_file_path)
        np_img = np.asarray(img_file)
        a = np_img.shape[0]
        b = np_img.shape[1]
        i = np.random.randint(a-256)
        j = np.random.randint(b-256)
        it += 1
        if it%100 == 0:
            print(it)
        img_window = np_img[i:i+256,j:j+256,:]
        img_window = np.transpose(img_window, (2,1,0))
        file_name = "data_dir/img{}.npz".format(2*it-1)
        ohe = np.array([0,0,0,1])
        np.savez(file_name, x=img_window, y=ohe)
    except Exception as e:
        print('ERROR:', e)
 
