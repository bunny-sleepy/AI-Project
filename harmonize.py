import coconet.coconet_sample as cs
import coconet.lib_util as lib_util
import os
import re
import tensorflow.compat.v1 as tf
import pretty_midi
import numpy as np
import note_seq as ns

def generate_coconet_model(coconet_model_path):
    """Generate a coconet model based on the model path
    Args:
        coconet_model_path: the directory that contains the coconet model

    Return:
        the loaded coconet model ready for use
    """
    tf.compat.v1.disable_eager_execution()
    coconet_model = cs.instantiate_model(coconet_model_path)
    return coconet_model

# TODO: change the instrument of the harmonized sample
def harmonize(file_path, output_dir, coconet_model, batch_size = 1, file_name = '', to_piano = False):
    """harmonize a midi file

    Args:
        file_path: the input path
        coconet_model: the loaded coconet model
        output_dir: the output path
        file_name: the name of the generated piece
        batch_size: how many samples to generate each time
        to_piano: whether or not to convert the output to piano

    Return:
        None
    """
    file1 = open('original.txt', 'w+')
    noteseq = ns.midi_file_to_note_sequence(file_path)
    file1.write(str(noteseq))
    strategy = "harmonize_midi_melody"
    generator = cs.Generator(coconet_model, strategy)
    midi_outs = generator.run_generation(midi_in = pretty_midi.PrettyMIDI(file_path),
                                         gen_batch_size = batch_size)

    # Creates a folder for storing the process of the sampling.
    label = "%s_harmonized_%s" % (file_name, lib_util.timestamp())
    basepath = os.path.join(output_dir, label)
    tf.logging.info("basepath: %s", basepath)
    tf.gfile.MakeDirs(basepath)

    # Saves the results as midi or returns as midi out.
    midi_path = os.path.join(basepath, "midi")
    tf.gfile.MakeDirs(midi_path)
    tf.logging.info("Made directory %s", midi_path)
    cs.save_midis(midi_outs, midi_path, label)

    result_npy_save_path = os.path.join(basepath, "generated_result.npy")
    tf.logging.info("Writing final result to %s", result_npy_save_path)
    with tf.gfile.Open(result_npy_save_path, "wb") as p:
        np.save(p, generator.pianorolls)

    # Stores all the (intermediate) steps.
    intermediate_steps_path = os.path.join(basepath, "intermediate_steps.npz")
    with lib_util.timing("writing_out_sample_npz"):
        tf.logging.info("Writing intermediate steps to %s", intermediate_steps_path)
        generator.logger.dump(intermediate_steps_path)

    # Save the prime as midi and npy if in harmonization mode.
    # First, checks the stored npz for the first (context) and last step.
    tf.logging.info("Reading to check %s", intermediate_steps_path)
    with tf.gfile.Open(intermediate_steps_path, "rb") as p:
        foo = np.load(p)
        for key in foo.keys():
            if re.match(r"0_root/.*?_strategy/.*?_context/0_pianorolls", key):
                context_rolls = foo[key]
                context_fpath = os.path.join(basepath, "context.npy")
                tf.logging.info("Writing context to %s", context_fpath)
                with lib_util.atomic_file(context_fpath) as context_p:
                    np.save(context_p, context_rolls)
                if "harm" in strategy:
                    # Only synthesize the one prime if in Midi-melody-prime mode.
                    primes = context_rolls
                    if "Melody" in strategy:
                        primes = [context_rolls[0]]
                    prime_midi_outs = cs.get_midi_from_pianorolls(primes, generator.decoder)
                    cs.save_midis(prime_midi_outs, midi_path, label + "_prime")
                break
    tf.logging.info("Done")
    if to_piano:
        file_list = os.listdir(midi_path)
        path = os.path.join(output_dir, "%s_piano_harmonized_%s" % (file_name, lib_util.timestamp()))
        tf.gfile.MakeDirs(path)
        for file_path in file_list:
            midi_file_name = os.path.basename(file_path)
            save_path = os.path.join(path, midi_file_name)
            convert_to_piano(os.path.join(midi_path, file_path), save_path)

def convert_to_piano(path, output_path):
    """convert a midi file to piano
    Args:
        path: the path of the midi file
        output_path: the output file path that contains the whole name, e.g., D:/out/out1.mid

    Return:
        None
    """
    noteseq = ns.midi_file_to_note_sequence(path)
    file2 = open('after.txt', 'w+')
    # TODO(wwh): change the factor of the weaken of non-prime tracks
    for note in noteseq.notes:
        if note.program != 68:
            note.velocity = int(note.velocity / 2)
        note.program = 0
    file2.write(str(noteseq))
    ns.note_sequence_to_midi_file(noteseq, output_path)

# example of usage
def main():
    coconet_model_path = "D:/code/Github/repository/coconet_model"
    coconet_model = generate_coconet_model(coconet_model_path)
    file_path = "D:/code/Github/AI-Project/midi_input/test.mid"
    output_path = "D:/code/Github/AI-Project/midi_output/harmonize_output"
    harmonize(file_path, output_path, coconet_model = coconet_model, file_name = 'test', to_piano = True)

if __name__ == "__main__":
    main()