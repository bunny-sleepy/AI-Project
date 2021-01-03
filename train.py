import numpy as np
import save_preprocessed_file.load_prepared as lp
import word2latent as w2l
import os

def main():
    dataset_path = 'D:/code/Github/repository/encoded_data_2021_1_3'
    z_list, mu_list, sigma_list, midi_wordvec_list = lp.load_prepared_dataset_without_err(dataset_path, max_number = None)
    base_model_dir = 'D:/code/Github/AI-Project/model/'
    label = '2021_1_2'
    model_dir = os.path.join(base_model_dir, label)
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    checkpoint_dir_mean = os.path.join(model_dir, 'mean')
    if not os.path.exists(checkpoint_dir_mean):
        os.mkdir(checkpoint_dir_mean)
    checkpoint_dir_variance = os.path.join(model_dir, 'variance')
    if not os.path.exists(checkpoint_dir_variance):
        os.mkdir(checkpoint_dir_variance)
    w2l_model_variance = w2l.train_model_variance(np.array(midi_wordvec_list), np.array(sigma_list), checkpoint_path_variance = checkpoint_dir_variance,
                                epochs = 6000, batch_size = 512, load = True, save_every_n_epochs = 1000)
    w2l_model_mean = w2l.train_model_mean(np.array(midi_wordvec_list), np.array(mu_list), checkpoint_path_mean = checkpoint_dir_mean,
                                  epochs = 6000, batch_size = 512, load = True, save_every_n_epochs = 1000)

if __name__ == "__main__":
    main()