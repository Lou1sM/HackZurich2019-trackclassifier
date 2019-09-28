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
    
    def __init__(self, num_classes, device):
        super(CNNClassifier, self).__init__()
        self.device = device
        self.pretrained_cnn = models.vgg19(pretrained=True)
        self.avgpool = nn.AdaptiveAvgPool2d((7,7))
        self.classifier = nn.Sequential(
            #nn.Linear(512 * 7 * 7, 4096),
            nn.Linear(512 * 7 * 7, 1024),
            nn.ReLU(True),
            nn.Dropout(),
            #nn.Linear(4096,1024),
            #nn.ReLU(True),
            #nn.Dropout(),
            nn.Linear(1024, num_classes),
        )
        #elif self.cnn_type == "nasnet":
            #model_name = 'nasnetalarge'
            #self.cnn = pretrainedmodels.__dict__[model_name](num_classes=1000, pretrained='imagenet')

        #self.resize = nn.Linear(self.hidden_size, ARGS.ind_size+1)

    def cnn_vector(self, input_):
        x = self.cnn.features(input_)
        x = self.cnn.avgpool(x)
        x = x.view(x.size(0), -1)
        #x = self.cnn.classifier[0](x)
        #elif self.cnn_type == "nasnet":
            #x = self.cnn.features(input_)
            #x = self.cnn.relu(x)
            #x = self.cnn.avg_pool(x)
            #x = x.view(x.size(0),-1)
        return x

    def forward(self, input_):
        x = self.pretrained_cnn.features(input_)
        #print(x.shape)
        x = self.avgpool(x)
        #print(x.shape)
        x = torch.flatten(x,1)
        #print(x.shape)
        x = self.classifier(x)
        #print(x.shape)

        return x
      
    
def train():
    criterion = nn.BCEWithLogitsLoss() 
    train_generator = load_data('data_dir', batch_size=10, shuffle=True) 
    model = CNNClassifier(4, 'cuda')
    print(torch.cuda.is_available())
    optimizer = optim.Adam(params=model.parameters(), lr=1e-3, weight_decay=0.1)
    for x,y in train_generator:
        #print(x.shape)
        #print(y.shape)
        pred = model(x)
        print(pred)
        #loss = criterion(pred,y)
        #print(loss)
        #loss.backward()
        #optimizer.step()
    
   
if __name__ == "__main__":
    #test_img_file = Image.open("/siemens/data/Trackpictures/Trackpictures_HiRes/001_-_Landquart_-_Klosters_Platz/VIRB0022-1000.JPG")
    #test_img = np.asarray(test_img_file)
    #test_img = torch.tensor(test_img).float()
    #test_img_window = test_img[:256, :256, :].transpose(0,2)
    #test_img_window = test_img_window.unsqueeze(0)
    #print(test_img_window.shape)
    train()
    
    #model = CNNClassifier(4, 'cuda')
    #prediction = model(test_img_window)
    #print(prediction)
