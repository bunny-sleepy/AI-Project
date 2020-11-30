from music_vae.trained_model import TrainedModel
import note_seq
import os, sys
import music_vae.configs as configs

class NoExtractedExamplesError(Exception):
  pass

# TODO: find the appropriate batch size
config_str = 'hierdec-mel_16bar'
config = configs.CONFIG_MAP[config_str]
config.data_converter.max_tensors_per_item = None
batch_size = 8
checkpoint_dir = './../repository/musicvae_hierdec-mel_16bar'
trained_model = TrainedModel(config,
                             batch_size,
                             checkpoint_dir_or_path = checkpoint_dir)

# TODO: concatenate the generated word vector with this function
def decode(trained_model = trained_model, z_batch = [], samples_per_batch = 1, temperature = 0.5):
    """ decode the generated z into note sequences

    Args:
        trained_model: the trained model, may be loaded from checkpoints or
          use the music_vae.trained_model.TrainedModel method.
        z_batch: the input batch of z, each np.array generates one output.
        samples_per_batch: how many note sequences to generate for each z.
        temperature: softmax temperature used in model.decode.

    Return:
        a batch of note sequences.
    """
    note_seq_batch = []
    for z in z_batch:
        for _ in range(samples_per_batch):
            note_seqs = trained_model.decode(z, temperature = temperature)
            note_seq = []
            for ns in note_seqs:
                note_seq.extend(ns)
            note_seq_batch.append(note_seq)
    return note_seq_batch