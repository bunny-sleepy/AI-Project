from music_vae.trained_model import TrainedModel
import note_seq
import os
import music_vae.configs as configs
import time

class NoExtractedExamplesError(Exception):
  pass

# NOTE: plz do not change the directory here, since you can always specify out side this file
def generate_model(config_str = 'hierdec-mel_16bar', checkpoint_dir = None):
    config = configs.CONFIG_MAP[config_str]
    config.data_converter.max_tensors_per_item = None
    batch_size = 8
    trained_model = TrainedModel(config,
                                 batch_size,
                                 checkpoint_dir_or_path = checkpoint_dir)
    return trained_model

def decode(trained_model,
           length = 256,
           z_batch = [],
           samples_per_batch = 1,
           temperature = 0.5):
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
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    note_seq_batch = []
    for z in z_batch:
        for _ in range(samples_per_batch):
            note_seqs = trained_model.decode(z, length = length, temperature = temperature)
            note_seq = []
            for ns in note_seqs:
                note_seq.append(ns)
            note_seq_batch.append(note_seq)
    return note_seq_batch

def decode_to_midi(target_directory,
                   trained_model,
                   length = 256,
                   z_batch = None,
                   samples_per_batch = 1,
                   temperature = 0.5,
                   file_name = ''):
    """ decode the generated z into note sequences

    Args:
        target_directory: the directory to hold the generated piece.
        trained_model: the trained model, may be loaded from checkpoints or
          use the music_vae.trained_model.TrainedModel method.
        length: pass
        z_batch: the input batch of z, each np.array generates one output.
        samples_per_batch: how many note sequences to generate for each z.
        temperature: softmax temperature used in model.decode.
        file_name: the file_name to attach to the front

    Return:
        a batch of note sequences.
    """
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    if z_batch is None:
        z_batch = []
    note_seq_batch = decode(trained_model, length, z_batch, samples_per_batch, temperature)
    basename = os.path.join(
        target_directory,
        '%s_vae_output_%s_%03d_*.mid' %
        (file_name, date_and_time, samples_per_batch))
    output_file_paths = []
    for noteseq in note_seq_batch:
        i = 0
        for ns in noteseq:
            i = i + 1
            file_path = basename.replace('*', '%03d' % i)
            note_seq.sequence_proto_to_midi_file(ns, file_path)
            output_file_paths.append(file_path)
    return output_file_paths