import magenta.scripts.convert_dir_to_note_sequences as converter

def construct_dataset(input_dir, output_dir):
    ''' convert midi files (stored in a directory) into TFRecord

    Args:
        input_dir: directory of midi files
        output_dir: target dir

    Return: no return
    '''

    converter.convert_directory(input_dir, output_dir, recursive=True)


if __name__ == "__main__":
    construct_dataset("I:/input", "I:/output/res.tfrecord")