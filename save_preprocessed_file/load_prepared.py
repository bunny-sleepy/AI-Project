import numpy as np 
import os
import shutil

def load_prepared_dataset_with_err(file_path, pooling = False, max_number = None):
    midi_wordvec_list = []
    z_list = []
    mu_list = []
    sigma_list = []
    dirs = os.listdir(file_path)
    num = 0
    for dir in dirs:
        if max_number is not None:
            if num >= max_number:
                break
        num += 1
        print("Loading %d-th folder" % num)
        path = os.path.join(file_path, dir)
        z_path = os.path.join(path, 'z')
        mu_path = os.path.join(path, 'mu')
        sigma_path = os.path.join(path, 'sigma')
        # if not os.path.exists(z_path) or not os.path.exists(mu_path) or not os.path.exists(sigma_path):
        #     os.remove(path)
        try:
            files = os.listdir(path)
            z_files = os.listdir(z_path)
            mu_files = os.listdir(mu_path)
            sigma_files = os.listdir(sigma_path)
            name = None
            for file in files:
                if file == 'name.npy':
                    npath = os.path.join(path, file)
                    name = np.load(npath)
            for file in z_files:
                z = np.load(os.path.join(z_path, file))
                if not pooling:
                    midi_wordvec_list.append(np.array(name[0]))
                else:
                    midi_wordvec_list.append(np.max(name, axis = 0))
                z_list.append(z)
            for file in mu_files:
                mu = np.load(os.path.join(mu_path, file))
                mu_list.append(mu)
            for file in sigma_files:
                sigma = np.load(os.path.join(sigma_path, file))
                sigma_list.append(sigma)
            print('Loaded successfully')
        except:
            print('Failed to Load at %s' % path)
            shutil.rmtree(path)
    return z_list, mu_list, sigma_list, midi_wordvec_list

def load_prepared_dataset_without_err(file_path, pooling = False, max_number = None):
    midi_wordvec_list = []
    z_list = []
    mu_list = []
    sigma_list = []
    dirs = os.listdir(file_path)
    num = 0
    for dir in dirs:
        if max_number is not None:
            if num >= max_number:
                break
        num += 1
        print("Loading %d-th folder" % num)
        path = os.path.join(file_path, dir)
        z_path = os.path.join(path, 'z')
        mu_path = os.path.join(path, 'mu')
        sigma_path = os.path.join(path, 'sigma')
        # if not os.path.exists(z_path) or not os.path.exists(mu_path) or not os.path.exists(sigma_path):
        #     os.remove(path)
        files = os.listdir(path)
        z_files = os.listdir(z_path)
        mu_files = os.listdir(mu_path)
        sigma_files = os.listdir(sigma_path)
        name = None
        for file in files:
            if file == 'name.npy':
                npath = os.path.join(path, file)
                name = np.load(npath)
        for file in z_files:
            z = np.load(os.path.join(z_path, file))
            if not pooling:
                midi_wordvec_list.append(np.array(name[0]))
            else:
                midi_wordvec_list.append(np.max(name, axis = 0))
            z_list.append(z)
        for file in mu_files:
            mu = np.load(os.path.join(mu_path, file))
            mu_list.append(mu)
        for file in sigma_files:
            sigma = np.load(os.path.join(sigma_path, file))
            sigma_list.append(sigma)
        print('Loaded successfully')
    return z_list, mu_list, sigma_list, midi_wordvec_list

# Test
def main():
    # filepath = 'C:/Users/Li/Desktop/Latex file/AI_proj/AI-proj/testback/storetest'
    filepath = 'D:/code/Github/repository/encoded_data_2021_1_3'
    z_list, mu_list, sigma_list, wordvec_list = load_prepared_dataset(filepath)
    print(z_list)
    print(mu_list)
    print(sigma_list)

if __name__ == "__main__":
    main()