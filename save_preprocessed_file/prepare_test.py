from save_preprocessed_file.dataset_prepare import prepare_dataset
import latent_vec_generate as lvg

def main():
    dataset_path = 'C:/Users/Li/Desktop/Latex file/AI_proj/AI-proj/musictest'
    stored_path = 'C:/Users/Li/Desktop/Latex file/AI_proj/AI-proj/testback/storetest'
    # dataset_path = 'D:/code/Github/AI-Project/midi_input'

    music_vae_config_str = 'hierdec-mel_16bar'
    music_vae_checkpoint_dir = 'C:/Users/Li/Desktop/Latex file/AI_proj/hierdec-mel_16bar'
    music_vae_model = lvg.generate_model(config_str = music_vae_config_str,
                                         checkpoint_dir = music_vae_checkpoint_dir)

    prepare_dataset(music_vae_model, dataset_path, stored_path)
    #c = np.load(filepath)
    # print (c)

if __name__ == "__main__":
    main()