import os
import numpy as np
import re
import preprocessing.preprocess_title as ppt
import bert_try as bt
import latent_vec_generate as lvg
import preprocessing.preprocess_midi as ppm
import note_seq

try:
    word_dct = ppt.word_dict('./preprocessing/word.txt')
except:
    word_dct = None

def prepare_dataset(musicvae_model, dataset_path, stored_path, word_dict = word_dct, max_num = 1000):
    file_list = os.listdir(dataset_path)
    curr_num = 0
    for filename in file_list:
        if curr_num < max_num:
            midi_file = "%s/%s" % (dataset_path, filename)
            midi_store_path = "%s/%s" % (stored_path, os.path.splitext(filename)[0])
            print(midi_file)
            if (".mid" in filename) or (".midi" in filename):
                file_valid, title = ppt.file_title(midi_file, word_dict)
                if file_valid:
                    midi_wordvec = bt.encode_nlp(title)
                    ns = note_seq.midi_file_to_note_sequence(midi_file)
                    try:
                        if not os.path.exists(midi_store_path): 
                            os.mkdir(midi_store_path)
                        np.save("%s/name.npy" % midi_store_path, midi_wordvec)
                        new_ns = ppm.get_new_ns(ppm.skyline(ns), ns)
                        z_list, _, _ = lvg.encode_ns(musicvae_model, new_ns)
                        i = 0
                        for z in z_list:
                            np.save('%s/%02d.npy' % (midi_store_path, i), z)
                            i = i + 1
                        curr_num += 1
                        print("%04d/%04d: data loaded successfully at %s" % (curr_num, max_num, filename))
                    except:
                        print("unable to load the file at %s" % filename)
                else:
                    print("invalid midi file at %s" % filename)

# Test on this method
def main():
    dataset_path = 'C:/Users/Li/Desktop/Latex file/AI_proj/AI-proj/musictest'
    stored_path = 'C:/Users/Li/Desktop/Latex file/AI_proj/AI-proj/testback/storetest'
    music_vae_config_str = 'hierdec-mel_16bar'
    music_vae_checkpoint_dir = 'C:/Users/Li/Desktop/Latex file/AI_proj/hierdec-mel_16bar'
    music_vae_model = lvg.generate_model(config_str = music_vae_config_str,
                                         checkpoint_dir = music_vae_checkpoint_dir)
    prepare_dataset(music_vae_model, dataset_path, stored_path)

if __name__ == "__main__":
    main()