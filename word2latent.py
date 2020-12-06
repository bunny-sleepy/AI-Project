import bert_try as bt
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers

def train_model(wordvec_batch = None,
                latentvec_batch = None,
                dense_layer_size = 256,
                dropout_rate = 0.2,
                epochs = 10000,
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
        model = tf.keras.models.Sequential([
            layers.Dense(dense_layer_size,
                         activation = 'relu',
                         input_shape = (wordvec_length, ),
                         kernel_initializer='RandomNormal',
                         bias_initializer='RandomNormal'),
            layers.Dense(dense_layer_size,
                         activation = 'relu',
                         kernel_initializer = 'RandomNormal',
                         bias_initializer = 'RandomNormal'),
            layers.Dense(dense_layer_size,
                         activation = 'relu',
                         kernel_initializer = 'RandomNormal',
                         bias_initializer = 'RandomNormal'),
            layers.Dense(dense_layer_size,
                         activation = 'relu',
                         kernel_initializer = 'RandomNormal',
                         bias_initializer = 'RandomNormal'),
            layers.Dense(dense_layer_size,
                         activation = 'relu',
                         kernel_initializer = 'RandomNormal',
                         bias_initializer = 'RandomNormal'),
            layers.Dense(dense_layer_size,
                         activation = 'relu',
                         kernel_initializer = 'RandomNormal',
                         bias_initializer = 'RandomNormal'),
            layers.Dense(dense_layer_size,
                         activation = 'relu',
                         kernel_initializer = 'RandomNormal',
                         bias_initializer = 'RandomNormal'),
            # layers.Dropout(dropout_rate),
            layers.Dense(latentvec_length,
                         kernel_initializer='RandomNormal',
                         bias_initializer='RandomNormal') # output layer
        ])
        model.compile(optimizer = 'adam',
                      loss = 'mse',
                      metrics = ['mse', 'mae'])
        model.fit(wordvec_batch, latentvec_batch, batch_size = 5, epochs=epochs)
        model.summary()
        model.save(checkpoint_path)
    elif not os.path.exists(checkpoint_path):
        print("ERROR: No existing checkpoint")
    else:
        model = tf.keras.models.load_model(checkpoint_path)
    return model