from music_vae.trained_model import TrainedModel
import note_seq
import pretty_midi
import music_vae.configs as configs
import os, sys

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

# test: transfer a midi file into note sequence and encode it
midi_path = 'test1.mid'
midi_file = pretty_midi.PrettyMIDI(midi_path)
noteseq = note_seq.midi_file_to_note_sequence(midi_path)
'''
Note: before we encode some note sequences,
we should always check its length when converted to tensors.
If the length of the tensors is greater than 1,
we should split it to several sequences.
'''
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

print(trained_model.encode_tensors(inputs, lengths, controls))