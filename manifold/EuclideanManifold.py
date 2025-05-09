import torch
import torch.nn as nn, torch.nn.functional as F
from dgl.nn.pytorch import TypedLinear
import config
import math
from torch_geometric.nn import LayerNorm
from torch_scatter import scatter
from torch_geometric.utils import softmax
from torch.autograd import Function, Variable
from manifold.manifold_utils import *


class EuclideanManifold:

    def __init__(self, args, logger, max_norm=1, EPS=1e-8):
        self.args = args
        self.logger = logger
        self.max_norm = max_norm
        self.EPS = EPS

    def init_embed(self, embed, irange=1e-3):
        embed.weight.data.uniform_(-irange, irange)
        embed.weight.data.copy_(self.normalize(embed.weight.data))

    def distance(self, u, v):
        return torch.sqrt(clamp_min(torch.sum((u - v).pow(2), dim=1), self.EPS))

    def log_map_zero(self, y):
        return y

    def log_map_x(self, x, y):
        return y - x

    def metric_tensor(self, x, u, v):
        return th_dot(u, v)

    def exp_map_zero(self, v):
        return self.normalize(v)

    def exp_map_x(self, x, v, approximate=False):
        return self.normalize(x + v)

    def parallel_transport(self, src, dst, v):
        return v

    def rgrad(self, p, d_p):
        return d_p

    def normalize(self, w):
        if self.max_norm:
            return clip_by_norm(w, self.max_norm)
        else:
            return w
