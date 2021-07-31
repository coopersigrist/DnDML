import numpy as np
import torch
import torch.nn as nn
import networkx as nx
import time as tm
from utilities import ModelTorch


class ModelWrapper():

    def __init__(self, inputFeatures, outputFeatures):
        # Input features
        self.inputFeatures = inputFeatures
        # Output features
        self.outputFeatures = outputFeatures
        # Initialize dictionary of idx:modules in architecture
        self.modulesDict = {}
        # Initialize connectivity graph
        self.connectivityGraph = nx.DiGraph()
        self.connectivityGraph.add_nodes_from(['in', 'out'])

    def insertModule(self, moduleType=nn.ReLU, *args, **kwargs):
        idx = self.__getFreeIdx()
        self.modulesDict[idx] = moduleType(*args, **kwargs)
        self.connectivityGraph.add_node(idx,
                                        type=moduleType,
                                        size=args,
                                        param=kwargs)
        return idx

    def __getFreeIdx(self):
        idx = 1
        while self.__modulesExist(idx):
            idx += 1
        return idx

    def __modulesExist(self, *indices):
        return set(indices).issubset(self.connectivityGraph.nodes())

    def popModule(self, idx):
        try:
            self.modulesDict.pop(idx)
            self.connectivityGraph.remove_node(idx)
        except KeyError:
            print('Missing module {} in graph'.format(idx))

    def addConnectionBetween(self, idx1, idx2):
        if self.__modulesExist(idx1, idx2):
            self.connectivityGraph.add_edge(idx1, idx2)
        else:
            print('Missing module {} in graph'.format((idx1, idx2)))

    def isConnectivityGraphCorrect(self, moduleIdx='in', inputDimension=None):
        print('Checking', moduleIdx)

        if moduleIdx == 'in':
            inputDimension = self.inputFeatures

        if moduleIdx == 'out':
            return inputDimension == self.outputFeatures

        outputDimension = self.computeOutputDimensions(
            moduleIdx, inputDimension)
        moduleNeighbors = self.connectivityGraph.neighbors(moduleIdx)

        if outputDimension is None:
            return False

        print('\t', inputDimension, '==>', outputDimension)

        for neighbor in moduleNeighbors:
            print('\tNeighbor', neighbor)
            if not self.isConnectivityGraphCorrect(neighbor, outputDimension):
                return False

        return True

    def computeOutputDimensions(self, moduleIdx, inputDimension):
        if moduleIdx == 'in':
            return self.inputFeatures

        elif moduleIdx == 'out':
            return self.outputFeatures

        elif isinstance(self.modulesDict[moduleIdx], torch.nn.modules.ReLU):
            return inputDimension

        elif isinstance(self.modulesDict[moduleIdx], torch.nn.modules.conv.Conv2d):
            try:
                inputChannels, inputHeight, inputWidth = inputDimension
            except ValueError:
                return None

            if inputChannels != self.modulesDict[moduleIdx].in_channels:
                print('''\tMismatch between output channels ({}) from previous
                      module and input channels ({}) from current module
                      '''.format(inputChannels, self.modulesDict[moduleIdx].in_channels))
                return None

            padding = self.modulesDict[moduleIdx].padding
            dilation = self.modulesDict[moduleIdx].dilation
            kernel = self.modulesDict[moduleIdx].kernel_size
            stride = self.modulesDict[moduleIdx].stride
            outputChannels = self.modulesDict[moduleIdx].out_channels

            outputHeight = int((inputHeight + 2. * padding[0] - dilation[0]
                                * (kernel[0] - 1.) - 1.) / stride[0] + 1.)
            outputWidth = int((inputWidth + 2. * padding[1] - dilation[1]
                               * (kernel[1] - 1.) - 1.) / stride[1] + 1.)

            return (outputChannels, outputHeight, outputWidth)

        elif isinstance(self.modulesDict[moduleIdx], torch.nn.modules.flatten.Flatten):
            inputChannels, inputHeight, inputWidth = inputDimension

            return (inputChannels * inputHeight * inputWidth,)

        elif isinstance(self.modulesDict[moduleIdx], torch.nn.modules.linear.Linear):
            inputFeatures, = inputDimension

            if inputFeatures != self.modulesDict[moduleIdx].in_features:
                print('''\tMismatch between output features ({}) from previous
                      module and input features ({}) from current module
                      '''.format(inputFeatures, self.modulesDict[moduleIdx].in_features))
                return None

            outputFeatures = self.modulesDict[moduleIdx].out_features

            return (outputFeatures,)

    def showConnectivityGraph(self):
        nx.draw_networkx(self.connectivityGraph)

    def createModel(self):
        if self.isConnectivityGraphCorrect('in'):
            print('Model created!')
            self.modelTorch = ModelTorch(self.modulesDict, self.connectivityGraph)
        else:
            print('Impossible to create model')


if __name__ == "__main__":
    # Create model
    mw = ModelWrapper((3, 32, 32), (10,))

    # Insert different layers
    mw.insertModule(nn.Conv2d, 3, 20, kernel_size=3, padding=1)
    mw.insertModule()
    mw.insertModule(nn.Conv2d, 20, 10, kernel_size=4, stride=4)
    mw.insertModule()
    mw.insertModule(nn.Flatten)

    mw.insertModule(nn.Conv2d, 3, 10, kernel_size=5, padding=2)
    mw.insertModule()
    mw.insertModule(nn.Conv2d, 10, 10, kernel_size=4, stride=4)
    mw.insertModule()
    mw.insertModule(nn.Flatten)

    mw.insertModule(nn.Linear, 640, 10)
    # mw.showConnectivityGraph()

    # Connect the modules
    mw.addConnectionBetween('in', 1)
    mw.addConnectionBetween(1, 2)
    mw.addConnectionBetween(2, 3)
    mw.addConnectionBetween(3, 4)
    mw.addConnectionBetween(4, 5)
    mw.addConnectionBetween(5, 11)

    mw.addConnectionBetween('in', 6)
    mw.addConnectionBetween(6, 7)
    mw.addConnectionBetween(7, 8)
    mw.addConnectionBetween(8, 9)
    mw.addConnectionBetween(9, 10)
    mw.addConnectionBetween(10, 11)

    mw.addConnectionBetween(11, 'out')
    mw.showConnectivityGraph()

    # Check connectivity graph
    print(mw.isConnectivityGraphCorrect())
    
    # Create model
    mw.createModel()
    print(mw.modelTorch)
