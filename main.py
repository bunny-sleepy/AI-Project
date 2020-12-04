import bert_try as bt
import numpy as np
import os
import tensorflow as tf
import word2latent as w2l
from tensorflow.keras import layers
import latent_vec_decode as decode

# NOTE: you should change this configuration YOURSELF
music_vae_config_str = 'hierdec-mel_16bar'
music_vae_checkpoint_dir = 'D:/code/Github/repository/musicvae_hierdec-mel_16bar'
target_directory = './midi_output/generate_output'
generate_temperature = 0.5

'''
input: word_vec
output: latent vector
'''
def GenerateMidi(word_string,
                 wordvec_to_latentvec_model,
                 music_vae_checkpoint_dir,
                 music_vae_config_str = 'hierdec-mel_16bar',
                 target_directory = './midi_output/generate_output',
                 generate_temperature = 0.5):

    word_vec_array = bert_try.encode_nlp(word_string)
    # maximum pooling
    word_vec = np.max(word_vec_array, axis = 0)
    # model output
    latent_vec = model.run(word_vec)
    # decode latent_vec to midi output
    music_vae_model = decode.generate_model(config_str=music_vae_config_str, checkpoint_dir=music_vae_checkpoint_dir)
    decode.decode_to_midi(target_directory=target_directory, trained_model=music_vae_model, length = len(latent_vec), z_batch = [latent_vec], temperature=generate_temperature)

# TODO: write a tentative main function
def main():
    pass

if __name__ == '__main__':
    main()