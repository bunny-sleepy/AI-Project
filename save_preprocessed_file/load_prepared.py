import numpy as np 
import os

def load_prepared_dataset(file_path):
    midi_wordvec_list = []
    midi_latentvec_list = []
    dirs = os.listdir(file_path)
    for dir in dirs:
        # print (dir)
        path = "%s/%s" % (file_path, dir)
        files = os.listdir(path)
        # name: the
        name = None
        for file in files:
            if file == 'name.npy':
                npath = '%s/name.npy' % path
                name =  np.load(npath)
        for file in files:
            if file != 'name.npy':
                latent = np.load("%s/%s" % (path, file))
                midi_wordvec_list.append(np.array(name))
                midi_latentvec_list.append(latent)
    
    return midi_latentvec_list, midi_wordvec_list

# Test on this method
def main():
    # filepath = 'C:/Users/Li/Desktop/Latex file/AI_proj/AI-proj/testback/storetest'
    filepath = 'D:/code/Github/repository/encoded_data_test'
    latent_list, wordvec_list = load_prepared_dataset(filepath)
    print((wordvec_list))

if __name__ == "__main__":
    main()