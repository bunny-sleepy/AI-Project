import bert_try, latent_vec_generate
import numpy as np
import os
import tensorflow as tf
import word2latent as w2l
from tensorflow.keras import layers
import latent_vec_decode as decode

# NOTE: you should change this configuration YOURSELF
music_vae_config_str = 'hierdec-mel_16bar'
music_vae_checkpoint_dir = './../repository/musicvae_hierdec-mel_16bar'
target_directory = './midi_output/total_output'
generate_temperature = 0.5

'''
input: word_vec
output: latent vector
'''
def generateMidi(word_string,
                 wordvec_to_latentvec_model,
                 music_vae_model,
                 target_directory = './midi_output/generate_output',
                 generate_temperature = 0.5):
    word_vec_array = bert_try.encode_nlp(word_string)
    # maximum pooling
    word_vec = np.max(word_vec_array, axis = 0)
    # model output
    latent_vec = wordvec_to_latentvec_model.predict(np.array([word_vec]))
    decode.decode_to_midi(target_directory=target_directory, trained_model=music_vae_model, length = len(latent_vec), z_batch = [latent_vec], temperature=generate_temperature)

# TODO: write a tentative main function
def main():
    word_train = []
    word_train.append(np.max(bert_try.encode_nlp("Back To December"), axis=0))
    word_train.append(np.max(bert_try.encode_nlp("test1"), axis=0))
    path1 = './midi_input/BackToDecember.mid'
    path2 = './midi_input/test1.mid'
    p = []
    latent_train = []
    p.append(path1)
    p.append(path2)
    music_vae_model = decode.generate_model(config_str=music_vae_config_str, checkpoint_dir=music_vae_checkpoint_dir)
    encoded_list = latent_vec_generate.encode(trained_model=music_vae_model, midi_batch=p)
    z,u,v = encoded_list['BackToDecember.mid']
    latent_train.append(z[0])
    z,u,v = encoded_list['test1.mid']
    latent_train.append(z[0])
    w2vmodel = w2l.train_model(np.array(word_train), np.array(latent_train))      
    
    word_input = "Hello world!"

    generateMidi(word_input,
                 w2vmodel,
                 music_vae_model = music_vae_model,
                 target_directory = target_directory)

if __name__ == '__main__':
    main()