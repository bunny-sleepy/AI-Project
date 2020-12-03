import note_seq
import os, sys

test_target = './preprocessing/SomebodyThatIUsedToKnow(BetterVersion).mid'
file = open('note_seq3.txt', 'w+')
seq = note_seq.NoteSequence()
ns = note_seq.midi_file_to_note_sequence(test_target)

# print(ns.tempos[0].qpm)
seq.tempos.add().qpm = ns.tempos[0].qpm
seq.ticks_per_quarter = ns.ticks_per_quarter

new_notes = []

number = {}

for note in ns.notes:
    if not note.is_drum:
        if note.instrument in number.keys():
            number[note.instrument] += 1
        else:
            number[note.instrument] = 1

print(number)

for note in ns.notes:
    if not note.is_drum:
        new_notes.append(note)

seq.notes.extend(new_notes)
# file.write(str(ns))

note_seq.sequence_proto_to_midi_file(seq, 'out3.mid')