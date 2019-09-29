"""Script to make the positive training examples. Images are selected
that are known to contain a given object at a given region, and a num-
ber of image patches containing this region are selected.
"""

import os
from PIL import Image
from PIL import ExifTags
import numpy as np
import maptracks


balise_file_paths = maptracks.get_with('balise')
distsig_file_paths = maptracks.get_with('distant_signal')
mainsig_file_paths = maptracks.get_with('main_signal')


img_file_name_by_id, annot_by_id = maptracks.get_full_img_with()
img_dir = '/siemens/data/Trackpictures/Trackpictures_HiRes'
data, images = maptracks.load()

it=0
for annot in data['annotations']:
    img_file_name = img_file_name_by_id[annot['image_id']]
    
    print(img_file_name)
    img_file_path = os.path.join(img_dir, img_file_name)
    img_file = Image.open(img_file_path)
    np_img = np.asarray(img_file)
    img_patches = []
    x1= int(annot['bbox'][0])
    y1= int(annot['bbox'][1])
    x2= x1+int(annot['bbox'][2])
    y2 =y1+int(annot['bbox'][3])
    for i in range(y2-256, y1, 100):
        for j in range(x2-256,x1,100):
            it+=1
            img_patch = np_img[i:i+256,j:j+256,:]
            img_patch = np.transpose(img_patch, (2,1,0))
            ohe = np.eye(4)[annot['category_id']]
            file_name = "data_dir/img{}.npz".format(2*it)
            np.savez(file_name, x=img_patch, y=ohe)
            #print(ohe)


