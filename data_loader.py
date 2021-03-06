"""Script to load the data from (input,output) tuples stored as .npz
files. The load_data() function is designed for export. It returns a
generator object that can define a training loop.
"""

import os
import numpy as np
import torch
from torch.utils import data
import matplotlib.pyplot as plt


class VideoDataset(data.Dataset):
    def __init__(self, data_dir):
        #self.file_list= [os.path.join(data_dir, file_name) for file_name in os.listdir(data_dir)]
        self.data_dir = data_dir

    def __getitem__(self, index):
        #img_file_path = self.file_list[index]
        img_file_path = os.path.join(self.data_dir, "img{}.npz".format(index))
        img= np.load(img_file_path)['x']
        ohe = np.load(img_file_path)['y']
        int_target = np.where(ohe==1)[0][0]
        #plt.imshow(np.transpose(img,(2,1,0)))
        #plt.show()
        #return torch.tensor(img).float(), torch.tensor(ohe).long()
        return torch.tensor(img).float().cuda(), torch.tensor(int_target).cuda()

    def __len__(self):
        # Hard code the size of dataset because some files 
        # beyond this point are missing
        return 17917 
        return len(self.file_list)

    def close(self):
        self.archive.close()


def load_data(data_dir, batch_size, shuffle):
    transforms.ToTensor()
    transform = transforms.Compose(
        [transforms.ToTensor()],
        )

    new_data = VideoDataset(data_dir)
    new_data_loaded = data.DataLoader(new_data, batch_size=batch_size, shuffle=shuffle, drop_last=True)

    return new_data_loaded

