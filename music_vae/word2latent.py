from trained_model import TrainedModel as tm
import copy
import os
import re
import tarfile
import tempfile

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

# TODO: find out the dimensions of inputs and outputs
wordvec_length = -1
latentvec_length = -1

dense_layer_size = -1
dropout_rate = 0.2

# TODO: add the dataset
wordvec_batch = []
latentvec_batch = []
epochs = -1

model = tf.keras.models.Sequential([
    layers.Dense(dense_layer_size, activation = 'relu', input_dim = wordvec_length),
    layers.Dropout(dropout_rate),
    layers.Dense(latentvec_length) # output layer
])

model.compile(optimizer = 'adam', loss = 'MSE', metrics = ['accuracy'])

model.fit(wordvec_batch, latentvec_batch, epochs = epochs)