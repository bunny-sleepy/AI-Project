from music_vae.trained_model import TrainedModel
import note_seq
import os, sys
import music_vae.configs as configs

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

def encode_ns(trained_model, ns):
    """encode a note sequence according to a trained model.

    Args:
        trained_model: the trained model, may be loaded from checkpoints or
          use the music_vae.trained_model.TrainedModel method.
        ns: the input note sequence object to encode.

    Return:
        the encoded latent_vec
    """
    config = configs.CONFIG_MAP['hierdec-mel_16bar']
    tensors = config.data_converter.to_tensors(ns)
    if not tensors.inputs:
        raise NoExtractedExamplesError(
            'No examples extracted from NoteSequence')
    inputs = []
    controls = []
    lengths = []
    for i in range(len(tensors.inputs)):
        inputs.append(tensors.inputs[i])
        controls.append(tensors.controls[i])
        lengths.append(tensors.lengths[i])
    z, mu, sigma = trained_model.encode_tensors(inputs, lengths, controls)
    return z, mu, sigma

def encode(trained_model, midi_batch = None):
    """encode a midi_batch according to a trained model.

    Args:
        trained_model: the trained model, may be loaded from checkpoints or
          use the music_vae.trained_model.TrainedModel method.
        midi_batch: the input batch of midi file names.

    Return:
        the encoded dictionary latent_vec, that takes the midi file name as index
          >>> latent_vec['test.midi']
          (z, mu, sigma)
          this is an example of usage.
    """
    noteseqs = {}
    for midi_path in midi_batch:
        noteseq = note_seq.midi_file_to_note_sequence(midi_path)
        midi_file_name = os.path.basename(midi_path)
        noteseqs[midi_file_name] = noteseq
    '''
    Note: before we encode some note sequences,
    we should always check its length when converted to tensors.
    If the length of the tensors is greater than 1,
    we should split it to several sequences.
    '''
    latent_vecs = {}
    config = configs.CONFIG_MAP['hierdec-mel_16bar']
    for midi_file_name in noteseqs:
        noteseq = noteseqs[midi_file_name]
        tensors = config.data_converter.to_tensors(noteseq)
        if not tensors.inputs:
            raise NoExtractedExamplesError(
                'No examples extracted from NoteSequence: %s' % midi_file_name)
        inputs = []
        controls = []
        lengths = []
        for i in range(len(tensors.inputs)):
            inputs.append(tensors.inputs[i])
            controls.append(tensors.controls[i])
            lengths.append(tensors.lengths[i])
        z, mu, sigma = trained_model.encode_tensors(inputs, lengths, controls)
        latent_vecs[midi_file_name] = (z, mu, sigma)
    return latent_vecs

def main():
    path = "./midi_input/test1.mid"
    ns = note_seq.midi_file_to_note_sequence(path)
    music_vae_config_str = 'hierdec-mel_16bar'
    music_vae_checkpoint_dir = './../repository/musicvae_hierdec-mel_16bar'
    music_vae_model = generate_model(config_str = music_vae_config_str,
                                     checkpoint_dir = music_vae_checkpoint_dir)
    print(encode_ns(music_vae_model, ns))

if __name__ == "__main__":
    main()