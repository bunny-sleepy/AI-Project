import os
import re
import note_seq

# TODO: devise these sets more wisely
char_set = {'朘','朅','#','œ', '抯', '’','Ç', 'á','朏', ']', '&', 'ü',
 '=', 'Φ','骃', '＆', '[','é', '朙', 'î','閛', 'Ø', 'à', 'ン','ス', '鉶', '閡', 
 'è','+','ï','№','朠', '鵪', '驪', 'í', 'û','朣', 'ダ', '抦'}
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

def word_dict(dict_path = 'word.txt'):
    """Return an array of words
    This function IS effective, even if it is plain look up without using data structures

    Args:
        dict_path: the dictionary file path

    Return:
        The array

    Note:
        To use this, you should write
        >>> my_dict = word_dict('word.txt')
        >>> for word_to_check in words_to_check:
        >>>     print(word_to_check in my_dict)
    """
    dict_file = open(dict_path, 'r')
    dict_words = dict_file.readlines()
    for i in range(len(dict_words)):
        dict_words[i] = dict_words[i].lower()
        dict_words[i] = dict_words[i].replace('\n', '')
        dict_words[i] = dict_words[i].replace('\r', '')
    return {}.fromkeys(dict_words, 1)

# Preprocess Titles (currently adding blank spaces)
# TODO: find a better preprocess method
def file_title(file_path, worddct):
    """ Return the file name string with blank spaces
    Args:
        file_path: the file to get title
        worddct: the word dictionary to detect spelling errors

    Return:
        (flg, name_string)
        where flg = True if the title is of desired characters
    """
    global pattern
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # detect invalid midi files
    if not detect_failure(file_path):
        return False, None
    midi_file_name = os.path.basename(file_path)
    # remove file extension
    midi_file_name = midi_file_name.replace('.midi', '')
    midi_file_name = midi_file_name.replace('.mid', '')
    # detect invalid characters
    for char in char_set:
        if char in midi_file_name:
            return False, None
    # remove version id
    for char in id_set:
        midi_file_name = midi_file_name.replace(char, '')
    # remove parenthesis
    midi_file_name = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", midi_file_name)
    # add spacing between files
    midi_file_name = re.sub(pattern, lambda x: " " + x.group(0), midi_file_name)
    # remove first spacing
    if midi_file_name[0] == ' ':
        midi_file_name = midi_file_name[1:]
    # check spelling errors
    new_file_name = None
    for number in numbers:
        new_file_name = midi_file_name.replace(number, '')
    new_file_name = new_file_name.lower()
    words = new_file_name.split()
    print(words)
    for word in words:
        if not worddct.__contains__(word):
            print('invalid word: %s' % word)
            return False, None
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
    worddct = word_dict('./word.txt')
    # print (worddct)
    # test_file1 = './midi_input/broken_midi.mid'
    # print(file_title(test_file1))
    test_file2 = './../midi_input/BackToDecember.mid'
    print(file_title(test_file2, worddct))
    # word_1 = 'zebra'
    # for i in range(100000):
    #     # try:
    #     #     tmp = worddct[word_1]
    #     #     print(True)
    #     # except:
    #     #     print(False)
    #     print(worddct.__contains__(word_1))

if __name__ == "__main__":
    main()