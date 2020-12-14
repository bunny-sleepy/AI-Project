import os
import re
import preprocessing.preprocess_title as ppt
import bert_try as bt
import latent_vec_generate as lvg
import numpy as np
import preprocessing.preprocess_midi as ppm
import note_seq

word_dict = ppt.word_dict('./preprocessing/word.txt')

# NOTE: absolute path recommended
def load_dataset(musicvae_model, midi_directory = "PATH", pooling = True, word_dict = word_dict, max_num = 1000):
    """ load midi dataset from a given directory

    Args:
        musicvae_model: the musicvae_model to load
        midi_directory: directory of midi files
        max_num: how many files to load
        word_dict: the dictionary of word from ppt
        pooling: whether use maximum pooling method

    Return:
        the x, y data ready for training
    """

    file_list = os.listdir(midi_directory)
    midi_wordvec_list = []
    midi_latentvec_list = []

    curr_num = 0
    for filename in file_list:
        if curr_num < max_num:
            midi_file = "%s/%s" % (midi_directory, filename)
            print(midi_file)
            if (".mid" in filename) or (".midi" in filename):
                file_valid, title = ppt.file_title(midi_file, word_dict)
                if file_valid:
                    midi_wordvec = bt.encode_nlp(title, pooling)
                    ns = note_seq.midi_file_to_note_sequence(midi_file)
                    # TODO: change this midi preprocessing method
                    # if True:
                    try:
                        new_ns = ppm.get_new_ns(ppm.skyline(ns), ns)
                        z_list, _, _ = lvg.encode_ns(musicvae_model, new_ns)
                        for z in z_list:
                            midi_latentvec_list.append(z)
                            midi_wordvec_list.append(midi_wordvec)
                        curr_num += 1
                        print("%04d/%04d: data loaded successfully at %s" % (curr_num, max_num, filename))
                    except:
                        print("unable to load the file at %s" % filename)
                else:
                    print("invalid midi file at %s" % filename)
    return midi_wordvec_list, midi_latentvec_list

def main():
    music_vae_checkpoint_dir = 'D:/code/Github/repository/musicvae_hierdec-mel_16bar'
    music_vae_model = lvg.generate_model(config_str = 'hierdec-mel_16bar',
                                         checkpoint_dir = music_vae_checkpoint_dir)
    list1 = load_dataset(music_vae_model, midi_directory = "./midi_input/")

if __name__ == "__main__":
    main()