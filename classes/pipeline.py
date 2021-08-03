import numpy as np
import matplotlib.pyplot as plt
import torch
import os

from .Data import create_wrapper
from .Model import saveModel, loadModel


class pipeline():

    def __init__():

        self.model = None
        self.trained_model_dict = None
        self.dataset = None
        self.dataset_dict = {}
        self.loss = None
        self.optimizer = None
        self.plotting = False
        self.device = "cpu"
        self.save = False
        self.save_interval = 1
        self.save_name = ""
        self.save_path = ""

        self.torchvision_list = ["CelebA", "CIFAR10","CIFAR100","Cityscapes","CocoCaptions","CocoDetection",
                                "DatasetFolder","EMNIST","FakeData","FashionMNIST","Flickr30k","Flickr8k", "ImageFolder", "ImageNet",
                                "Kinetics-400","KMNIST", "LSUN", "LSUNClass", "MNIST", "Omniglot", "PhotoTour", "Places365",
                                "QMNIST", "SBD", "SBU", "SEMEION", "STL10",
                                "SVHN", "UCF101","USPS","VOCDetection", "VOCSegmentation"]

        for ds in self.torchvision_list:
            self.add_dataset(ds)

    def set_optimizer(self, optimizer):

        self.optimizer = optimizer

    def set_model(self, model):
        
        self.model = model
    
    def set_loss(self, loss):

        self.loss = loss

    def add_dataset(self, dataset_name):

        self.dataset_dict[dataset_name] = create_wrapper(dataset_name)

    def set_dataset(self, dataset_name):

        self.dataset = self.dataset_dict[dataset]

    def save_model(self, model, name):

        saveModel(model, name)

    def train_model(self):

        model = self.model.to(self.device)

        for epoch in range(self.epochs):

            for i, (x,y) in enumerate(self.dataset):

                # Normal Pytorch Training loop ###

                x = x.to(self.device)
                y = y.to(self.device)

                self.optimizer.zero_grad()

                prediction = model(x)

                loss = self.loss(prediction, y)

                loss.backward()

                self.optimizer.step()

                ###################################
        
            if (self.save_interval is not None and epoch % self.save_interval == 0 and self.save):

                # Will save every "self.save_interval" epochs if save_interval is not None and self.save is True
                # If the later is true but not the former then it will only save after fully training

                self.save_checkpoint(self.save_path, model, epoch)
        
        self.trained_model = model


            

                

        







