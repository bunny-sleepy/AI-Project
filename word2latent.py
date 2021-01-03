import os
import tensorflow as tf
from tensorflow.keras import layers

def train_model_variance(wordvec_batch = None,
                latent_variance_batch = None,
                dense_layer_size = 2048,
                dropout_rate = 0.2,
                learning_rate = 1e-2,
                batch_size = 16,
                epochs = 1000,
                wordvec_length = 768,
                latentvec_length = 512,
                checkpoint_path_variance = None,
                train = True,
                load = False,
                save_every_n_epochs = None):
    """
    Args:
        wordvec_batch: list of word vectors.
        latent_variance_batch: list of latent variances
        dense_layer_size: size of hidden layers.
        dropout_rate: percentage of neurons dropout.
        learning_rate: the learning rate.
        batch_size: the batch size
        epochs: training epochs.
        wordvec_length: length of word vector.
        latentvec_length: length of latent vector.
        checkpoint_path_variance: the path to store/load the model of variance.
        train: whether to train or to use the model.
        load: whether or not to load model from previous checkpoint
        save_every_n_epochs: save the model every n epochs

    Return:
        the trained model
    """
    model_variance = None
    if train:
        if load and checkpoint_path_variance is not None:
            model_variance = tf.keras.models.load_model(checkpoint_path_variance)
        else:
            model_variance = tf.keras.models.Sequential([
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
        model_variance.compile(optimizer = 'adam',
                      loss = 'mse',
                      metrics = ['mse'])
        model_variance.summary()
        if save_every_n_epochs is not None:
            for i in range(0, epochs, save_every_n_epochs):
                model_variance.fit(wordvec_batch, latent_variance_batch, batch_size = batch_size, epochs = save_every_n_epochs, use_multiprocessing = True)
                model_variance.save(checkpoint_path_variance)
                print("Finished %d epochs" % (i + save_every_n_epochs))
        else:
            model_variance.fit(wordvec_batch, latent_variance_batch, batch_size = batch_size,
                               epochs = epochs, use_multiprocessing = True)
            model_variance.save(checkpoint_path_variance)
    elif not os.path.exists(checkpoint_path_variance):
        print("ERROR: No existing checkpoint")
    else:
        model_variance = tf.keras.models.load_model(checkpoint_path_variance)
    return model_variance


def train_model_mean(wordvec_batch = None,
                     latent_mean_batch = None,
                     dense_layer_size = 2048,
                     dropout_rate = 0.2,
                     learning_rate = 1e-2,
                     batch_size = 16,
                     epochs = 1000,
                     wordvec_length = 768,
                     latentvec_length = 512,
                     checkpoint_path_mean = None,
                     train = True,
                     load = False,
                     save_every_n_epochs = None):
    """
    Args:
        wordvec_batch: list of word vectors.
        latent_mean_batch: list of latent means.
        dense_layer_size: size of hidden layers.
        dropout_rate: percentage of neurons dropout.
        learning_rate: the learning rate.
        batch_size: the batch size
        epochs: training epochs.
        wordvec_length: length of word vector.
        latentvec_length: length of latent vector.
        checkpoint_path_mean: the path to store/load the modell of mean.
        train: whether to train or to use the model.
        load: whether or not to load model from previous checkpoint
        save_every_n_epochs: save the checkpoints every n epochs

    Return:
        the trained model
    """
    model_mean = None
    if train:
        if load and checkpoint_path_mean is not None:
            model_mean = tf.keras.models.load_model(checkpoint_path_mean)
        else:
            model_mean = tf.keras.models.Sequential([
                layers.Input(shape = (wordvec_length,)),
                layers.Dense(dense_layer_size,
                             activation = 'relu',
                             kernel_initializer = 'RandomNormal',
                             bias_initializer = 'RandomNormal'),
                layers.Dense(dense_layer_size,
                             activation = 'relu',
                             kernel_initializer = 'RandomNormal',
                             bias_initializer = 'RandomNormal'),
                layers.Dropout(dropout_rate),
                layers.Dense(latentvec_length,
                             kernel_initializer = 'RandomNormal',
                             bias_initializer = 'RandomNormal')  # output layer
            ])
        optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate)
        model_mean.compile(optimizer = 'adam',
                          loss = 'mse',
                          metrics = ['mse'])
        model_mean.summary()
        if save_every_n_epochs is not None:
            for i in range(0, epochs, save_every_n_epochs):
                model_mean.fit(wordvec_batch, latent_mean_batch, batch_size = batch_size, epochs = save_every_n_epochs,
                               use_multiprocessing = True)
                model_mean.save(checkpoint_path_mean)
                print("Finished %d epochs" % (i + save_every_n_epochs))
        else:
            model_mean.fit(wordvec_batch, latent_mean_batch, batch_size = batch_size, epochs = epochs, use_multiprocessing = True)
            model_mean.save(checkpoint_path_mean)
    elif not os.path.exists(checkpoint_path_mean):
        print("ERROR: No existing checkpoint")
    else:
        model_mean = tf.keras.models.load_model(checkpoint_path_mean)
    return model_mean