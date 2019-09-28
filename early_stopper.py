import os
import numpy as np
import torch

class EarlyStopper:
    """Early stops the training if validation loss doesn't improve after a given patience."""
    def __init__(self, patience=7, verbose=False):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement. 
                            Default: False
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.early_stop = False
        self.max_acc = 0
        self.best_model = None

    def __call__(self, acc, model, checkpoint_path):

        if acc > self.max_acc:
            print('Accuracy increased from {} to {}, saving to {}'.format(self.max_acc, acc, checkpoint_path))
            self.save_checkpoint(acc, model, checkpoint_path)
            self.max_acc = acc
            self.best_model = model
            self.counter = 0
        else:
            self.counter += 1
            print('Val loss was {}, no improvement on best of {}'.format(acc, self.max_acc))
            print('EarlyStopping counter: {} out of {}'.format(self.counter, self.patience))
            if self.counter >= self.patience:
                self.early_stop = True

    def save_checkpoint(self, acc, model_dict, checkpoint_path):
        '''Saves model when validation loss decrease.'''
        try:
            torch.save(model_dict,checkpoint_path)
        except FileNotFoundError:
            print("Can't save file to {} because the directory doesn't exist.".format(filename))
        self.max_acc=acc 
        
