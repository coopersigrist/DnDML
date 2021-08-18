import numpy as np
import matplotlib.pyplot as plt
import pickle
import torch
import os

from .Data import create_data_wrapper
from .Loss import create_loss_wrapper
from .Model import saveModel, loadModel
from .Optimizer import create_optim_wrapper



class Workspace():

    def __init__(self, saved_workspace = "default.pt"):


        # Checks whether saved_workspace exists -- if so loads it instead of initializing a new one
        if os.path.exists(saved_workspace):
            with open(saved_workspace, 'rb') as f:
                self = pickle.load(f)
                return

        
        self.model = None
        self.trained_model_dict = {}
        self.dataset = None
        self.datasets_dict = {}
        self.loss = None
        self.losses_dict = {}
        self.optimizer = None
        self.optimizers_dict = {}
        self.modules_dict = {}
        self.plotting = False
        self.plot = None
        self.plot_defaults_dict = {}
        self.plotted_val_dict = {}
        self.saved_plots_dict = {}
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
    
        self.torch_optim_list = ["Adadelta","Adagrad","Adam","AdamW","SparseAdam","Adamax",
                            "ASGD","LBFGS","RMSprop","Rprop","SGD"]
        for optim in self.torch_optim_list:
            self.add_optimizer(optim)

        self.torch_loss_list = ["L1Loss","MSELoss","CrossEntropyLoss","CTCLoss","NLLLoss","PoissonNLLLoss",
                                "GaussianNLLLoss","KLDivLoss","BCELoss","BCEWithLogitsLoss","MarginRankingLoss","HingeEmbeddingLoss", 
                                "MultiLabelMarginLoss", "HuberLoss","SmoothL1Loss","SoftMarginLoss", "MultiLabelSoftMarginLoss", 
                                "CosineEmbeddingLoss", "MultiMarginLoss","TripletMarginLoss", "TripletMarginWithDistanceLoss"]
        for loss in self.torch_loss_list:
            self.add_optimizer(loss)

    def save_workspace(self, save_name):
        # Saves the current Workspace to a pickle file with name save_name -- 
        # this lets us save different groupings of modules, data, etc

        # TODO Ideally we also save something to identify this workspace for users (maybe a PNG of the model)

        with open(save_name+'.pt', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

        pass

    def delete_workspace(self):
        # TODO First delete all of the data and all other saved elements from this workspace,
        # then delete this workspace and the corresponding pickle file

        pass

    def add_optimizer(self, optimizer_name):
        
        self.optimizers_dict[optimizer_name] = create_optim_wrapper(optimizer_name)

    def set_optimizer(self, optimizer_name):

        self.optimizer = self.optimizers_dict[optimizer_name]


    def set_model(self, model_name):
        
        self.model = self.trained_model_dict[model_name]
    
    def add_loss(self, loss_name):
        
        self.losses_dict[loss_name] = create_loss_wrapper(loss_name)

    def set_loss(self, loss_name):

        self.loss = self.losses_dict[loss_name]

    def add_dataset(self, dataset_name):

        self.datasets_dict[dataset_name] = create_data_wrapper(dataset_name)

    def set_dataset(self, dataset_name):

        self.dataset = self.datasets_dict[dataset_name]


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


            

                

        







