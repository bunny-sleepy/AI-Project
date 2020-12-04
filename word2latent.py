import bert_try as bt
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers

'''

Dataset input:
wordvec_batch: list of word vectors
latentvec_batch: list of latent vectors
NOTE: the two lists MUST be in the same order

Training settings:
dense_layer_size: size of hidden layers
dropout_rate: percentage of neurons dropout
epochs: training epochs

Shape of dataset:
wordvec_length: length of word vector
latentvec_length: length of latent vector

'''

def train_model(wordvec_batch, latentvec_batch,
 dense_layer_size = 1024, dropout_rate = 0.2, epochs = 1000,
 wordvec_length = 768, latentvec_length = 512):

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

    # Train the model
    model.fit(wordvec_batch, latentvec_batch, epochs=epochs)
    model.save('./Model/model.h5')
    return model