import bert_try as bt
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt

def train_model(wordvec_batch = None,
                latentvec_batch = None,
                dense_layer_size = 2048,
                dropout_rate = 0.2,
                learning_rate = 1e-2,
                batch_size = 16,
                epochs = 1000,
                wordvec_length = 768,
                latentvec_length = 512,
                checkpoint_path = "model.h5",
                train = True,
                load = False,
                save_every_n_epoch = None):
    """
    Args:
        wordvec_batch: list of word vectors.
        latentvec_batch: list of latent vectors.
        dense_layer_size: size of hidden layers.
        dropout_rate: percentage of neurons dropout.
        learning_rate: the learning rate.
        batch_size: the batch size
        epochs: training epochs.
        wordvec_length: length of word vector.
        latentvec_length: length of latent vector.
        checkpoint_path: the path to store the model.
        train: whether to train or to use the model.
        load: whether or not to load model from previous checkpoint
        save_every_n_epoch: to save the model every n epochs

    Return:
        the trained model
    """

    # TODO: evaluate the effectiveness of this model
    # TODO: save the trained model with training time
    model = None
    if train:
        if load:
            model = tf.keras.models.load_model(checkpoint_path)
        else:
            model = tf.keras.models.Sequential([
                layers.Input(shape = (wordvec_length, )),
                layers.Dense(dense_layer_size,
                             activation = 'relu',
                             kernel_initializer='RandomNormal',
                             bias_initializer='RandomNormal'),
                layers.Dense(dense_layer_size,
                             activation = 'relu',
                             kernel_initializer = 'RandomNormal',
                             bias_initializer = 'RandomNormal'),
                layers.Dropout(dropout_rate),
                layers.Dense(latentvec_length,
                             kernel_initializer='RandomNormal',
                             bias_initializer='RandomNormal') # output layer
            ])
        optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate)
        model.compile(optimizer = 'adam',
                      loss = 'mse',
                      metrics = ['mse'])
        model.summary()
        model.fit(wordvec_batch, latentvec_batch, batch_size = batch_size, epochs = epochs, use_multiprocessing = True)
        # history.history.keys()
        # plt.plot(history.epoch, history.history.get('loss'))
        # plt.plot(history.epoch, history.history.get('acc'))
        model.save(checkpoint_path)
    elif not os.path.exists(checkpoint_path):
        print("ERROR: No existing checkpoint")
    else:
        model = tf.keras.models.load_model(checkpoint_path)
    return model