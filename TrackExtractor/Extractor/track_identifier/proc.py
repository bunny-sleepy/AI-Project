import os
import numpy as np
import sklearn.externals.joblib as joblib

from track_identifier.utils import features
from track_identifier.utils.misc import traverse_dir

from miditoolkit.midi import parser

cur_path = os.path.dirname(os.path.realpath(__file__))
PATH_MODEL = os.path.join(cur_path, 'model/2019-6-24.pkl')

def testing(X):
    # load model
    loaded_model = joblib.load(PATH_MODEL)

    # prediction
    predict_loaded_y = loaded_model.predict(X)
    return list(predict_loaded_y)
    # max_val = -1000
    # for val in list(predict_loaded_y):
    #     if val > max_val:
    #         max_val = val
    # ret_lst = []
    # ret_lst.append(max_val)
    # return ret_lst

def identify_single_track(pianoroll):
    X = features.extract_features(pianoroll)
    test_x = np.array([X])
    return testing(test_x)[0]

def identify_multiple_track(pianorolls):
    # extract features
    num = len(pianorolls)
    test_x = []
    for idx in range(num): 
        X = features.extract_features(pianorolls[idx])
        test_x.append(X)
    test_x = np.array(test_x)
    return testing(test_x)
   
def identify_song(input_obj):
    # loading
    if isinstance(input_obj, str):
        midi_file = parser.MidiFile(path_midi)
    else:
        midi_file = input_obj
    
    # processing
    num_instr = len(midi_file.instruments)

    pianorolls = []
    for idx in range(num_instr):
        pr = midi_file.get_instrument_pianoroll(idx, resample_resolution=24)
        # pr = notes2pianoroll(midi_file.instruments[idx].notes,
        #                     midi_file.ticks_per_beat,
        #                     resample_factor = 24,
        #                     resample_method = round,
        #                     binary_thres = None,
        #                     max_tick = midi_file.max_tick,
        #                     keep_note = True)
        pianorolls.append(pr)
    ys = identify_multiple_track(pianorolls)
    return ys
