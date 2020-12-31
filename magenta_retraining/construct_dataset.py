import magenta.magenta.scripts.convert_dir_to_note_sequences as converter

def construct_dataset(input_dir, output_dir):
    ''' convert midi files into TFRecord

    Args:
        input_dir: directory of midi files
        output_dir: target dir

    Return: no return
    '''
    converter.convert(input_dir, output_dir)


if __name__ == "__main__":
    construct_dataset()