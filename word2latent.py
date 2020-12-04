# from trained_model import TrainedModel as tm
# import copy
# import re
# import tarfile
# import tempfile
import bert_try as bt

import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers

# TODO: find out the dimensions of inputs and outputs
# Solved
wordvec_length = 768
latentvec_length = 512


# kernel_size = [3, 1]
dense_layer_size = 1024
dropout_rate = 0.2

# TODO: add the dataset
wordvec_files = [bt.encode_nlp('hello world!')]

wordvec_batch = []
latentvec_batch = []
epochs = 1000


# maximum pooling
for word_vec in wordvec_files:
    wordvec_batch.append(np.max(word_vec, axis = 0))

# print(wordvec_batch)

# TODO: evaluate the effectiveness of this model

# TODO: save the trained model with training time
model = None
if not os.path.exists(".\Model\model.h5"):
    model = tf.keras.models.Sequential([
        layers.Dense(dense_layer_size, activation = 'relu', input_shape = (wordvec_length, )),
        layers.Dense(dense_layer_size, activation = 'relu'),
        layers.Dropout(dropout_rate),
        layers.Dense(latentvec_length) # output layer
    ])
    model.compile(optimizer = 'adam', loss = 'MSE', metrics = ['accuracy'])

else:
    model = tf.keras.models.load_model('./Model/model.h5')

# TODO: train the model
model.fit(wordvec_batch, latentvec_batch, epochs=epochs)
model.save('./Model/model.h5')
print(model.summary())