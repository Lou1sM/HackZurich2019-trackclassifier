"""Script containing the functions for building, training and testing
the prediction CNN. This CNN is trained to predict whether image pat-
ches contain one of three railway devices. At test time it examines
all patches in the image separately to determine a classification for
the overall image.
"""

import json
import os
import math
import numpy as np
import random
from random import shuffle
import re
import string
import time
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, models, transforms
from early_stopper import EarlyStopper
from data_loader import load_data
#import pretrainedmodels


class CNNClassifier(nn.Module):
    """Class containing the classifier CNN."""
    def __init__(self, num_classes, device):
        super(CNNClassifier, self).__init__()
        self.device = device
        self.pretrained_cnn = models.vgg19(pretrained=True)
        self.avgpool = nn.AdaptiveAvgPool2d((7,7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096,1024),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(1024, num_classes),
        )

    def forward(self, input_):
        x = self.pretrained_cnn.features(input_)
        x = self.avgpool(x)
        x = torch.flatten(x,1)
        x = self.classifier(x)

        return x
      
    
def train(restore=None):
    """Train the network on a dataset of 256*256
    image patches, which are annotated with classes
    from 1-4.
    """

    if restore:
        model = torch.load(restore)['model']
    else:
        model = CNNClassifier(num_classes=4, device='cuda')
    criterion = nn.CrossEntropyLoss() 
    train_generator = load_data('../data_dir', batch_size=6, shuffle=True) 
    model.cuda()
    earlystopper = EarlyStopper(patience=5)
    optimizer = optim.Adam(params=model.parameters(), lr=1e-6)
    num_epochs = 10
    batch_idx = 0
    save_dict = {'model': model}
    remembered_accs = []
    for epoch in range(num_epochs):
        print("Epoch:", epoch)
        for x,y in train_generator:
            batch_idx += 1
            pred = model(x)
            loss = criterion(pred,y)
            int_pred = torch.argmax(pred, dim=-1)
            batch_acc = torch.sum(int_pred == y).item()/6
            remembered_accs.append(batch_acc)
            if batch_idx % 100 == 0:
                chunk_acc = sum(remembered_accs[-100:])/100
                checkpoint_path = 'checkpoints/{}.pt'.format(int(batch_idx/100))
                earlystopper(chunk_acc, save_dict, checkpoint_path=checkpoint_path)
                if earlystopper.early_stop:
                    return checkpoint_path
            loss.backward()
            optimizer.step()
   
def test(model, img, label, thresh):
    """Test whether the model correctly classifies a 
    single img. Each patch is examined separately, and
    if any devices are found, to a given threshold of 
    confidence, then the most commonly predicted one 
    is returned as the prediction for the whole image. 

    ARGS:
        model: CNN to be tested
        img: img to be tested on
        label: ground truth label for the image
        threshold: confidence above which classificat-
                    ion is made
    """

    a = img.shape[0]
    b = img.shape[1]
    img_ohe_pred = torch.tensor([0,0,0,0])
    for i in range(0, a-256, 256):
        for j in range(0, b-256, 256):
            img_patch = img[i:i+256, j:j+256, :]
            ohe_pred = model(img_patch)
            pred = np.where(ohe_pred==1)[0][0]
            img_ohe_pred += ohe_pred
    object_preds = img_ohe_pred[:-1]
    object_confidence = torch.max(object_preds)
    if object_confidence > thresh:
        img_pred = torch.argmax(object_preds)
    else:
        img_pred = 3
    return img_pred == label


def dev_id_from_img_path(img_file_name, annot_data):
    """Find the device id (ie the classification) for an 
    image, given its file_name.

    ARGS:
        img_file_name (str): the given filename
        annot_data: json object containing device id info
    """
    
    img_id_list = [img['id'] for img in annot_data['images'] if img['file_name'].split('/')[1]  == img_file_name]
    if len(img_id_list) == 0:
        return 3
    elif len(img_id_list)==1:
        img_id = img_id_list[0]
        dev_id_list = [annot['category_id'] for annot in annot_data['annotations'] if annot['image_id'] == img_id]
        return dev_id_list[0]
    else:
        return None #Ignore images with multiple objects for now


def annotate_new_img(model, img_file_path, thresh=1):
    model.batch_size = 1
    img = torch.tensor(np.asarray(Image.open(img_file_path))).float().transpose(0,2).unsqueeze(0).cuda()
    img = img[:,:,1000:-1000,750:-750]
    a = img.shape[2]
    b = img.shape[3]
    for i in range(0, a-256, 256):
        for j in range(0, b-256, 256):
            img_patch = img[:, :, i:i+256, j:j+256]
            #pred = model(img_patch).cpu().detach().numpy()
            pred = model(img_patch)
            pred = torch.argmax(pred)
            if pred < 3 and torch.max(pred) > 0.4::
                return list(np.eye(4)[pred])
    return [0,0,0,1]
    

    
   
if __name__ == "__main__":
    #best_checkpoint_path = train()
    #model = torch.load(best_checkpoint_path)['model']
    model = torch.load('checkpoints/38.pt')['model']
    model.cuda()

    #img_paths = [os.path.join('test_imgs', fname) for fname in os.listdir('test_imgs')]
    with open('COCO.json') as f:
        annot_data = json.load(f)
    #imgs = [(np.asarray(Image.open(os.path.join('test_imgs', img_file_name))), dev_id_from_img_path(img_file_name, annot_data)) for img_file_name in os.listdir('test_imgs')]
    #imgs = list(filter(lambda img: img[1] != None, imgs))

    #unannotated_imgs = [os.path.join('test_imgs', img_file_name) for img_file_name in os.listdir('test_imgs')]
    unannotated_imgs = [os.path.join('Trackpictures_HiRes', '006_-_Klosters_Platz_-_Landquart', img_file_name) for img_file_name in os.listdir('Trackpictures_HiRes/006_-_Klosters_Platz_-_Landquart')]
    json_list = []
    for img_file_name in unannotated_imgs:
        annotation = annotate_new_img(model, os.path.abspath(img_file_name))
        json_list.append({'name': os.path.abspath(img_file_name), 'object': annotation})
        print(len(json_list))
    annotated_imgs = [{'name': os.path.abspath(img_file_name), 'object' : annotate_new_img(model, os.path.abspath(img_file_name))} for img_file_name in unannotated_imgs]  

    with open('annotated.json', 'w') as f:
        json.dump(annotated_imgs, f)


    # TODO: continue code for searching for a prediction threshold
    """
    best_thresh_acc = 0
    best_thresh = -1
    thresh_results = []
    for thresh in range(20):
        for img, label in imgs:
            new_result = test(model, img, label, thresh)
            thresh_results.append(new_result)
        thresh_acc = sum(thresh_results)/len(thresh_results)
        if thresh_acc > best_thresh_acc:
            best_thresh_acc = thresh_acc
            best_thresh = thresh
    print('Best thresh:', best_thresh)
    print('Best thresh acc:', best_thresh_acc)
    """
    
    
