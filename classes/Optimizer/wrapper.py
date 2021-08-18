import shutil
import torch
import torch.optim as optim

def create_optim_wrapper(optimizer_name):
    '''
    Creates an 'Optimizer' class, its a wrapper of PyTorch optimizers


    PARAMS:
        optimizer: The name (string) of the optimizer you wish to make a wrapper for -- so far just PyTorch optimizers (e.g. SGD)

    RETURNS: 
        a OptimizerWrapper class that wraps a PyTorch optimizer

    '''

    torch_optim_list = ["Adadelta","Adagrad","Adam","AdamW","SparseAdam","Adamax",
     "ASGD","LBFGS","RMSprop","Rprop","SGD"]

    if type(optimizer_name) == str:

        if optimizer_name in torch_optim_list:

            super_optimizer = getattr(optim, optimizer_name)
    
    else:

        super_optimizer = optimizer_name # This would mean that a function was passed instead of the name string


    class OptimizerWrapper(super_optimizer):

        def __init__(self,*args,**kwargs):

            super().__init__(*args, **kwargs)

            self.root = kwargs[0]
            self.deleted = False
            self.args = args
            self.kwargs = kwargs
        
        def __getitem__(self, ind: int):
            if self.deleted:
                raise Exception("This optimizer was already deleted :/")

            return super().__getitem__(ind)
        
        def __len__(self):
            if self.deleted:
                raise Exception("This optimizer was already deleted :/")

            return super().__len__()
        
        def remove(self):
            shutil.rmtree(self.root)
            self.installed = True
    
    return OptimizerWrapper

