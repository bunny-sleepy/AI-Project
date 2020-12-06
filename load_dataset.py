import os
import re
import preprocessing.preprocess_title as ppt
import bert_try as bt
import latent_vec_generate as lvg
import numpy as np
import preprocessing.preprocess_midi as ppm
import note_seq

# NOTE: absolute path recommended
def load_dataset(musicvae_model, midi_directory = "PATH", max_num = 1000):
    """ load midi dataset from a given directory

    Args:
        musicvae_model: the musicvae_model to load
        midi_directory: directory of midi files
        max_num: how many files to load

    Return:
        the x, y data ready for training
    """

    file_list = os.listdir(midi_directory)
    midi_wordvec_list = []
    midi_latentvec_list = []

    curr_num = 0
    if curr_num < max_num:
        for filename in file_list:
            # only append midi files
            midi_file = midi_directory + '/' + filename
            print(midi_file)
            if (".mid" in filename) or (".midi" in filename):
                file_valid, title = ppt.file_title(midi_file)
                if file_valid:
                    # this will remove ".mid", ".midi", "(*)", "[*]", "{*}" from filename
                    # NOTE: ".midi" MUST be before ".mid"
                    midi_wordvec = np.max(bt.encode_nlp(title), axis=0)
                    ns = note_seq.midi_file_to_note_sequence(midi_file)
                    # z_list, _, _ = lvg.encode_ns(musicvae_model, ns)
                    # TODO: change this midi preprocessing method
                    # if True:
                    try:
                        new_ns = ppm.get_new_ns(ppm.skyline(ns), ns)
                        # note_seq.sequence_proto_to_midi_file(new_ns, 'tmp.mid')
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
    list1 = load_dataset("I:/FinalProj/AI-Project/midi_input")
    for item in list1:
        print(item)

if __name__ == "__main__":
    main()