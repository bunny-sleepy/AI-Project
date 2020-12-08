import numpy as np
from track_identifier import proc
from miditoolkit.midi import parser

# save only melodic track
# path_midi = 'test_midis/aladdin-medley-of-all-songs-mid.mid'
path_midi = 'test_midis/SomebodyThatIUsedToKnow.mid'
midi_file = parser.MidiFile(path_midi)
ys = proc.identify_song(midi_file)

print(ys)
midx = list(np.where(np.array(ys)==0)[0])
print(midx)
midi_file.dump(filename='melody.mid', instrument_idx=midx)
