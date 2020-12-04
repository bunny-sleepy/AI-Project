import latent_vec_decode, latent_vec_generate
from music_vae.trained_model import TrainedModel
import music_vae.configs as configs
import numpy as np

# TODO: find the appropriate batch size
config_str = 'hierdec-mel_16bar'
config = configs.CONFIG_MAP[config_str]
config.data_converter.max_tensors_per_item = None
batch_size = 8
# NOTE: you should change your directory HERE
checkpoint_dir = 'D:/code/Github/repository/musicvae_hierdec-mel_16bar'
trained_model = TrainedModel(config,
                             batch_size,
                             checkpoint_dir_or_path = checkpoint_dir)

# test on the decode test1.mid
test_file_path = './midi_input/test1.mid'
z, mu, sigma = latent_vec_generate.encode(trained_model = trained_model,
                                          midi_batch=[test_file_path])['test1.mid']
target_directory = './midi_output/decode_output'
latent_vec_decode.decode_to_midi(
    target_directory,
    trained_model = trained_model,
    length = len(z),
    z_batch = [z])

