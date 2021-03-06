import numpy as np
import save_preprocessed_file.load_prepared as lp
import word2latent as w2l
import os

def main():
    dataset_path = 'D:/code/Github/repository/encoded_data_2020_12_26'
    z_list, mu_list, sigma_list, midi_wordvec_list = lp.load_prepared_dataset(dataset_path, max_number = None)
    base_model_dir = 'D:/code/Github/AI-Project/model/'
    label = '2020_12_31'
    model_dir = os.path.join(base_model_dir, label)
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    checkpoint_dir_mean = os.path.join(model_dir, 'mean')
    if not os.path.exists(checkpoint_dir_mean):
        os.mkdir(checkpoint_dir_mean)
    w2l_model_mean = w2l.train_model_mean(np.array(midi_wordvec_list),
                                          np.array(mu_list),
                                          checkpoint_path_mean = checkpoint_dir_mean,
                                          epochs = 20000,
                                          batch_size = 512,
                                          load = True)

if __name__ == "__main__":
    main()