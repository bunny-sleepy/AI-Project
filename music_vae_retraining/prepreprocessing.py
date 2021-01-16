import os

ref_dir_name = "I:\\ref"
midi_dir_name = "I:\\input"

if __name__ == "__main__":

    ref_list = os.listdir(ref_dir_name)
    midi_list = os.listdir(midi_dir_name)

    total_midi_count = len(midi_list)
    passed_midi_count = 0
    failed_midi_count = 0

    for midi_file_name in midi_list:
        if midi_file_name[0:-4] not in ref_list:
            os.remove(midi_dir_name + "\\" + midi_file_name)
            failed_midi_count += 1
            print("total " + str(total_midi_count) +
                  ", passed: " + str(passed_midi_count) +
                  ", failed: " + str(failed_midi_count))
        else:
            passed_midi_count += 1
            print("total " + str(total_midi_count) +
                  ", passed: " + str(passed_midi_count) +
                  ", failed: " + str(failed_midi_count))
