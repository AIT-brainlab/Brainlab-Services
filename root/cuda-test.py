# imports for examples
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from torchtest import test_suite

device='cuda:1'

inputs = Variable(torch.randn(20, 20))
targets = Variable(torch.randint(0, 2, (20,))).long()
batch = [inputs, targets]
model = nn.Linear(20, 2)
loss_fn=F.cross_entropy
optim=torch.optim.Adam(model.parameters())

test_suite(
    model,  # a model moved to GPU
    loss_fn, optim, batch,
    test_inf_vals=True,
    device='cuda:0'
    )