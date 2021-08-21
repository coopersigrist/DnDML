import shutil
import torch
import torch.nn as nn

def create_loss_wrapper(loss_name):
    '''
    Creates a 'Loss' class, its a wrapper of PyTorch loss functions


    PARAMS:
        loss_func: The name (string) of the loss function you wish to make a wrapper for -- so far just PyTorch loss functions (e.g. MSELoss)

    RETURNS: 
        a LossWrapper class that wraps a PyTorch loss function  

    '''

    torch_loss_list = ["L1Loss","MSELoss","CrossEntropyLoss","CTCLoss","NLLLoss","PoissonNLLLoss",
     "GaussianNLLLoss","KLDivLoss","BCELoss","BCEWithLogitsLoss","MarginRankingLoss","HingeEmbeddingLoss", 
     "MultiLabelMarginLoss", "HuberLoss","SmoothL1Loss","SoftMarginLoss", "MultiLabelSoftMarginLoss", 
     "CosineEmbeddingLoss", "MultiMarginLoss","TripletMarginLoss", "TripletMarginWithDistanceLoss"]

    

    if type(loss_name) == str:

        if loss_name in torch_loss_list:

            super_loss_func = getattr(nn, loss_name)
    
    else:

        super_loss_func = loss_name # This would mean that a function was passed instead of the name string


    class LossWrapper(super_loss_func):

        def __init__(self,*args,**kwargs):

            super().__init__(*args, **kwargs)

            self.root = kwargs[0]
            self.deleted = False
            self.args = args
            self.kwargs = kwargs
        
        def __getitem__(self, ind: int):
            if self.deleted:
                raise Exception("This loss_func was already deleted :/")

            return super().__getitem__(ind)
        
        def __len__(self):
            if self.deleted:
                raise Exception("This loss_func was already deleted :/")

            return super().__len__()
        
        def remove(self):
            shutil.rmtree(self.root)
            self.installed = True
    
    return LossWrapper

