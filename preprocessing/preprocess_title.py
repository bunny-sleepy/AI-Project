import os
import re
import note_seq

# TODO: devise these sets more wisely
char_set = {'朘','朅','#','œ', '抯', '’','Ç', 'á','朏', ']', '&', 'ü',
 '=', 'Φ','骃', '＆', '[','é', '朙', 'î','閛', 'Ø', 'à', 'ン','ス', '鉶', '閡', 
 'è','+','ï','№','朠', '鵪', '驪', 'í', 'û','朣', 'ダ', '抦'}

# TODO: use 'for' instead
id_set = {'(1)','(2)','(3)','(4)','(5)','(6)','(7)','(8)','(9)'}

pattern= "[A-Z]"

def detect_failure(file_path):
    """ detect whether a .mid file is broken

    Args:
        file_path: the path of the file. e.g., "D:/dataset/test.mid"

    Return:
        True if it is not broken
        False otherwise
    """
    try:
        ns = note_seq.midi_file_to_note_sequence(file_path)
        return True
    except:
        return False

# Preprocess Titles (currently adding blank spaces)
# TODO: find a better preprocess method
def file_title(file_path):
    """ Return the file name string with blank spaces
    Args:
        file_path: the file to get title

    Return:
        (flg, name_string)
        where flg = True if the title is of desired characters
    """
    global pattern
    if not detect_failure(file_path):
        return False, None
    midi_file_name = os.path.basename(file_path)
    midi_file_name = midi_file_name.replace('.midi', '')
    midi_file_name = midi_file_name.replace('.mid', '')
    for char in char_set:
        if char in midi_file_name:
            return False, None
    for char in id_set:
        midi_file_name = midi_file_name.replace(char, '')
    midi_file_name = re.sub(pattern, lambda x: " " + x.group(0), midi_file_name)
    if midi_file_name[0] == ' ':
        midi_file_name = midi_file_name[1:]
    return True, midi_file_name

# TODO: find a better preprocess method
def PreprocessDataset(dataset_path = "I:\\FinalProj\\AI-Project\\preprocessing\\TitlePreprocessor\\dataset"):
    """ Preprocess the dataset
    Args:
        dataset_path: the dataset folder path that contains the midi files

    Return:
        nothing
    """
    for filename in os.listdir(dataset_path):
        has_deleted = False
        if not detect_failure(filename):
            os.remove(dataset_path + "\\" + filename)
            has_deleted = True
        for char in char_set:
            if char in filename and not has_deleted:
                os.remove(dataset_path + "\\" + filename)
                has_deleted = True
        for char in id_set:
            if char in filename and not has_deleted:
                os.remove(dataset_path + "\\" + filename)
                has_deleted = True

# Rename files
def Rename(dataset_path = "I:\\FinalProj\\AI-Project\\preprocessing\\TitlePreprocessor\\dataset"):
    global pattern
    for filename in os.listdir(dataset_path):
        # split
        # new_filename = re.sub(pattern,lambda x:" "+x.group(0), filename)
        new_filename = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", filename)
        try:
            os.rename(dataset_path + "\\" + filename, dataset_path + "\\" + new_filename)
        except:
            os.remove(dataset_path + "\\" + filename)

def main():
    test_file1 = './midi_input/broken_midi.mid'
    print(file_title(test_file1))
    test_file2 = './midi_input/BackToDecember.mid'
    print(file_title(test_file2))

if __name__ == "__main__":
    main()