import numpy as np
from track_identifier import proc
from miditoolkit.midi import parser
import preprocessing.preprocess_midi as pm
import preprocessing.preprocess_title as pt
import note_seq
import os

# save only melodic track
# path_midi = 'test_midis/aladdin-medley-of-all-songs-mid.mid'

def preprocess(path_midi, dump_path = 'tmp.mid'):
    midi_file = parser.MidiFile(path_midi)
    ys = proc.identify_song(midi_file)
    midx = list(np.where(np.array(ys)==0)[0])
    midi_file.dump(filename = dump_path, instrument_idx = midx)

def extract_track(input_directory, file_name, output_directory):
    path_mid = input_directory + "/" + file_name
    dump_path = output_directory + "/" + file_name + ".tmp"
    # algo according to script.py
    try:
        preprocess(path_mid, dump_path)
        # algo according to filters
        ns = note_seq.midi_file_to_note_sequence(dump_path)
        new_ns = pm.get_new_ns(pm.skyline(ns, mode = 'argmax'), ns)
        # save the output
        save_path = output_directory + "/" + file_name
        note_seq.sequence_proto_to_midi_file(new_ns, save_path)
    except:
        try:
            ns = note_seq.midi_file_to_note_sequence(path_mid)
            new_ns = pm.get_new_ns(pm.skyline(ns, mode = 'variance_first'), ns)
            save_path = output_directory + "/" + file_name
            note_seq.sequence_proto_to_midi_file(new_ns, save_path)
        except:
            pass
    if os.path.exists(dump_path):
        os.remove(dump_path)

def batch_extract_track(input_dir_name, dic_path, output_dir_name):
    for filename in os.listdir(input_dir_name):
        is_valid, _ = pt.file_title(input_dir_name + "/" + filename, pt.word_dict(dic_path))
        if is_valid:
            extract_track(input_dir_name, filename, output_dir_name)

def main():
    batch_extract_track("I:/input",
                        "I:/FinalProj/AI-Project/preprocessing/word.txt",
                        "I:/output")

if __name__ == "__main__":
    main()