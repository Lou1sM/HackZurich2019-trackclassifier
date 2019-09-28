import os
from PIL import Image
from PIL import ExifTags
import numpy as np
import maptracks

img_file = "/siemens/data/Trackpictures/Trackpictures_HiRes/001_-_Landquart_-_Klosters_Platz/VIRB0022-1000.JPG"

img = Image.open(img_file)
np_img = np.asarray(img)
#exif_data = img._getexif()
exif_data = {ExifTags.TAGS[k]:v for k,v in img._getexif().items() if k in ExifTags.TAGS}
print(exif_data.keys())
maptracks.load()

balise_file_paths = maptracks.get_with('balise')
distsig_file_paths = maptracks.get_with('distant_signal')
mainsig_file_paths = maptracks.get_with('main_signal')


print(len(balise_file_paths), len(distsig_file_paths), len(mainsig_file_paths))
print(len(list(set(balise_file_paths).intersection(set(distsig_file_paths),set(mainsig_file_paths)))))

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

# Now create negative examples

"""
for img_id, img_file_name in img_file_name_by_id.items():
    img_file_path = os.path.join(img_dir, img_file_name)
    img_file = Image.open(img_file_path)
    np_img = np.asarray(img_file)
    annots = annot_by_id[img_id]
    print('num_annots', len(annots))
    #if img_filepath in balise_file_paths:
        #img_y = np.array([0,1,0,0])
    #elif img_filepath in distsig_file_paths:
        #img_y = np.array([0,0,1,0])
    #elif img_filepath in mainsig_file_paths:
        #img_y = np.array([0,0,0,1])
    #else:
        #img_y = np.array([1,0,0,0])

    a = np_img.shape[0]
    b = np_img.shape[1]

    it = 0
    for i in range(0,a-256,256):
        for j in range(0,b-256,256):
            it += 1
            img_window = np_img[i:i+256,j:j+256,:]
            img_window = np.transpose(img_window, (2,1,0))
            file_name = "data_dir/img{}.npz".format(it)
            #for a in annots:
                #print(a['segmentation'][0][0] > i )
                #print(a['segmentation'][0][1] > j )
                #print(a['segmentation'][0][2] < i+256 )
                #print(a['segmentation'][0][3] < j+256 )
            cat_ids = [a['category_id'] for a in annots if a['segmentation'][0][0] > i and a['segmentation'][0][2] < i+256 and a['segmentation'][0][1] > j and a['segmentation'][0][3] < j+256 and a['image_id'] == img_id]
            
            if len(cat_ids) == 0:
                cat_id = 3
            elif len(cat_ids) == 1:
                cat_id = cat_ids[0]
            else:
                print(img_id)
                print(cat_ids)
            assert(len(cat_ids) <= 1)
            try:
                ohe = np.eye(4)[cat_id]
            except Exception as e:
                print(e, cat_id)
            print('catid', cat_id)
            np.savez(file_name, x=img_window, y=ohe)
"""

