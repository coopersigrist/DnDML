
import torch
import torch.nn as nn


class AND(nn.Module):
    @torch.no_grad()
    def __init__(self, bit_width):
            self.bit_width = bit_width
            self.a = 0
            self.b = 0
            super().__init__()
            net = nn.Linear(2*bit_width, bit_width)
            net.weight.fill_(0.)
            for i in range(bit_width):
                net.weight[i][i].fill_(1)
                net.weight[i][i + bit_width].fill_(1)
            net.bias.data.fill_(-1)
            self.net = net

    def forward(self, a, b):
        max_length = a.shape[0] if a.shape[0] > b.shape[0] else b.shape[0]
        self.a = torch.nn.functional.pad(a,(0, self.bit_width-a.shape[0]))
        self.b = torch.nn.functional.pad(b,(0, self.bit_width-b.shape[0]))
        
        reshaped = torch.cat([self.a, self.b])
        out = torch.relu(self.net(reshaped))
        out = out[:max_length]
        return out



class OR(nn.Module):
    @torch.no_grad()
    def __init__(self, bit_width):
            self.bit_width = bit_width
            self.a = 0
            self.b = 0
            super().__init__()
            net = nn.Linear(2*bit_width, bit_width, bias=False)
            net.weight.fill_(0.)
            for i in range(bit_width):
                net.weight[i][i].fill_(1)
                net.weight[i][i + bit_width].fill_(1)
            self.net = net

    def forward(self, a, b):
        self.a = torch.nn.functional.pad(a,(0, self.bit_width-a.shape[0]))
        self.b = torch.nn.functional.pad(b,(0, self.bit_width-b.shape[0]))
        
        reshaped = torch.cat([self.a, self.b])
        out =  self.net(reshaped)
        return (out >= 1).float()



