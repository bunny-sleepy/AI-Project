import note_seq
import os, sys

test_target = './preprocessing/7Days.mid'
file = open('note_seq1.txt', 'w+')
seq = note_seq.NoteSequence()
ns = note_seq.midi_file_to_note_sequence(test_target)
seq.tempos.add().qpm = note_seq.DEFAULT_QUARTERS_PER_MINUTE
seq.ticks_per_quarter = note_seq.STANDARD_PPQ

new_notes = []

number = {}

for note in ns.notes:
    if note.instrument in number.keys():
        number[note.instrument] += 1
    else:
        number[note.instrument] = 1

print(number)
seq.notes.extend(new_notes)

# note_seq.sequence_proto_to_midi_file(seq, 'out.mid')