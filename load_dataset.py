import os
import re
import preprocessing.preprocess_title as ppt


# NOTE: absolute path recommended
def load_dataset(midi_directory = "PATH"):
    """ load midi dataset from a given directory

    Args:
        midi_directory: directory of midi files

    Return:
        a batch of note sequences.
    """

    file_list = os.listdir(midi_directory)
    midi_list = []

    for filename in file_list:
        # only append midi files
        if (".mid" in filename) or (".midi" in filename):
            file_valid, modified_filename = ppt.file_title(midi_directory + "/" + filename)
            if (file_valid):
                # this will remove ".mid", ".midi", "(*)", "[*]", "{*}" from filename
                # NOTE: ".midi" MUST be before ".mid"
                title = re.sub(u"\\.midi|\\.mid|\\(.*?\\)|\\{.*?}|\\[.*?]", "", modified_filename)
                midi_list.append([midi_directory + '/' + filename , title])

    return midi_list

list1 = load_dataset("I:/FinalProj/AI-Project/midi_input")
for item in list1:
    print(item)