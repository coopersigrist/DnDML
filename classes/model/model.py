# import numpy as np
import torch
import torch.nn as nn
import networkx as nx
# import time as tm
# from utilities import ModelTorch


class ModelWrapper(nn.Module):

    def __init__(self, inputFeatures, outputFeatures):
        super(ModelWrapper, self).__init__()
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
            print('Missing module {} or {} in graph'.format(idx1, idx2))

    def isConnectivityGraphCorrect(self, moduleIdx='in', inputDimension=None):
        print('Checking', moduleIdx)

        if moduleIdx == 'in':
            inputDimension = self.inputFeatures

        outputDimension = self.__computeOutputDimension(
            moduleIdx, inputDimension)

        if outputDimension is None:
            return False

        print('\t', inputDimension, '==>', outputDimension)

        moduleSuccessors = self.connectivityGraph.successors(moduleIdx)
        for successor in moduleSuccessors:
            print('\tSuccessor', successor)
            if not self.isConnectivityGraphCorrect(successor, outputDimension):
                return False

        return True

    def __computeOutputDimension(self, moduleIdx, inputDimension):
        try:
            if moduleIdx == 'in':
                return self.inputFeatures
            elif moduleIdx == 'out':
                return self.outputFeatures
            else:
                inputTensor = torch.randn(*inputDimension).unsqueeze(0)
                return tuple(self.modulesDict[moduleIdx](
                    inputTensor).squeeze(0).size())
        except RuntimeError:
            print('''\tMismatch between output features from previous
                  module and input features from current module.''')
            return None

    def _showConnectivityGraph(self):
        nx.draw_networkx(self.connectivityGraph, with_labels=True)

    def forward(self, inputTensor):
        return self.__computeOutput('out', inputTensor)

    def __computeOutput(self, moduleIdx='out', inputTensor=None):
        predecessorModules = self.connectivityGraph.predecessors(moduleIdx)

        for predecessor in predecessorModules:
            # TODO: What happens with ResNet networks
            pass

        if moduleIdx == 'in':
            return inputTensor
        if moduleIdx == 'out':
            return self.__computeOutput(
                moduleIdx=predecessor,
                inputTensor=inputTensor)

        return self.modulesDict[moduleIdx](
            self.__computeOutput(
                moduleIdx=predecessor,
                inputTensor=inputTensor))


if __name__ == "__main__":
    # Create model
    mw = ModelWrapper(inputFeatures=(3, 32, 32), outputFeatures=(10,))

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

    # mw.addConnectionBetween('in', 6)
    # mw.addConnectionBetween(6, 7)
    # mw.addConnectionBetween(7, 8)
    # mw.addConnectionBetween(8, 9)
    # mw.addConnectionBetween(9, 10)
    # mw.addConnectionBetween(10, 11)

    mw.addConnectionBetween(11, 'out')

    # Show connectivity graph
    mw._showConnectivityGraph()

    # Check connectivity graph
    print(mw.isConnectivityGraphCorrect())

    print(mw(torch.zeros(1, 3, 32, 32)))
