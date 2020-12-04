import note_seq
import os, sys

test_target = './midi_input/SomebodyThatIUsedToKnow(BetterVersion).mid'
# test_target = './midi_input/7Days.mid'
file = open('note_seq3.txt', 'w+')

ns = note_seq.midi_file_to_note_sequence(test_target)

# According to the maximum pitch difference
def max_pitch_diff(ns):
    number = {}
    for note in ns.notes:
        if not note.is_drum:
            if note.instrument in number.keys():
                number[note.instrument] = (min(note.pitch, number[note.instrument][0]),
                                           max(note.pitch, number[note.instrument][1]))
            else:
                number[note.instrument] = (note.pitch, note.pitch)
    # print(number)

    max_instrument = -1
    max_pitch_difference = -1
    for instrument in number:
        # print(number[instrument][0], number[instrument][1])
        if number[instrument][1] - number[instrument][0] > max_pitch_difference:
            max_instrument = instrument
            max_pitch_difference = number[instrument][1] - number[instrument][0]
    return max_instrument, number

# According to the maximum pitch
def max_pitch(ns):
    number = {}
    for note in ns.notes:
        if not note.is_drum:
            if note.instrument in number.keys():
                if note.pitch > number[note.instrument]:
                    number[note.instrument] = note.pitch
            else:
                number[note.instrument] = note.pitch
    max_instrument = -1
    max_pitch = -1
    for instrument in number:
        # print(number[instrument][0], number[instrument][1])
        if number[instrument] > max_pitch:
            max_instrument = instrument
            max_pitch = number[instrument]
    return max_instrument, number

# According to the pitch diversity
def max_diversity(ns):
    number = {}
    for note in ns.notes:
        if not note.is_drum:
            if note.instrument in number.keys():
                if not note.pitch in number[note.instrument]:
                    number[note.instrument].append(note.pitch)
            else:
                number[note.instrument] = [note.pitch]
    max_instrument = -1
    max_pitch_num = -1
    for instrument in number:
        # print(number[instrument][0], number[instrument][1])
        if len(number[instrument]) > max_pitch_num:
            max_instrument = instrument
            max_pitch_num = len(number[instrument])
    return max_instrument, number

def get_new_ns(max_instrument):
    seq = note_seq.NoteSequence()
    seq.tempos.add().qpm = ns.tempos[0].qpm
    seq.ticks_per_quarter = ns.ticks_per_quarter
    new_notes = []
    for note in ns.notes:
        if not note.is_drum:
            if note.instrument == max_instrument:
                new_notes.append(note)
    timing = 1000000.0
    for note in new_notes:
        if note.start_time < timing:
            timing = note.start_time
    for note in new_notes:
        note.start_time -= timing
        note.end_time -= timing
    seq.notes.extend(new_notes)
    return seq

def skyline(ns):
    """ Returns the melody track according to the skyline algorithm
    To get more detail on this algorithm,
    please see https://www.tastestars.com/index.php/2019/01/03/1-17/

    Args:
        ns: the note sequence to extract melody from

    Return:
        the melody note sequence object
    """
    pitch_diff = max_pitch_diff(ns)[1]
    pitch_max = max_pitch(ns)[1]
    pitch_diversity = max_diversity(ns)[1]
    print(pitch_max)
    print(pitch_diff)
    print(pitch_diversity)
    pick_num = 3
    top_diff = []
    top_max = []
    top_diversity = []
    for instrument in pitch_diff:
        if len(top_diff) < pick_num:
            top_diff.append(instrument)
        else:
            min_index = -1
            min_diff = 10000
            for ins in top_diff:
                curr_diff = pitch_diff[ins][1] - pitch_diff[ins][0]
                if curr_diff < min_diff:
                    min_diff = curr_diff
                    min_index = top_diff.index(ins)
            if pitch_diff[instrument][1] - pitch_diff[instrument][0] > min_diff:
                top_diff[min_index] = instrument

    for instrument in pitch_max:
        if len(top_max) < pick_num:
            top_max.append(instrument)
        else:
            min_index = -1
            min_max = 10000
            for ins in top_max:
                curr_max = pitch_max[ins]
                if curr_max < min_max:
                    min_max = curr_max
                    min_index = top_max.index(ins)
            if pitch_diff[instrument][1] - pitch_diff[instrument][0] > min_max:
                top_max[min_index] = instrument

    for instrument in pitch_diversity:
        if len(top_diversity) < pick_num:
            top_diversity.append(instrument)
        else:
            min_index = -1
            min_diff = 10000
            for ins in top_diversity:
                curr_diff = pitch_diff[ins][1] - pitch_diff[ins][0]
                if curr_diff < min_diff:
                    min_diff = curr_diff
                    min_index = top_diversity.index(ins)
            if pitch_diff[instrument][1] - pitch_diff[instrument][0] > min_diff:
                top_diversity[min_index] = instrument
    print(top_diff, top_diversity, top_max)
    target = []
    for instrument in top_diversity:
        if (instrument in top_max) and (instrument in top_diff):
            target.append(instrument)
    if len(target) == 0:
        return None
    target_instrument = target[0]
    return target_instrument

def main():
    try:
        seq = get_new_ns(skyline(ns))
        note_seq.sequence_proto_to_midi_file(seq, './midi_output/preprocess_output/out%s.mid' % '1')
    except:
        print('No track selected')

if __name__ == '__main__':
    main()