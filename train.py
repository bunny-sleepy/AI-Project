import word2latent as w2l
import numpy as np
import load_dataset as ld
import latent_vec_generate as lvg
import word2latent_torch as w2lt
import torch

def main():
    dataset_path = 'D:/Downloads/midi'
    # dataset_path = 'D:/code/Github/AI-Project/midi_input'
    music_vae_config_str = 'hierdec-mel_16bar'
    music_vae_checkpoint_dir = 'D:/code/Github/repository/musicvae_hierdec-mel_16bar'
    music_vae_model = lvg.generate_model(config_str = music_vae_config_str,
                                         checkpoint_dir = music_vae_checkpoint_dir)
    midi_wordvec_list, midi_latentvec_list = ld.load_dataset(music_vae_model,
                                                             midi_directory = dataset_path,
                                                             max_num = 2)
    wordvec_tensors = torch.from_numpy(np.array(midi_wordvec_list))
    latentvec_tensors = torch.from_numpy(np.array(midi_latentvec_list))

    w2l_model = w2lt.train_model(wordvec_tensors,
                    latentvec_tensors,
                    epochs = 1000,
                    train = True)


if __name__ == "__main__":
    main()