import os
import numpy as np
import bert_try as bt
import latent_vec_generate as lvg
import preprocessing.preprocess_midi as ppm
import note_seq
import preprocessing.preprocess_title as ppt

word_dct = ppt.word_dict('./preprocessing/preprocess_title.py')

def prepare_dataset(musicvae_model, dataset_path, stored_path, word_dict = word_dct, max_num = 1000):
    file_list = os.listdir(dataset_path)
    curr_num = 0
    for filename in file_list:
        # only append midi files
        if curr_num < max_num:
            midi_file = dataset_path + '/' + filename
            midi_store_path = stored_path + '/' + os.path.splitext(filename)[0]
            print(midi_file)
            if (".mid" in filename) or (".midi" in filename):
                file_valid, title = ppt.file_title(midi_file, word_dict)
                if file_valid:
                    # this will remove ".mid", ".midi", "(*)", "[*]", "{*}" from filename
                    # NOTE: ".midi" MUST be before ".mid"
                    midi_wordvec = np.max(bt.encode_nlp(title), axis=0)
                    ns = note_seq.midi_file_to_note_sequence(midi_file)
                    # z_list, _, _ = lvg.encode_ns(musicvae_model, ns)
                    # TODO: change this midi preprocessing method
                    try:
                        if not os.path.exists(midi_store_path): 
                            os.mkdir(midi_store_path)
                        midi_store_path_name = midi_store_path + '/name.npy'
                        np.save(midi_store_path_name, midi_wordvec)
                        new_ns = ppm.get_new_ns(ppm.skyline(ns), ns)
                        z_list, _, _ = lvg.encode_ns(musicvae_model, new_ns)
                        i = 0
                        for z in z_list:
                            np.save('%s/%02d.npy' % (midi_store_path, i))
                            i = i + 1
                        curr_num += 1
                        print("%04d/%04d: data loaded successfully at %s" % (curr_num, max_num, filename))
                    except:
                        print("unable to load the file at %s" % filename)
                else:
                    print("invalid midi file at %s" % filename)