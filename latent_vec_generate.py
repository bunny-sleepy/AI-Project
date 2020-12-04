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
checkpoint_dir = 'D:/code/Github/repository/musicvae_hierdec-mel_16bar'
trained_model = TrainedModel(config,
                             batch_size,
                             checkpoint_dir_or_path = checkpoint_dir)

# encode
# test: transfer a midi file into note sequence and encode it

def encode(trained_model = trained_model, midi_batch = []):
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
    for midi_file_name in noteseqs:
        noteseq = noteseqs[midi_file_name]
        tensors = config.data_converter.to_tensors(noteseq)
        if not tensors.inputs:
            raise NoExtractedExamplesError(
                'No examples extracted from NoteSequence: %s' % noteseq)
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

# z, mu, sigma = encode(trained_model, ['test1.mid'])['test1.mid']