import numpy as np
from track_identifier import proc
from miditoolkit.midi import parser
import preprocessing.preprocess_midi as pm
import note_seq

# save only melodic track
# path_midi = 'test_midis/aladdin-medley-of-all-songs-mid.mid'

def preprocess(path_midi, dump_path = 'tmp.mid'):
    midi_file = parser.MidiFile(path_midi)
    ys = proc.identify_song(midi_file)
    midx = list(np.where(np.array(ys)==0)[0])
    midi_file.dump(filename = dump_path, instrument_idx = midx)

def main():
    path_mid = 'test_midis/advance-wars-2-black-hole-rising-super-co-power-mid.mid'
    dump_path = '_tmp.mid'
    # algo according to script.py
    try:
        preprocess(path_mid, dump_path)
        # algo according to filters
        ns = note_seq.midi_file_to_note_sequence(dump_path)
        new_ns = pm.get_new_ns(pm.skyline(ns), ns)
        # save the output
        save_path = '_out.mid'
        note_seq.sequence_proto_to_midi_file(new_ns, save_path)
    except:
        ns = note_seq.midi_file_to_note_sequence(path_mid)
        new_ns = pm.get_new_ns(pm.skyline(ns, mode = 'variance_first'), ns)
        save_path = '_out.mid'
        note_seq.sequence_proto_to_midi_file(new_ns, save_path)

if __name__ == "__main__":
    main()