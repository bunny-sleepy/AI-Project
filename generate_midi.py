import bert_try, latent_vec_generate
import numpy as np
import os
import tensorflow as tf
import word2latent as w2l
from tensorflow.keras import layers
import latent_vec_decode as decode
import harmonize as har

'''
input: word_vec
output: latent vector
'''
def generateMidi(word_string,
                 wordvec_to_latentvec_model,
                 music_vae_model,
                 coconet_model = None,
                 pooling = False,
                 harmonize = True,
                 target_directory = './midi_output/generate_output',
                 generate_temperature = 0.5,
                 harmonize_temperature = 0.8,
                 harmonize_batch_size = 2):
    word_vec = bert_try.encode_nlp(word_string, pooling)
    # model output
    latent_vec = wordvec_to_latentvec_model.predict(np.array([word_vec]))
    output_files = decode.decode_to_midi(target_directory=target_directory,
                                         trained_model=music_vae_model,
                                         length = len(latent_vec),
                                         z_batch = [latent_vec],
                                         temperature=generate_temperature)
    if harmonize and (not coconet_model is None):
        for output_file in output_files:
            har.harmonize(output_file,
                          target_directory,
                          coconet_model = coconet_model,
                          temperature = harmonize_temperature,
                          batch_size = harmonize_batch_size)

# TODO: write a tentative main function
def main():
    # NOTE: you should change this configuration YOURSELF
    music_vae_config_str = 'hierdec-mel_16bar'
    music_vae_checkpoint_dir = './../repository/musicvae_hierdec-mel_16bar'
    target_directory = './midi_output/total_output'
    generate_temperature = 0.5
    coconet_checkpoint_dir = 'D:/code/Github/repository/coconet_model'
    harmonize_temperature = 0.8
    harmonize_batch_size = 2

    music_vae_model = decode.generate_model(config_str = music_vae_config_str,
                                            checkpoint_dir = music_vae_checkpoint_dir)
    coconet_model = har.generate_coconet_model(coconet_model_path = coconet_checkpoint_dir)
    # train model
    w2vmodel = w2l.train_model(train = False)
    # test output
    # word_input = "Hello world!"
    # generateMidi(word_input,
    #              w2vmodel,
    #              music_vae_model = music_vae_model,
    #              target_directory = target_directory)
    word_input = "Happy"
    generateMidi(word_input,
                 w2vmodel,
                 music_vae_model = music_vae_model,
                 coconet_model = coconet_model,
                 harmonize = True,
                 target_directory = target_directory,
                 generate_temperature = generate_temperature,
                 harmonize_temperature = harmonize_temperature,
                 harmonize_batch_size = harmonize_batch_size)

if __name__ == '__main__':
    main()