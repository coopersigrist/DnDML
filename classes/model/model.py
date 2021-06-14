import torch
import torch.nn as nn


class Model(nn.Module):

    def __init__(self,
                 input_features,
                 output_features):

        super(Model, self).__init__()
        # Initialize list of modules in architecture
        self.modules = []
        # Input features
        self.input_features = input_features
        # Output features
        self.output_features = output_features

    def insertModule(self,
                     idx,
                     module_type='dense',
                     params=None):

        if module_type == 'dense':
            if idx == 0:
                in_features = self.input_features
            else:
                in_features = self.modules[idx - 1].out_features

            if idx == len(self.modules):
                out_features = self.output_features
            else:
                out_features = self.modules[idx].in_features

            module = nn.Linear(
                in_features=in_features,
                out_features=out_features)

        elif module_type == 'relu':
            module = nn.ReLU()

        return self.modules.insert(idx, module)

    def popModule(self,
                  idx):

        return self.modules.pop(idx)

    def forward(self,
                x):

        out = x
        for module in self.modules:
            out = module(out)
        return out
