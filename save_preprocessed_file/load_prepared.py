import numpy as np 
import os

def load_prepared_dataset(file_path):
    midi_wordvec_list = []
    midi_latentvec_list = []
    dirs = os.listdir(file_path)
    for dir in dirs:
        # print (dir)
        path = file_path + '/' + dir 
        files = os.listdir(path)
        # name: the
        name = None
        for file in files: 
            if file == 'name.npy':
                npath = path + '/name.npy'
                name =  np.load(npath)
        for file in files:
            if file != 'name.npy':
                lpath = path + '/' + file
                latent = np.load(lpath)
                midi_wordvec_list.append(name)
                midi_latentvec_list.append(latent)
    
    return midi_latentvec_list, midi_wordvec_list