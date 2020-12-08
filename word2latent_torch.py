import torch
import math
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as Data
from torchvision import datasets, transforms

fc_size = 1024

class net(nn.Module):
    def __init__(self):
        super(net, self).__init__()
        self.fc1 = nn.Linear(768, fc_size)
        self.fc2 = nn.Linear(fc_size, fc_size)
        self.fc3 = nn.Linear(fc_size, 512)
    def forward(self, x):
        out = self.fc1(x)
        out = nn.functional.relu(out)
        out = self.fc2(out)
        out = nn.functional.relu(out)
        out = self.fc3(out)
        return out

def train_model(wordvec_batch = None,
                latentvec_batch = None,
                dense_layer_size = 2048,
                dropout_rate = 0.2,
                learning_rate = 1e-1,
                momentum = 0.9,
                epochs = 1000,
                wordvec_length = 768,
                latentvec_length = 512,
                checkpoint_path = "model.h5",
                train = True):
    """
    Args:
        wordvec_batch: list of word vectors.
        latentvec_batch: list of latent vectors.
        dense_layer_size: size of hidden layers.
        dropout_rate: percentage of neurons dropout.
        learning_rate: the learning rate.
        momentum: the momentum
        epochs: training epochs.
        wordvec_length: length of word vector.
        latentvec_length: length of latent vector.
        checkpoint_path: the path to store the model.
        train: whether to train or to use the model.

    Return:
        the trained model
    """
    # TODO: evaluate the effectiveness of this model
    # TODO: save the trained model with training time
    model = None
    if train:
        model = net()
        optimizer = optim.SGD(model.parameters(), lr = learning_rate, momentum = momentum)
        criterion = nn.CrossEntropyLoss()
        for epoch in range(epochs):
            out = model(wordvec_batch)
            loss = criterion(out, latentvec_batch)
            loss.backward()
            print('Train Epoch: {} \tLoss: {:.6f}'.format(
                epoch, loss.item()))
            optimizer.step()
    return model