import note_seq
import os, sys
import numpy as np

# test_target = './midi_input/BackToDecember.mid'
test_target = './midi_input/SomebodyThatIUsedToKnow(BetterVersion).mid'
# test_target = './midi_input/7Days.mid'
file = open('note_seq3.txt', 'w+')

ns = note_seq.midi_file_to_note_sequence(test_target)

def avg_velocity(ns):
    number = {}
    for note in ns.notes:
        if not note.is_drum:
            if note.instrument in number.keys():
                number[note.instrument].append(note.velocity)
            else:
                number[note.instrument] = [note.velocity]
    for instrument in number:
        mean_velocity = np.mean(number[instrument])
        number[instrument] = mean_velocity
    max_instrument = -1
    max_pitch_avg = -1.0
    for instrument in number:
        if number[instrument] > max_pitch_avg:
            max_instrument = instrument
            max_pitch_avg = number[instrument]
    return max_instrument, number

def total_time(ns):
    number = {}
    for note in ns.notes:
        if not note.is_drum:
            if note.instrument in number.keys():
                number[note.instrument].append(note.end_time - note.start_time)
            else:
                number[note.instrument] = [note.end_time - note.start_time]
    max_instrument = -1
    max_total_time = -1.0
    for instrument in number:
        if np.sum(number[instrument]) > max_total_time:
            max_instrument = instrument
            max_total_time = np.sum(number[instrument])
    return max_instrument, number

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
    if max_instrument is None:
        return None
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
    pitch_total_time = total_time(ns)[1]
    # print(pitch_max)
    # print(pitch_diff)
    # print(pitch_diversity)
    pick_num = len(pitch_max) / 3
    pick_num_max = len(pitch_max) * 3 / 4
    top_diff = []
    top_max = []
    top_diversity = []
    top_total_time = []

    for instrument in pitch_total_time:
        if len(top_total_time) < pick_num:
            top_total_time.append(instrument)
        else:
            min_index = -1
            min_total_time = 10000.0
            for ins in top_total_time:
                curr_total_time = np.sum(pitch_total_time[ins])
                if curr_total_time < min_total_time:
                    min_total_time = curr_total_time
                    min_index = top_total_time.index(ins)
            if np.sum(pitch_total_time[instrument]) > min_total_time:
                top_total_time[min_index] = instrument

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
        if len(top_max) < pick_num_max:
            top_max.append(instrument)
        else:
            min_index = -1
            min_max = 10000
            for ins in top_max:
                curr_max = pitch_max[ins]
                if curr_max < min_max:
                    min_max = curr_max
                    min_index = top_max.index(ins)
            if pitch_max[instrument] > min_max:
                top_max[min_index] = instrument

    for instrument in pitch_diversity:
        if len(top_diversity) < pick_num:
            top_diversity.append(instrument)
        else:
            min_index = -1
            min_diversity = 10000
            for ins in top_diversity:
                curr_diversity = len(pitch_diversity[ins])
                if curr_diversity < min_diversity:
                    min_diversity = curr_diversity
                    min_index = top_diversity.index(ins)
            if len(pitch_diversity[instrument]) > min_diversity:
                top_diversity[min_index] = instrument

    print(top_diff, top_diversity, top_max, top_total_time)
    target = []
    # for instrument in top_diversity:
    #     if (instrument in top_max) and (instrument in top_diff) and (instrument in top_total_time):
    #         target.append(instrument)
    # if len(target) == 0:
    #     return None
    # target_instrument = target[0]
    target.extend(top_diff)
    target.extend(top_diversity)
    target.extend(top_max)
    target.extend(top_total_time)

    counts = np.bincount(target)
    target_instrument = np.argmax(counts)
    return target_instrument

def main():
    notes = skyline(ns)
    if notes is None:
        print('No track selected')
    else:
        seq = get_new_ns(notes)
        note_seq.sequence_proto_to_midi_file(seq, './midi_output/preprocess_output/out%s.mid' % '1')

if __name__ == '__main__':
    main()