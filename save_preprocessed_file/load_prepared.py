import numpy as np 
import os

def load_prepared_dataset(file_path, pooling = False, max_number = None):
    midi_wordvec_list = []
    midi_latentvec_list = []
    dirs = os.listdir(file_path)
    num = 0
    for dir in dirs:
        if max_number is not None:
            if num >= max_number:
                break
        num += 1
        print("Loading %d-th folder" % num)
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
                if not pooling:
                    midi_wordvec_list.append(np.array(name[0]))
                else:
                    midi_wordvec_list.append(np.max(name, axis = 0))
                midi_latentvec_list.append(latent)
    
    return midi_latentvec_list, midi_wordvec_list

# Test on this method
def main():
    # filepath = 'C:/Users/Li/Desktop/Latex file/AI_proj/AI-proj/testback/storetest'
    filepath = 'D:/code/Github/repository/encoded_data_test'
    latent_list, wordvec_list = load_prepared_dataset(filepath)
    print(wordvec_list)

if __name__ == "__main__":
    main()