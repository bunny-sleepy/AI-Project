import note_seq
import numpy as np

# According to the average velocity of notes
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

# According to the total time
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
    max_instrument = -1
    max_pitch_difference = -1
    for instrument in number:
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
    max_pt = -1
    for instrument in number:
        if number[instrument] > max_pt:
            max_instrument = instrument
            max_pt = number[instrument]
    return max_instrument, number

# According to maximum variance
def pitch_var(ns):
    number = {}
    for note in ns.notes:
        if not note.is_drum:
            if note.instrument in number.keys():
                number[note.instrument].append(note.pitch)
            else:
                number[note.instrument] = [note.pitch]
    for instrument in number:
        var_pitch = np.var(number[instrument])
        number[instrument] = var_pitch
    max_instrument = -1
    max_pitch_var = -1.0
    for instrument in number:
        if number[instrument] > max_pitch_var:
            max_instrument = instrument
            max_pitch_var = number[instrument]
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
        if len(number[instrument]) > max_pitch_num:
            max_instrument = instrument
            max_pitch_num = len(number[instrument])
    return max_instrument, number

def get_new_ns(max_instrument, ns):
    if max_instrument is None:
        return None
    seq = note_seq.NoteSequence()
    seq.source_info.parser = ns.source_info.parser
    seq.source_info.encoding_type = ns.source_info.encoding_type
    for tempo in ns.tempos:
        seq.tempos.add().qpm = tempo.qpm
    seq.ticks_per_quarter = ns.ticks_per_quarter
    for ns_time_signature in ns.time_signatures:
        time_signature = seq.time_signatures.add()
        try:
            time_signature.numerator = ns.time_signatures.numerator
            time_signature.denominator = ns.time_signatures.denominator
        except:
            time_signature.numerator = 4
            time_signature.denominator = 4
    for ns_key_signature in ns.key_signatures:
        key_signature = seq.key_signatures.add()
        key_signature = ns_key_signature

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
    seq.total_time = ns.total_time - timing
    return seq

def skyline(ns, mode = 'argmax'):
    """ Returns the melody track according to the skyline algorithm
    To get more details on this algorithm,
    please see https://www.tastestars.com/index.php/2019/01/03/1-17/

    Args:
        ns: the note sequence to extract melody from
        mode: the allowed mode
            argmax: argmax of all filters
            variance_first: restricted on the first 1/3 variance of the tracks

    Return:
        the melody note sequence object
    """
    pitch_diff = max_pitch_diff(ns)[1]
    pitch_max = max_pitch(ns)[1]
    pitch_diversity = max_diversity(ns)[1]
    pitch_total_time = total_time(ns)[1]
    pitch_velocity = avg_velocity(ns)[1]
    pitch_variance = pitch_var(ns)[1]
    pick_num = max(int(len(pitch_max) / 3), 1)
    pick_num_max = max(int(len(pitch_max) * 2 / 3), 1)
    top_diff = []
    top_max = []
    top_diversity = []
    top_total_time = []
    top_velocity = []
    top_variance = []

    for instrument in pitch_variance:
        if len(top_variance) < pick_num:
            top_variance.append(instrument)
        else:
            min_index = -1
            min_variance = 10000.0
            for ins in top_variance:
                curr_variance = pitch_variance[ins]
                if curr_variance < min_variance:
                    min_variance = curr_variance
                    min_index = top_variance.index(ins)
            if pitch_variance[instrument] > min_variance:
                top_variance[min_index] = instrument

    if len(top_variance) == 0:
        return None

    for instrument in pitch_velocity:
        if len(top_velocity) < pick_num:
            top_velocity.append(instrument)
        else:
            min_index = -1
            min_velocity = 10000.0
            for ins in top_velocity:
                curr_velocity = pitch_velocity[ins]
                if curr_velocity < min_velocity:
                    min_velocity = curr_velocity
                    min_index = top_velocity.index(ins)
            if pitch_velocity[instrument] > min_velocity:
                top_velocity[min_index] = instrument

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
    if mode == 'argmax':
        target = []
        target.extend(top_diff)
        target.extend(top_diversity)
        target.extend(top_max)
        target.extend(top_total_time)
        target.extend(top_velocity)
        target.extend(top_variance)

        counts = np.bincount(target)
        target_instrument = np.argmax(counts)
        return target_instrument
    elif mode == 'variance_first':
        target = []
        target.extend(list(set(top_diff).intersection(set(top_variance))))
        target.extend(list(set(top_diversity).intersection(set(top_variance))))
        target.extend(list(set(top_max).intersection(set(top_variance))))
        target.extend(list(set(top_total_time).intersection(set(top_variance))))
        target.extend(list(set(top_velocity).intersection(set(top_variance))))

        counts = np.bincount(target)
        target_instrument = np.argmax(counts)
        return target_instrument
    else: # default: top variance
        return top_variance[0]

# TODO: change the file directory
def main():
    test_target = './../midi_input/Anchor.mid'
    ns = note_seq.midi_file_to_note_sequence(test_target)
    file1 = open('./../1.txt', 'w+')
    file2 = open('./../2.txt', 'w+')
    target_instrument = skyline(ns)
    if target_instrument is None:
        print('No track selected')
    else:
        seq = get_new_ns(target_instrument, ns)
        file1.write(str(seq))
        note_seq.sequence_proto_to_midi_file(seq, './../midi_output/preprocess_output/out%s.mid' % '1')
        file2.write(str(note_seq.midi_file_to_note_sequence('./../midi_output/preprocess_output/out%s.mid' % '1')))

if __name__ == '__main__':
    main()