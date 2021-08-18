import shutil
import torch
import torchvision

def create_data_wrapper(dataset_name):
    '''
    Creates a 'Dataset' class which has deletion functionality and anything else we'd like to add,
    its a wrapper of Trochvision datasets, but we can expand that to other dataset libraries

    PARAMS:
        dataset_name: The name (string) of the dataset you wish to make a wrapper for -- so far just torchvision datasets (e.g. MNIST)

    RETURNS: 
        a DatasetWrapper class that wraps a torchvision dataset  

    '''

    Torchvision_list = ["CelebA", "CIFAR10","CIFAR100","Cityscapes","CocoCaptions","CocoDetection",
     "DatasetFolder","EMNIST","FakeData","FashionMNIST","Flickr30k","Flickr8k", "ImageFolder", "ImageNet",
     "Kinetics-400","KMNIST", "LSUN", "LSUNClass", "MNIST", "Omniglot", "PhotoTour", "Places365",
     "QMNIST", "SBD", "SBU", "SEMEION", "STL10",
     "SVHN", "UCF101","USPS","VOCDetection", "VOCSegmentation"]

    if type(dataset_name) == str:

        if dataset_name in Torchvision_list:

            super_dataset = getattr(torchvision.datasets, dataset_name)
    
    else:

        super_dataset = dataset_name # This would mean that a dataset was passed instead of the name 


    class DatasetWrapper(super_dataset):

        def __init__(self,*args,**kwargs):

            super().__init__(*args, **kwargs)

            self.root = kwargs[0]
            self.deleted = False
            self.args = args
            self.kwargs = kwargs
        
        def __getitem__(self, ind: int):
            if self.deleted:
                raise Exception("This dataset was already deleted :/")

            return super().__getitem__(ind)
        
        def __len__(self):
            if self.deleted:
                raise Exception("This dataset was already deleted :/")

            return super().__len__()
        
        def remove(self):
            shutil.rmtree(self.root)
            self.installed = True
    
    return DatasetWrapper

