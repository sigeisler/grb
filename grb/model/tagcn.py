import torch
import torch.nn as nn
import torch.nn.functional as F


class TAGConv(nn.Module):
    def __init__(self, in_features, out_features, k=2, activation=None, dropout=False, norm=False):
        super(TAGConv, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.linear = nn.Linear(in_features * (k + 1), out_features)
        self.norm = norm
        self.norm_func = nn.BatchNorm1d(out_features, affine=False)
        self.activation = activation
        self.dropout = dropout
        self.k = k
        self.reset_parameters()

    def reset_parameters(self):
        if self.activation == F.relu:
            gain = nn.init.calculate_gain('relu')
        elif self.activation == F.leaky_relu:
            gain = nn.init.calculate_gain('leaky_relu')
        else:
            gain = nn.init.calculate_gain('relu')
        nn.init.xavier_normal_(self.linear.weight, gain=gain)

    def forward(self, x, adj, dropout=0):

        fstack = [x]
        for i in range(self.k):
            y = torch.spmm(adj, fstack[-1])
            fstack.append(y)
        x = torch.cat(fstack, dim=-1)
        x = self.linear(x)
        if self.norm:
            x = self.norm_func(x)
        if not (self.activation is None):
            x = self.activation(x)
        if self.dropout:
            x = F.dropout(x, dropout)

        return x


class TAGCN(nn.Module):
    def __init__(self, in_features, out_features, hidden_features, k, activation=F.leaky_relu, dropout=True):
        super(TAGCN, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        if type(hidden_features) is int:
            hidden_features = [hidden_features]

        self.layers = nn.ModuleList()
        self.layers.append(TAGConv(in_features, hidden_features[0], k, activation=activation, dropout=dropout))
        for i in range(len(hidden_features) - 1):
            self.layers.append(
                TAGConv(hidden_features[i], hidden_features[i + 1], k, activation=activation, dropout=dropout))
        self.layers.append(TAGConv(hidden_features[-1], out_features, k))
        self.reset_parameters()

    def reset_parameters(self):
        for layer in self.layers:
            layer.reset_parameters()

    def forward(self, x, adj, dropout=0):
        for i in range(len(self.layers)):
            x = self.layers[i](x, adj, dropout=dropout)

        return x