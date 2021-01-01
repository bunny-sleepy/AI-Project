import magenta.models.music_vae.preprocess_tfrecord as preprocessor
import apache_beam as beam


def preprocess_dataset(input_file_name,
                       output_file_name,
                       output_shards=32,
                       config="hierdec-mel_16bar"):
    """ Preprocess dataset for further training

    Args:
    input_file_name: name of input TFRecord
    output_file_name: name of output TFRecord
    output_shards: number of fragments for output
    config: model and training configuration
        try "hierdec-mel_16bar", "hier-mel_16bar" or "flat-mel_16bar"
        TODO: try out other two configs
        TODO: define our own CONFIG

    Return: no return
    """

    filters = {  # pylint: disable=g-long-ternary
        # NoteSequences that lasts longer than this (in seconds) will be ignored.
        'max_total_time': 600,
        # NoteSequences that have more notes than this will be ignored.
        'max_num_notes': 10000,
        # NoteSequences with fewer unique velocities than this will be skipped.
        'min_velocities': 1,
        # NoteSequences with fewer unique metric positions between quarter notes
        # than this will be skipped.
        'min_metric_positions': 1,
        # If None, filtering will consider drums and non-drums. If True, only drums
        # will be considered. If False, only non-drums will be considered.
        'is_drum': False,
        # If True, NoteSequences with non-drum instruments will be skipped.
        'drums_only': False,
    }
    pipeline_options = beam.options.pipeline_options.PipelineOptions(
        "--runner=DirectRunner")
    preprocessor.run_pipeline(input_file_name, output_file_name, output_shards,
                              config, filters, pipeline_options)

if __name__ == "__main__" :
    preprocess_dataset("I:\\output\\res.tfrecord",
                       "I:\\output\\res_processed.tfrecord")
